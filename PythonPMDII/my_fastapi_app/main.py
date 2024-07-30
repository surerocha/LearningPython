# main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
import models, schemas

app = FastAPI()

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/alunos/", response_model=schemas.Aluno)
def criar_aluno(aluno: schemas.AlunoCreate, db: Session = Depends(get_db)):
    db_aluno = models.Aluno(nome=aluno.nome, idade=aluno.idade)
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

@app.get("/alunos/", response_model=list[schemas.Aluno])
def listar_alunos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Aluno).offset(skip).limit(limit).all()

@app.get("/alunos/{aluno_id}", response_model=schemas.Aluno)
def listar_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(models.Aluno).filter(models.Aluno.id == aluno_id).first()
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno

@app.put("/alunos/{aluno_id}", response_model=schemas.Aluno)
def atualizar_aluno(aluno_id: int, aluno: schemas.AlunoCreate, db: Session = Depends(get_db)):
    db_aluno = db.query(models.Aluno).filter(models.Aluno.id == aluno_id).first()
    if db_aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    db_aluno.nome = aluno.nome
    db_aluno.idade = aluno.idade
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

@app.delete("/alunos/{aluno_id}", response_model=schemas.Aluno)
def excluir_aluno(aluno_id: int, db: Session = Depends(get_db)):
    db_aluno = db.query(models.Aluno).filter(models.Aluno.id == aluno_id).first()
    if db_aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    db.delete(db_aluno)
    db.commit()
    return db_aluno
