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
library(fastmap)

########################################

PAPERS_PER_VENUE <- 5

papers <- fread("../output/venues_validated.csv", header=TRUE, sep=",", quote="\"", strip.white=TRUE, showProgress=TRUE, encoding="UTF-8", na.strings=c("", "null"), stringsAsFactors=FALSE)
papers <- fread("../output/venues_2019_validated.csv", header=TRUE, sep=",", quote="\"", strip.white=TRUE, showProgress=TRUE, encoding="UTF-8", na.strings=c("", "null"), stringsAsFactors=FALSE)
nrow(papers)
# 1,564 / 265 (2019)

papers <- unique.data.frame(papers)
nrow(papers)
# 1564 / 265 (2019)

papers <- papers[papers$is_full_paper == TRUE]
nrow(papers)
# 1,215 / 265 (2019)

unique_venues <- unique(papers$identifier)
length(unique_venues)
# 20 / 4 (2019)

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
# 100 / 20 (2019)

# randomize order
sample <- sample[randomSequence(min=1, max=nrow(sample), col=1, check=TRUE)[,1]]

#write.table(sample, file="../output/sample.csv", sep=",", col.names=TRUE, row.names=FALSE, na="", quote=TRUE, qmethod="double", fileEncoding="UTF-8")
write.table(sample, file="../output/sample_2019.csv", sep=",", col.names=TRUE, row.names=FALSE, na="", quote=TRUE, qmethod="double", fileEncoding="UTF-8")

########################################

# read sample
#sample <- fread("../output/sample.csv", header=TRUE, sep=",", quote="\"", strip.white=TRUE, showProgress=TRUE, encoding="UTF-8", na.strings=c("", "null"), stringsAsFactors=FALSE)
sample <- fread("../output/sample_2019.csv", header=TRUE, sep=",", quote="\"", strip.white=TRUE, showProgress=TRUE, encoding="UTF-8", na.strings=c("", "null"), stringsAsFactors=FALSE)
nrow(sample)
# 100 / 20 (2019)

# check for journal extensions of conference papers (same authors)

authors_papers <- fastmap()

for (i in 1:nrow(sample)) {
  authors <- strsplit(sample[i]$authors, ";")
  authors <- unlist(lapply(authors, trimws))
  authors <- paste(authors[order(authors)], collapse="; ")
  if (authors_papers$has(authors)) {
    authors_papers$set(authors, paste(authors_papers$get(authors), sample[i]$title, sep=";"))
  } else {
    authors_papers$set(authors, sample[i]$title)
  }
}

length(authors_papers$keys())
# 100 / 20 (2019)

for (authors in authors_papers$keys()) {
  papers <- unlist(strsplit(authors_papers$get(authors), ";"))
  if (length(papers) >= 1) {
    print(paste0("Authors: ", authors))
    print(paste0("Papers: ", paste(papers, collapse="; ")))
  }
}
