# Projeto de API de Análise de Prompt

## Visão Geral

Este projeto é uma API desenvolvida com **FastAPI** que permite analisar prompts de texto e registrar o resultado da
análise. Além disso, oferece endpoints para consultar o histórico das análises realizadas.

## Tecnologias Utilizadas

- **Python 3.12**
- **FastAPI** - Framework web para criar APIs rápidas e assíncronas.
- **SQLAlchemy** (async) - ORM para interagir com o banco de dados.
- **Alembic** - Ferramenta de migração de banco de dados.
- **Pydantic** - Validação de dados via modelos.
- **AsyncSession** - Suporte a transações assíncronas no SQLAlchemy.

## Dependências Principais

- `fastapi`
- `uvicorn`
- `sqlalchemy[asyncio]`
- `alembic`
- `python-dotenv` (para gerenciamento de variáveis de ambiente)
- `aiogram` (ou outra biblioteca de serviço de IA, caso aplicável)

## Endpoints Principais

| Método | Rota                | Descrição                                      |
|--------|---------------------|------------------------------------------------|
| `POST` | `/analyze`          | Recebe um prompt de texto e executa a análise. |
| `GET`  | `/history`          | Retorna o histórico completo de análises.      |
| `GET`  | `/history/{log_id}` | Retorna um registro específico pelo ID.        |

## Como Executar

1. **Clonar o repositório**
   ```bash
   git clone <url-do-repositorio>
   cd <pasta-do-projeto>
   ```

2. **Criar e ativar o ambiente virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   .\\venv\\Scripts\\activate   # Windows
   ```

3. **Instalar as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar o banco de dados**
    - Crie um banco PostgreSQL (ou outro compatível).
    - Defina a variável de ambiente `DATABASE_URL` com a string de conexão.

5. **Aplicar migrações (se houver)**
   ```bash
   alembic upgrade head
   ```

6. **Executar a aplicação**
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Testar a API**  
   Acesse a documentação interativa automática em:
   ```
   http://127.0.0.1:8000/docs
   ```

## Testes

- Execute os testes unitários com `pytest` ou a ferramenta de teste que o projeto utiliza.
- Certifique-se de que todas as dependências de teste (como `pytest-asyncio`) estejam instaladas.

## Contribuição

- Fork o projeto.
- Crie uma branch para a sua feature (`git checkout -b feature/nova-funcionalidade`).
- Commit suas mudanças (`git commit -m 'Add some feature'`).
- Faça push para a branch (`git push origin feature/nova-funcionalidade`).
- Abra um Pull Request.
