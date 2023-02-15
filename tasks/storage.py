from tasks import staluigi, validations
import sqlite3
import os
import pickle

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

    def connect(self):
        return sqlite3.connect(self.storagePath)

# add the final EBSSBS_PRL_A_PRIM.sqlite for primary series of EBSSBS_PRL_A 
class EBSSBS_PRL_A_PRIM(staluigi.StaTask):

    SQL_FILE = 'EBSSBS_PRL_A_PRIM'
    def run(self):
        with open(os.path.join(self.context["domainRoot"], 'storage', self.SQL_FILE + '.sql'), 'r') as sqlfile:
            sql_script = sqlfile.read()
        self.logger.debug(sql_script)
        with self.output().connect() as conn:
            conn.execute(sql_script)
            conn.commit()

    def output(self):
        return StoreSQLiteTarget(self.SQL_FILE)

