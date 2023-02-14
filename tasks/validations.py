import luigi
import yaml

from tasks import workflow1

class Validation1(workflow1.StaTask):
    inputfile = luigi.Parameter()
    
    def requires(self):
        return [workflow1.TakeInputFile(self.inputfile), workflow1.CreateStageSQLiteTask()]

    def run(self):
        print("Running Validation1 for: ", self.inputfile)
        self.logger.debug("Running Validation1 for: " + self.inputfile)
        self.output().create()

    def output(self):
        return workflow1.SQLiteTarget(self)

class Validation2(workflow1.StaTask):
    inputfile = luigi.Parameter()
    
    def requires(self):
        return [workflow1.TakeInputFile(self.inputfile), workflow1.CreateStageSQLiteTask()]

    def run(self):
        print("Running Validation2 for: ", self.inputfile)
        self.logger.debug("Running Validation2 for: " + self.inputfile)
        self.output().create()
        raise ValueError('Some error')

    def output(self):
        return workflow1.SQLiteTarget(self)

class Validation3(workflow1.StaTask):
    inputfile = luigi.Parameter()

    def requires(self):
        return [workflow1.TakeInputFile(self.inputfile), workflow1.CreateStageSQLiteTask()]

    def run(self):
        print("Running Validation3 for: ", self.inputfile)
        self.logger.debug("Running Validation3 for: " + self.inputfile)
        self.output().create()

    def output(self):
        return workflow1.SQLiteTarget(self)


class ValidationsTask(workflow1.StaTask):
    inputfile = luigi.Parameter()

    def requires(self):
        with open('tasks/validations.yaml', 'r') as yamlfile:
            config = yaml.safe_load(yamlfile)
        subtasks = {
            "Validation1": Validation1,
            "Validation2": Validation2,
            "Validation3": Validation3
        }
        self.logger.debug('ValidationsTask' + str(config))
        retList = [workflow1.TakeInputFile(self.inputfile)] + [subtasks[task_name](self.inputfile) for task_name, run in config["validations"].items() if run]
        self.logger.debug('ValidationsTask' + str(retList))
        return retList

    def output(self):
        return self.input()[0]
