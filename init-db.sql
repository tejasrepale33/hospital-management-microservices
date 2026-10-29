-- Auto-create databases if they don't exist
SELECT 'CREATE DATABASE patient_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'patient_db')\gexec

SELECT 'CREATE DATABASE doctor_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'doctor_db')\gexec
