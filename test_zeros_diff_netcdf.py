#!/usr/bin/env python

import netCDF4
import numpy as np

def test_assert(logexpr, msg):
    #assert logexpr, msg
    if not logexpr:
        print(msg)
        return True

def nans_are_zero(expr):
    if np.isnan(expr):
        return 0
    else:
        return expr

def test_failed(var, varname, failed, usenan=True):
    if usenan:
        min = np.min
        max = np.max
        mean = np.mean
    else:
        min = np.nanmin
        max = np.nanmax
        mean = np.nanmean

    for afunc, aname in zip([min, max, mean],
                            ['min','max','mean']):
        failed = failed or test_assert(nans_are_zero(afunc(var)) == 0, '-- ERROR ' + varname + ' field is not bit-zero for {}!'.format(aname))
    test_assert(not np.sum(np.isnan(var)), '\t\t ' + varname + ' is nan -- CAUTION!!!')
    return failed


def diff(fname1, fname2, exceptions):
    print('Determining if fields are the same for %s and %s:'%(fname1, fname2))
    print(' ')
    fin1 = netCDF4.Dataset(fname1, 'r')
    fin2 = netCDF4.Dataset(fname2, 'r')
    combinedvars = list(set(fin1.variables) & set(fin2.variables))
    combinedvars.sort()
    for varname in np.setdiff1d(combinedvars, exceptions.split(',')):
        try:
            print('Testing %s:'%(varname))
            failed = False
            if varname == 'cellsOnCell' or varname == 'edgesOnCell' or varname == 'verticesOnCell':
                for anum, nEdgesOnCell in enumerate(fin1.variables['nEdgesOnCell']):
                    var = fin1.variables[varname][anum,:nEdgesOnCell] - fin2.variables[varname][anum,:nEdgesOnCell]
                    failed = test_failed(var, varname, failed)
                    if failed:
                        break
            elif varname == 'edgesOnEdge':
                for anum, nEdgesOnEdge in enumerate(fin1.variables['nEdgesOnEdge']):
                    var = fin1.variables[varname][anum,:nEdgesOnEdge] - fin2.variables[varname][anum,:nEdgesOnEdge]
                    if len(var) > 0:
                        failed = test_failed(var, varname, failed)
                    if failed:
                        break
            else:
                var = fin1.variables[varname][:] - fin2.variables[varname][:]
                failed = test_failed(var, varname, failed)
            if not failed:
                print( '\t\t ' + varname + ' is bit identical.')
            else:
              #print(var)
              print('min  ', fin1.variables[varname][:].nanmin(), fin2.variables[varname][:].nanmin())
              print( 'max  ', fin1.variables[varname][:].nanmax(), fin2.variables[varname][:].nanmax())
              print( 'mean ', fin1.variables[varname][:].nanmean(), fin2.variables[varname][:].nanmean())
              #print( 'min  diff ', (fin1.variables[varname][:] - fin2.variables[varname][:]).min())
              #print( 'max  diff ', (fin1.variables[varname][:] - fin2.variables[varname][:]).max())
              #print( 'mean diff ', (fin1.variables[varname][:] - fin2.variables[varname][:]).mean()
              #print( 'value', np.vstack((fin1.variables[varname][:], fin2.variables[varname][:])))
        except:
            print('-- WARNING: cannot test ' + varname + ' with values ' + fin1.variables[varname][:] + ' and ' + fin2.variables[varname][:])

if __name__ == "__main__":
    import sys
    diff(sys.argv[1], sys.argv[2], sys.argv[3])
