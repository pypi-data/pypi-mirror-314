Framework to define and run AB tests within a python ecosystempy

[![Documentation Status](https://readthedocs.org/projects/py-ab/badge/?version=latest)](https://py-ab.readthedocs.io/en/latest/?badge=latest)
[![PyPi Version](https://img.shields.io/pypi/v/py-ab-experiment.svg)](https://pypi.python.org/pypi/py-ab-experiment/)

# Installation
`pip install py-ab-experiment` to install the library

# Usage
You first need a suitable configuration to set up an experiment. You can use one of the sample files provided in `src/tests/unit/test_programs`, or create your own using the configuration file format (see the [documentation](https://py-ab.readthedocs.io) for details)

using the `splitter_test.pyab` definition, which is defined as
```
def basic_experiment_1{
        //some splitter fields
        splitters: my_id
        if field_1 == 'a'{
                return "Setting 1" weighted 4, "Setting 2" weighted 1
        }
        else{
                return "Setting 1" weighted 1, "Setting 2" weighted 1
        }
}
```

## Dynamic compilation

You can then load an experiment in python by
```
from pyab_experiment.experiment_evaluator import ExperimentEvaluator
with open(file_name, "r") as fp:
    evaluator = ExperimentEvaluator(fp.read()) # load and compile the experiment code
```

## Experiment execution
Then we run experiments by calling the experiment object with the fields needed
```
experiment_group = evaluator(my_id=123,field1='a')
```

The experiment group will return a "cohort" based on the 2 values defined in the configuration file. To Illustrate using the sample configuration defined above, when we repeatedly call `experiment` with `field1='a'`  we will get on average 'Setting 1' about 80% of the times (as long as my_id is uniformly distributed). If field1 is anything other than 'a' we will get on average a 50/50 split between 'Setting 1' and 'Setting 2'

The determinism comes from the fact that the same my_id will always result in the same group assignment, (in our example, given the same field_1 value)
