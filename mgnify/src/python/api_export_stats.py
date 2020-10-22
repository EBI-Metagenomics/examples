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
            fieldnames = ['biome', 'studies_count', 'samples_count']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for biome in s.iterate('biomes/root:Host-associated:Human:Digestive%20system/children'):
                studies = s.get('biomes/{}/studies'.format(biome.lineage))
                row = {
                    'biome': biome.id,
                    'samples_count': biome.samples_count,
                    'studies_count': studies.meta.pagination['count']
                }

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
