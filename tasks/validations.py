import luigi
import yaml
from tasks import workflow1

class Validation1(luigi.Task):
    inputfile = luigi.Parameter()
    def run(self):
        print("Running Validation1 for: ", self.inputfile)

class Validation2(luigi.Task):
    inputfile = luigi.Parameter()
    def run(self):
        print("Running Validation2 for: ", self.inputfile)
        raise ValueError('Some error')

class Validation3(luigi.Task):
    inputfile = luigi.Parameter()
    def run(self):
        print("Running Validation3 for: ", self.inputfile)

class ValidationsTask(luigi.Task):
    filename = luigi.Parameter()

    def requires(self):
        return workflow1.TakeInputFile(self.filename)

    def run(self):
        print("Running Validations")
        with open('tasks/validations.yaml', 'r') as yamlfile:
            config = yaml.safe_load(yamlfile)
        subtasks = {
            "Validation1": Validation1,
            "Validation2": Validation2,
            "Validation3": Validation3
        }
        for task_name, run in config["validations"].items():
             if run:
                subtasks[task_name](self.input()).run()

    def output(self):
        return self.input()
