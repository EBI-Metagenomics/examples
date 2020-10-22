#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import csv
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from pandas import DataFrame

from jsonapi_client import Session, Filter


API_BASE = 'https://www.ebi.ac.uk/metagenomics/api/latest/'


def main(args=None):
    filename = args.filename

    with open(filename, "w") as csvfile:
        with Session(API_BASE) as s:
            fieldnames = ['study', 'study_name', 'biomes', 'samples_count', 'metadata', 'publications']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for study in s.iterate('biomes/root:Host-associated:Human:Digestive%20system/studies'):
                biomes = [b.id for b in study.biomes]
                publications = "; ".join([p.doi for p in study.publications])
                row = {
                    'study': study.accession,
                    'study_name': study.study_name,
                    'biomes': biomes,
                    'samples_count': study.samples_count,
                    'publications': publications,
                }
                metadata = list()
                for sample in study.samples:
                    keys = [m['key'] for m in sample.sample_metadata]
                    metadata.extend(keys)
                row['metadata'] = "; ".join(sorted(set(metadata)))
                writer.writerow(row)

if __name__ == '__main__':
    """
    Example:
    python api_export_biomes.py --filename output.csv
    """

    parser = argparse.ArgumentParser(description='Export to csv')
    parser.add_argument('--filename', '-f', required=True,
                        help='Output name')
    args = parser.parse_args()
    main(args)
