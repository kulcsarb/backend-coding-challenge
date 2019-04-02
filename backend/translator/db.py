from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.schema import MetaData
import sqlalchemy.exc
import psycopg2
import traceback
import logging 
import time 
from . import POSTGRESQL_URL

LOGGER = logging.getLogger('translator.db')

translations = None
engine = None
connection = None

def init():
    global engine, connection, translations
    LOGGER.info('PostgreSQL at ' + POSTGRESQL_URL)
    while True:
        try:            
            engine = create_engine(POSTGRESQL_URL, poolclass=StaticPool)
            connection = engine.connect()

            meta = MetaData()
            meta.reflect(bind=engine)
            translations = meta.tables['translations']            
            break
        except sqlalchemy.exc.OperationalError as e:            
            time.sleep(1.0)
            print(e)
        except sqlalchemy.exc.NoSuchTableError as e:            
            time.sleep(1.0)
            print(e)
        except Exception as e:
            LOGGER.error(e)
            print(e)
            time.sleep(1.0)


def execute(query):
    global connection
    retries = 3
    while retries:
        if not connection:            
            init()

        try:
            return connection.execute(query)
        except sqlalchemy.exc.DBAPIError as e:
            if e.connection_invalidated:
                connection = None
            LOGGER.warning('!!!')
            time.sleep(1.0)
        finally:
            retries -= 1


def new_translation(sid, uid, text, source, target, status):
    execute( 
        translations
            .insert()
            .values(sid=sid, \
                    id=uid, \
                    text=text,
                    source_language=source, \
                    target_language=target, \
                    status=status
                    )
        )

def update_translation(uid, status, translation):
    execute(
        translations
            .update()
            .where(translations.c.id == uid)
            .values(
                translation = translation, \
                status = status
                )            
        )
