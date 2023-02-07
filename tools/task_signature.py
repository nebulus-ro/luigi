import luigi

class MyTask(luigi.Task):
    param1 = luigi.IntParameter()
    param2 = luigi.Parameter()

    def run(self):
        # Implementation of the task
        pass

task = MyTask(param1=123, param2="hello")

# Retrieve the class name of the task
class_name = type(task).__name__
# print(f"Class name: {class_name}")

# Retrieve all parameters with their values
params = task.get_params()
print(params)
parlist = []
for param_name, param_value in params:
    var = param_value
    # parlist.append(f"{param_name}= {task.get_param_values(params, {}, {})}")
# luigi.parameter.IntParameter().task_value(class_name, param_name)
print(f'{str(task)}')