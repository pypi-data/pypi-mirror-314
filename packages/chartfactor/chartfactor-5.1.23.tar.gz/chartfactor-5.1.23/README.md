# ChartFactor for Python

[ChartFactor Py](https://chartfactor.com/doc/latest/cfpy_overview/) is built on top of [ChartFactor](https://chartfactor.com), the lightweight visual analytics platform. It includes [ChartFactor Studio](https://chartfactor.com/doc/latest/studio_intro/) and the [ChartFactor Toolkit](https://chartfactor.com/doc/latest/architecture/) between other components.

# Installing Chartfactor Py

Visit the [installation section](https://chartfactor.com/doc/latest/cfpy_installing/) in the ChartFactor Py documentation for a detailed guide.

# Usage

Create a new notebook and do the following

#### Cell 1

```python
from chartfactor import *
import pandas as pd
```

#### Cell 2

```python
titanic = pd.read_csv('https://chartfactor.com/resources/tutorials/titanic.csv')
```

#### Cell 3

```python
cf.studio("My titanic app")
```

#### The output will display an empty Studio app, select the dataframe in the Data Sources window
![image](https://chartfactor.com/resources/images/chartfactor-py/studio-empty.png)

#### Then, add some widgets like Raw Data Table, Bars, Tree Map, etc...
![image](https://chartfactor.com/resources/images/chartfactor-py/studio-widgets.png)
