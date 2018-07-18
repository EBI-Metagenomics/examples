# load libraries, use install.packages(library) if not installed
library("rjsonapi")

# MGYS00000389 (ERP005831) Stable isotope probing/metagenomics of terrestrial dimethylsulfide degrading microorganisms
accession = "MGYS00000389"

# MGYS00000453 (ERP009004) Hydrocarbon Metagenomics Project
# accession = "MGYS00000453"

# MGYS00000601 (ERP013908) Assessment of Bacterial DNA Extraction Procedures for Metagenomic Sequencing Evaluated
# on Different Environmental Matrices.
# accession = "MGYS00000601"

# MGYS00001984 (ERP104045) EMG produced TPA metagenomics assembly of the Canadian MetaMicrobiome Library Projects
# (Canadian MetaMicrobiome) data set
# accession = "MGYS00001984"

# create connection to the MGnify API
conn <- jsonapi_connect("https://www.ebi.ac.uk", "metagenomics/api/v1")

# Fetch samples
samples <- conn$route(paste0("studies/", accession, "/samples", "?page_size=250"))

# select columns and combine data into one DataFrame
df = cbind(
  samples$data$attributes[,c("accession", "longitude", "latitude", "sample-name", "geo-loc-name")],
  biome=samples$data$relationships$biome$data$id
)

# save to csv
fname = paste0("~/", accession, "-example.csv")
write.csv(df, file=fname)

