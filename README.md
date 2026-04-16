# Detector de Prompt Injection

API especializada em detecção de ataques de injeção de prompt em sistemas de IA, desenvolvida com FastAPI e Python 3.12. Analisa textos em busca de padrões maliciosos utilizando modelos do Hugging Face e Google SDK, persistindo o histórico de análises em PostgreSQL.

---

## Stack

| Camada | Tecnologias |
|---|---|
| **API** | Python 3.12, FastAPI, Uvicorn |
| **IA / Modelos** | Hugging Face Transformers, Google SDK |
| **Banco de Dados** | PostgreSQL, SQLAlchemy (Async), Alembic |
| **Validação** | Pydantic v2 |
| **Infra** | Docker, Docker Compose |

---

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/analyze` | Analisa um prompt e retorna o resultado da classificação |
| `GET` | `/history` | Lista o histórico completo de análises |
| `GET` | `/history/{log_id}` | Retorna uma análise específica pelo ID |

---

## Como rodar

### Pré-requisitos
- Docker e Docker Compose instalados

### Com Docker (recomendado)
```bash
git clone https://github.com/carloswps/detector-prompt-injection.git
cd detector-prompt-injection
cp .env.example .env  # configure as variáveis
docker compose up --build
```

Acesse a documentação interativa em: `http://localhost:8000/docs`

### Sem Docker

```bash
# 1. Ambiente virtual
python -m venv venv
source venv/bin/activate      # Linux/Mac
.\\venv\\Scripts\\activate    # Windows

# 2. Dependências
pip install -r requirements.txt

# 3. Variáveis de ambiente
cp .env.example .env

# 4. Migrações
alembic upgrade head

# 5. Rodar
uvicorn app.main:app --reload
```

---

## Variáveis de ambiente

```ini
DATABASE_URL=...
HUGGINGFACE_API_KEY=hf_...
GOOGLE_API_KEY=...
```

---

## Testes

```bash
pip install pytest pytest-asyncio
pytest
```

---

## Licença

MIT
