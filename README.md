# MAC0350
Repositório para armazenar exercícios, trabalhos e projetos da disciplina MAC0350 - Introdução ao Desenvolvimento de Sistemas de Software.

## Projeto Individual 

O projeto é um sistema de planejamento e gerenciamento de viagens. Nele será possível criar viagens, itinerários, planejar gastos e visualizar seu histórico de viagens e destinos visitados.

### Funcionalidades

Ao todo foram desenvolvidas as seguintes funcionalidades:
- Autenticação usando cookies e sessões de usuários
- Páginas de login/registro de contas
- Página de perfil para visualizar dados gerais
- Página de gerenciamento de viagens (criação, edição e exclusão)
- Página home para apresentar o projeto

### Modelagem dos dados
O seguinte diagrama mostra a modelagem dos dados utilizada para esse projeto:

<img width="677" height="547" alt="models" src="https://github.com/user-attachments/assets/40fcdd10-8bdf-4f0f-870b-55ed405f492e" />


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

