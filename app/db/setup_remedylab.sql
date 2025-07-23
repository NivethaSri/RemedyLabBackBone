-- 1. Create user with superuser permission
DROP ROLE IF EXISTS remedylab_backbone;
CREATE ROLE remedylab_backbone WITH LOGIN PASSWORD 'remedylab123' SUPERUSER;

-- 2. Drop existing database if it exists
DROP DATABASE IF EXISTS remedylab_db;

-- 3. Create database owned by the new user
CREATE DATABASE remedylab_db OWNER remedylab_backbone;

-- 4. Show all databases
\l
