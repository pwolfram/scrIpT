#!/bin/bash

# make tags for the ocean case
ctags -R --exclude=src/core_atmosphere/* --exclude=src/core_init_atmosphere/* --exclude=src/core_landice/* --exclude=src/core_sw/* --exclude=Doxygen* --fortran-kinds=+i --exclude=LPT_beforePools --exclude=MPAS_develop --exclude=working2.54.15PM_with_original_bug
