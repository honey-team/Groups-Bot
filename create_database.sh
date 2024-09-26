#!/usr/bin/bash
psql -h localhost -U postgres  -c "CREATE DATABASE groupsbot;"

psql -h localhost -U postgres -d groupsbot -c """
    CREATE TABLE groupsTable (
    id SERIAL PRIMARY KEY,
    guild_id BIGINT,
    category_id BIGINT NULL,
    special_roles TEXT[] NULL,
    lang TEXT DEFAULT 'ru'
);
"""