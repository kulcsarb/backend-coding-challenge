from yoyo import read_migrations, get_backend
from fabric.api import task, run
import psycopg2
import os
from subprocess import call
import traceback


PG_HOST = os.environ.get('PG_HOST', None)
PG_PORT = os.environ.get('PG_PORT', None)
PG_USER = os.environ.get('PG_USERNAME', None)
PG_PASSWORD = os.environ.get('PG_PASSWORD', None)
DATABASE = os.environ.get('DATABASE', None)

URL = f'postgres://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{DATABASE}'

@task
def create():    
    with psycopg2.connect(host=PG_HOST, user=PG_USER, port=PG_PORT, password=PG_PASSWORD) as connection:
        connection.autocommit = True      
        try:  
            with connection.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE {DATABASE}")
        except:
            pass

@task
def drop():    
    with psycopg2.connect(host=PG_HOST, user=PG_USER, port=PG_PORT, password=PG_PASSWORD) as connection:
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(f"DROP DATABASE {DATABASE}")


@task
def migrate():    
    try:
        backend = get_backend(URL, '_migrations')
        migrations = read_migrations('./db/migrations')
        backend.apply_migrations(backend.to_apply(migrations))
    except:
        print(traceback.format_exc())


@task
def rollback():    
    backend = get_backend(URL, '_migrations')
    migrations = read_migrations('./db/migrations')[-1:]
    backend.rollback_migrations(backend.to_rollback(migrations))


@task
def init():    
    create()
    migrate()