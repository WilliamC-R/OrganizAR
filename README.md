# OrganizAR

Aplicação full-stack para controle financeiro pessoal/empresarial com autenticação, separação por usuário e base para evoluir módulos futuros.

## Stack

- Frontend: Angular + TypeScript + Reactive Forms + Router + HttpClient
- Backend: Python + Flask (API REST JSON)
- Banco: PostgreSQL
- ORM: SQLAlchemy
- Migrations: Flask-Migrate (Alembic)
- Auth: JWT com access token curto e refresh token longo em cookies HttpOnly
- Segurança: CORS restrito, CSRF com double submit cookie, senhas com hash forte

## Estrutura

```
/backend
  /app
    /config
    /db
    /models
    /repositories
    /services
    /routes
    /schemas
    /security
    /utils
  /migrations
  /tests
  requirements.txt
  Dockerfile
  wsgi.py
/frontend
  /src/app
    /core
    /shared
    /features
```

## Setup local

1. Copie `.env.example` para `.env` e ajuste valores.
2. Suba o banco e a API:

```bash
docker-compose up --build
```

3. Rode as migrations:

```bash
cd backend
flask db upgrade
```

4. Frontend:

```bash
cd frontend
npm install
npm start
```

Acesse: `http://localhost:4200`

## Migrations

```bash
cd backend
export FLASK_APP=wsgi.py
flask db migrate -m "init"
flask db upgrade
```

## Endpoints principais

- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/refresh`
- `POST /api/auth/logout`
- `GET /api/auth/me`
- `GET /api/categories`
- `POST /api/categories`
- `PUT /api/categories/:id`
- `DELETE /api/categories/:id`
- `GET /api/entries`
- `POST /api/entries`
- `PUT /api/entries/:id`
- `DELETE /api/entries/:id`
- `GET /api/reports/summary`

## Smoke test (mental)

1. `docker-compose up --build`
2. `flask db upgrade`
3. Registrar usuário
4. Login
5. Criar categoria
6. Criar lançamento
7. Ver listagem e relatório

## Observações de segurança

- Tokens JWT armazenados em cookies HttpOnly e `SameSite`.
- CSRF via double submit cookie (header `X-CSRF-Token`).
- Segredos em `.env` (não comitar).
