from utils.libs import *

opt, parser = None, None

def setup_program(opt):
    check_dir_exists(opt.data_path)
    create_dir(opt.logging_root)
    pass

def main():
    global opt
    global parser

    print(f"Hello World! From {sys.argv[0]}")
    setup_program(opt)

    pass

if __name__ == "__main__":
    # Initialize option and parser objects.
    
    opt, parser = get_cmd_line_opts()

    main()
    pass