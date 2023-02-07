import luigi
import os
import pickle
import json

def replace_extension(file_name, new_extension):
    return ".".join(file_name.split(".")[:-1]) + "." + new_extension

class FileExistTask(luigi.Task):
    filePath = luigi.Parameter()

    # def run(self):
    #     id = luigi.configuration.get_config().get('session', 'id')
    #     if not self.filePath:
    #         raise Exception("File path is missing.")
    #     if not os.path.exists(f'sessions/{id}/{self.filePath}'):
    #         raise Exception("File does not exist.")

    def output(self):
        id = luigi.configuration.get_config().get('session', 'id')
        # parameter format is important because without the Target will be a text file (and we need it binary)
        return luigi.LocalTarget(f'sessions/{id}/{self.filePath}', format=luigi.format.Nop)

class Pickle2Json(luigi.Task):
    filePath = luigi.Parameter()

    def requires(self):
        return FileExistTask(self.filePath)

    def run(self):
        # id = luigi.configuration.get_config().get('session', 'id')
        with self.input().open("r") as infile:
        # with open(f'sessions/{id}/{self.filePath}', 'rb') as infile:
            content = pickle.load(infile)
            with self.output().open("w") as outfile:
                json.dump(content, outfile)


    def output(self):
        id = luigi.configuration.get_config().get('session', 'id')
        return luigi.LocalTarget(f'sessions/{id}/{replace_extension(self.filePath, "json")}')