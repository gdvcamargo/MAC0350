# MAC0350
Repositório para armazenar exercícios, trabalhos e projetos da disciplina MAC0350 - Introdução ao Desenvolvimento de Sistemas de Software.

## Projeto Individual 

O projeto é um sistema de planejamento e gerenciamento de viagens. Nele será possível criar viagens, itinerários, planejar gastos e visualizar seu histórico de viagens e destinos visitados.

### Como rodar o projeto ?

Eu utilizei [poetry](https://python-poetry.org/docs/) para gerenciamento de pacotes, porém, existe um ```requirements.txt```para instalação usando pip.

Uma vez que o venv esteja corretamente instalado e ativado siga os seguintes passos:

Criar as tabelas no SQLite:

```bash
python3 startup.py
```

Uma vez criado as tabelas basta rodar o fastapi:

```bash
fastapi dev app.py
```

