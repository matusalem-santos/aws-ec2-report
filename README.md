# Objetivo 

Criar planilha de todas as instancias em uma conta da AWS

## Dependencias 

- Python3
- Modulo boto3 do python3(pip3 install boto3)
- Modulo pyzabbix do python3(pip3 install pyzabbix)

## Modo de usar

- Depois de dar um clone no repositório, acesse o diretório **list_instances** onde o script **report-instances.py** está armazenado 
- Executar o script **report-instances.py** passando os parâmetros necessários 

```sh
    ./report-instances.py "AWS_ACCESS_KEY_ID" "AWS_SECRET_KEY" "NOME_DO_ARQUIVO.CSV"

```
- Caso deseje criar uma planilha com verificação se as instancias na AWS estão sendo monitoradas pelo Zabbix executar o script passando os demais parâmetros 

```sh
    ./report-instances.py "AWS_ACCESS_KEY_ID" "AWS_SECRET_KEY" "DOMAIN_ZABBIX" "USUARIO_ZABBIX" "SENHA_ZABBIX" "NOME_DO_ARQUIVO.CSV"
```

### Parâremtros

- **AWS_ACCESS_KEY_ID**/**AWS_SECRET_KEY** - Access key e secret key de um usuario no IAM que tenha permissão **AmazonEC2ReadOnlyAccess**

- **DOMAIN_ZABBIX** - URL de domínio do Zabbix que está monitorando as instancias

- **USUARIO_ZABBIX**/**SENHA_ZABBIX** - Usuario para acesso ao Zabbix que está monitorando as instancias

- **NOME_DO_ARQUIVO.CSV** - Passar o nome do arquivo desejado com a extensão **CSV** para gerar a planilha



