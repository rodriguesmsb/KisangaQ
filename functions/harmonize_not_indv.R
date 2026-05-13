#create a function to harmonize demographics information

harmonize_demographics <- function(data) {
  data <- data %>%
    mutate(
      idade = nu_ano - ano_nasc,
      sexo = if_else(cs_sexo == "M", "M", "F", NA_character_),
      gestante = case_when(
        cs_gestant == 1 ~ "Pri_trimestre",
        cs_gestant == 2 ~ "Sec_trimestre",
        cs_gestant == 3 ~ "Ter_trimestre",
        cs_gestant == 4 ~ "Gestante",
        cs_gestant == 5 ~ "Nao_gestante",
        .default = NA_character_
      ),
      raca_cor = case_when(
        cs_raca == 1 ~ "Branca",
        cs_raca == 2 ~ "Preta",
        cs_raca == 3 ~ "Amarela",
        cs_raca == 4 ~ "Parda",
        cs_raca == 5 ~ "Indigena",
        .default =   NA_character_
      ),
      escolaridade = case_when(
        cs_escol_n == 1 ~ "4 incompleta",
        cs_escol_n == 2 ~ "4 completa",
        cs_escol_n == 3 ~ "5-8 incompleta",
        cs_escol_n == 4 ~ "Ensino fundamental completo",
        cs_escol_n == 5 ~ "Ensino medio incompleto",
        cs_escol_n == 6 ~ "Ensino medio completo",
        cs_escol_n == 7 ~ "Ensino superior incompleto",
        cs_escol_n == 8 ~ "Ensino superior completo",
        .default = NA_character_)
    ) %>% 
    rename(
      municipio_residencia = id_mn_resi
    ) %>%
    select(-c(cs_gestant,cs_raca,cs_escol_n))
  return(data)
}
      