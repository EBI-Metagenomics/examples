#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jsonapi_client import Session

API_BASE = "https://www.ebi.ac.uk/metagenomics/api/v1"

# API call
with Session(API_BASE) as session:

    sample = session.get("samples", "SRS2704733").resource

    # done, data retrieved
    print("Sample attributes")
    print("  Accession:", sample.accession)
    print("  Sample Name:", sample.sample_name)
    print("  Longitude:", sample.longitude)
    print("  Latitude:", sample.latitude)
    print("  Geo. loc. name:", sample.geo_loc_name)

    print("Sample relationships")
    print("  Biome: ", sample.biome.id)
    print("  Runs:")
    for run in sample.runs:
        print("    ", run.accession, " - ", run.links.self)
