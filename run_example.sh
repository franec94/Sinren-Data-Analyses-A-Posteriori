#!/usr/bin/env bash

data_path="../../../../results/23-10-2020/1603410154-248962/"
logging_root="../results/"

chmod u+x analysis-single-run
python3 analysis-single-run \
  --data_path ${data_path} \
  --logging_root ${logging_root}

exit 0

