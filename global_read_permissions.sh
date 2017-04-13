#!/usr/bin/env bash

echo 'setting global read permissions at '$PWD
find . -type f -exec chmod g+r,o+r {} +
find . -type d -exec chmod g+rx,o+rx {} +
echo 'make sure that there are read / execute permissions for group and others at the top level of the directory, e.g., home'
