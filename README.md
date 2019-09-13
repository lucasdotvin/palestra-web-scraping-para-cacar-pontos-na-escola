# Web Scraping para Caçar Pontos na Escola

Este repositório contém os scripts utilizados por mim na palestra "Web Scraping para Caçar Pontos na Escola".

Os códigos vasculham um repositório online usado por um ex-professor e listam no console os novos itens desse diretório. A partir da agilidade em obter os novos arquivos e links carregados pelo docente, eu pude resolver com antecedência, por exemplo, a desafios de programação que valiam nota.

## Instalação

Copie o repositório e crie um ambiente virtual:

```bash
python -m venv venv
```

Em seguida, use o gerenciador de pacotes [pip](https://pypi.org/project/pip/) para instalar as dependências do código:

```bash
pip install -r requirements
```

## Uso

Inicialmente, ative o ambiente virtual. No Posix:

```bash
$ source <venv>/bin/activate
```

No Windows:

```bash
C:\<venv>\Scripts\activate.bat
```

Em seguida, entre na pasta *src*:

```bash
cd src
```

Por fim, execute o arquivo *run.py*:

```bash
python run.py
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
