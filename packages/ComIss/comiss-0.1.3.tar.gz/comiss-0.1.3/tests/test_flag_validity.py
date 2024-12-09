import argparse

# parse arguments
def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--message-type')
    parser.add_argument('--impact-type')
    parser.add_argument('--change-type')
    return parser.parse_args(args)

# valid flags for our CLI
VALID_FLAGS = ['--message-type', '--impact-type', '--change-type']

def check_flag_validity(args):
    for arg in args:
        if arg.startswith('--') and arg not in VALID_FLAGS:
            raise ValueError(f"Invalid flag used: {arg}")

def test_invalid_flag():
    args = ['--invalid_flag']

    try:
        check_flag_validity(args)
    except ValueError as e:
        invalid = str(e) == "Invalid flag used: --invalid_flag"
        print("invalid = " + str(invalid))
        assert invalid
    else:
        print("false: Expected ValueError for invalid flag, but none was raised.")
        assert False, "Expected ValueError for invalid flag, but none was raised."

def test_valid_flag():
    args = ['--message-type', 'message']
    check_flag_validity(args)
    parsed_args = parse_args(args)
    valid = parsed_args.message_type == 'message'
    print("valid = " + str(valid))
    assert valid, "Expected --message-type to be parsed correctly."

if __name__ == '__main__':
    test_valid_flag()
    test_invalid_flag()
    