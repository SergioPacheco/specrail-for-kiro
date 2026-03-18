# Structure Steering

## Migration file layout
```
db/migration/
├── V001__create_users_table.sql
├── V002__create_orders_table.sql
├── V003__add_email_index_to_users.sql
├── V004__add_status_to_orders.sql
├── R001__rollback_V004.sql          ← rollback scripts
└── seed/
    └── dev-data.sql                 ← dev-only seed data, never runs in prod
```

## Naming conventions
- Tables: `snake_case`, plural — `user_accounts`, `order_items`
- Columns: `snake_case` — `created_at`, `order_total`, `is_active`
- Indexes: `idx_{table}_{columns}` — `idx_users_email`, `idx_orders_status_created`
- Foreign keys: `fk_{table}_{referenced_table}` — `fk_orders_users`
- Constraints: `chk_{table}_{rule}` — `chk_orders_total_positive`
- Migrations: `V{number}__{description}.sql` — double underscore, descriptive name
- Rollbacks: `R{number}__rollback_V{number}.sql`

## Schema conventions
- Every table has: `id BIGSERIAL PRIMARY KEY`, `created_at TIMESTAMPTZ DEFAULT NOW()`, `updated_at TIMESTAMPTZ DEFAULT NOW()`
- Use `TIMESTAMPTZ` not `TIMESTAMP` — always store timezone info
- Use `TEXT` not `VARCHAR(n)` unless there's a real business constraint on length
- Use `BOOLEAN` not `SMALLINT` for true/false
- Use `JSONB` not `JSON` when you need to store semi-structured data
- Enums: use `TEXT` with `CHECK` constraint, not PostgreSQL `ENUM` type (enums can't be altered easily)
