#!/usr/bin/env python3.3

import argparse
import sys

def run(): 
    parser = argparse.ArgumentParser()
    parser.add_argument('hdf_file')
    parser.add_argument(
        '-o', '--out-dir', help='output dir (default %(default)s)', 
        default='plots')
    parser.add_argument(
        '-e', '--ext', help='plot extension (default %(default)s)', 
        default='.pdf')

    fdict = {f.name: f for f in [ctag, roc, pt]}
    parser.add_argument(
        '-p', '--plots', help='plots to make (default %(default)s)', 
        choices=fdict.keys(), default='all')
    parser.add_argument(
        '-t', '--taggers', help='only plot a subset of b-taggers', nargs='+')
    args = parser.parse_args(sys.argv[1:])
    
    if args.plots == 'all': 
        plots = fdict.keys()
    else: 
        plots = [args.plots]
    for plt in plots: 
        fdict[plt](args)

def name(name): 
    def named(function): 
        function.name = name
        return function
    return named

@name('ctag')
def ctag(args): 
    from tagperf import ctaging
    print('making ctag plots')
    ctaging.make_plots(args.hdf_file, 'REJREJ_CACHE.h5', args.out_dir, 
                        args.ext)

@name('roc')
def roc(args): 
    from tagperf import tagroc
    print('making roc plots')
    tagroc.make_plots(args.hdf_file, args.out_dir, args.ext)

@name('pt')
def pt(args): 
    from tagperf import tagpt
    print('making pt plots')
    tagpt.make_plots(args.hdf_file, args.out_dir, args.ext, 
                     subset=args.taggers)

if __name__ == '__main__': 
    run()
