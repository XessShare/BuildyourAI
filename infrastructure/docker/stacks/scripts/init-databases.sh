#!/bin/bash
set -e

# PostgreSQL initialization script
# Creates databases for Authentik and other services

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Create Authentik database
    SELECT 'CREATE DATABASE authentik' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'authentik')\gexec

    -- Create Authentik user
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'authentik') THEN
            CREATE USER authentik WITH PASSWORD '${AUTHENTIK_POSTGRESQL_PASSWORD}';
        END IF;
    END
    \$\$;

    -- Grant privileges
    GRANT ALL PRIVILEGES ON DATABASE authentik TO authentik;

    -- Create n8n database (optional)
    SELECT 'CREATE DATABASE n8n' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'n8n')\gexec

    -- Log success
    \echo '✅ Databases initialized successfully'
EOSQL

echo "PostgreSQL initialization complete"
