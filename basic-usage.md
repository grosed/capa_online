# CAPA online 

## Installation

To install the **capa_online** package from github using pip

 

```bash
python -m pip install 'git+https://github.com/grosed/capa_online/#egg=capa_online&subdirectory=package'
```

## Basic Usage

### Example 1

#### Generate data 


```python
# create a simple example time series
import numpy as np

np.random.seed(1)
Z = [float(z) for z in list(np.random.normal(3, 5, 2000)) + 
    list(np.random.normal(10, 5, 200)) + # collective anomaly
    list(np.random.normal(3, 5, 1000))]
Z[1100] = 50 # point anomaly

# visualise the data
import matplotlib.pyplot as plt

plt.plot(Z)

```




    [<matplotlib.lines.Line2D at 0x75124f1309a0>]




    
![png](output_6_1.png)
    


#### Determine the underlying distribution using 1000 points for "burn in" period and create a transformer.


```python
from capa_online import *
from statistics import mean,stdev

burn_in = Z[:1000]
transformer = scale(mean(burn_in),stdev(burn_in))

Z = Z[1000:]

plt.plot(Z)
```




    [<matplotlib.lines.Line2D at 0x75124e7234c0>]




    
![png](output_8_1.png)
    


#### Create a cost function with a window size of 500 and calculate penalties


```python
from math import log

cost = capa_normal_mean(500)
beta = 4*log(len(Z))
beta_dash = 3*log(len(Z))
```


```python
import numpy as np
from statistics import mean,stdev
from math import log
```

#### Create a CAPA "scanner" from the cost and the transformer


```python
scanner = compose(capa(cost,beta,beta_dash),transformer)
```

#### Simulate a stream of data using the time series, scan the data using CAPA, and store the change history.


```python
history = list()
for z in Z :
    changes = scanner(z)
    history.append(changes)
```


```python
history[1300]
```




    [(196, 392)]




```python
Y = [transformer(z) for z in Z]
plt.plot(Y)
```




    [<matplotlib.lines.Line2D at 0x75124c992bf0>]




    
![png](output_17_1.png)
    

