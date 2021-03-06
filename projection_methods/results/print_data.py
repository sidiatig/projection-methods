"""Utility script to print pickled problem data generated by experiment.py"""
import argparse
import cPickle

from pprint import pprint

parser = argparse.ArgumentParser()
parser.add_argument(
    'data', metavar='D', help='filename of pickled data to print.')
parser.add_argument(
    '-e', '--exclude_keys', type=str, nargs='+', default=['it', 'res'],
    help='keys to omit from the output')
args = parser.parse_args()


with open(args.data, 'rb') as f:
    data = cPickle.load(f)

pdata = {k: data[k] for k in data.keys() if k not in args.exclude_keys}
pprint(pdata)


