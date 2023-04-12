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

LOSCAR keeps track the concentrations of various biogeochemical tracers (including total carbon-TC, total alkalinity-TA, stable carbon isotopes-13C, and others) in different boxes. These tracers compose the state variables ($\overrightarrow{y_i}$) of the model and their dynamic changes over time are governed by the following first-order ordinary equation system (Zeebe, 2012):

$\frac{d\overrightarrow{y_i}}{dt} = F(t, \overrightarrow{y_i})$,   (Eq. 1)

where $t$ is time, and F is a konwn function to calculate the derivatives of $\overrightarrow{y_i}$. The dimension of $\overrightarrow{y_i}$ is 140 (modern setup) or 184 (palaeo setup). Note that model parameters required for derivative calculation except the state variables are implicitly included in the function F. For the convenience of introducing the inverse algorithm, we rewrite Eq. 1 as:
$\frac{d\overrightarrow{y_i}}{dt} = f(\overrightarrow{y_i}, \lambda, \theta (t)$, (Eq. 2)

where $\lambda$ represents the assembly of time-invariant parameters and $\theta$ for the time-dependent parameters. $\lambda$ can be subdivided into three categories: i. the model architecture settings (e.g., ocean volume and areas, oceanic Mg and Ca concentrations, the area percentage of each sediment layer, the thermohaline intensity et al.,); ii. initial fluxes and correponding isotopic values (e.g, the initial silicate and weathering fluxes, the initial primary productivity in the high box, et al.,); iii. to describe the dynamic evolution of each flux (e.g., the calcite dissolution constant, silicate and carbonate weathering exponent, air-sea CO2 exchange coefficient, biopump efficiency, rain ratio et al.,). In most LOSCAR applications, the flux from possilbe carbon input sources is the only item in $\theta$.

According to Eq.2, we can define two main glasses main classes of problems in the carbon cycle study: forward solution and parameter estimation inversely from  the data. The first type of models solve the temporal evolution of $y_i$ with $f, \lambda, \theta$ are known and $y(t=0)$ is given, while the latter type starts from available $y_i$ records (e.g., proxy-derived pH, pCO2 records) and aims to find out parameters $lambda and theta$ that best describe the observed data. Usually only several parameters of key interest in $lambda and theta$ will be inversely constrained. 

In iLOSCAR, the forward model allows user to tune parameters of interest and runs experiments in the same way as in LOSCAR. The inverse model draws the emission trajectory constrained by the proxy records data in a single run. In both models, users can tune the model parameters and run experiments from a web-based interface interactively instead of diving into the complex code files. 

### Forward model


## Parameter explaination
### Mode control.  
 1. Forward vs Inverse
 
