#!/usr/bin/env python

import json
import numpy as np
import sys

with open(sys.argv[1]) as fin:
  data = json.load(fin)
  values = np.asarray(data[0]['RGBPoints']).reshape((16,4))
  with open(sys.argv[1].split('.')[0].split('/')[-1] + '.rgb','w') as fout:
      for line in np.floor(values[:,1:]*255):
          fout.write('{} {} {}\n'.format(*line))
