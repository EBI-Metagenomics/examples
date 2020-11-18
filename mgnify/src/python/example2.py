#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import csv
from jsonapi_client import Session, Filter

from plotnine import *
import pandas

API_BASE = "https://www.ebi.ac.uk/metagenomics/api/v1"

TAX_RANK = "phylum"


# MGYS00002474 (DRP001073) Metabolically active microbial communities
# in marine sediment under high-CO2 and low-pH extremes
study_accession = "MGYS00002474"

# MGYS00002421 (ERP009568) Prokaryotic microbiota associated to the digestive
# cavity of the jellyfish Cotylorhiza tuberculata
# study_accession = "MGYS00002421"

# MGYS00002371 (DRP000490) Porcupine Seabight 16S Ribosomal RNA
# study_accession = "MGYS00002371"

# MGYS00002441 EMG produced TPA metagenomics assembly of
# the doi: 10.3389/fmicb.2016.00579
# study_accession = "MGYS00002441"

# MGYS00002394 (SRP051741) Subgingival plaque and peri-implant biofilm
# study_accession = "MGYS00002394"

# MGYS00001211 (SRP076746) Human gut metagenome Metagenome
# study_accession = "MGYS00001211"

# MGYS00000601 (ERP013908) Assessment of Bacterial DNA Extraction Procedures for Metagenomic Sequencing Evaluated
# on Different Environmental Matrices.
# study_accession = "MGYS00000601"

# MGYS00002115
# The study includes fungal genetic diversity assessment by ITS-1 next generation sequencing (NGS) analyses
# study_accession = "MGYS00002115"

resource = "studies/" + study_accession + "/analyses"

rows = []

with Session(API_BASE) as session:

    analyses = session.get(resource).resources

    analyses_accs = [a.accession for a in analyses]

    # Select individual analyses, e.g. OSD
    # analyses_accs = [""]

    for analysis_accession in analyses_accs:

        for t in session.iterate(
            "/".join(["analyses", analysis_accession, "taxonomy", "ssu"])
        ):
            if t.hierarchy.get(TAX_RANK):
                rows.append(
                    {
                        "analysis": analysis_accession,
                        "study": study_accession,
                        TAX_RANK: t.hierarchy.get(TAX_RANK),
                        "count": t.count,
                        "rel_abundance": 0,  # this will be filled afterwards
                    },
                )
    
    # end of data fetch

    data_frame = pandas.DataFrame(rows)

    # let's aggregate by Phyla
    data_frame = data_frame.groupby(["analysis", TAX_RANK])["count"].sum().reset_index()

    # let's get the relative abundance of each phyla
    for analysis, frame in data_frame.groupby("analysis"):
        data_frame.loc[data_frame["analysis"] == analysis, "rel_abundance"] = (
            frame["count"] / frame["count"].sum() * 100
        )

    # let's save a copy in csv
    data_frame.to_csv(study_accession + "_" + TAX_RANK + ".csv")

    # let's aggregate the abundances to reduce the noise, let's keep the top 10
    # and move the small ones to the Other category
    top10 = sorted(
        list(
            data_frame.groupby([TAX_RANK])["rel_abundance"]
            .agg("sum")
            .nlargest(10)
            .index
        )
    )

    for analysis, frame in data_frame.groupby("analysis"):
        top_rows = data_frame.loc[
            (data_frame["analysis"] == analysis) & (data_frame[TAX_RANK].isin(top10)),
            "rel_abundance",
        ]
        # The Other aggregated row
        data_frame = data_frame.append(
            {
                "analysis": analysis,
                "study": study_accession,
                "rel_abundance": 100 - top_rows.sum(),
                TAX_RANK: "Other",
                "count": 0,
            },
            ignore_index=True,
        )

    # keep only top10 or Other
    data_frame = data_frame.drop(
        data_frame[
            (~data_frame[TAX_RANK].isin(top10)) & (data_frame[TAX_RANK] != "Other")
        ].index
    )

    # define colors for plotting
    colors = [
        "#A3A3A3",
        "#FFED6F",
        "#CCEBC5",
        "#BC80BD",
        "#D9D9D9",
        "#FCCDE5",
        "#B3DE69",
        "#FDB462",
        "#80B1D3",
        "#FB8072",
        "#FFFFB3",
        "#BEBADA",
        "#8DD3C7",
    ]

    top10.insert(0, "Other")
    data_frame[TAX_RANK] = pandas.Categorical(data_frame[TAX_RANK], top10)
    data_frame = data_frame.sort_values(TAX_RANK)

    gb = geom_bar(stat="identity", colour="darkgrey", size=0.3, width=0.6, alpha=0.7)
    gg = (
        ggplot(
            data_frame,
            aes(
                x=data_frame["analysis"],
                y=data_frame["rel_abundance"],
                fill=TAX_RANK,
            ),
        )
        + gb
        + ggtitle(study_accession)
        + ylab("Relative abundance (%)")
        + theme(panel_grid_major=element_blank(), panel_grid_minor=element_blank())
        + scale_fill_manual(values=colors)
        + theme(axis_text_x=element_text(angle=90))
        + theme(axis_title_y=element_text(size=10))
        + theme(axis_text_y=element_text(size=10))
        + theme(axis_title_x=element_blank())
        + theme(axis_text_x=element_text(size=10))
    )

    ggsave(
        filename=study_accession + "_" + TAX_RANK + "_plot.png",
        plot=gg,
        device="png",
        dpi=600,
    )
