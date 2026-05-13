#' Recode SINAN TB Variables
#'
#' Applies standardized recoding to SINAN TB notification fields.
#' Designed to work inside a dplyr pipeline via `mutate()`.
#' Uses `dplyr::case_match()` (requires dplyr >= 1.1.0).
#'
#' @param df A data frame containing raw SINAN TB variables.
#' @return A data frame with recoded columns appended/replaced.
#'
#' @examples
#' df_clean <- df_raw |> recode_sinan_tb()
recode_sinan_tb <- function(df) {
  
  # Helper: apply a named-vector map to a column via case_match

  remap <- function(col, ...) {
    dplyr::case_match(col, ..., .default = NA)
  }
  
  df |>
    dplyr::mutate(
      
      # Race
      cs_raca = dplyr::coalesce(remap(raca_cor,
                                      "Branca" ~ "White"),
                                "Non White"
                      
      ),
      
      # Sex
      cs_sexo = remap(cs_sexo,
                      "F" ~ "F",
                      "M" ~ "M"
      ),
      
      # Vulnerable populations: 1 = Yes, 0 = No
      pop_imig  = remap(pop_imig,  1 ~ 1, 2 ~ 0, 9 ~ NA_real_),
      pop_rua   = remap(pop_rua,   1 ~ 1, 2 ~ 0, 9 ~ NA_real_),
      pop_saude = remap(pop_saude, 1 ~ 1, 2 ~ 0, 9 ~ NA_real_),
      pop_liber = remap(pop_liber, 1 ~ 1, 2 ~ 0, 9 ~ NA_real_),
      
      # Pregnancy:
      gestante = dplyr::coalesce(remap(gestante,
                      "Nao_gestante" ~ "No pregnant",
                      "Gestante" ~ "Pregnant",
                      "Sec_trimestre" ~ "First_trimester",
                      "Pri_trimestre" ~ "Second_trimester",
                      "Ter_trimestre" ~ "Third_trimester"),
                      NA_character_
                       
      ),
      
      # Case closure outcome 
      situa_ence = remap(situa_ence,
                         1  ~ "Cure",
                         2  ~ "Treatment incomplete",
                         3  ~ "Death",
                         4  ~ "Death",
                         5  ~ "Transfer",
                         6  ~ "Diagnostic change",
                         7  ~ "Regimen switch",
                         8  ~ "Regimen switch",
                         9  ~ "Failure",
                         10 ~ "Treatment incomplete"
      ),
      
      # Education 
      education = dplyr::coalesce(remap(escolaridade,
                                         "4 incompleta" ~ "Elementary incomplete",                                      
                                         "Ensino medio incompleto" ~ "High school incomplete",      
                                         "4 completa"  ~ "Elementary school",
                                         "5-8 incompleta" ~ "High school incomplete",
                                         "Ensino medio completo" ~  "High school",     
                                         "Ensino superior incompleto" ~ "High school", 
                                         "Ensino superior completo" ~ "Bachelor's degree or higher",
                                         "Ensino fundamental completo" ~ "Elementary school",
                                           ),
                                   NA_character_
                      
      ),
      
      # HIV infection
      hiv = remap(hiv, 1 ~ "Yes", 2 ~"No"),
      
      ## Comorbidities
      
      # Ilicit drug use,
      agravdroga = remap(agravdroga, 1 ~ "Yes", 2 ~ "No", 9 ~ NA_character_),
      # HIV/AIDS,
      agravaids  = remap(agravaids,  1 ~ "Yes", 2 ~ "No", 9 ~ NA_character_),
      # Smoking
      agravtabac = remap(agravtabac, 1 ~ "Yes", 2 ~ "No", 9 ~ NA_character_),
      # Alcohol mismuse
      agravalcoo = remap(agravalcoo, 1 ~ "Yes", 2 ~ "No", 9 ~ NA_character_),
      # Diabetes
      agravdiabe = remap(agravdiabe, 1 ~ "Yes", 2 ~ "No", 9 ~ NA_character_),
      # Mental illness
      agravdoenc = remap(agravdoenc, 1 ~ "Yes", 2 ~ "No", 9 ~ NA_character_),
      # Other comorbidities Other
      agravoutra = remap(agravoutra, 1 ~ "Yes", 2 ~ "No", 9 ~ NA_character_),
      
      # Case type
      tratamento = dplyr::coalesce(
        remap(tratamento,
              1 ~ "New Case",
              2 ~ "Relapse",
              3 ~ "Re enter",
              4 ~ "New Case",
              5 ~ "Transfer",
              6 ~ "After dead"
        ),
        "New Case"
      ),
      
      # Chest X-ray
      raiox_tora = remap(raiox_tora, 1 ~ "Abnormal", 2 ~ "Normal"),
      
      # --- Directly Observed Therapy (DOT)

      tratsup_at = dplyr::coalesce(
        remap(tratsup_at, 1 ~ "Yes", 2 ~ "No")
      ),
      
      #  Antiretroviral therapy
      ant_retro = remap(ant_retro, 1 ~ "Yes", 2 ~ "No", 9 ~ NA_character_),
      
      # Sputum smear microscopy
      bacilosc_e = remap(bacilosc_e,
                         1 ~ "Positive", 
                         2 ~ "Negative",
                         3 ~ "Not performed", 
                         4 ~ NA_character_),
      
      # Histopathology 
      histopatol = remap(histopatol,
                         1 ~ "Baar Positive",
                         2 ~ "Probably TB",
                         3 ~ "Probably no TB",
                         4 ~ NA_character_,
                         5 ~ "Not performed"
      ),
      
      # -Sputum culture
      cultura_es = remap(cultura_es,
                         1 ~ "Positive", 2 ~ "Negative",
                         3 ~ NA_character_, 4 ~ "Not performed"
      ),
      
      # Drug sensitivity test
      test_sensi = remap(test_sensi,
                         1 ~ "Resistant to Isoniazid",
                         2 ~ "Resistant to Rifampicin",
                         3 ~ "Resistant to Isoniazid and Rifampicin",
                         4 ~ "Resistant to other first-line drugs",
                         5 ~ "Sensitive",
                         6 ~ "on going",
                         7 ~ "not performed",
                         9 ~ "missing"
      ),
      
      # Molecular test (GeneXpert / NAAT)
      test_molec = remap(test_molec,
                         1 ~ "Detectável sensível à Rifampicina",
                         2 ~ "Detectável resistente à Rifampicina",
                         3 ~ "Não detectável",
                         4 ~ "Inconclusivo",
                         5 ~ "Não realizado"
      ),
      
      # Social benefit (Bolsa Família etc.)
      benef_gov = remap(benef_gov, 1 ~ "Yes", 2 ~ "No"),
      
      # Disease form 
      forma = dplyr::coalesce(
        remap(forma,
              1 ~ "Pulmonary",
              2 ~ "Extra-pulmonary",
              3 ~ "Booth"
        ),
        "Pulmonary"
      ),
      
      # -Monthly sputum smear follow-up (months 1–6) 
      dplyr::across(
        dplyr::matches("^bacilosc_[1-6]$"),
        ~ remap(.x,
                1 ~ "Positive",
                2 ~ "Negative",
                3 ~ "on going",
                4 ~ "Not performed"
        )
      )
    )
}