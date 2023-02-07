import luigi
import sqlite3
import os
import csv

class SQLiteTarget(luigi.Target):

    STAGE_DB = 'stage.sqlite'

    def __init__(self, value = None):
        self.value = value
        id = luigi.configuration.get_config().get('session', 'id')
        self.database_path = f'sessions/{id}/{SQLiteTarget.STAGE_DB}'

    def exists(self):
        if not os.path.exists(self.database_path):
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
            return result is not None

    def connect(self):
        return sqlite3.connect(self.database_path)


class CreateStageSQLiteTask(luigi.Task):

    def run(self):
        with self.output().connect() as conn:
            conn.execute("CREATE TABLE targets (id INTEGER PRIMARY KEY, name TEXT)")

    def output(self):
        return SQLiteTarget()


class TestCopyToTable(luigi.Task):
    
    TEST_TABLE = 'tests'

    def requires(self):
        return CreateStageSQLiteTask()

    def run(self):
        with self.output().connect() as conn:
            # if table tests to not exists, create it
            try:
                conn.execute(f"SELECT 1 FROM {TestCopyToTable.TEST_TABLE} LIMIT 1")
            except:
                conn.execute(f"CREATE TABLE {TestCopyToTable.TEST_TABLE} (id INTEGER PRIMARY KEY, name TEXT)")
        # Start a transaction
        conn.execute("BEGIN TRANSACTION")
        try:
            conn.execute(f"INSERT INTO targets (name) VALUES ('{str(self)}')")
            conn.execute(f"INSERT INTO {TestCopyToTable.TEST_TABLE} (id, name) VALUES (2, 'Jane')")
            # commit the transaction
            conn.commit()
        except:
            # rollback the transaction if something goes wrong
            conn.rollback()
            raise

    def output(self):
        return SQLiteTarget(self)

class TestExportSQLite(luigi.Task):
    
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
        id = luigi.configuration.get_config().get('session', 'id')
        return luigi.LocalTarget(f'sessions/{id}/TestExportSQLite.csv')
