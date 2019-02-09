# set working directory (see https://stackoverflow.com/a/35842119)
dir = tryCatch({
  # script being sourced
  getSrcDirectory()[1]
}, error = function(e) {
  # script being run in RStudio
  dirname(rstudioapi::getActiveDocumentContext()$path)
})
setwd(dir)

library(data.table)
library(random)
library(hashmap)

PAPERS_PER_VENUE <- 5

papers <- fread("../output/venues_validated.csv", header=TRUE, sep=",", quote="\"", strip.white=TRUE, showProgress=TRUE, encoding="UTF-8", na.strings=c("", "null"), stringsAsFactors=FALSE)
nrow(papers)
# 1,564

papers <- unique.data.frame(papers)
nrow(papers)
# 1564

papers <- papers[papers$is_full_paper == TRUE]
nrow(papers)
# 1,215

unique_venues <- unique(papers$identifier)
length(unique_venues)
# 20

sampled_rows <- integer()
for (venue in unique_venues) {
  print(paste0("Processing venue ", venue))
  venue_rows <- which(papers$identifier==venue)
  selected_rows <- venue_rows[randomSequence(min=1, max=length(venue_rows), col=1, check=TRUE)[1:PAPERS_PER_VENUE,1]]
  stopifnot(length(unique(selected_rows)) == PAPERS_PER_VENUE)
  sampled_rows <- c(sampled_rows, selected_rows)
}

sample <- papers[sampled_rows,]
nrow(sample)
# 100

# randomize order
sample <- sample[randomSequence(min=1, max=nrow(sample), col=1, check=TRUE)[,1]]

write.table(sample, file="../output/sample.csv", sep=",", col.names=TRUE, row.names=FALSE, na="", quote=TRUE, qmethod="double", fileEncoding="UTF-8")

########################################

# read sample
sample <- fread("../output/sample.csv", header=TRUE, sep=",", quote="\"", strip.white=TRUE, showProgress=TRUE, encoding="UTF-8", na.strings=c("", "null"), stringsAsFactors=FALSE)
nrow(sample)
# 100

# check for journal extensions of conference papers (same authors)

authors_papers <- hashmap(character(), character())

for (i in 1:nrow(sample)) {
  authors <- strsplit(sample[i]$authors, ";")
  authors <- unlist(lapply(authors, trimws))
  authors <- paste(authors[order(authors)], collapse="; ")
  if (is.na(authors_papers$find(authors))) {
    authors_papers$insert(authors, sample[i]$title)
  } else {
    authors_papers$insert(authors, paste(authors_papers$find(authors), sample[i]$title, sep=";"))
  }
}

length(authors_papers$keys())
# 100

for (authors in authors_papers$keys()) {
  papers <- unlist(strsplit(authors_papers$find(authors), ";"))
  if (length(papers) > 1) {
    print(paste0("Authors: ", authors))
    print(paste0("Papers: ", paste(papers, collapse="; ")))
  }
}
