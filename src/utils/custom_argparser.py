import configargparse

def get_cmd_line_opts():
    p = configargparse.ArgumentParser()
    p.add_argument('--data_path', type=str, required=True, help='path to directory containing data to be analysed.')
    p.add_argument('--logging_root', type=str, default='./logs', help='root for logging.')


    opt = p.parse_args()
    return opt, p