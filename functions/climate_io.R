#create a function to read the file
get_data <- function(folder_name) {
  dir <- paste0("~/Dados/", folder_name, "/compiled")
  file <- list.files(dir, pattern = "\\.csv$", full.names = TRUE)
  return(read_csv(file))
}












