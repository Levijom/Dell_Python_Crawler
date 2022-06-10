import argparse

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help="Operation", dest="command")
parser.add_argument("--version", help="Show version", action="version", version="1.0A1")

parser_get = subparsers.add_parser("get")
parser_update = subparsers.add_parser("update")
parser_cache = subparsers.add_parser("cache")

parser_get.add_argument("sourceFile", type=str, help="Source File (txt format)")
parser_get.add_argument("destFile", type=str, help="Destination file (xlsx format")
args = parser.parse_args()

print(args)
print(args.command)
