#!/usr/bin/env bash

date_timestampe_partial_path=""

data_path="..\\tmp"
logging_root="..\\results\\"

chmod u+x src/main.py
python src/main.py \
  --data_path ${data_path} \
  --logging_root ${logging_root}

exit 0