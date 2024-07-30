# schemas.py
from pydantic import BaseModel

class AlunoBase(BaseModel):
    nome: str
    idade: int

class AlunoCreate(AlunoBase):
    pass

class Aluno(AlunoBase):
    id: int

    class Config:
        orm_mode = True
