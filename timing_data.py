#!/usr/bin/env python

import numpy as np
import os
import glob
import re
# plot on HPC
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation


def find_file_str(afile, astr):
  matcher = re.compile(astr)
  with open(afile, 'r') as af:
    matches = matcher.findall(('').join(af.readlines()))
  assert len(matches) == 1, 'More matches than expected for %s in %s!'%(astr, afile)
  return matches[0]

def split_num_units(astr):
  vals = astr.split()
  num = float(vals[0])
  units = vals[1]
  return num, units

class valuecontainer: #{{{
  def __init__(self):
    self.files = []
    self.vals = []
    self.units = set()

  def add_vals_units(self, fname, num, unit): #{{{
    self.files.append(fname)
    self.vals.append(num)
    self.units.add(unit)
    assert len(self.units) < 2, 'More than one set of units: %s!'%(self.units)
    return #}}}

  def sort(self, files=False): #{{{
    self.files = np.asarray(self.files)
    self.vals = np.asarray(self.vals)
    if files:
      idx = np.argsort(self.files)
    else:
      idx = np.argsort(self.vals)
    self.vals = self.vals[idx]
    self.files = self.files[idx]
    return #}}}

  def to_file(self, fname): #{{{
    with open(fname,'w') as af:
      af.write('Units = %s\n'%(self.units))
      for fn, vl in zip(self.files, self.vals):
        af.write('%s  %f\n'%(fn, vl))
    return #}}}

  def plot(self, savename, astr='.*_fcomp(.*)_focean(.*)_CPL', xlabel='fcomp', ylabel='focean'):
    """ astr is used to build indices from files"""
    matcher = re.compile(astr)
    matches = [(matcher.findall(af)[0][0], matcher.findall(af)[0][1], val) for af, val in zip(self.files, self.vals) if matcher.findall(af) != []]
    points = np.squeeze(np.asarray(matches, dtype='f8'))

    plt.figure()
    tri = Triangulation(points[:,0], points[:,1])
    plt.tripcolor(tri, points[:,2], cmap='viridis')
    plt.colorbar()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(self.units)
    plt.savefig(savename + '.png')

    return #}}}

#}}}

def main(dirs, prefix):

  model_cost = valuecontainer()
  model_throughput = valuecontainer()

  for adir in dirs:
    print 'Performing analysis on ' + adir
    for afile in glob.glob(adir):
      fname = os.path.dirname(os.path.abspath(afile)).replace('/timing','')
      model_cost.add_vals_units(fname, *split_num_units(find_file_str(afile, 'Model Cost\s*:\s+(.*)\s+\n')))
      model_throughput.add_vals_units(fname, *split_num_units(find_file_str(afile, 'Model Throughput\s*:\s+(.*)\s+\s\n')))

  model_cost.sort()
  model_throughput.sort()

  # write to files now
  model_cost.to_file(prefix + 'model_cost.txt')
  model_throughput.to_file(prefix + 'model_throughput.txt')

  # make plots
  model_cost.plot(prefix + 'model_cost')
  model_throughput.plot(prefix + 'model_throughput')

  return



if __name__ == "__main__":
  main(['../LayoutStudyTemp/Nodes3_*/timing/cesm_timing.*', '/lustre/scratch1/turquoise/pwolfram/ACME-cases/Nodes3_*/timing/cesm_timing.*'],
      prefix='Nodes3_')

  main(['../LayoutStudyTemp/Nodes4_*/timing/cesm_timing.*', '/lustre/scratch1/turquoise/pwolfram/ACME-cases/Nodes4_*/timing/cesm_timing.*'],
      prefix='Nodes4_')

