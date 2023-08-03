import argparse
import json
from common import types

def model_config_parser(filepath: str) -> dict:
    config = None
    with open(filepath, "rt") as f:
        config = json.loads(f.read())
    return config

def platform_config_parser(filepath: str) -> dict:
    config = None
    with open(filepath, "rt") as f:
        config = json.loads(f.read())
    return config


def arg_parser() -> types.ArgsType:
    parser = argparse.ArgumentParser(description="Please provide the model config file and platform config file.")
    parser.add_argument("-m", "--model", type=str, required=False,     default='model.json',
                        help="model config file for simulation")
    parser.add_argument("-p", "--platform", type=str, required=False,  default='platform.json',
                        help="platform config file for simulation")
    parser.add_argument("-o", "--out", type=str, required=False,
                        help="trace file name that simulator will generator")
    args = parser.parse_args()
    return args
#############################################################################

def prepare_environment() -> type[types.Environment]:
    return dict()

#############################################################################
def __test():
    args = arg_parser()
    print( args )
    model_filename, platform_filename = args.model, args.platform
    print( model_config_parser( model_filename ) )

if __name__ == '__main__':
    __test()