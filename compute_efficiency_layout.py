#!/usr/bin/env python


import numpy as np
import datetime
import subprocess
import glob
import re
import os

def run_cmd(cmd, echo=False): #{{{
  if echo:
    print cmd
  try:
    out = subprocess.check_output(cmd)
  except CalledProcessError:
    print CalledProcessError.output

  return out#}}}

def cat(afile): #{{{
  with open(afile, 'r') as f:
    for line in f.readlines():
      print line
  return #}}}

def date_hash(): #{{{
  return ('%s'%(datetime.datetime.now()))\
      .replace(' ','_')\
      .replace('.','')\
      .replace(':','') #}}}

def define_case_name(layoutname, alayout, nodeprocs, #{{{
    prefix='/users/pwolfram/ACME-cases/240km_G_analysis_test_'):
  """
  Layouts gives the bool of processors used and nodeprocs gives the node number for each proc

  example:
    layouts = {'OCN': np.array([0,1,0])}, nodeprocs = np.array([0,1,2]) for a three-node, single-comp machine
  """
  casename = layoutname
  for comp in alayout.keys():
    values = alayout[comp]
    casename += '_' + comp + 'of' +  \
        '%d'%(np.sum(values)) + 'on' + '-'.join(np.char.mod('%d', np.unique(nodeprocs[values])))

  # add date hash
  casename += '_' + date_hash()

  return casename #}}}

def simple_hardware_layout(nnodes=3, nprocs=24): #{{{
  nodeprocs = np.ones((nnodes*nprocs))

  for anode in np.arange(nnodes):
    nodeprocs[anode*nprocs:(anode+1)*nprocs] = anode

  return nodeprocs #}}}

def validate_layouts(layouts, nodeprocs): #{{{

  for case in layouts:
    for comp in layouts[case].keys():
      procs = layouts[case][comp]

      assert np.min(np.logical_or(procs == 1, procs == 0)), 'Processors specified incorrectly'
      assert np.sum(procs) <= len(nodeprocs), 'Size of %s is too large for hardware layout'%(comp)
      assert np.min(np.diff(procs) <= 1), 'Non-contiguous layout in use!'

  return #}}}

def create_case(casename, config, script_cmd='./create_newcase'): #{{{

  cmd = [script_cmd, '-case', casename]
  for option in config:
    cmd.append('-' + option)
    cmd.append(config[option])

  output = run_cmd(cmd)
  assert 'Successfully created' in output, 'Building case failed with %s'%(output)

  return output #}}}

def make_like_othercase(othercase, sourcemods=True, namelist=True): #{{{

  if sourcemods:
    cmd = ['cp', '-r', othercase + 'SourceMods/', 'SourceMods']
    run_cmd(cmd)

  if namelist:
    for af in glob.glob(othercase + 'user_nl_*'):
      cmd = ['cp', af, '.']
      run_cmd(cmd)

  return #}}}

def configure_case(clean=True): #{{{

  if clean:
    cmd = ['./cesm_setup','--clean']
    run_cmd(cmd)

  cmd = ['./cesm_setup']
  output = run_cmd(cmd)

  # if decomposition doesn't exist, create it
  notfound = re.compile('NOT FOUND:\s*(.*)\n')
  missingfiles = notfound.findall(output)
  if len(missingfiles):
    for mf in missingfiles:
      print 'Getting ' + mf
      get_missing_file(mf)
    output = configure_case()

  return output #}}}

def general_case_run(ext):
  casename = os.path.basename(os.getcwd())
  return run_cmd(['./' + casename + ext], echo=True)

def build_case():
  return general_case_run('.build')

def submit_case():
  return general_case_run('.submit')

def change_proc_counts(layout): #{{{

  totalcomp = ['ATM', 'LND', 'ICE', 'OCN', 'CPL', 'GLC', 'ROF', 'WAV']

  def change_mach_pes(idname, value):
    cmd = ['./xmlchange', '-file', 'env_mach_pes.xml', '-id', str(idname), '-val', str(value)]
    return run_cmd(cmd)

  for comp in layout:
    procs = layout[comp]
    change_mach_pes('NTASKS_' + comp, np.sum(procs))
    change_mach_pes('ROOTPE_' + comp, np.where(procs)[0][0])

  # make other layouts for data use all processors
  for comp in np.setdiff1d(totalcomp, layout.keys()):
    change_mach_pes('NTASKS_' + comp, len(procs))
    change_mach_pes('ROOTPE_' + comp, 0)

  return #}}}

