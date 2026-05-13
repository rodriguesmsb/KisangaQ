
libraries <- c(
  "tidyverse", "lubridate", "read.dbc", "readr"
)

#load and install packages
for(lib in libraries) {
  if (!require(lib, character.only = TRUE)) {
    install.packages(lib, dependencies = TRUE)
    library(lib, character.only = TRUE)
  }
}


#create a function to list dbc files
list_datasus_files <- function(folder_name) {
  dir <- paste0("~/Dados/", folder_name)
  list.files(dir, pattern = "\\.dbc$|\\.zip$", full.names = TRUE)
}


read_datasus_files <- function(folder_name, extension){
  files <- list_datasus_files(folder_name)
  if(extension == "dbc") {
    data_list <- lapply(files, read.dbc)
  } 
  else if(extension == "zip"){
    data_list <- lapply(files, read_csv)
  }
  combined_data <- bind_rows(data_list)
  
  #convert column names to lowercase and remove leading/trailing whitespaces
  combined_data <- combined_data %>%
    rename_with(~ str_squish(tolower(.)))
  return(combined_data)
}






















