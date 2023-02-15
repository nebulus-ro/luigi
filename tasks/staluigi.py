import sqlite3
import luigi
import logging.config
import os
import pickle

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
