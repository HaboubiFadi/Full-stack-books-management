-- Create the main application role (group role)
CREATE ROLE backend_app;

-- Create the actual database user
CREATE USER backend_user WITH PASSWORD 'securepassword';

-- Allow the backend_app role to connect to the database
GRANT CONNECT ON DATABASE postgres_db TO backend_app;

-- Grant usage on the public schema
GRANT USAGE ON SCHEMA public TO backend_app;

-- Allow the user to create, alter, and drop tables
GRANT CREATE ON SCHEMA public TO backend_app;
GRANT TEMP ON DATABASE postgres_db TO backend_app; -- For temporary tables

-- Grant full table privileges on existing tables
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO backend_app;

-- Grant sequence privileges (required for tables with SERIAL or IDENTITY columns)


GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO backend_app;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES FOR ROLE backend_app 
IN SCHEMA public 
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO backend_app;

-- Set default privileges for future sequences
ALTER DEFAULT PRIVILEGES FOR ROLE backend_app 
IN SCHEMA public 
GRANT ALL PRIVILEGES ON SEQUENCES TO backend_app;
GRANT backend_app TO backend_user;
