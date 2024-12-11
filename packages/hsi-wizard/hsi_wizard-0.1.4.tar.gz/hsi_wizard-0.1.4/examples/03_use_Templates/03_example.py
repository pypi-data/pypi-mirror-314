import wizard
import numpy as np


# create a dc
dc = wizard.DataCube(np.random.rand(20, 640, 460))

# load and execute the template
dc.execute_template('03_example.yml')