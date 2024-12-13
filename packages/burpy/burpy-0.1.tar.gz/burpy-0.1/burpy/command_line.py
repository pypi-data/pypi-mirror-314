import argparse
import burpy


parser = argparse.ArgumentParser(description='Parse Burp Suite HTTP history')
parser.add_argument('--file_path', help='The path to the Burp HTTP history export')
parser.add_argument('--output_format', choices={"json", "csv", "xlsx"}, help='The format of the output')

args = parser.parse_args()

def main():
    burpy.log_analysis(args.file_path, args.output_format)