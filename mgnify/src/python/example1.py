#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import csv
import sys
from urllib.parse import urlencode

from jsonapi_client import Filter, Session

API_BASE = "https://www.ebi.ac.uk/metagenomics/api/v1"

# if you change the filters you may want to rename the output file
FILE_NAME = "example1.csv"

print("Fetching data...")

with open(FILE_NAME, "w") as csvfile:
    # CSV initialization
    fieldnames = [
        "accession",
        "sample-name",
        "longitude",
        "latitude",
        "geo-loc-name",
        "studies",
        "biome",
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # API call
    with Session(API_BASE) as session:

        # configure the filters
        params = {
            "latitude_gte": 70,
            "experiment_type": "metagenomic",
            "ordering": "accession",
        }

        api_filter = Filter(urlencode(params))

        total = 0

        # sessions.iterate will take care of the pagination for us
        for sample in session.iterate(
            "biomes/root:Environmental:Aquatic/samples", api_filter
        ):
            total += 1
            row = {
                "accession": sample.accession,
                "sample-name": sample.sample_name,
                "longitude": sample.longitude,
                "latitude": sample.latitude,
                "geo-loc-name": sample.geo_loc_name,
                "studies": ",".join([study.accession for study in sample.studies]),
                "biome": sample.biome.id,
            }
            writer.writerow(row)

        print("Data retrieved from the API")
        print("Total samples", str(total))
