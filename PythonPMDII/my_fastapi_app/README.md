# API de Alunos com FastAPI

Este é um exemplo de uma API de gerenciamento de alunos utilizando o FastAPI com um banco de dados SQLite. Esta API permite criar, listar, atualizar e excluir registros de alunos.

## Requisitos

Antes de começar, certifique-se de que você tem os seguintes requisitos instalados:

- Python 3.11 ou superior
- `pip`

## Instalação

1. **Clone o Repositório**

   ```bash
   git clone https://github.com/surerocha/LearningPython.git
   cd LearningPython
   ```

2. **Crie e Ative um Ambiente Virtual**

   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```

3. **Instale as Dependências**

   Com o ambiente virtual ativado, instale as dependências necessárias:

   ```bash
   pip install fastapi[all] uvicorn
   ```

## Configuração

1. **Crie o Arquivo `main.py`**

   No diretório do projeto, crie um arquivo chamado `main.py` com o seguinte conteúdo:

   ```python
   from fastapi import FastAPI, HTTPException
   from pydantic import BaseModel
   from typing import List

   app = FastAPI()

   class Aluno(BaseModel):
       nome: str
       idade: int

   alunos_db = []

   @app.post("/alunos/", response_model=Aluno)
   def criar_aluno(aluno: Aluno):
       alunos_db.append(aluno)
       return aluno

   @app.get("/alunos/", response_model=List[Aluno])
   def listar_alunos():
       return alunos_db

   @app.get("/alunos/{id}", response_model=Aluno)
   def listar_aluno(id: int):
       if id >= len(alunos_db):
           raise HTTPException(status_code=404, detail="Aluno não encontrado")
       return alunos_db[id]

   @app.put("/alunos/{id}", response_model=Aluno)
   def atualizar_aluno(id: int, aluno: Aluno):
       if id >= len(alunos_db):
           raise HTTPException(status_code=404, detail="Aluno não encontrado")
       alunos_db[id] = aluno
       return aluno

   @app.delete("/alunos/{id}")
   def excluir_aluno(id: int):
       if id >= len(alunos_db):
           raise HTTPException(status_code=404, detail="Aluno não encontrado")
       alunos_db.pop(id)
       return {"detail": "Aluno excluído"}
   ```

2. **Inicie o Servidor**

   Execute o servidor Uvicorn com o seguinte comando:

   ```bash
   uvicorn main:app --reload
   ```

   Isso iniciará o servidor na URL `http://127.0.0.1:8000`.

## Testando a API com o Postman

Para testar a API, siga estas instruções no Postman:

### 1. Criar Aluno

- **Método**: `POST`
- **URL**: `http://127.0.0.1:8000/alunos/`
- **Cabeçalhos**:
  - `Content-Type: application/json`
- **Corpo** (JSON):

  ```json
  {
      "nome": "João Silva",
      "idade": 22
  }
  ```

- **Resposta Esperada**:

  ```json
  {
      "nome": "João Silva",
      "idade": 22
  }
  ```

### 2. Listar Alunos

- **Método**: `GET`
- **URL**: `http://127.0.0.1:8000/alunos/`
- **Resposta Esperada**:

  ```json
  [
      {
          "nome": "João Silva",
          "idade": 22
      }
  ]
  ```

### 3. Listar um Aluno por ID

- **Método**: `GET`
- **URL**: `http://127.0.0.1:8000/alunos/{id}`
  - Substitua `{id}` pelo ID do aluno que você deseja recuperar.
- **Resposta Esperada**:

  ```json
  {
      "nome": "João Silva",
      "idade": 22
  }
  ```

### 4. Atualizar Aluno

- **Método**: `PUT`
- **URL**: `http://127.0.0.1:8000/alunos/{id}`
  - Substitua `{id}` pelo ID do aluno que você deseja atualizar.
- **Cabeçalhos**:
  - `Content-Type: application/json`
- **Corpo** (JSON):

  ```json
  {
      "nome": "João da Silva",
      "idade": 23
  }
  ```

- **Resposta Esperada**:

  ```json
  {
      "nome": "João da Silva",
      "idade": 23
  }
  ```

### 5. Excluir Aluno

- **Método**: `DELETE`
- **URL**: `http://127.0.0.1:8000/alunos/{id}`
  - Substitua `{id}` pelo ID do aluno que você deseja excluir.
- **Resposta Esperada**:

  ```json
  {
      "detail": "Aluno excluído"
  }
  ```
