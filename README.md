# MTP-ICTD
This repository contains the hydrological datasets and all my work done in ICTD lab during my MTech.


# QGIS setup
The following lines are example to setup a Python environment where you can interact with QGIS functions and algorithms, perform spatial analyses, and automate geospatial workflows without relying on the QGIS desktop interface.

```Python
from qgis.core import *
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
import processing, qgis
from processing.core.Processing import Processing
import os, sys, json

qspath = '~/qgis_sys_paths.csv' 
# provide the path where you saved this file.
paths = pd.read_csv(qspath).paths.tolist()
sys.path += paths

# set up environment variables
qepath = '/Users/xyz/qgis_env.json'
js = json.loads(open(qepath, 'r').read())
for k, v in js.items():
    os.environ[k] = v

# set the PYTHONHOME environment variable (from the JSON file) for QGIS to locate its Python installation.
QgsApplication.setPrefixPath(js['PYTHONHOME'], True) 
qgs = QgsApplication([], False)
qgs.initQgis()

feedback = QgsProcessingFeedback()

Processing.initialize()
QgsApplication.processingRegistry().addProvider(qgis.analysis.QgsNativeAlgorithms())
```