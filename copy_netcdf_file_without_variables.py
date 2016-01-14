#!/usr/bin/env python
"""
Make a copy of a netCDF file retaining dimensions
and attributes but exclude the variables.

Phillip J. Wolfram
01/14/2016
"""

import netCDF4
import sys, socket, os, datetime

def copy_netcdf_file_without_variables(infile, outfile):
  """
  Copy dimensions and attributes from infile netCDF file to outfile.
  Phillip J. Wolfram
  01/14/2016
  """

  ifile = netCDF4.Dataset(infile,'r')
  ofile = netCDF4.Dataset(outfile,'w')

  # transfer dimensions
  for dim in ifile.dimensions.values():
    ofile.createDimension(dim.name, len(dim))

  # transfer global attributes
  for name, value in zip(ifile.__dict__.keys(), ifile.__dict__.values()):
    ofile.setncattr(name, value)

  # modify history and store metadata
  callcmd = ' '.join(sys.argv)
  ofile.history = callcmd + '; ' + ofile.history
  ofile.meta_cwd = os.getcwd()
  ofile.meta_host = socket.gethostname()
  ofile.meta_call = ' '.join(sys.argv)
  ofile.meta_user = os.getenv('USER')
  ofile.meta_time = str(datetime.datetime.now())

  ifile.close()
  ofile.close()

if __name__ == "__main__":
  from optparse import OptionParser

  parser = OptionParser()
  parser.add_option("-f", "--infile", dest="inputfilename", \
      help="Input file to be copied sans variables, of form '*.nc'", metavar="FILE")
  parser.add_option("-o", "--outfile", dest="outputfilename", \
      help="Output file sans variables, of form '*.nc'", metavar="FILE")

  options, args = parser.parse_args()
  if not options.inputfilename:
    parser.error("Input filename or expression ('-f') is a required input... e.g., -f 'input*.nc'")
  options, args = parser.parse_args()
  if not options.inputfilename:
    parser.error("Output filename or expression ('-o') is a required input... e.g., -o 'output*.nc'")

  copy_netcdf_file_without_variables(options.inputfilename, options.outputfilename)
