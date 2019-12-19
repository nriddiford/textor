#!/usr/bin/env python
from __future__ import print_function, division
import json
import ntpath
import os
import pysam
import re
import sys
from collections import defaultdict
from optparse import OptionParser


def extract_reads(options):
    bam_file = pysam.Samfile(options.bam, "rb")

    for read in bam_file.fetch('X', 1e6, 1.5e6):
        if read.is_supplementary:
            try:
                sa_te = read.get_tag('AD').split(',')[0]
                sa_te = '_'.join(sa_te.split('_')[1:])
                if options.debug: print("read has supplementary alignment to TE:", sa_te, read.query_name)
            except KeyError:
                pass
        else:
            try:
                te = read.get_tag('BR').split(',')[0]
                te = '_'.join(te.split('_')[1:])
                print(te)
            except KeyError:
                pass

    bam_file.close()

    return True


def main():
    parser = OptionParser()
    parser.add_option("-b", "--bam", dest="bam", help="Bam file to extract reads from")
    # parser.add_option("-w", "--window", dest="window", action="store", type=int, help="The distance to search for connected breakpoints [Default: 1kb]")
    parser.add_option("-o", "--out_dir", dest="out_dir", action="store", help="Directory to write output to " + "[Default: '.']")
    parser.add_option("-d", "--debug", dest="debug", action="store_true", help="Run in debug mode")

    parser.set_defaults(out_dir=os.getcwd())
    options, args = parser.parse_args()

    if options.bam is None:
        parser.print_help()
        print()
    else:
        try:
            extract_reads(options)
        except IOError as err:
            sys.stderr.write("IOError " + str(err) + "\n")
            return


if __name__ == "__main__":
    sys.exit(main())
