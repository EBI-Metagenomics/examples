# load libraries, use install.packages(library) if not installed
library("ggplot2")
library("data.table")
library("RColorBrewer")
library("jsonlite")
library("rjsonapi")


# create connection to the MGnify API
conn <- jsonapi_connect("https://www.ebi.ac.uk", "metagenomics/api/v1")

# MGYS00002474 (DRP001073) Metabolically active microbial communities
# in marine sediment under high-CO2 and low-pH extremes
accession = "MGYS00002474"

# MGYS00002421 (ERP009568) Prokaryotic microbiota associated to the digestive
# cavity of the jellyfish Cotylorhiza tuberculata
# accession = "MGYS00002421"

# MGYS00002441 EMG produced TPA metagenomics assembly of
# the doi: 10.3389/fmicb.2016.00579
# accession = "MGYS00002441"

# MGYS00002394 (SRP051741) Subgingival plaque and peri-implant biofilm
# accession = "MGYS00002394"

# MGYS00001211 (SRP076746) Human gut metagenome Metagenome
# accession = "MGYS00001211"

analyses <- conn$route(paste0("studies/", accession ,"/analyses"))

# load all the accessions
accessions = analyses$data$attributes$accession

# Select individual analyses, e.g. OSD
# accessions = c( )

# check if the dataset already exists
if (exists("access.df")){
  rm(access.df)
}

# load and format each individual csv
for (a in accessions) {
  
  taxa = conn$route(paste("analyses", a, "taxonomy", sep="/"))
  if (length(taxa$data) < 1) {
    taxa = conn$route(paste("analyses", a, "taxonomy", "ssu", sep="/"))
  }
  
  df = taxa$data$attributes
  relabs = as.numeric(df[,1])/sum(df$count)*100
  phy.counts = data.frame(relabs, df[,"hierarchy"][,"genus"], stringsAsFactors = FALSE)
  colnames(phy.counts) = c("Rel.Ab", "Genus")
  phy.merged = aggregate(Rel.Ab ~ Genus, data=phy.counts, sum)
  phy.merged$Accession = a
  if (!exists("access.df")){
    access.df = phy.merged
  } else {
    access.df = rbind(access.df, phy.merged)
  }
}

# format combined dataset
colnames(access.df) = c("Genus", "Rel.Ab", "Accessions")

# determine most common phyla across accessions
summ = aggregate(Rel.Ab ~ Genus, data=access.df, sum)
top.genus = summ[order(summ$Rel.Ab, decreasing=TRUE)[1:10],"Genus"]


# keep only most common phyla
for (b in unique(access.df$Accessions)){ # for each accession
  relab.other = 100-sum(as.numeric(access.df[which(access.df$Accessions == b & access.df$Genus %in% top.genus),"Rel.Ab"])) # take relative abundance for all non-top phyla
  access.df = rbind(access.df, c("Other", relab.other, b))
}
access.df = access.df[which(access.df$Genus %in% top.genus | access.df$Genus == "Other"),] # only keep top phyla and the other category
access.df$Genus = factor(access.df$Genus, levels=rev(c(top.genus, "Other"))) # reorder phylum for plotting

# plot bargraph with counts
phy.colors = c("#A3A3A3", "#FFED6F","#CCEBC5","#BC80BD","#D9D9D9","#FCCDE5",
               "#B3DE69", "#FDB462", "#80B1D3", "#FB8072", "#FFFFB3", "#BEBADA", "#8DD3C7") # define colors for plotting phyla
print(ggplot(access.df, aes(x=Accessions, y=as.numeric(Rel.Ab), fill=Genus)) 
      + geom_bar(stat="identity", colour = "darkgrey", size = 0.3, width = 0.6, alpha=0.7)
      + theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5))
      + ggtitle(accession)
      + ylab("Relative abundance (%)")
      + theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())
      + scale_fill_manual(values=c(phy.colors))
      + theme(axis.title.y = element_text(size=10))
      + theme(axis.text.y = element_text(size=10))
      + theme(axis.title.x = element_blank())
      + theme(axis.text.x = element_text(size=10)))
