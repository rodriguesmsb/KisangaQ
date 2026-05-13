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

O arquivo `data_analysis/2026_Generate_sample_df.Rmd` gera amostras de dados climáticos e ambientais para uso no aplicativo web.

## Script disponível

### `data_analysis/2026_Generate_sample_df.Rmd`

Este documento RMarkdown:

1. carrega o pacote `tidyverse`;
2. importa funções auxiliares de `functions/climate_io.R`;
3. lê bases de temperatura, pluviosidade, NDVI e queimadas com `get_data()`;
4. seleciona uma amostra de 10 linhas de cada base;
5. exporta arquivos CSV para o repositório `kisangaQ_web`, em `data/samples/`.

Bases usadas no script:

```r
temp     <- get_data("Temperature")
rainfall <- get_data("Rainfall")
ndvi     <- get_data("NDVI")
burn     <- get_data("Burning")
```

Arquivos exportados:

```text
temp_sample.csv
rainfall_sample.csv
ndvi_sample.csv
burn_sample.csv
```

## Dependências

O script atual usa:

```r
install.packages("tidyverse")
```

Também é necessário disponibilizar o arquivo auxiliar:

```text
functions/climate_io.R
```

Esse arquivo deve conter a função `get_data()`, responsável por localizar e carregar as bases climáticas e ambientais.

## Como executar

Clone o repositório:

```bash
git clone https://github.com/rodriguesmsb/KisangaQ.git
cd KisangaQ
```

Abra o arquivo RMarkdown em RStudio ou execute via R:

```r
rmarkdown::render("data_analysis/2026_Generate_sample_df.Rmd")
```

Se o objetivo for apenas gerar as amostras para o aplicativo web, verifique antes se o caminho de saída existe. O script atual escreve os arquivos diretamente no repositório `kisangaQ_web`:

```text
~/Hubic/Analise_de_dados/KisangaQ_web/data/samples/
```

Caso o projeto esteja em outro computador, ajuste esses caminhos antes de executar.

## Fluxo recomendado de trabalho

```text
1. Identificar bases relevantes
2. Ingerir dados brutos ou harmonizados
3. Padronizar nomes, códigos geográficos e unidades temporais
4. Criar metadados e documentação das variáveis
5. Gerar amostras públicas ou sintéticas
6. Exportar produtos para o kisangaQ_web
7. Validar produtos com equipe técnica e parceiros comunitários
```

## Organização sugerida para próximas versões

À medida que o repositório crescer, uma estrutura mais explícita pode facilitar manutenção e reprodutibilidade:

```text
KisangaQ/
├── README.md
├── data_analysis/
│   └── 2026_Generate_sample_df.Rmd
├── functions/
│   ├── climate_io.R
│   ├── health_io.R
│   ├── spatial_io.R
│   └── metadata_io.R
├── metadata/
│   └── data_dictionary.csv
├── scripts/
│   ├── 01_ingest_data.R
│   ├── 02_clean_data.R
│   ├── 03_generate_indicators.R
│   └── 04_export_web_samples.R
└── outputs/
    ├── samples/
    ├── figures/
    └── reports/
```

## Relação com o Índice de Vulnerabilidade Quilombola

Um dos produtos analíticos esperados do KISANGA-Q é o desenvolvimento de um Índice de Vulnerabilidade Quilombola, organizado em três dimensões:

- **exposição**, relacionada a riscos ambientais e climáticos;
- **sensibilidade**, relacionada a condições socioeconômicas, demográficas e de saúde;
- **capacidade adaptativa**, relacionada a regularização fundiária, acesso a políticas públicas, redes comunitárias e práticas tradicionais de manejo e cuidado.

Este repositório pode servir como espaço para desenvolver, testar e documentar as rotinas de cálculo desses indicadores.

## Relação com o aplicativo web

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

Dados sensíveis ou identificáveis não devem ser versionados diretamente no GitHub.

## Boas práticas recomendadas

- Evitar caminhos absolutos em scripts compartilhados.
- Usar arquivos de configuração, por exemplo `.Renviron`, `config.yml` ou variáveis de ambiente.
- Documentar a origem de cada base.
- Versionar apenas scripts, metadados e amostras públicas ou sintéticas.
- Manter dados brutos grandes fora do GitHub.
- Criar dicionários de dados para cada produto derivado.
- Registrar decisões de harmonização em arquivos legíveis por humanos.

## Status

Em desenvolvimento inicial.

## Licença

Licença ainda não definida. Recomenda-se adicionar uma licença explícita antes da distribuição pública ampla do código, metadados ou produtos derivados.

## Contato

Moreno Rodrigues  
GitHub: [@rodriguesmsb](https://github.com/rodriguesmsb)

