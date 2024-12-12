import argparse


parser = argparse.ArgumentParser()

parser.add_argument(
    "--switch", type=bool, default=True, action=argparse.BooleanOptionalAction
)

args = parser.parse_args()


print(args)
