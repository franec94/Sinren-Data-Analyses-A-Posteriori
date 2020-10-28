#!/usr/bin/env bash

# --- Global Variables ---
script_name=$0
src_path=""
declare -A conf_table


# --- Functions ---
function update_src_path() {
    # Update src path to be queryed
    # exploiting infos within input config file,
    # which have been stored inside a bash hash table.

    keys_for_src_path=("user" "image_name" "date" "timestamp")
    src_path=${conf_table["src_dir"]}
    for k in ${keys_for_src_path[@]} ; do
      # echo $k
      val=${conf_table[$k]}
      # echo $val
      src_path="${src_path/${k}/${conf_table["${k}"]}}" 
      # echo $src_path
    done
    # echo $src_path
}

function create_conf_array() {
    # Create hash table made from
    # infos within input conf file.

    local conf_file=$1
     echo $conf_file

    while IFS= read -r line ; do
      # echo "$line"
      if [ ${#line} == 0 ] ; then
        continue
      fi

      key=$(echo ${line} | cut -d "=" -f 1)
      value=$(echo ${line} | cut -d "=" -f 2)
      # echo "k=${key} v=${value}"

      conf_table["${key}"]="${value}"
      # echo "${conf_table[${key}]}"

    done < "$conf_file"

    unset conf_file
}

function check_cmd_args() {
    # Check whether input args
    # to script are correct.

    local cmd_args=$@

    if [ ${#cmd_args[@]} != "1" ] ; then
      echo "${#cmd_args[@]}"
      echo "Usage: $script_name conf.txt"
      exit -1
    elif [ ! -f ${cmd_args[0]} ] ; then
      echo "Error: '${cmd_args[0]}' is not a file!"
      exit -1
    fi
    unset cmd_args
}

# --- Start Script ---
check_cmd_args $@

# Create table with conf data.
conf_file=$1
create_conf_array ${conf_file}

# Update target src path for querying
# in order to retrieve data.
update_src_path

# src_path="${conf_table["src_path"]/user/${conf_table["user"]}}" 
# src_path="${src_path/date/${conf_table["date"]}}"
# src_path="${src_path/timestamp/${conf_table["timestamp"]}}"
echo ${src_path}
# exit 0

# Get data from remote server.
CMD="pscp"
# echo "${CMD} -r ${conf_table["user"]}@${conf_table["remote_server"]}:${src_path} ${conf_table["dest_dir"]}"
${CMD} -r ${conf_table["user"]}@${conf_table["remote_server"]}:${src_path} ${conf_table["dest_dir"]}
# exit 0

# Check wheter data collected.
if [ $? -ne 0 ] ; then
  echo "Error: ${CMD} failed!"
  exit -1
fi


exit 0

