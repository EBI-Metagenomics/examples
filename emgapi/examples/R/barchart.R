# load libraries, use install.packages(library) if not installed
library(ggplot2)
library(data.table)
library(RColorBrewer)
library(jsonlite)
library(rjsonapi)

# set working directory
setwd("~/EBI/emg-api-client.git/tests/wmd/")

##########
accessions = c("MGYA00102827", "MGYA00005043")
(conn <- jsonapi_connect("https://www.ebi.ac.uk", "metagenomics/api/v1"))

# check if the dataset already exists
if (exists("access.df")){
  rm(access.df)
  rm(biomes)
}

# load and format each individual csv
for (a in accessions) {
  (tax <- conn$route(paste("analyses", a, "taxonomy", sep="/")))
  df = tax$data$attributes
  relabs = as.numeric(df[,1])/sum(tax$data$attributes$count)*100
  phy.counts = data.frame(relabs, df[,"hierarchy"][,"phylum"], stringsAsFactors = FALSE)
  colnames(phy.counts) = c("Rel.Ab", "Phylum")
  phy.merged = aggregate(Rel.Ab ~ Phylum, data=phy.counts, sum)
  phy.merged$Accession = a
  if (!exists("access.df")){
    access.df = phy.merged
  } else {
    access.df = rbind(access.df, phy.merged)
  }
}

# format combined dataset
biomes = access.df
#biomes = biomes[which(biomes$X != "total"),]
colnames(biomes) = c("Phylum", "Rel.Ab", "Accessions")
#biomes$Phylum = gsub(".*:", "", biomes$Phylum)

# determine most common phyla across biomes
summ = aggregate(Rel.Ab ~ Phylum, data=biomes, sum)
top.phylum = summ[order(summ$Rel.Ab, decreasing=TRUE)[1:10],"Phylum"]

# normalize counts into relative abundance
# biomes$Rel.Ab = rep(0,nrow(biomes))
# for (i in 1:nrow(biomes)){
#   biomes$Rel.Ab[i] = as.numeric(biomes$Counts[i])/sum(as.numeric(biomes$Counts[which(biomes$Biome == biomes$Biome[i])]))*100
# }

# keep only most common phyla
for (b in unique(biomes$Accessions)){ # for each accession
  #counts.other = sum(as.numeric(biomes[which(biomes$Biome == b & !biomes$Phylum %in% top.phylum),"Counts"])) # take counts for all non-top phyla
  relab.other = 100-sum(as.numeric(biomes[which(biomes$Accessions == b & biomes$Phylum %in% top.phylum),"Rel.Ab"])) # take relative abundance for all non-top phyla
  biomes = rbind(biomes, c("Other", relab.other, b))
}
biomes = biomes[which(biomes$Phylum %in% top.phylum | biomes$Phylum == "Other"),] # only keep top phyla and the other category
biomes$Phylum = factor(biomes$Phylum, levels=rev(c(top.phylum, "Other"))) # reorder phylum for plotting

# plot bargraph with counts
phy.colors = c("#A3A3A3", "#FFED6F","#CCEBC5","#BC80BD","#D9D9D9","#FCCDE5",
               "#B3DE69", "#FDB462", "#80B1D3", "#FB8072", "#FFFFB3", "#BEBADA", "#8DD3C7") # define colors for plotting phyla
print(ggplot(biomes, aes(x=Accessions, y=as.numeric(Rel.Ab), fill=Phylum)) 
      + geom_bar(stat="identity", colour = "darkgrey", size = 0.3, width = 0.6, alpha=0.7)
      + theme_bw()
      + ylab("Relative abundance (%)")
      #+ scale_x_discrete(limits=c("Human", "Animal", "Plant", "Soil", "Marine", "Food"))
      + theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())
      + scale_fill_manual(values=c(phy.colors))
      + theme(axis.title.y = element_text(size=14))
      + theme(axis.text.y = element_text(size=12))
      + theme(axis.title.x = element_blank())
      + theme(axis.text.x = element_text(size=12)))