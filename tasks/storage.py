from tasks import staluigi, validations, pEBSSBS_PRL_A_PRIM, workflow1
import sqlite3
import os
import pickle
import luigi

class StoreSQLiteTarget(staluigi.StaTarget):

    def __init__(self, sqlfile, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sqlfile = sqlfile
        with open(os.path.join(self.sessionPath, 'context.pickle'), 'rb') as pFile:
            self.context = pickle.load(pFile)
        self.storagePath = os.path.join(self.context["domainRoot"], 'storage', self.sqlfile + '.sqlite')

    def exists(self):
        if not os.path.exists(self.storagePath):
            self.logger.warning(f'StoreSQLiteTarget: No {self.storagePath} file found in target.')
            return False
        return True

    def connect(self):
        return sqlite3.connect(self.storagePath)

# add the final EBSSBS_PRL_A_PRIM.sqlite for primary series of EBSSBS_PRL_A 
class EBSSBS_PRL_A_PRIM(staluigi.StaTask):

    SQL_FILE = 'EBSSBS_PRL_A_PRIM'

    def run(self):
        with open(os.path.join(self.context["domainRoot"], 'storage', self.SQL_FILE + '.sql'), 'r') as sqlfile:
            sql_script = sqlfile.read()
        self.logger.debug(sql_script)
        try:
            with self.output().connect() as conn:
                conn.executescript(sql_script)
                conn.commit()
        except Exception as ex:
            self.logger.error('EBSSBS_PRL_A_PRIM: ' + str(ex))
            raise ex

    def output(self):
        return StoreSQLiteTarget(self.SQL_FILE)

class Add_EBSSBS_PRL_A_PRIM(staluigi.StaTask):
    inputfile = luigi.Parameter()

    def requires(self):
        return [EBSSBS_PRL_A_PRIM(), validations.ValidationsTask(self.inputfile)]

    def run(self):
        try:
            with open(workflow1.TakeInputFile(self.inputfile).output().path, 'rb') as pfile:
                dataset = pickle.load(pfile)
            with self.input()[0].connect() as conn:
                pEBSSBS_PRL_A_PRIM.process_set(conn, dataset)
            self.output().create()
        except Exception as ex:
            self.logger.error('Add_EBSSBS_PRL_A_PRIM: ' + str(ex))
            raise ex

    def output(self):
        return staluigi.SQLiteTarget(self)
