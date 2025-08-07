# Pipeline Cloud para Análise de Cotações da B3 com Azure

## 1. Introdução

### 1.1. Descrição Geral do Sistema
Esse é um sistema em nuvem na plataforma Azure, projetado para a análise de cotações da Bolsa de Valores do Brasil (B3). O projeto aborda o desafio de processar os arquivos de cotações diárias disponibilizados pela B3, que contêm informações como código do ativo, data, preços de abertura, máximo, mínimo, fechamento e volume financeiro. A solução propõe um pipeline de dados completo para extrair, transformar, carregar (ETL) e analisar esses dados em larga escala, resultando na disponibilização das informações para consumo em dashboards analíticos.

### 1.2. Objetivos do Projeto
O principal objetivo é criar uma arquitetura de nuvem robusta e automatizada. Os objetivos específicos incluem:
- Construir uma arquitetura para extração, transformação e carga de dados em grande escala.
- Aplicar de forma prática os conceitos de Big Data, ETL com Data Factory, Computação Serverless, Bancos de Dados em Nuvem e Containers Docker.
- Desenvolver e demonstrar habilidades em arquitetura de nuvem, integração de múltiplos serviços e automação de pipelines de dados.

<br>

## 2. Visão Geral da Arquitetura

### 2.1. Descrição da arquitetura em alto nível
A arquitetura do sistema é desenhada como um pipeline de dados moderno e automatizado, implementado inteiramente na nuvem Microsoft Azure. O projeto segue o padrão de **ETL** para processar arquivos de cotações da B3, desde sua ingestão até o armazenamento em um banco de dados relacional para análise.
O fluxo arquitetural pode ser resumido em três fases principais:
 - 1. Extração (Extract): O processo é iniciado pela ingestão de dados, simulada por um **Container Docker**. Este container envia os arquivos brutos de cotações para um repositório central no **Azure Storage Account**.
 - 2. Transformação (Transform): O **Azure Data Factory** atua como o orquestrador central do pipeline. Ele é responsável por ler os arquivos brutos do Storage, aplicar as transformações necessárias para limpar e estruturar os dados e, em seguida, salvar os arquivos processados de volta no Azure Storage Account.
 - 3. Carga (Load): Nesta fase, uma **Azure Function** é acionada automaticamente. Utilizando um padrão de computação *serverless*, a função realiza uma carga incremental dos dados processados diretamente no **Azure SQL Database**, que serve como o banco de dados analítico final.

Adicionalmente, o **Logic Apps** é utilizado para automatizar notificações e alertas, como o envio de e-mails sobre o status da execução do pipeline, e para integrar o fluxo com serviços de visualização, como o Power BI.

### 2.2. Tecnologias e padrões utilizados

O sistema utiliza um conjunto de tecnologias e padrões de arquitetura modernos para garantir automação, escalabilidade e manutenibilidade.
- *Padrão de Pipeline de Dados (ETL)*: A arquitetura inteira é baseada no padrão de ETL, onde os dados passam por estágios distintos de extração, transformação e carga, orquestrados pelo Azure Data Factory.
- *Computação Serverless (Serverless Computing)*: Este padrão é implementado com a Azure Function para a carga de dados no banco. A abordagem permite executar a lógica de carga de forma reativa e escalável, sem a necessidade de gerenciar a infraestrutura de servidores.
- *Contêineres (Containers)*: O uso do Docker para simular a ingestão de arquivos representa o padrão de conteinerização. Isso encapsula a aplicação de ingestão e suas dependências, garantindo consistência e portabilidade.
- *Automação e Orquestração*: A automação é um pilar do projeto. O Azure Data Factory orquestra o fluxo de dados principal , enquanto o Logic Apps automatiza tarefas secundárias, como o envio de notificações e a integração entre serviços.
- *Banco de Dados como Serviço (DBaaS)*: O Azure SQL Database é utilizado como um serviço de banco de dados gerenciado em nuvem, eliminando a necessidade de administração de um servidor de banco de dados tradicional.
- *Data Lake*: O Azure Storage Account funciona como um Data Lake, um repositório centralizado para armazenar grandes volumes de dados em seus formatos nativos (brutos) e processados.

<br>

## 3. Requisitos e Restrições Arquiterurais

### 3.1. Requisitos Funcionais
- **RF01: Ingestão de Dados:** O sistema deve ter a capacidade de simular a extração de arquivos diários de cotações da B3 e enviá-los para o Azure Blob Storage.
- **RF02: Armazenamento de Arquivos:** O sistema deve armazenar os arquivos brutos (originais) e os arquivos já processados em um Azure Storage Account.
- **RF03: Transformação de Dados:** O sistema deve possuir um pipeline ETL para transformar os dados brutos em um formato estruturado e limpo, adequado para análise posterior.
- **RF04: Extração de Informações:** O pipeline deve ser capaz de extrair as informações essenciais dos arquivos, como código do ativo, data do pregão, preços de abertura, máximo, mínimo, fechamento e volume financeiro. A tabela final, no entanto, exige `Ativo`, `DataPregao`, `Abertura`, `Fechamento` e `Volume` .
- **RF05: Carga de Dados:** O sistema deve carregar os dados transformados em uma tabela específica dentro de um Azure SQL Database.
- **RF06: Carga Incremental:** A carga de dados no banco de dados deve ser incremental, ou seja, deve adicionar apenas os novos dados a cada execução, sem duplicar registros existentes.
- **RF07: Automação de Alertas:** O sistema deve enviar notificações por e-mail para informar sobre o status da execução do pipeline (sucesso ou falha).
- **RF08: Disponibilização para Análise:** Os dados finais armazenados no banco de dados devem estar disponíveis para serem consumidos por ferramentas de visualização, como Power BI ou Synapse Analytics.


### 3.2. Requisitos Não Funcionais
- **RNF01: Escalabilidade:** A arquitetura deve ser projetada para suportar o processamento e a análise de dados em larga escala, conforme o objetivo educacional do projeto.
- **RNF02: Automação de Pipeline:** Todo o fluxo de dados, desde a ingestão até a carga final, deve ser automatizado para minimizar a necessidade de intervenção manual.
- **RNF03: Entregáveis Específicos:** O projeto deve resultar em um conjunto de entregáveis bem definidos, incluindo um documento de arquitetura, o pipeline do Data Factory, o código da Azure Function, o container Docker, a Logic App e os scripts SQL necessários.


### 3.3. Restrições
- **R01: Plataforma Cloud:** Toda a solução deve ser obrigatoriamente construída e hospedada na nuvem da Microsoft Azure. 
- **R02: Ferramenta de Orquestração:** O pipeline de ETL deve ser implementado exclusivamente com o Azure Data Factory. 
- **R03: Tecnologia de Carga de Dados:** A lógica para a carga incremental de dados no banco de dados deve ser desenvolvida utilizando Azure Function (Serverless). 
- **R04: Linguagem da Função:** A Azure Function para a carga de dados deve ser escrita na linguagem Python. 
- **R05: Banco de Dados:** O armazenamento dos dados processados e estruturados deve ser feito em um Azure SQL Database. 
- **R06: Ferramenta de Ingestão:** A simulação da extração e envio de arquivos para a nuvem deve ser realizada por meio de um Container Docker. 
- **R07: Ferramenta de Automação de Alertas:** A automação de notificações e a integração com outros serviços devem ser feitas com Logic Apps. 










*Grupo: Thaís Bustamante e Emily*
