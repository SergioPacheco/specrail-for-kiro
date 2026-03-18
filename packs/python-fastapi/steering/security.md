# Security Steering

## Authentication and authorization
- Use FastAPI's `Depends()` for auth injection — never check auth inside route handler body
- JWT validation: `python-jose` or `authlib` with RS256
- Role-based access: custom `Depends()` that checks user roles
- CORS: configure explicitly in `main.py`, never `allow_origins=["*"]` in production

## Input validation
- Pydantic validates all request bodies automatically — leverage this
- Path/query parameters: use `Path(...)`, `Query(...)` with constraints
- File uploads: validate MIME type, enforce size limits via `UploadFile`
- Never trust client-provided filenames — sanitize or generate new ones

## SQL injection prevention
- SQLAlchemy parameterized queries by default — safe
- Raw SQL: always use `text()` with `:param` bind parameters
- Never use f-strings or `.format()` in SQL queries

## Secrets management
- Never commit secrets to git
- Use `pydantic-settings` to load from environment variables
- For complex setups: AWS Secrets Manager, HashiCorp Vault
- If a secret was committed: rotate immediately

## Dependency security
- Run `pip-audit` or `safety check` in CI
- Keep dependencies updated — `uv lock --upgrade` or `poetry update`
- Critical CVEs: patch within 7 days

## API security
- Rate limiting: `slowapi` or reverse proxy (nginx, API gateway)
- HTTPS only in production
- Security headers via middleware: `X-Content-Type-Options`, `X-Frame-Options`
- Disable `/docs` and `/redoc` in production or secure behind auth
