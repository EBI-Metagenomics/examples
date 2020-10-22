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
    accession = args.accession

    with open(filename, "w") as csvfile:
        with Session(API_BASE) as s:
            fieldnames = ['study', 'sample', 'biome', 'lineage', 'longitude', 'latitude']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            study = s.get('studies', accession).resource
            for sample in study.samples:
                biome = sample.biome
                row = {
                    'study': study.accession,
                    'sample': sample.accession,
                    'biome': biome.biome_name,
                    'lineage': biome.lineage,
                    'longitude': sample.longitude,
                    'latitude': sample.latitude
                }
                writer.writerow(row)

if __name__ == '__main__':
    """
    Example:
    python api_export.py --filename output.csv --accession ERP005831
    """

    parser = argparse.ArgumentParser(description='Export to csv')
    parser.add_argument('--filename', '-f', required=True,
                        help='Output name')
    parser.add_argument('--accession', '-a', required=True,
                        help='Study accession')
    args = parser.parse_args()
    main(args)
