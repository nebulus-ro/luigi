import luigi
import sqlite3
import os
import csv
import pandas as pd
import pickle
import logging.config
import logging
import yaml

def table_exists(conn, tableName):
    try:
        conn.execute(f"SELECT 1 FROM {tableName} LIMIT 1")
        return True
    except sqlite3.OperationalError:
        return False

class StaTarget(luigi.Target):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sessionId = luigi.configuration.get_config().get('session', 'id')
        self.sessionPath = os.path.join('sessions', self.sessionId)
        logging.config.fileConfig('logging.conf')
        self.logger = logging.getLogger('luigi')
        self.logger.debug('StaTarget: ' + self.sessionPath)

class SQLiteTarget(StaTarget):

    STAGE_DB = 'stage.sqlite'

    def __init__(self, value = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = value
        self.logger.debug('SQLiteTarget: ' + str(value))
        self.database_path = os.path.join(self.sessionPath, self.STAGE_DB)
        self.logger.debug('SQLiteTarget: ' + self.database_path)

    def exists(self):
        if not os.path.exists(self.database_path):
            self.logger.warning(f'SQLiteTarget: No {self.database_path} file found in target.')
            return False
        if self.value is None:
            return True
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            # here we check if we heve the signature of the task.
            # Ex. str(task) will return something like this: MyTask(param1=123, param2=hello)
            # string that must uniquely describe an instance of a task
            query = f"SELECT 1 FROM targets WHERE name = '{str(self.value)}'"
            result = cursor.execute(query).fetchone()
            self.logger.debug('SQLiteTarget: ' + str(result))
            return result is not None

    def create(self):
        try:
            with self.connect() as conn:
                conn.execute(f"INSERT INTO targets (name) VALUES ('{str(self.value)}')")
                conn.commit()
        except Exception as ex:
            self.logger.error(ex)

    def connect(self):
        return sqlite3.connect(self.database_path)

class StaTask(luigi.Task):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.config.fileConfig('logging.conf')
        self.logger = logging.getLogger('luigi')
        self.sessionId = luigi.configuration.get_config().get('session', 'id')
        self.sessionPath = os.path.join('sessions', self.sessionId)
        self.logger.debug('StaTask: ' + self.sessionPath)
        with open(os.path.join(self.sessionPath, 'context.pickle'), 'rb') as pFile:
            self.context = pickle.load(pFile)

class CreateStageSQLiteTask(StaTask):

    def run(self):
        with self.output().connect() as conn:
            conn.execute("CREATE TABLE targets (id INTEGER PRIMARY KEY, name TEXT)")
            conn.commit()

    def output(self):
        return SQLiteTarget()

class TakeInputFile(StaTask):
    filename = luigi.Parameter()

    def run(self):
        try:
            with open(os.path.join(self.context["domainRoot"], 'tasks', 'EBSSBS_PRL_A-PTYPES.yaml'), 'r') as dtFile:
                DTYPES = yaml.safe_load(dtFile)
            self.logger.debug(str(DTYPES))
            inputPath = os.path.join(self.context["domainRoot"], 'in-data', self.filename)
            self.logger.debug(f'TakeInputFile: Input file: {inputPath}')
            df = pd.read_csv(inputPath, sep=';', dtype=DTYPES)
            df.to_pickle(self.output().path)
        except Exception as ex:
            self.logger.error(ex)

    def output(self):
        pre, _ = os.path.splitext(self.filename)
        return luigi.LocalTarget(os.path.join(self.sessionPath, pre + '.pickle'))
        

class TestCopyToTable(StaTask):
    
    TEST_TABLE = 'tests'

    def requires(self):
        return CreateStageSQLiteTask()

    def run(self):
        with self.output().connect() as conn:
            # if table tests to not exists, create it
            if not table_exists(conn, self.TEST_TABLE):
                self.logger.debug(f'TestCopyToTable: First time! Create table {self.TEST_TABLE}.')
                conn.execute(f"CREATE TABLE {self.TEST_TABLE} (id INTEGER PRIMARY KEY, name TEXT)")
        # Start a transaction
        conn.execute("BEGIN TRANSACTION")
        try:
            conn.execute(f"INSERT INTO targets (name) VALUES ('{str(self)}')")
            conn.execute(f"INSERT INTO {self.TEST_TABLE} (id, name) VALUES (2, 'Jane')")
            # commit the transaction
            conn.commit()
            self.logger.info('TestCopyToTable: Transaction OK.')
        except:
            # rollback the transaction if something goes wrong
            conn.rollback()
            self.logger.error('TestCopyToTable: Transaction rollback!')
            raise

    def output(self):
        return SQLiteTarget(self)

class TestExportSQLite(StaTask):
    
    def requires(self):
        return TestCopyToTable()

    def run(self):
        with self.input().connect() as conn:
            # Execute the query
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {TestCopyToTable.TEST_TABLE}")

            # Write the query result to a CSV file
            with self.output().open('w') as outfile:
                writer = csv.writer(outfile)
                writer.writerow([i[0] for i in cursor.description])  # write header
                writer.writerows(cursor)



    def output(self):
        return luigi.LocalTarget(os.path.join(self.sessionPath, 'TestExportSQLite.csv'))