def get_missing_file(mf):
  graphtype = re.compile('graph\.info')
  if graphtype.findall(mf) is not None:
    basegraph = ('.').join(mf.split('.')[:-2])
    procsneeded = mf.split('.')[-1]
    cmd = ['gpmetis', basegraph, procsneeded]
    #cmdmv = ['mv', basegraph + '.part.%s'%(procsneeded), mf]
    print 'Building decomposition via ' + (' ').join(cmd) #+ ' AND ' + (' ').join(cmdmv)
    run_cmd(cmd)
    #run_cmd(cmdmv)
  else:
    assert False, 'Filetype %s is not known how to obtained'%(mf)

def compute_layout_case(alayout, layouts, nodeprocs, config, acmedir='/users/pwolfram/ACME/cime/scripts', #{{{
    casedir='/users/pwolfram/ACME-cases/', casetemplate='/users/pwolfram/ACME-cases/240km_G_analysis_AMs/'):

  casename = define_case_name(alayout, layouts[alayout], nodeprocs)
  casepath = casedir + casename

  print 'Creating case for ' + casepath

  # build the case
  os.chdir(acmedir)
  create_case(casepath, config)

  # set up the case
  os.chdir(casepath)
  make_like_othercase(casetemplate)

  # change processor counts
  #cat('env_mach_pes.xml')
  change_proc_counts(layouts[alayout])
  #cat('env_mach_pes.xml')

  # configure, build, submit
  out = configure_case()
  build_case()
  submit_case()

  return #}}}

def variable_layout(fcomp, focean, nodeprocs): #{{{
  assert 0 < fcomp and fcomp <= 1, 'need to do computational work that is reasonable'
  assert 0 < focean  and focean < 1, 'fraction must allow there to be cores for ice'

  compnodes = np.zeros_like(nodeprocs, dtype='bool')
  oceannodes = np.zeros_like(nodeprocs, dtype='bool')
  totalproc = len(nodeprocs)
  compnodes[:int(np.floor(fcomp*totalproc))] = 1
  totalcompproc = np.sum(compnodes)
  oceannodes[:int(np.floor(focean*totalcompproc))] = 1

  return {'CPL': np.logical_not(compnodes), 'OCN': oceannodes, 'ICE': np.logical_not(oceannodes)} #}}}

if __name__ == "__main__":

  caseconfig = {'compset': 'GMPAS_NYF', 'res': 'T62_oQU240', 'mach': 'mustang', \
      'compiler': 'gnu', 'proj': 's11_climateacme'}

  layouts = {}
  for nnodes in np.arange(3,4+1):
    nodeprocs = simple_hardware_layout(nnodes, nprocs=24)

    layouts.update({'Nodes%d_EvenSplit'%(nnodes) : {'OCN': nodeprocs == 0, 'ICE': nodeprocs == 1, 'CPL': nodeprocs ==2},
               'Nodes%d_Collocated'%(nnodes): {'OCN': nodeprocs >=0,  'ICE': nodeprocs >= 0, 'CPL': nodeprocs >=0},
              })

    varlayouts = {}
    Ncomp = 5
    Nocean = 4
    for fcomp in np.linspace(0,1,Ncomp)[1:-1]:
      for focean in np.linspace(0,1,Nocean)[1:-1]:
        casename = 'Nodes%d_Variable_fcomp%0.2f_focean%0.2f'%(nnodes, fcomp, focean)
        varlayouts.update({casename : variable_layout(fcomp, focean, nodeprocs)})

    layouts.update(varlayouts)

  print 'Considering %s cases: %s'%(len(layouts), layouts.keys())

  validate_layouts(layouts, nodeprocs)
  for alayout in layouts:
    compute_layout_case(alayout, layouts, nodeprocs, caseconfig, casedir='/users/pwolfram/ACME-cases/LayoutStudyTemp/')

