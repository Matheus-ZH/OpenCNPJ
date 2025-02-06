<h1 align="center">📝 Open CNPJ 📝</h1> 
<div align="center">
    <a href="https://www.python.org/" target="_blank"><img src="https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white" target="_blank"></a>
    <a href="https://www.postgresql.org/docs/" target="_blank"><img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white" target="_blank"></a>
    <a href="https://docs.getdbt.com/" target="_blank"><img src="https://img.shields.io/badge/DBT-%23FF694B?style=for-the-badge&logo=dbt&logoColor=white
    " target="_blank"></a>
    <a href="https://docs.docker.com/" target="_blank"><img src="https://img.shields.io/badge/Docker-%232496ED?style=for-the-badge&logo=docker&logoColor=white
    " target="_blank"></a>
</div>

## *Objetivos do Projeto*

Criar um pipeline de dados eficiente e modular para processar, armazenar e disponibilizar os dados do CNPJ em uma arquitetura moderna de camadas (bronze, silver, gold). A ideia é aprender tecnologias que são amplamente usadas no mercado, como Python, PostgreSQL, DBT, Docker, CI/CD e ferramentas de qualidade de dados e data catalog, enquanto estruturamos os dados em um Data Warehouse funcional e escalável.

## *Estrutura Geral do Projeto*

    Automação para Download dos Dados
        Tarefa: Fazer o download automatizado dos arquivos disponibilizados pela Receita Federal via SFTP.
        Solução Atual: Um script em Python que:
            Faz download dos arquivos.
            Organiza os arquivos por mês em pastas dentro do diretório /data.
            Verifica se o arquivo já foi baixado para evitar duplicações.

    Processamento e Carregamento Inicial
        Tarefa: Processar os arquivos brutos (CSV, texto, etc.) e carregá-los no banco de dados PostgreSQL (camada bronze).
        Solução Atual:
            Utilizar Python e pandas para leitura e transformação inicial dos dados.
            Usar psycopg2 ou SQLAlchemy para carregar os dados no PostgreSQL.

    Transformação e Organização dos Dados
        Tarefa: Realizar transformações no DBT para preparar os dados para análises.
        Arquitetura:
            Bronze: Dados brutos.
            Silver: Dados limpos e organizados.
            Gold: Tabelas analíticas e métricas prontas para consulta.
        Solução Atual: DBT conectado ao PostgreSQL para criar modelos que implementam essa arquitetura.

    Camada de Qualidade e Data Catalog
        Qualidade de Dados: Usar Great Expectations para definir e rodar testes de qualidade que garantem a confiabilidade dos dados carregados.
        Data Catalog: Utilizar Amundsen ou OpenMetadata para documentar e catalogar os dados.

    Ambiente Contêinerizado
        Docker: Usar containers para rodar serviços como PostgreSQL, DBT e possivelmente ferramentas como o data catalog.
        Benefício: Facilita a configuração do ambiente, o isolamento de dependências e a portabilidade.

    Automação e CI/CD
        CI/CD: Criar um pipeline automatizado que:
            Baixe os dados periodicamente.
            Processe e carregue os dados.
            Execute as transformações e os testes de qualidade.
        Ferramentas: GitHub Actions para implementar a automação.

## *Tecnologias no Projeto*

    - Python: Para baixar, processar e carregar dados.
    - PostgreSQL: Banco de dados relacional usado para armazenar as camadas bronze, silver e gold.
    - DBT (Data Build Tool): Para realizar transformações de dados em SQL de forma modular e versionada.
    - Docker: Para criar um ambiente padronizado de execução dos serviços.
    - Great Expectations: Para validação e controle de qualidade dos dados.
    - Amundsen ou OpenMetadata: Para documentar e catalogar os dados, ajudando a explorar e entender o que está disponível.
    - Git e GitHub: Para controle de versão e colaboração.
    - GitHub Actions: Para automação de pipeline de CI/CD.