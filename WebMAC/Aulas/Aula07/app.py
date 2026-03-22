from fastapi import FastAPI
from sqlmodel import Session, select, SQLModel, create_engine, col
from models import Aluno, Tarefa

arquivo_sqlite = "exercicio_7.db"
url_sqlite = f"sqlite:///{arquivo_sqlite}"

engine = create_engine(url_sqlite)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()

@app.post("/alunos")
def criar_aluno(aluno: Aluno) -> Aluno:
    with Session(engine) as session:
        session.add(aluno)
        session.commit()
        session.refresh(aluno)
        return aluno

@app.post("/tarefas")
def criar_tarefa(tarefa: Tarefa):
    with Session(engine) as session:
        session.add(tarefa)
        session.commit()
        session.refresh(tarefa)
        return tarefa


@app.get("/alunos")
def listar_alunos() -> list[Aluno]:
    with Session(engine) as session:
        return list(session.exec(select(Aluno)).all())

@app.get("/tarefas")
def listar_tarefas() -> list[Tarefa]:
    with Session(engine) as session:
        return list(session.exec(select(Tarefa)).all())

@app.get("/alunos/{aluno_nusp}/tarefas")
def listar_tarefas_do_aluno(aluno_nusp: int):
    with Session(engine) as session:
        tarefas = session.exec(select(Tarefa).where(col(Tarefa.aluno_nusp) == aluno_nusp))
        return list(tarefas)