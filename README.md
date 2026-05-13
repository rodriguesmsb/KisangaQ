# KisangaQ

Repositório de análise, preparação e organização de dados do projeto **KISANGA-Q – Síntese Quilombola entre Biodiversidade, Clima e Saúde para o Bem Viver**.

O KISANGA-Q é uma iniciativa de síntese científica voltada à integração de dados ambientais, climáticos, sociais, fundiários e de saúde para compreender relações entre integridade ecológica, vulnerabilidade social, mudanças climáticas e saúde física e mental em territórios quilombolas da Amazônia, Cerrado e Caatinga.

## Objetivo do repositório

Este repositório concentra scripts e rotinas para apoiar a construção da biblioteca de dados do KISANGA-Q. Ele funciona como a camada analítica do ecossistema, responsável por preparar bases, gerar amostras, organizar metadados e alimentar a interface web disponível em [`kisangaQ_web`](https://github.com/rodriguesmsb/kisangaQ_web).

Em outras palavras:

```text
KisangaQ = preparação, análise e curadoria dos dados
kisangaQ_web = interface Shiny para catálogo, comunicação e visualização
```

## Escopo científico

O projeto integra dados de múltiplos domínios:

- biodiversidade e cobertura/uso da terra;
- clima e variabilidade ambiental;
- saúde pública e bem-estar;
- condições sociais e demográficas;
- regularização fundiária;
- conflitos territoriais e violência;
- governança, políticas públicas e devolutivas comunitárias.

A proposta final é produzir evidências, indicadores, mapas, painéis e produtos de síntese que possam apoiar políticas públicas intersetoriais voltadas ao bem viver quilombola.

## Fontes de dados previstas

O ecossistema KISANGA-Q prevê integração de fontes como:

| Domínio | Fontes principais |
|---|---|
| Populacional | IBGE Censo 2022, Censo 2022 Quilombola, PNAD Contínua |
| Saúde | DATASUS, SINAN, SIM, CNES |
| Clima | ERA5, CHIRPS, INMET, CMIP6 |
| Ambiente | MapBiomas, INPE, MODIS, PPBio, SinBiose |
| Território | INCRA, Cadastro Nacional de Territórios Quilombolas |
| Social | CadÚnico, ENAP, indicadores municipais |
| Violência e conflitos | Fórum Brasileiro de Segurança Pública, Comissão Pastoral da Terra |

## Estrutura atual do repositório

```text
KisangaQ/
├── README.md
└── data_analysis/
    └── 2026_Generate_sample_df.Rmd
```

O repositório [`kisangaQ_web`](https://github.com/rodriguesmsb/kisangaQ_web) consome arquivos de amostra e metadados gerados aqui.

Fluxo prático:

```text
KisangaQ/data_analysis
  └── gera temp_sample.csv, rainfall_sample.csv, ndvi_sample.csv, burn_sample.csv
        ↓
kisangaQ_web/data/samples
  └── exibe prévias no Catálogo de Dados
```

## Governança e segurança dos dados

O KISANGA-Q deve adotar uma política de gestão de dados que respeite:

- princípios FAIR: dados localizáveis, acessíveis, interoperáveis e reutilizáveis;
- proteção de dados sensíveis de saúde e território;
- LGPD, quando aplicável;
- consentimento livre, prévio e informado em produtos que envolvam comunidades quilombolas;
- soberania e governança coletiva dos dados;
- distinção entre dados públicos, dados agregados, dados restritos e dados que não devem ser publicados.


## Status

Em desenvolvimento inicial.

## Licença



## Contato

Moreno Rodrigues  
GitHub: [@rodriguesmsb](https://github.com/rodriguesmsb)

