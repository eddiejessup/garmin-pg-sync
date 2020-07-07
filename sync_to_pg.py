import os
import os.path
import sqlite3
import psycopg2
from psycopg2.extras import execute_batch

PG_DB = os.environ['PG_DB']
PG_USER = os.environ['PG_USER']
PG_PASSWORD = os.environ['PG_PASSWORD']
PG_HOST = os.environ['PG_HOST']
PG_PORT = os.environ['PG_PORT']

print(f'$PG_DB: {PG_DB}')
print(f'$PG_USER: {PG_USER}')
print(f'$PG_PASSWORD has length: {len(PG_PASSWORD)}')
print(f'$PG_HOST: {PG_HOST}')
print(f'$PG_PORT: {PG_PORT}')

SQLITE_DB_PATH = os.path.expanduser('~/HealthData/DBs/garmin_monitoring.db')

print(f'SQLITE_DB_PATH: {SQLITE_DB_PATH}')

print('# Reading from SQLite')

sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)
print('Got SQLite connection')
sqlite_cursor = sqlite_conn.cursor()
print('Got SQLite cursor')
sqlite_cursor.execute('select timestamp, heart_rate from monitoring_hr')
print('Executed SQLite read query')
rows = sqlite_cursor.fetchall()
print(f'Got {len(rows)} rows')

print('# Writing to PostgreSQL')

pg_conn = psycopg2.connect(
    dbname=PG_DB,
    user=PG_USER,
    password=PG_PASSWORD,
    host=PG_HOST,
    port=PG_PORT,
)
print('Got PostgreSQL connection')
pg_cursor = pg_conn.cursor()
print('Got PostgreSQL cursor')
execute_batch(
    pg_cursor,
    '''
        INSERT INTO monitoring_hr (measure_time, heart_rate)
        VALUES (%s, %s)
        ON CONFLICT (measure_time) DO UPDATE SET heart_rate = EXCLUDED.heart_rate
    ''',
    rows,
)
print('Executed PostgreSQL write query')
pg_conn.commit()
print('Commited PostgreSQL transaction')
