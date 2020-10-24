#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import csv
from urllib.parse import urlencode
from jsonapi_client import Session, Filter

API_BASE = "https://www.ebi.ac.uk/metagenomics/api/v1"


if __name__ == "__main__":

    with open("exercise1.csv", "w") as csvfile:
        # CSV initialization
        fieldnames = [
            "accession",
            "sample-name",
            "longitude",
            "latitude",
            "geo-loc-name",
            "study",
            "biome",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # API calls
        with Session(API_BASE) as session:
            params = {
                "latitude_gte": 70,
                "experiment_type": "metagenomic",
                "ordering": "accession",
            }
            api_filter = Filter(urlencode(params))

            # sessions.iterate will take care of the pagination for us
            total = 0
            for sample in session.iterate(
                "biomes/root:Environmental:Aquatic/samples", api_filter
            ):
                total += 1
                for study in sample.studies:
                    row = {
                        "accession": sample.accession,
                        "sample-name": sample.sample_name,
                        "longitude": sample.longitude,
                        "latitude": sample.latitude,
                        "geo-loc-name": sample.geo_loc_name,
                        "study": study.accession,
                        "biome": sample.biome.id,
                    }
                    writer.writerow(row)

            print("Retrieved " + str(total) + " samples from the API")
