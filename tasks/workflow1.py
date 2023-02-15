import luigi
import os
import csv
import pandas as pd
import yaml

from tasks import staluigi

class TakeInputFile(staluigi.StaTask):
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
        

class TestCopyToTable(staluigi.StaTask):
    
    TEST_TABLE = 'tests'

    def requires(self):
        return staluigi.CreateStageSQLiteTask()

    def run(self):
        with self.output().connect() as conn:
            # if table tests to not exists, create it
            if not staluigi.table_exists(conn, self.TEST_TABLE):
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
        return staluigi.SQLiteTarget(self)

class TestExportSQLite(staluigi.StaTask):
    
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
