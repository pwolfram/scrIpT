#!/usr/bin/env python
# derived from https://gist.github.com/douglasjacobsen/0ddcf9529f462dc6ca7c
import argparse
import ConfigParser
import os

parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-f", "--file", dest="filename", help="Path to config file", metavar="FILE", required=True)
parser.add_argument("-t", "--type", dest="type", help="Type of config file to setup", metavar="TYPE", required=True)
parser.add_argument("-b", "--branch", dest="branch", help="Path to setup directory", metavar="PATH", required=True)
args = parser.parse_args()

if not args.filename:
    parser.error("A config file is required")

if not args.type:
    parser.error("A type is required")

if not args.branch:
    parser.error("A branch is required")

configParser = ConfigParser.RawConfigParser()

try:
    configParser.read(args.filename)
except:
    print "Error while trying to read file %s\n"%(args.filename)
    exit()

if args.type == "ocean":
    configParser.set("namelists", "forward", "%s/default_inputs/namelist.ocean.forward"%(args.branch))
    configParser.set("namelists", "init", "%s/default_inputs/namelist.ocean.init"%(args.branch))
    configParser.set("streams", "forward", "%s/default_inputs/streams.ocean.forward"%(args.branch))
    configParser.set("streams", "init", "%s/default_inputs/streams.ocean.init"%(args.branch))
    configParser.set("executables", "model", "%s/ocean_model"%(args.branch))
    configParser.set("executables", "mesh_converter", "/Users/pwolfram/Documents/MPAS-Tools/grid_gen/mesh_conversion_tools/MpasMeshConverter.x")
    configParser.set("executables", "cell_culler", "/Users/pwolfram/Documents/MPAS-Tools/grid_gen/mesh_conversion_tools/MpasCellCuller.x")
    configParser.set("executables", "mask_creator", "/Users/pwolfram/Documents/MPAS-Tools/grid_gen/mesh_conversion_tools/MpasMaskCreator.x")
    configParser.set("executables", "metis", "/usr/local/bin/gpmetis")
    configParser.set("paths", "mesh_database", "/Users/pwolfram/Documents/MPAS-MeshDatabase")
    configParser.set("paths", "initial_condition_database", "/Users/pwolfram/Documents/MPAS-InitCondDatabase")
    configParser.set("paths", "gemoetric_features", "/Users/pwolfram/Documents/MPAS-geometric_features")

elif args.type == "test":
    configParser.set("namelists", "forward", "%s/default_inputs/namelist.test"%(args.branch))
    configParser.set("streams", "forward", "%s/default_inputs/streams.test"%(args.branch))
    configParser.set("executables", "model", "%s/test_model"%(args.branch))
    configParser.set("executables", "mesh_converter", "/Users/pwolfram/Documents/MPAS-Tools/grid_gen/mesh_conversion_tools/MpasMeshConverter.x")
    configParser.set("executables", "cell_culler", "/Users/pwolfram/Documents/MPAS-Tools/grid_gen/mesh_conversion_tools/MpasCellCuller.x")
    configParser.set("executables", "metis", "/usr/local/bin/gpmetis")
    configParser.set("paths", "mesh_database", "/Users/pwolfram/Documents/MPAS-MeshDatabase")

elif args.type == "landice":
    configParser.set("namelists", "forward", "%s/default_inputs/namelist.landice"%(args.branch))
    configParser.set("streams", "forward", "%s/default_inputs/streams.landice"%(args.branch))
    configParser.set("executables", "grid_to_li_grid", "/usr/local/bin/create_landice_grid_from_generic_MPAS_grid.py")
    configParser.set("executables", "model", "%s/landice_model"%(args.branch))
    configParser.set("executables", "mesh_converter", "/Users/pwolfram/Documents/MPAS-Tools/grid_gen/mesh_conversion_tools/MpasMeshConverter.x")
    configParser.set("executables", "cell_culler", "/Users/pwolfram/Documents/MPAS-Tools/grid_gen/mesh_conversion_tools/MpasCellCuller.x")
    configParser.set("executables", "metis", "/usr/local/bin/gpmetis")
    configParser.set("paths", "mesh_database", "/Users/pwolfram/Documents/MPAS-MeshDatabase")
    configParser.set("paths", "initial_condition_database", "/Users/pwolfram/Documents/MPAS-InitCondDatabase")

config_file = open("/tmp/%s.config"%(args.type), "w+")

try:
    configParser.write(config_file)
    print "wrote file: /tmp/%s.config"%(args.type)
except:
    print "Error trying to write file %s\n"%(args.filename)
    exit()

config_file.close()
