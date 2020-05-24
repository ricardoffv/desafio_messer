# Projeto de Gerenciamento de Vendas

Este repositório contém a organização do projeto referente a um gerenciamento de vendas online. A organização do projeto ocorre da seguinte maneira:
* database_information: contém as informações de conexão ao SQL Server
* database_payload_insertion: realiza a inserção dos dados da planilha Excel no banco de dados
* script.sql: contém todos os scripts executados diretamente no SQL Server, contendo a criação das bases de dados e das procedures
* Jupyter Notebook: contém os insights extraídos das bases de dados populadas
* get_igpm: crawler que busca o valor do IGP-M e insere no banco de dados
* igpm_timer: job que roda mensalmente para criar uma nova versão do valor do IGP-M no banco.

## Recomendações

Executar o script no SQL Server, em seguida, executar o script Python de inserção de dados no banco e, então, será possível reproduzir os códigos de visualização.

### Pré-requisitos

É necessário ter algumas bibliotecas do python instaladas para a execução correta dos códigos. São elas:
* requests
* python-crontab
* wordcloud
* matplotlib
* numpy
* pyodbc
* pandas
* seaborn

## Autor

* **Ricardo Vale**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

