#!/usr/bin/env bash

function show_info_v1 () {
	echo "Training already performed following runs:"
	cat train_log.txt \
	| grep -E "^hidden_layers" \
	| sort \
	| uniq -c \
	| awk '
	BEGIN{
		header_str = sprintf("hidden_layers\tno. attempts");
		printf("%s\n", header_str);
		for (i = 0; i < length(header_str); i++)
			printf("-");
		printf("\n");
	}
	{printf("%d\t%d\n", $3, $1)}
	END{}'
}

hf=$(cat train_log.txt | grep -E "^INFO:root:hidden_features" | sort | uniq | cut -d ' ' -f 2)

cat train_log.txt \
	| grep -E "^hidden_layers" \
	| sort \
	| uniq -c \
	| awk -v hf=${hf} '
	BEGIN{}
	{print sprintf("%d,%d,%d", hf, $3, $1) > "trials_done.csv"}
	END{}'

python scripts/python_scripts/show_hl_vs_trials_done.py -h

python scripts/python_scripts/show_hl_vs_trials_done.py --csv_filename trials_done.csv
		


