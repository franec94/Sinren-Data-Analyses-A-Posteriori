SCRIPT_GET_REMOTE_DATA = get_train_log-v001.sh
ARGS_GET_REMOTE_DATA = conf.txt

SCRIPT_GET_REMOTE_DATA_v2 = get_train_log-v002.sh
ARGS_GET_REMOTE_DATA_v2 = conf.txt
# =============================================== #
# Targets
# =============================================== #

get_train_log:
	chmod u+x $(SCRIPT_GET_REMOTE_DATA)
	./$(SCRIPT_GET_REMOTE_DATA) $(ARGS_GET_REMOTE_DATA)

get_train_log_v2:
	chmod u+x $(SCRIPT_GET_REMOTE_DATA_v2)
	./$(SCRIPT_GET_REMOTE_DATA_v2) $(ARGS_GET_REMOTE_DATA_v2)
