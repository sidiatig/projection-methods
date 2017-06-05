import argparse
import cPickle
from glob import glob
from pathlib2 import PosixPath

import matplotlib.pyplot as plt
from mpldatacursor import datacursor

from projection_methods.experiment import k_apop

def main():
    parser = argparse.ArgumentParser()
    # --- input/output --- #
    parser.add_argument(
        'data', metavar='D',
        help=('glob matching pickled results to plot; results should be '
        'generated by experiment.py'))
    parser.add_argument(
        '-o', '--output', type=str, default=None,
        help=('output filename of plot (w/o extension); if None, plot is '
        'shown but not saved.'))
    # --- plot settings --- #
    parser.add_argument(
        '-t', '--title', type=str, default='Residuals for feasibility problem.',
        help='plot title')
    args = vars(parser.parse_args())

    if args['output'] is not None:
        output_path = PosixPath(args['output'] + '.png')
        if output_path.is_file():
            raise ValueError('Output file % already exists!' % str(output_path))

    data_paths = [PosixPath(f) for f in glob(args['data'])]
    data = []
    for p in data_paths:
        if not p.is_file():
            raise ValueError('File %s does not exist.' % str(p))
        with p.open('rb') as f:
            data.append(cPickle.load(f))

    plt.figure() 
    max_its = 0
    for d in data:
        res = d['res']
        if hasattr(res[0], '__iter__'):
            res = [sum(r) for r in res]
        if 0 in res:
            res = [r + 1e-20 for r in res]
        it = range(len(res))
        if len(res) > max_its:
            max_its = len(res)
        plt.plot(it, res, '-o', label=d['name'])
    plt.semilogy()
    plt.xticks(range(0, max_its+1, 1))
    plt.title(args['title']) 
    plt.legend()

    if args['output'] is not None:
        plt.savefig(str(output_path))
    else:
        datacursor(formatter='{label}'.format)
        plt.show()
    

if __name__ == '__main__':
    main()
