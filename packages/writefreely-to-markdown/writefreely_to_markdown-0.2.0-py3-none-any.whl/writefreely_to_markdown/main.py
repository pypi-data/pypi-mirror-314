import argparse
import json
from writefreely_to_markdown import lib


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="The json file you downloaded from your instance")
    parser.add_argument("--output-dir", "-o", dest="output_dir", default="exported", help="The output directory to put all the files, default to ./exported")
    args = parser.parse_args()

    with open(args.file) as fp:
        json_obj = json.load(fp)
        lib.write_json_as_markdown(json_obj, args.output_dir)


if __name__ == "__main__":
    main()
