# load libraries, use install.packages(library) if not installed
library("rjsonapi")

# create connection to the MGnify API
conn <- jsonapi_connect("https://www.ebi.ac.uk", "metagenomics/api/v1")

# declare samples variable
if (exists("samples")){
  rm(samples)
}
samples=data.frame()

# start from first page
p = 1

# repeat until last page
repeat{
  # fetch each page
  # change biome: 'root:Environmental:Terrestrial:Soil'"
  # change geolocation latitude_gte=-10&latitude_lte=10
  # OSD onlyu study_accession=MGYS00000462

  sam <- conn$route(
    paste0("biomes/root:Environmental:Aquatic/samples", 
           "?latitude_gte=70", 
           "&experiment-type=metagenomic",
           "&ordering=accession",
           "&page=", p)
  )
  sdf = cbind(
    sam$data$attributes[,c("accession", "sample-name", "longitude", "latitude", "geo-loc-name")],
    study=sapply(sapply(sam$data$relationships$studies$data, `[[`, 2),`[[`, 1),
    biome=sam$data$relationships$biome$data$id
  )
  # append to samples
  samples = rbind(sdf, samples, stringsAsFactors=FALSE)
  message("Retrieving page ", p)
  
  # check if next page exists
  p = sam$meta$pagination$page + 1
  if (p > sam$meta$pagination$pages) {
    break
  }
  
}

# save to csv
write.csv(samples, file="~/exercise1.csv")
