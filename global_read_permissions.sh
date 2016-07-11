#!/usr/bin/env bash

echo 'setting global read permissions at '$PWD
find . -type f -exec chmod g+r,o+r {} +
find . -type d -exec chmod g+rx,o+rx {} +


