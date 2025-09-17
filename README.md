# Pipeline Cloud para Análise de Cotações da B3 com Azure
 
## 📑 Índice
- [:pushpin: Introdução](#1-introdução)
  - [Descrição Geral do Sistema](#11-descrição-geral-do-sistema)
  - [Objetivos do Projeto](#12-objetivos-do-projeto)
- [:memo: Requisitos e Restrições Arquiteturais](#2-requisitos-e-restrições-arquiteturais)
  - [Requisitos Funcionais](#21-requisitos-funcionais)
  - [Requisitos Não Funcionais](#22-requisitos-não-funcionais)
  - [Restrições](#23-restrições)
- [:open_file_folder: Casos de Uso](#3-casos-de-uso)
  - [Casos de Uso do Sistema](#31-casos-de-uso-do-sistema)
  - [Diagrama de Classes](#32-diagrama-de-classes)
  - [Detalhamento dos Componentes e Relacionamentos](#33-detalhamento-dos-componentes-e-relacionamentos-do-diagrama)
- [:triangular_ruler: Visão Geral da Arquitetura](#4-visão-geral-da-arquitetura)
  - [Descrição da Arquitetura em Alto Nível](#41-descrição-da-arquitetura-em-alto-nível)
  - [Tecnologias e Padrões Utilizados](#42-tecnologias-e-padrões-utilizados)
- [:bar_chart: Diagrama de Arquitetura](#5-diagrama-de-arquitetura)
  - [Diagrama do Pipeline de Dados na Azure](#51-diagrama-do-pipeline-de-dados-na-azure)
  - [Detalhamento do Fluxo de Dados](#52-detalhamento-do-fluxo-de-dados)


<br>


##  :pushpin: 1. Introdução

### 1.1. Descrição Geral do Sistema
Esse é um sistema em nuvem na plataforma Azure, projetado para a análise de cotações da Bolsa de Valores do Brasil (B3). O projeto aborda o desafio de processar os arquivos de cotações diárias disponibilizados pela B3, que contêm informações como código do ativo, data, preços de abertura, máximo, mínimo, fechamento e volume financeiro. A solução propõe um pipeline de dados completo para extrair, transformar, carregar (ETL) e analisar esses dados em larga escala, resultando na disponibilização das informações para consumo em dashboards analíticos.

### 1.2. Objetivos do Projeto
O principal objetivo é criar uma arquitetura de nuvem robusta e automatizada. Os objetivos específicos incluem:
- Construir uma arquitetura para extração, transformação e carga de dados em grande escala.
- Aplicar de forma prática os conceitos de Big Data, ETL com Data Factory, Computação Serverless, Bancos de Dados em Nuvem e Containers Docker.
- Desenvolver e demonstrar habilidades em arquitetura de nuvem, integração de múltiplos serviços e automação de pipelines de dados.

<br>

## :memo: 2. Requisitos e Restrições Arquiteturais

### 2.1. Requisitos Funcionais
- **RF01: Ingestão de Dados:** O sistema deve ter a capacidade de simular a extração de arquivos diários de cotações da B3 e enviá-los para o Azure Blob Storage.
- **RF02: Armazenamento de Arquivos:** O sistema deve armazenar os arquivos brutos (originais) e os arquivos já processados em um Azure Storage Account.
- **RF03: Transformação de Dados:** O sistema deve possuir um pipeline ETL para transformar os dados brutos em um formato estruturado e limpo, adequado para análise posterior.
- **RF04: Extração de Informações:** O pipeline deve ser capaz de extrair as informações essenciais dos arquivos, como código do ativo, data do pregão, preços de abertura, máximo, mínimo, fechamento e volume financeiro. A tabela final, no entanto, exige `Ativo`, `DataPregao`, `Abertura`, `Fechamento` e `Volume` .
- **RF05: Carga de Dados:** O sistema deve carregar os dados transformados em uma tabela específica dentro de um Azure SQL Database.
- **RF06: Carga Incremental:** A carga de dados no banco de dados deve ser incremental, ou seja, deve adicionar apenas os novos dados a cada execução, sem duplicar registros existentes.
- **RF07: Automação de Alertas:** O sistema deve enviar notificações por e-mail para informar sobre o status da execução do pipeline (sucesso ou falha).
- **RF08: Disponibilização para Análise:** Os dados finais armazenados no banco de dados devem estar disponíveis para serem consumidos por ferramentas de visualização, como Power BI ou Synapse Analytics.


### 2.2. Requisitos Não Funcionais
- **RNF01: Escalabilidade:** A arquitetura deve ser projetada para suportar o processamento e a análise de dados em larga escala, conforme o objetivo educacional do projeto.
- **RNF02: Automação de Pipeline:** Todo o fluxo de dados, desde a ingestão até a carga final, deve ser automatizado para minimizar a necessidade de intervenção manual.
- **RNF03: Entregáveis Específicos:** O projeto deve resultar em um conjunto de entregáveis bem definidos, incluindo um documento de arquitetura, o pipeline do Data Factory, o código da Azure Function, o container Docker, a Logic App e os scripts SQL necessários.


### 2.3. Restrições
- **R01: Plataforma Cloud:** Toda a solução deve ser obrigatoriamente construída e hospedada na nuvem da Microsoft Azure. 
- **R02: Ferramenta de Orquestração:** O pipeline de ETL deve ser implementado exclusivamente com o Azure Data Factory. 
- **R03: Tecnologia de Carga de Dados:** A lógica para a carga incremental de dados no banco de dados deve ser desenvolvida utilizando Azure Function (Serverless). 
- **R04: Linguagem da Função:** A Azure Function para a carga de dados deve ser escrita na linguagem Python. 
- **R05: Banco de Dados:** O armazenamento dos dados processados e estruturados deve ser feito em um Azure SQL Database. 
- **R06: Ferramenta de Ingestão:** A simulação da extração e envio de arquivos para a nuvem deve ser realizada por meio de um Container Docker. 
- **R07: Ferramenta de Automação de Alertas:** A automação de notificações e a integração com outros serviços devem ser feitas com Logic Apps. 

<br>

## :open_file_folder: 3. Casos de Uso

### 3.1. Casos de Uso do Sistema

**Caso de Uso 1: Processar Pipeline de Dados de Cotações**
- Nome do Caso de Uso: Processar Pipeline de Dados de Cotações
- Ator Principal: Sistema (de forma automatizada)
- Ator Secundário: Desenvolvedor/Operador
- Descrição: Descreve o fluxo ponta-a-ponta, totalmente automatizado, para processar um arquivo de cotação desde sua chegada na nuvem até a carga final no banco de dados e a notificação do resultado.
- Pré-condições:
   - A infraestrutura na Azure (Storage, Data Factory, Function, SQL DB, Logic Apps) está devidamente configurada.
   - Um novo arquivo de cotações foi depositado na área de dados brutos do Azure Storage Account.
- **Fluxo Principal (Caminho Feliz):**
   1. A chegada de um novo arquivo no Azure Storage aciona o pipeline no Azure Data Factory para iniciar o processamento.
   2. O pipeline lê o arquivo bruto, aplica as transformações para limpar e estruturar os dados e salva o resultado como um novo arquivo na área de dados processados.
   3. Ao término da etapa de transformação, o Data Factory aciona a Azure Function.
   4. A Azure Function lê o arquivo processado e realiza a carga incremental dos novos dados na tabela `Cotacoes` do Azure SQL Database.
   5. Ao final da execução bem-sucedida do pipeline, a Logic App é acionada.
   6. A Logic App envia um e-mail de "Sucesso" para o Desenvolvedor/Operador.
 - **Fluxo de Exceção:**
   1. Se ocorrer um erro em qualquer etapa do pipeline do Data Factory (transformação ou carga), a execução é interrompida.
   2. A Logic App configurada para monitorar falhas é acionada.
   3. A Logic App envia um e-mail de "Falha" para o Desenvolvedor/Operador, informando sobre o erro.
- Pós-condições:
   - Em caso de sucesso, os novos dados de cotações estão disponíveis para consulta no Azure SQL Database.
   - O Desenvolvedor/Operador recebe um e-mail informando o status final (sucesso ou falha) da execução do pipeline.


**Caso de Uso 2: Ingerir Arquivo de Cotações**
- Nome do Caso de Uso: Ingerir Arquivo de Cotações
- Ator Principal: Desenvolvedor
- Descrição: Detalha o processo manual de simulação da extração e envio de um arquivo de cotações para a nuvem, que serve como gatilho para o "Caso de Uso 1".
- Pré-condições:
   - O container Docker está devidamente configurado e pronto para ser executado.
   - O Azure Storage Account está criado e acessível.
- **Fluxo Principal:**
    1.  O Desenvolvedor/Operador executa o container Docker.
    2.  O script dentro do container realiza o envio de um ou mais arquivos de cotações para o container de dados brutos no Azure Blob Storage.
- **Fluxo de Exceção:**
    1. Se o container Docker não conseguir ser executado (ex: erro de configuração do Docker na máquina local), o processo falha e uma mensagem de erro é exibida no terminal do Desenvolvedor.
    2. Se o script dentro do container não conseguir se conectar ao Azure Storage (ex: chave de acesso incorreta, falta de permissão, problema de rede), o script termina com um erro e o arquivo não é enviado.
- Pós-condições:
   - Sucesso: O arquivo de cotações está armazenado na área de dados brutos da nuvem, pronto para acionar o pipeline de processamento.
   - Falha: O arquivo não é enviado para a nuvem e o pipeline principal não é acionado. Uma mensagem de erro é registrada localmente.


**Caso de Uso 3: Analisar Dados de Cotações**
- Nome do Caso de Uso: Analisar Dados de Cotações
- Ator Principal: Analista de Dados
- Descrição: Mostra como um usuário final consome os dados já processados pelo pipeline para criar visualizações e gerar insights.
- Pré-condições:
    - O "Caso de Uso 1" foi executado com sucesso pelo menos uma vez.
    - Os dados de cotações estão armazenados no Azure SQL Database.
    - O Analista de Dados possui uma ferramenta de visualização (como Power BI) com as credenciais de acesso ao banco de dados.
- **Fluxo Principal:**
   1. O Analista de Dados utiliza uma ferramenta de visualização, como Power BI ou Synapse Analytics.
   2. O Analista estabelece uma conexão com a base de dados Azure SQL Database que contém as cotações processadas.
   3. O Analista cria relatórios e dashboards para analisar os dados.
- **Fluxo de Exceção:**
    1. Se a ferramenta de visualização não conseguir se conectar ao Azure SQL Database (ex: credenciais inválidas, firewall bloqueando a conexão, banco de dados offline), uma mensagem de erro de conexão é exibida para o Analista na própria ferramenta.
    2. Se uma consulta (query) executada pela ferramenta no banco de dados for inválida, o banco retornará um erro que será exibido na ferramenta de visualização.
- Pós-condições:
    - Sucesso: As informações das cotações são apresentadas de forma visual, permitindo a análise.
    - Falha: O Analista de Dados não consegue acessar os dados e recebe uma mensagem de erro, precisando corrigir o problema de conexão ou da consulta para continuar. 



### 3.2. Diagrama de Classes

![Diagrama de Classes do Projeto](https://github.com/thabus/Projeto_Cloud/blob/main/imagens/diagrama_de_classes.png)

### 3.3 Detalhamento dos Componentes e Relacionamentos do Diagrama

- **Cotacao:** É a classe que modela os dados de cotações processados . Ela é o destino final do nosso pipeline de dados.
- **DockerContainer:** Componente responsável por iniciar o fluxo. Sua função é `enviarArquivoBruto()` para o Azure Storage.
- **AzureStorageAccount:** Atua como repositório central (Data Lake). Armazena os arquivos brutos e os processados, além de acionar a Azure Function quando um novo arquivo processado chega.
- **AzureDataFactory:** O orquestrador do ETL. Ele lê os dados brutos, executa a transformação e salva o resultado no Storage.
- **AzureFunction:** Componente serverless que contém a lógica de negócio para a carga. Ele é acionado (`trigger`) pela chegada de um arquivo no Storage, lê esse arquivo e o carrega no banco de dados.
- **AzureSqlDatabase:** O banco de dados relacional que armazena permanentemente os objetos da classe `Cotacao`. A relação "1 para muitos" indica que o banco armazena múltiplas cotações.
- **LogicApps:** Responsável pela automação de alertas. Ele monitora o status do `AzureDataFactory` e envia notificações, desacoplando a lógica de alerta do pipeline principal.

<br>


## :triangular_ruler: 4. Visão Geral da Arquitetura

### 4.1. Descrição da arquitetura em alto nível
A arquitetura do sistema é desenhada como um pipeline de dados moderno e automatizado, implementado inteiramente na nuvem Microsoft Azure. O projeto segue o padrão de **ETL** para processar arquivos de cotações da B3, desde sua ingestão até o armazenamento em um banco de dados relacional para análise.
O fluxo arquitetural pode ser resumido em três fases principais:
 - 1. Extração (Extract): O processo é iniciado pela ingestão de dados, simulada por um **Container Docker**. Este container envia os arquivos brutos de cotações para um repositório central no **Azure Storage Account**.
 - 2. Transformação (Transform): O **Azure Data Factory** atua como o orquestrador central do pipeline. Ele é responsável por ler os arquivos brutos do Storage, aplicar as transformações necessárias para limpar e estruturar os dados e, em seguida, salvar os arquivos processados de volta no Azure Storage Account.
 - 3. Carga (Load): Nesta fase, uma **Azure Function** é acionada automaticamente. Utilizando um padrão de computação *serverless*, a função realiza uma carga incremental dos dados processados diretamente no **Azure SQL Database**, que serve como o banco de dados analítico final.

Adicionalmente, o **Logic Apps** é utilizado para automatizar notificações e alertas, como o envio de e-mails sobre o status da execução do pipeline, e para integrar o fluxo com serviços de visualização, como o Power BI.

### 4.2. Tecnologias e padrões utilizados

| **Tecnologia / Padrão**                 | **Função no Projeto**                                                                                                        |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **Padrão de Pipeline de Dados (ETL)**   | Estrutura o fluxo em três etapas (Extração, Transformação e Carga) orquestradas pelo Azure Data Factory.                     |
| **Computação Serverless**               | Implementada com Azure Function para a carga incremental no banco, permitindo execução sob demanda sem gerenciar servidores. |
| **Contêineres (Docker)**                | Utilizados para simular a ingestão de arquivos, encapsulando dependências e garantindo portabilidade.                        |
| **Automação e Orquestração**            | Azure Data Factory gerencia o fluxo principal, enquanto Logic Apps automatiza notificações e integra serviços.               |
| **Banco de Dados como Serviço (DBaaS)** | Azure SQL Database armazena os dados processados, eliminando a necessidade de administrar servidores.                        |
| **Data Lake**                           | Azure Storage Account centraliza o armazenamento de arquivos brutos e processados.                                           |

<br>

<br>

## :bar_chart: Diagrama de Arquitetura

### 5.1. Diagrama do Pipeline de Dados na Azure
Este diagrama visualiza a arquitetura do pipeline de dados, detalhando o fluxo de informações entre os principais serviços da Microsoft Azure e os componentes do projeto. Ele representa a jornada dos dados, desde a ingestão simulada até a carga final para análise.

![Diagrama de Arquitetura do Pipeline de Dados para Análise de Cotações da B3 com Azure](https://github.com/thabus/Projeto_Cloud/blob/main/imagens/Arquitetura_do_Pipeline_B3_no_Azure.png?raw=true)

### 5.2. Detalhamento do Fluxo de Dados
A seguir, detalhamos cada etapa do fluxo apresentado no diagrama:

- **1. Ingestão (Container Docker):**
  - A simulação da extração dos arquivos de cotações da B3 é realizada por um **Container Docker**. Este contêiner envia os arquivos brutos para um contêiner específico no Azure Blob Storage, conhecido como `raw zone`.

- **2. Orquestração e Transformação (Azure Data Factory):**
  - A chegada de um novo arquivo na `raw zone` atua como um gatilho para o **Azure Data Factory**. Ele orquestra o pipeline de ETL, lendo o arquivo bruto e aplicando as transformações necessárias para limpar e estruturar os dados. O resultado desse processamento é salvo em um segundo contêiner no mesmo Storage Account, a `processed zone`.

- **3. Carga Incremental (Azure Function):**
  - Um segundo gatilho, desta vez na `processed zone`, aciona uma **Azure Function**. Esta função, desenvolvida em Python, é responsável por ler o arquivo processado e realizar a carga incremental dos dados na tabela `Cotacoes` do **Azure SQL Database**.

- **4. Monitoramento e Notificações (Logic Apps):**
  - Paralelamente ao pipeline principal, o **Logic Apps** monitora o status da execução do Azure Data Factory. Em caso de sucesso ou falha, ele envia notificações automáticas por e-mail, garantindo a visibilidade e o controle sobre o processo.

- **5. Análise (Azure SQL Database):**
  - Os dados, agora limpos e organizados no **Azure SQL Database**, estão prontos para serem consumidos por ferramentas de visualização, como o Power BI, permitindo a criação de dashboards e relatórios analíticos.

<br>

<h4>Grupo: Thaís Bustamante, Emilly Fernandes e João Gabriel Rodriguez</h4>
