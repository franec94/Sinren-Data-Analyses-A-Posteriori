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
timestamp=$(cat train_log.txt | grep timestamp | grep -E "^INFO:root:Start" | cut -d "=" -f 2 | cut -d ']' -f 1)
date_train=$(cat train_log.txt | grep timestamp | grep -E "^INFO:root:Start" | cut -d '[' -f 2 | cut -d ']' -f 1)

echo $hf $timestamp $date_train

cat train_log.txt \
	| grep -E "^hidden_layers" \
	| sort \
	| uniq -c \
	| awk -v hf=${hf} -v timestamp=${timestamp} -v date_train=${date_train} '
	BEGIN{}
	{print sprintf("%s,%s,%d,%d,%d", date_train, timestamp, hf, $3, $1) > "trials_done.csv"}
	END{}'

perl scripts/perl_scripts/a_script.pl -h

perl scripts/perl_scripts/a_script.pl --file_path trials_done.csv
		


