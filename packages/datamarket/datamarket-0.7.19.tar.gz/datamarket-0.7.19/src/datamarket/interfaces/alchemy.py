########################################################################################################################
# IMPORTS

import logging
from urllib.parse import quote_plus

from sqlalchemy import DDL, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

########################################################################################################################
# CLASSES

logger = logging.getLogger(__name__)


class AlchemyInterface:
    def __init__(self, config):
        if "db" in config:
            self.config = config["db"]

            self.engine = create_engine(self.get_conn_str())
            self.session = sessionmaker(bind=self.engine)()
            self.cursor = self.session.connection().connection.cursor()

        else:
            logger.warning("no db section in config")

    def get_conn_str(self):
        return (
            f'{self.config["engine"]}://'
            f'{self.config["user"]}:{quote_plus(self.config["password"])}'
            f'@{self.config["host"]}:{self.config["port"]}'
            f'/{self.config["database"]}'
        )

    @staticmethod
    def get_schema_from_table(table):
        schema = "public"

        if isinstance(table.__table_args__, tuple):
            for table_arg in table.__table_args__:
                if isinstance(table_arg, dict) and "schema" in table_arg:
                    schema = table_arg["schema"]

        elif isinstance(table.__table_args__, dict) and "schema" in table.__table_args__:
            schema = table.__table_args__["schema"]

        if schema == "public":
            logger.warning(f"no database schema provided, switching to {schema}...")

        return schema

    def create_tables(self, tables):
        for table in tables:
            schema = self.get_schema_from_table(table)

            with self.engine.connect() as conn:
                conn.execute(DDL(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
                conn.commit()

                if hasattr(table, "is_view") and table.is_view:
                    if not conn.dialect.has_table(conn, table.__tablename__, schema=schema):
                        logger.info(f"creating view {table.__tablename__}...")
                        table.create_view(conn)
                        conn.commit()
                    else:
                        logger.info(f"view {table.__tablename__} already exists")
                else:
                    if not conn.dialect.has_table(conn, table.__tablename__, schema=schema):
                        logger.info(f"creating table {table.__tablename__}...")
                        table.__table__.create(conn)
                        conn.commit()
                    else:
                        logger.info(f"table {table.__tablename__} already exists")

    def drop_tables(self, tables):
        for table in tables:
            schema = self.get_schema_from_table(table)

            with self.engine.connect() as conn:
                if hasattr(table, "is_view") and table.is_view:
                    if conn.dialect.has_table(conn, table.__tablename__, schema=schema):
                        logger.info(f"dropping view {table.__tablename__}...")
                        conn.execute(DDL(f"DROP VIEW {schema}.{table.__tablename__} CASCADE"))
                        conn.commit()
                else:
                    if conn.dialect.has_table(conn, table.__tablename__, schema=schema):
                        logger.info(f"dropping table {table.__tablename__}...")
                        conn.execute(DDL(f"DROP TABLE {schema}.{table.__tablename__} CASCADE"))
                        conn.commit()

    def reset_db(self, tables, drop):
        if drop:
            self.drop_tables(tables)

        self.create_tables(tables)

    def insert_alchemy_obj(self, alchemy_obj, silent=False):
        try:
            if not silent:
                logger.info(f"adding {alchemy_obj}...")

            self.session.add(alchemy_obj)
            self.session.commit()

        except IntegrityError:
            if not silent:
                logger.info(f"{alchemy_obj} already in db")

            self.session.rollback()
