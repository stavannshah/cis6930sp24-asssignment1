import argparse
import glob
import sys
import os

from assignment1.main import *


def process_files(args):
    raw_files = []
    for inp_glob in args.input:
        raw_files += glob.glob(inp_glob)
    return raw_files


def censor_data(raw_file, data, censor_functions):
    censor_counts = {}
    censor_list = {}

    for censor_func in censor_functions:
        data, censored_items = censor_func(data)
        censor_counts[censor_func.__name__ + "_count"] = len(censored_items)
        censor_list[censor_func.__name__ + "_list"] = censored_items

    return data, censor_counts, censor_list


def write_to_file(output_path, data):
    with open(output_path, 'w') as f:
        f.write(data)


def main(args):
    censor_functions = [censor_address, censor_names, censor_dates, censor_phones, censor_genders]

    final_stats = ""
    for raw_file in process_files(args):
        print("Processing", raw_file, "==>")
        data = ""
        try:
            with open(raw_file, 'r') as f:
                data = f.read()
        except:
            print(f"{raw_file} file cannot be read and therefore cannot be censored.\n")
            continue

        data, censor_counts, censor_list = censor_data(raw_file, data, censor_functions)

        if args.output == 'stdout' or args.output == 'stderr':
            output_stream = sys.stdout if args.output == 'stdout' else sys.stderr
            output_stream.write(data + '\n')
        else:
            write_to_file(os.path.join(args.output, os.path.splitext(os.path.basename(raw_file))[0] + '.censored'), data)

        stats = censor_stats(args, censor_counts, censor_list)
        final_stats += f"------Data is censored from {raw_file} file, below is the statistics of the censorions made in file------\n" + stats + "\n\n"

    if args.stats == 'stdout':
        sys.stdout.write("\n-----------Data is censored from {raw_file} file, below is the statistics of the censorions made in file---------------\n")
        sys.stdout.write(final_stats + '\n')
    elif args.stats == 'stderr':
        sys.stderr.write("\n-----------Data is censored from {raw_file} file, below is the statistics of the censorions made in file---------------\n")
        sys.stderr.write(final_stats + '\n')
    else:
        write_to_file(args.stats, final_stats)


def censor_stats(args, censor_counts, censor_list):
    stats_list = []

    for arg_name, censor_type in [("names", "names"), ("dates", "dates"), ("phones", "phone numbers"), ("genders", "genders"), ("address", "address/es")]:
        if vars(args)[arg_name]:
            stats_list.append(f"In total {censor_counts[arg_name + '_count']} {censor_type} got censored.")
            stats_list.append(f"\tThe {censor_type} that got censored are {censor_list[arg_name + '_list']} ")

    return "\n".join(stats_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, type=str, action="append", help='Input file(s) to be processed.')
    parser.add_argument('--names', action="store_true", help='Censor names from input file(s).')
    parser.add_argument('--dates', action="store_true", help='Censor dates from input file(s).')
    parser.add_argument('--phones', action="store_true", help='Censor phone numbers from input file(s).')
    parser.add_argument('--genders', action="store_true", help='Censor gender revealing words from input file(s).')
    parser.add_argument('--address', action="store_true", help='Censor addresses in input file(s).')
    parser.add_argument('--concept', type=str, action="append", help='Censor concept statements in input file(s).')
    parser.add_argument('--output', required=True, help='Specify the output format for censored data (stdout, stderr, or a directory path).')
    parser.add_argument('--stats', required=True, help='Specify the output format for censoring statistics (stdout, stderr, or a file path).')

    args = parser.parse_args()
    main(args)

