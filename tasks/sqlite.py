import luigi
from luigi.contrib.sqla import SQLAlchemyTarget
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlite3

Base = declarative_base()

class Target(Base):
    __tablename__ = "targets"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)


class SQLiteTarget(luigi.Target):

    STAGE_DB = 'stage.sqlite'

    def __init__(self, value):
        self.value = value
        
    def exists(self):
        id = luigi.configuration.get_config().get('session', 'id')
        localTarget = luigi.LocalTarget(f'sessions/{id}/{SQLiteTarget.STAGE_DB}', format=luigi.format.Nop)
        if not localTarget.exists():
            engine = create_engine(f"sqlite:///{localTarget.path}")
            Session = sessionmaker(bind=engine)
            session = Session()
            
            result = session.query(Target).filter(getattr(Target, 'name')==self.value).first()
            session.close()
            
            return result is not None
        else:
            return False

class CreateStageSQLiteTask(luigi.Task):

    def run(self):
        if not self.localTarget.exists():
            with self.output().engine.connect() as conn:
                conn.execute("CREATE TABLE targets (id INTEGER PRIMARY KEY, name TEXT)")

    def output(self):
        id = luigi.configuration.get_config().get('session', 'id')
        self.localTarget = luigi.LocalTarget(f'sessions/{id}/{SQLiteTarget.STAGE_DB}', format=luigi.format.Nop)
        return SQLAlchemyTarget(f"sqlite:///{self.localTarget.path}", "targets", 1)

class TestCopyToTable(luigi.Task):
    
    TEST_TABLE = 'tests'

    def requires(self):
        return CreateStageSQLiteTask()

    def run(self):
        id = luigi.configuration.get_config().get('session', 'id')
        localTarget = luigi.LocalTarget(f'sessions/{id}/{SQLiteTarget.STAGE_DB}', format=luigi.format.Nop)
        engine = create_engine(f"sqlite:///{localTarget.path}")
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # if table tests to not exists, create it
        # try:
        #     session.execute(f"SELECT 1 FROM {TestCopyToTable.TEST_TABLE} LIMIT 1")
        #     session.close()
        # except SQLAlchemyError:
        session.execute(f"CREATE TABLE {TestCopyToTable.TEST_TABLE} (id INTEGER PRIMARY KEY, name TEXT)")
        close()

        # start a transaction
        # trans = engine.connect().begin()
        # try:
        #     conn.execute(f"INSERT INTO targets (name) VALUES ({self.__class__.__name__})")
        #     conn.execute(f"INSERT INTO {TestCopyToTable.TEST_TABLE} (id, name) VALUES (2, 'Jane')")
        #     # commit the transaction
        #     trans.commit()
        # except:
        #     # rollback the transaction if something goes wrong
        #     trans.rollback()
        #     raise

    def output(self):
        return SQLiteTarget(self.__class__.__name__)

class TestExportSQLite(luigi.Task):
    
    def requires(self):
        return [CreateStageSQLiteTask(), TestCopyToTable()]

    def run(self):
        with self.input()[0].engine.connect() as conn:
            # check if the data already exists
            result = conn.execute(f"SELECT * FROM {TestCopyToTable.TEST_TABLE}").fetchall()
            with self.output().open('w') as outfile:
                outfile.write(result)

    def output(self):
        id = luigi.configuration.get_config().get('session', 'id')
        return luigi.LocalTarget(f'sessions/{id}/TestExportSQLite.csv', format=luigi.format.Nop)
