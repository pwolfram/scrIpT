#!/usr/bin/env bash

ORIG_TEXT=$1
NEW_TEXT=$2
git grep -l $ORIG_TEXT | xargs sed -i -e "s/$ORIG_TEXT/$NEW_TEXT/g"
