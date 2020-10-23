#!/usr/bin/env bash

date_timestampe_partial_path="23-10-2020/1603410154-248962"

data_path="../../../../results/${date_timestampe_partial_path}"
logging_root="../results/${date_timestampe_partial_path}"

chmod u+x analysis-single-run
python3 analysis-single-run \
  --data_path ${data_path} \
  --logging_root ${logging_root}

exit 0

