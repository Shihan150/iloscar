# iloscar
 A web-based interactive carbon cycle model, built upon the classic LOSCAR model. Forward and inverse mode incorporated.

## Install it from PyPI

```bash
pip install iloscar
```

## Usage

```py
from iloscar import iloscar_run

iloscar_run()

```
Open [http://127.0.0.1:7777/](http://127.0.0.1:7777/) to run the model. 

## Model description
The overall framework of iLOSCAR is built upon the LOSCAR (*Long-term Ocean-atmosphere Sediment CArbon cycle Reservoir*). LOSCAR is a carbon cycle box model that can operate on both short-term (centuries) and long-term (millions of years) time scales, efficiently computing the partitioning of carbon between various model components (ocean, atmosphere, and sediments). The thorough description of the equations and corresponding processes in the model is given in [***Zeebe (2012)***](https://gmd.copernicus.org/articles/5/149/2012/). Here I will briefly introduce the original forward model from the mathematic perspective, and the algorithm for the inverse model.

The ocean component in LOSCAR is composed of three (four in the palaeo version) ocean reservoirs (Atlantic, Indian, Pacific, and Tethys in the palaeo set-up). Each of the basins is further subdivided into three depth boxes (surface, intermediate, and deep) and there is one gereric box representing the high latitude ocean. The ocean part is coupled with a genuine sediment model, which contains 13 layers of diffenrent depths and calculates %CaCO3 in each layer.

LOSCAR keeps track the concentrations of various biogeochemical tracers (including total carbon-TC, total alkalinity-TA, stable carbon isotopes-13C, and others) in different boxes. These tracers compose the state variables ($\overrightarrow{\y_i}$) of the model and their dynamic changes over time are governed by the following first-order ordinary equation system (Zeebe, 2012):
<div align="center">
$\frac{d\overrightarrow{y_i}}{dt}$
</div>

## Parameter explaination
### Mode control.  
 1. Forward vs Inverse
 
