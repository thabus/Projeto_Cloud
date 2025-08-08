# Pipeline Cloud para Análise de Cotações da B3 com Azure

## Índice
- [INTRODUÇÃO](https://github.com/thabus/Projeto_Cloud/blob/main/README.md#1-introdu%C3%A7%C3%A3o)
  - [Descrição Geral do Sistema](https://github.com/thabus/Projeto_Cloud#11-descri%C3%A7%C3%A3o-geral-do-sistema)
  - [Objetivos do Projeto](https://github.com/thabus/Projeto_Cloud#12-objetivos-do-projeto)
- [REQUISITOS E RESTRIÇÕES ARQUITETURAIS](https://github.com/thabus/Projeto_Cloud/blob/main/README.md#3-requisitos-e-restri%C3%A7%C3%B5es-arquiterurais)
  - [Requisitos Funcionais](https://github.com/thabus/Projeto_Cloud#31-requisitos-funcionais)
  - [Requisitos Não Funcionais](https://github.com/thabus/Projeto_Cloud#32-requisitos-n%C3%A3o-funcionais)
  - [Restrições](https://github.com/thabus/Projeto_Cloud#33-restri%C3%A7%C3%B5es)
- [CASOS DE USO](https://github.com/thabus/Projeto_Cloud?tab=readme-ov-file#4-casos-de-uso)
- [VISÃO GERAL DA ARQUITETURA](https://github.com/thabus/Projeto_Cloud/blob/main/README.md#2-visão-geral-da-arquitetura)
  - [Descrição da Arquitetura em alto nível](https://github.com/thabus/Projeto_Cloud#21-descri%C3%A7%C3%A3o-da-arquitetura-em-alto-n%C3%ADvel)
  - [Tecnologias e Padrões Utilizados](https://github.com/thabus/Projeto_Cloud#22-tecnologias-e-padr%C3%B5es-utilizados)

<br>

## 1. Introdução

### 1.1. Descrição Geral do Sistema
Esse é um sistema em nuvem na plataforma Azure, projetado para a análise de cotações da Bolsa de Valores do Brasil (B3). O projeto aborda o desafio de processar os arquivos de cotações diárias disponibilizados pela B3, que contêm informações como código do ativo, data, preços de abertura, máximo, mínimo, fechamento e volume financeiro. A solução propõe um pipeline de dados completo para extrair, transformar, carregar (ETL) e analisar esses dados em larga escala, resultando na disponibilização das informações para consumo em dashboards analíticos.

### 1.2. Objetivos do Projeto
O principal objetivo é criar uma arquitetura de nuvem robusta e automatizada. Os objetivos específicos incluem:
- Construir uma arquitetura para extração, transformação e carga de dados em grande escala.
- Aplicar de forma prática os conceitos de Big Data, ETL com Data Factory, Computação Serverless, Bancos de Dados em Nuvem e Containers Docker.
- Desenvolver e demonstrar habilidades em arquitetura de nuvem, integração de múltiplos serviços e automação de pipelines de dados.

<br>

## 2. Requisitos e Restrições Arquiterurais

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

## 3. Casos de Uso

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
    1.  O Desenvolvedor/Operador executa o container Docker.
    2.  O script dentro do container realiza o envio de um ou mais arquivos de cotações para o container de dados brutos no Azure Blob Storage.
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

![Diagrama de Classes do Projeto](https://www.mermaidchart.com/app/projects/1dbf83d3-7cb5-4698-b822-ef9d289c4e91/diagrams/81ab2952-df1a-437a-90b5-7039ef5cfe19/version/v0.1/edit)


<br>


## 4. Visão Geral da Arquitetura

### 4.1. Descrição da arquitetura em alto nível
A arquitetura do sistema é desenhada como um pipeline de dados moderno e automatizado, implementado inteiramente na nuvem Microsoft Azure. O projeto segue o padrão de **ETL** para processar arquivos de cotações da B3, desde sua ingestão até o armazenamento em um banco de dados relacional para análise.
O fluxo arquitetural pode ser resumido em três fases principais:
 - 1. Extração (Extract): O processo é iniciado pela ingestão de dados, simulada por um **Container Docker**. Este container envia os arquivos brutos de cotações para um repositório central no **Azure Storage Account**.
 - 2. Transformação (Transform): O **Azure Data Factory** atua como o orquestrador central do pipeline. Ele é responsável por ler os arquivos brutos do Storage, aplicar as transformações necessárias para limpar e estruturar os dados e, em seguida, salvar os arquivos processados de volta no Azure Storage Account.
 - 3. Carga (Load): Nesta fase, uma **Azure Function** é acionada automaticamente. Utilizando um padrão de computação *serverless*, a função realiza uma carga incremental dos dados processados diretamente no **Azure SQL Database**, que serve como o banco de dados analítico final.

Adicionalmente, o **Logic Apps** é utilizado para automatizar notificações e alertas, como o envio de e-mails sobre o status da execução do pipeline, e para integrar o fluxo com serviços de visualização, como o Power BI.

### 4.2. Tecnologias e padrões utilizados

O sistema utiliza um conjunto de tecnologias e padrões de arquitetura modernos para garantir automação, escalabilidade e manutenibilidade.
- *Padrão de Pipeline de Dados (ETL)*: A arquitetura inteira é baseada no padrão de ETL, onde os dados passam por estágios distintos de extração, transformação e carga, orquestrados pelo Azure Data Factory.
- *Computação Serverless (Serverless Computing)*: Este padrão é implementado com a Azure Function para a carga de dados no banco. A abordagem permite executar a lógica de carga de forma reativa e escalável, sem a necessidade de gerenciar a infraestrutura de servidores.
- *Contêineres (Containers)*: O uso do Docker para simular a ingestão de arquivos representa o padrão de conteinerização. Isso encapsula a aplicação de ingestão e suas dependências, garantindo consistência e portabilidade.
- *Automação e Orquestração*: A automação é um pilar do projeto. O Azure Data Factory orquestra o fluxo de dados principal , enquanto o Logic Apps automatiza tarefas secundárias, como o envio de notificações e a integração entre serviços.
- *Banco de Dados como Serviço (DBaaS)*: O Azure SQL Database é utilizado como um serviço de banco de dados gerenciado em nuvem, eliminando a necessidade de administração de um servidor de banco de dados tradicional.
- *Data Lake*: O Azure Storage Account funciona como um Data Lake, um repositório centralizado para armazenar grandes volumes de dados em seus formatos nativos (brutos) e processados.


<br>

<h4>Grupo: Thaís Bustamante e Emily</h4>
