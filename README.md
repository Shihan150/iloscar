# iLOSCAR
A web-based interactive carbon cycle model, built upon the classic LOSCAR model. Forward and inverse model are included.  

When using iLOSCAR, cite as: 
  
Zeebe, R.E., 2012. LOSCAR: Long-term ocean-atmosphere-sediment carbon cycle reservoir model v2.0.4. Geoscientific Model Development 5, 149–166.   
Li, S., Zeebe, R. E., & Zhang, S. (2024). iLOSCAR: interactive Long-term Ocean-atmosphere-Sediment CArbon cycle Reservoir model v1.0. Global and Planetary Change, 236, 104413. https://doi.org/10.1016/j.gloplacha.2024.104413.

 
 Author  
 Shihan Li | Department of Oceanography, Texas A&M University, College Station, Texas, 77843, USA
 
 Contributors  
 Dr. Richard E. Zeebe | Department of Oceanography, University of Hawaii, Manoa Honolulu, Hawaii, 96822, USA  
 Dr. Shuang Zhang | Department of Oceanography, Texas A&M University, College Station, Texas, 77843, USA  
 
 For any questions, please contact shihan@tamu.edu
 
---
- [File structure](#File-structure)
- [Install](#install)
  * [0. Anaconda install](#0-anaconda-install)
  * [1. Create a virtual environment and run the model](#1-create-a-virtual-environment-and-run-the-model)
- [Model description](#model-description)
  
  * [Model functions](#Model-functions)
  * [Model structure](#Model-structure)
  * [Numeric algorithms](#Numeric-algorithms)
  * [External input files](#external-input-files)
  * [Output files](#output-files)
- [Example](#example)
  * [1. Forward model example](#1-forward-model-example)
  * [2. Inverse model example](#2-inverse-model-example)
- [Benchmark](#Benchmark)
- [Troubleshooting](#Troubleshooting)

### File structure
```
├── dat
├── iLOSCAR
├── Anaconda_install.md
├── README.md
├── iLOSCAR_tutorial.pdf
├── iloscar_mac.yml
├── iloscar_win.yml
```
The ***dat folder*** contains the data that can be used to replicate the experiments in our GPC paper.

The ***iLOSCAR folder*** contains the main functions of our model, which will be introduced [later in this tutorial](https://github.com/Shihan150/iloscar/blob/main/README.md#Model-structure).

The files ***Anaconda_install.md***, ***README.md***, and ***iLOSCAR_tutorial.pdf*** contain comprehensive tutorials on installing the model, setting up and running experiments, and troubleshooting common issues.

The files ***iloscar_mac.yml*** and ***iloscar_win.yml*** are used to create a virtual environment using Anaconda for running the model.


## Install  


***To successfully install iLOSCAR, please follow the tutorial provided.***

To avoid the potential Python package inconsistency, we highly recommend downloading the code directly from <a href="https://github.com/Shihan150/iloscar" target='_blank'>https://github.com/Shihan150/iloscar</a> (see below) and setting up an Anaconda virtual environment before running iLOSCAR. 

![image](https://github.com/Shihan150/iloscar/assets/57557675/76247891-d631-47bf-82b5-abe3bf14ff92)
<br>

### 0. Anaconda install  
Please refer to the [Anaconda_install.md](https://github.com/Shihan150/iloscar/blob/main/Anaconda_install.md) file for detailed instructions on installing Anaconda. Two options including Anaconda Distribution and Miniconda are provided in the tutorial. If you already have Anaconda installed, you can proceed to the next step.

### 1. Create a virtual environment and run the model

#### Mac system
1. Open the Terminal and go to the iloscar main directory downloaded in the previous step. One example is shown below and you need to specify your own path (the part after "cd"). You can learn more about navigating files and directories [here](https://docs.ycrc.yale.edu/PIL/02-filedir/).

<img width="394" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/3eaeb9bb-acb4-49e9-9b2e-0156c1c04677">

<br>

2. Type ***conda env create -f iloscar_mac.yml*** to install the iloscar environment. It may take ~1 - 5 min.

<img width="479" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/328bf928-994a-4378-b9f3-8cfb30582c3b">
<br>

3. Type ***conda activate iloscar***

<img width="394" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/e41e376c-aa75-4b36-90dd-efd0f102e1df">
<br>

4. Go to the iloscar coding directory by typing ***cd iloscar*** 

<img width="352" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/7968d5b8-f117-475f-b61a-9de921ab9c63">
<br>

5. Type ***python app.py*** and open [http://127.0.0.1:7777/](http://127.0.0.1:7777/) in your browser to run the model. It may take several to tens of seconds, depending on your machine.

<img width="387" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/eca0100f-7c9e-4fa8-a455-57d8ee86cc6e">
<img width="1839" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/d345d9c5-c5ff-4404-bf33-6ab708da7003">

Success!

<br>
<br>
<br>

----

#### Windows 10
1. Open the start menu and look for **Anaconda Prompt**. 
<img width="960" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/e5742f3d-11a9-4dff-872e-69620e491d64">


2. Go to the iloscar main directory downloaded in the previous step. One example is shown below by typing ***cd C:\Users\kaway\iloscar-main***. You need to specify your own path.

3. Type ***conda env create -f iloscar_win.yml*** to install the iloscar environment. It may take ~1-2 mins.
![image](https://github.com/Shihan150/iloscar/assets/57557675/4d85dae4-7816-4496-8850-cebf2541a2b7)


4. Type ***conda activate iloscar***
![image](https://github.com/Shihan150/iloscar/assets/57557675/30bf756c-7ef8-4c92-90c5-d3164c91d952)

5. Type ***python app.py*** and open [http://127.0.0.1:7777/](http://127.0.0.1:7777/) in your browser to run the model. It may take several to tens of seconds, depending on your machine.
![image](https://github.com/Shihan150/iloscar/assets/57557675/2e28f0cf-8c84-4e21-9ab0-cab5edd5e642)

Success!
<br>
<br>
<br>

## Model description
For details iLOSCAR, including the relevant processes, the physical meanings of parameters, model structure, and derivation of equations, please refer to our paper (in review) and [Zeebe, 2012, GMD](https://gmd.copernicus.org/articles/5/149/2012/).

### Model functions 


#### Forward model ####

In the forward mode, a specific emission trajectory is applied as the forcing and the model will return the temporal evolution of various parameters in the global carbon cycle (see Output files section). The core part is to solve the Ordinary Differential Equation (ODE) problem:   

$$ {d\vec y \over dt} = F(t, \vec y)   $$  
 
This is the ODE system that governs the dynamic changes of the model's state variables over time, where t is time, $\vec y$ is the vector containing various biogeochemical tracers, and F is the function used to calculate the derivatives of the state variables $\vec y$.
 
#### Inverse model ####

Five inversion options are provided in the inverse model. The aim of the inverse model is to derive the time-dependent carbon emission scenario ($fcinp{(t)}$) and the isotopic composition of emitted carbon ( $f\delta^{13}C{(t)}$) by minimizing the relative errors between observations and corresponding modeling results:  

$$  fcinp(t), f\delta^{13}C(t) = argmin\sum_{i=1}^n  | {x_{model}(t_i) - x_{obs}(t_i) \over x_{obs}(t_i)} |   $$  



|Option | Input   | Output | 
| ----------- | ----------- | ---------------- |
| pCO2 | pCO2 proxy records | fcinp(t) |
|  d13c | d13c proxy records | fcinp(t), needs to assume a constant d13c for the emission |
| GSpH | Global surface pH records | fcinp(t) |
| pCO2_d13c | pCO2 and mean surface d13C proxy records | fcinp(t) +  fd13C(t)|
| pH_d13c | pH and mean surface d13C proxy records | fcinp(t) +  fd13C(t)|

#### Smoothing function ####

A LOWESS smoothing function is available within the module. Users have the flexibility to upload data files and manually adjust the hyperparameters that control the fraction of the data used when estimating each y-value in LOWESS algorithm. Note that the default temporal resolution for output data is 0.2 kyr. For a comprehensive explanation of the smoothing algorithm, please refer to the following link: [LOWESS Smoothing Algorithm](https://www.statsmodels.org/dev/generated/statsmodels.nonparametric.smoothers_lowess.lowess.html). 


### Model structure
```
iLOSCAR
├── app.py
├── iLOSCAR_backend.py
├── style.py
├── pages
│   ├── home.py
│   ├── forward.py
│   ├── inverse.py
│   ├── Smoothing.py
├── petm_steady.dat
├── preind_steady.dat
```
#### Front-end  ####
The web-based interface in iLOSCAR is developed upon the [Dash](https://dash.plotly.com/) Package, which provides a low-code framework for rapidly building data apps in Python. The app.py is used to activate the model and the interface. The contents of the interface are controlled by the .py files in the 'pages' folder and their format is controlled by the style.py.  
#### Back-end  ####
The iLOSCAR_backen.py contains all the core functions to run the model, including setting up the model parameters and ODE functions, solutions for both forward and inverse models, saving the experiment results, as well as some tool functions such as solving the carbonate system from alkalinity (ALK) and dissolved inorganic carbon (DIC).   
#### Initial y file  ####
Two files (***petm_steady.dat*** and ***preind_steady.dat***) are provided, which are the initial state files from the original LOSCAR default settings.  

For each experiment, users can update parameters from the front-end, which will be transferred to call the backend functions.   

### Numeric algorithms
#### ODE solver for the forward model ####
The LSODA (an acronym for Livermore Solver for Ordinary Differential equations, with Automatic method switching for stiff and nonstiff problems) algorithm is employed as the default ODE solver, given its demonstrated stability when dealing with stiff problems, as highlighted by [Hindmarsh (1992)](https://www.osti.gov/biblio/145724). The algorithm is available in the [Python Scipy Package](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html).  

Users are encouraged to explore the performance of various ODE solvers. For example, the Backward Differentiation Formula (BDF) also exhibits comparable efficiency for stiff problems. To change the solver, users can navigate to Line 53 in the ./iloscar/iLOSCAR_backend.py file and uncomment the desired solver they wish to employ.

#### TOMS 748, a Root-finding algorithm, for the inverse model  ####
To solve the inverse problem, the TOMS 748 root-finding algorithm is applied, which uses a mixture of inverse cubic interpolation and Newton-quadratic steps to enclose zeros of contiguous univariate functions ([Alefeld et al., 1995](https://dl.acm.org/doi/10.1145/210089.210111)). This algorithm offers the advantage of a rapid convergence rate, which significantly accelerates the inversion process. Additionally, Algorithm 748 is readily available in the [Python Scipy package](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.toms748.html). Note that two parameters ($a, b$) need to be given to determine the boundaries of the algorithm search interval, i.e., $f(a)\times f(b) < 0$, where f is the function ${x_{model}(t_i) - x_{obs}(t_i) \over x_{obs}(t_i)}$. In our context, $a, b$ represent the potential minimum and maximum emission rates (in Gt), respectively. When $a$ is negative, it represents the carbon burial rate. Default settings are -0.1 and 2, which should work for most applications. Increasing the absolute value can reduce the failure probability of the experiment but at the expense of running time. Therefore, it's important for users to carefully select these values based on their domain knowledge. Careful consideration in this regard will help optimize the model's performance, ensuring a balance between accuracy and computational efficiency. 

### External input files
Some external files are required to run the model.

| Mode      | File usage| Format | Requirement
| ----------- | ----------- | ------- | -------
| Forward    | Initial y0   | .dat | 1 column, 140 (for modern) or 184  rows (for paleo); <br /> y0 satisfies dy0/dt = F(t=t0, y0) = 0 
|            | Emission file | .dat | When LOADFLAG == 2, two columns (age (yr) + emission mass (Gt/yr)).<br /> When LOADFLAG == 3, three columns (age (yr) + emission mass (Gt/yr)+d13c of input (per mil)).
|            | Save yfinal  | .dat | When auto-spinning the model to the steady state (i.e., 'Save ystart' in the Table == 1), <br /> y(t=tfinal) will be saved into the specified .dat file |
| Inverse | pCO2 data for inversion | .csv | 2 columns with headline, age (yr) + pCO2 (ppmv)
|          | mean surface pH data for inversion | .csv | 2 columns with headline, age (yr) + pH |
|          | mean surface d13c data for inversion | .csv | 2 columns with headline, age (yr) + d13c (per mil) |
| Function | data to be smoothed | .csv | 2 columns with headline, age (yr) + data |

  
### Output files
In each experiment, the model will output the following data files.

| File.csv    | Unit        | Variable         |
| ----------- | ----------- | ---------------- |
| tcb    |  (deg C)  | Ocean (OCN) temperature|
| dic    |   (mmol/kg) | OCN total dissolved inorganic carbon|
|  alk    |  (mmol/kg)| OCN total alkalinity|
|  po4   |    (umol/kg)| OCN phosphate|
|  dox   |    (mol/m3) | OCN dissolved oxygen|
|   dicc  |    (mmol/kg) |OCN DIC-13|
|  d13c   |   (per mil)| OCN delta13C(DIC)|
|   pco2a_d13c   |  (ppmv, per mil)   | Atmospheric pCO2 and d13c|
|    co3      | (umol/kg) |OCN carbonate ion concentration|
|   ph      |  (-)      | OCN pH (total scale)|
|    pco2ocn |  (uatm)   | OCN ocean pCO2|
|    omegaclc | (-)     |  OCN calcite saturation state|
|    omegaarg | (-)     |  OCN aragonite saturation state|
|     fca     | weight %   |   Sediment (SED) calcite content of Atlantic Ocean|
|    fci    |   weight %       |  SED calcite content of Indian Ocean|
|    fcp     |  weight %      |  SED calcite content of Pacific Ocean|
|    fct     |  weight %     |  SED calcite content Tethys (PALEO model version only)|
|    ccda   |   (m)     |  SED calcite compensation depth Atlantic|
|    ccdi   |   (m)     |  SED calcite compensation depth Indian|
|    ccdp   |   (m)     |  SED calcite compensation depth Pacific|
|     ccdt    |  (m)     |  SED calcite compensation depth Tethys (PALEO model version only)|
| Surface_dic_alk_d13c_ph | (mmol/kg, mmol/kg, per mil, -) |  Mean OCN surface DIC, ALK, d13c, and pH|
|        Carbon_inventory |   (mol)   |  Total carbon and alkalinity in the ocean|
        
        


## Example
(Example data files could be downloaded [here](https://github.com/Shihan150/iloscar/tree/main/dat)).    

For all tables, the first column can be adjusted manually.

### 1. Forward model example
The general workflow is as follows:   
    1. Select the desired version in Step 1 table;    
    2. Tune relevant parameters in Step 2 table and turn off the carbon emission in Step 3 table;   
    3. Change the t0 and tfinal in Step 3 table and spin up the model for 2e7 years. Check if the steady state is achieved;  
    4. Utilize the final steady state achieved in the previous step as the initial condition (y0). Enable the carbon emissions in Step 3 table and run the model.  
    
To assist users in becoming familiar withthe process of running iLOSCAR in a forward manner, an example is provided.

#### 1.1 Original PETM example from [Zeebe et al., 2009](https://www.nature.com/articles/ngeo578). 

Please note that this specific implementation does not include the prolonged carbon release following the main emission event or the inferred reverse circulation adopted in the original study by Zeebe et al., 2009.

##### Tuning the steady state
Please note that if you intend to run the default model for the modern and paleo setup, you can skip this part as the initial steady-state y0 values are already provided in our package (preind_steady.dat and petm_steady.dat), which can be used directly.

  1. Go to the Forward page   
![image](https://github.com/Shihan150/iloscar/assets/57557675/2f6984a8-06fc-41cf-a78f-93232b449aee)




  2. In Step 1 table, set the PALEO parameter to '1', LOADFLAG to '0', and Save ystart to '1'.
    The model parameters in Step 2 table will adjust automatically to the palaeo settings.
    Save ystart determines if the model will export the y values at t=tfinal. 
    The export file name can be manually specified in Step 4 table. In this example, we use the 'petm_steady.dat'.
    
    
 ![image](https://github.com/Shihan150/iloscar/assets/57557675/fb654bff-d91a-4b0f-a294-1788638cd85e)
    
   
  3. Turn off carbon emissions by changing the 'emission pattern' to 0 in Step 3 table.
    
![image](https://github.com/Shihan150/iloscar/assets/57557675/00f621d3-d1fc-435f-bc3d-b396a66d16c7)


  4. Modify 'tfinal' to '2e7' in Step 2 table.
![image](https://github.com/Shihan150/iloscar/assets/57557675/362a0071-4355-4f7d-a917-fba1570f967a)


    
  5. Provide a name for your experiment and run it. I name it Zeebe2009 here.
![image](https://github.com/Shihan150/iloscar/assets/57557675/1171abab-39c3-4999-9415-fa96c20f1fcb)

  6. The running information will be displayed in the following chunk. 
<img width="926" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/b32fb30d-6b34-4eeb-8a72-3d5d6c8fc83b">

  7. Once the integration is complete, the final steady state will be saved to the file specified in Step 4 table ('petm_steady.dat' in this case). 
    The exported file can be used as the initial y0 for perturbation experiments later.
<img width="794" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/dba35d27-b377-4943-8c7c-05f95377fbb3">

##### Perturbation experiment
The above steps are to set up the initial steady state before a geologic event. Now we will simulate the perturbation driven by the carbon injection. 

  1. Stay on the same page. In Step 1 table, set LOADFALG  to '1' and Save ystart to '0'.
![image](https://github.com/Shihan150/iloscar/assets/57557675/0481554b-a6db-49e8-8162-25faa08cbe83)

  2. In Step 2 table, change 'tfinal' to '2e5'.
 ![image](https://github.com/Shihan150/iloscar/assets/57557675/d08149a5-d8c1-47db-ac80-42b0db5e3e00)
    
  3. Select the carbon emission scenario in Step 3 table. In this example, set:
    'emission pattern' == 1, 'emission amount' == 3000, 
    'd13c emission' == -55, 'emission start' == 0, 
    'emission duration' == 6000.
    
![image](https://github.com/Shihan150/iloscar/assets/57557675/9ab1951a-0752-47eb-88e1-8793ccb0970e)



    
  4. Run the model. 
    Optionally, you can click the 'Clean the output' button to clear the experiment information from the previous run. 
    However, this step is optional, You can directly create a new perturbation scenario with the same initial state and run the next experiment.

![image](https://github.com/Shihan150/iloscar/assets/57557675/96f94b67-62ed-4d99-8ddf-2c3f33178344)


  5. Once the integration is complete, the modeling results will be saved in the exp_name folder (e.g., 'Zeebe2009').
    The folder will be located in the same directory where you ran your Python code. 
    Modeling mean surface DIC, ALK, pH and d13c, pCO2, and CCD for each ocean basin will be displayed when integration succeeds. 

![image](https://github.com/Shihan150/iloscar/assets/57557675/3bf77e45-77af-4c92-9fa2-e375fc50ec24)


### 2. Inverse model example
The general workflow for the inverse model is as follows:  
1. Tune the parameters and obtain the initial steady state y0 using the forward model page.
2. Go to the inverse model page and specify the file names that contain the proxy records.
3. Adjust the parameters based on the tuning results obtained from the forward model.
4. Run the inverse model.

#### 2.1 Inverse twin experiment 

To evaluate the performance of the inverse algorithm, an identical twin test can be conducted. In this type of test, a preliminary run of the forward model is performed to generate a synthetic 'truth' dataset that can be used for subsequent inversion experiments. This allows for a straightforward assessment of the accuracy of the inverse algorithm.

2.1.1. Preliminary run  

* In the Forward page, maintain all the default settings in Step 1 table and 2, except for setting 'tfinal' to '4e4'.   


* Set the 'emission pattern' to 3 in Step 3 table, and input 'pulse_emi.dat' in the second row of Step 4 table. 
Note that the file name should be provided as a relative path.

* 'pulse_emi.dat' file represents two emission events:  
a fast and short event (3000 Gt in 3 kyr) and a slow and long event (10000 Gt in 35 kyr).  
 This dataset serves as an excellent example for checking the performance of the inversion algorithm. 

* Provide a name for the experiment and run it.
    
<img width="1052" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/b2fd9071-bb9f-4a85-b9c9-68946cbf3b57">


2.1.2. Prepare data for inversion   

* Navigate to the twin_exp folder.
* Locate the pCO2 results in the pCO2_d13c.csv file.
* Select the desired pCO2 values and save them as twin_pco2_for_inv.csv. 
* Keep in mind that the forward modeling results may have a high temporal resolution (thus a lot of data points), so it is recommended to select a subset of data to ensure reasonable inversion times.
* Repeat the same process for the mean surface pH and surface d13C results. Select the relevant values and save them accordingly for use in the inversion experiment.
    
2.1.3. Inverse experiment     

* Go to the Inverse page.    
From the dropdown menu, select 'pCO2 + mean surface d13c'.
Manually input the target file names.
    
![image](https://github.com/Shihan150/iloscar/assets/57557675/9fc36a6d-31d7-4f84-a883-85d030800772)


* In Step 3 table, specify the boundary values for the Toms748 root-finding algorithm. 
These values represent the expected minimum and maximum degassing rates. 
The narrower the range, the faster the experiment will run, but there is a higher chance of failure. 
The default values of -0.1 and 2 Gt/yr should be suitable for most applications.
<img width="858" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/a75b26c8-33d2-4b80-890e-202a43095a4f">


    
    
* Provide a name for the experiment and run the model.

* If you need to terminate the ongoing experiment, simply click the 'Cancel' button.
![image](https://github.com/Shihan150/iloscar/assets/57557675/8fda005f-e110-484e-b072-6222f2b9ecfe)

    
* If you encounter an error similar to the figure below, it means that some degassing rates exceed the default upper boundary in Step 3 table.
Adjust the values in the second and third rows of Step 3 table accordingly.
    
![image](https://user-images.githubusercontent.com/57557675/232137441-c1a4c47b-5420-46a0-a88f-2f6841de7991.png)
    
* Once the inverse experiment is successful, the results will be displayed and saved in the exp_name folder (e.g., 'twin_exp' here).
<img width="468" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/d020b780-dae2-44fa-bfaa-3158dbc3a43b">


 
 

#### 2.2 PETM experiment after [Gutjahr et al., 2017](https://www.nature.com/articles/nature23646#Tab1)

1. Derive the steady state y0

* Go to the Forward page.
* In Step 1 table, set PALEO == 1, LOADFLAG == 0, Save ystart == 1
* In Step 2 table, set tfinal == 1e7, pCO2_ref == 834, pCO2_initial == 834, silicate weathering0 = 7.5, carbonate weathering0 = 17.5, d13c volcanic == -1.5
* In Step 4 table, input './gutjahr2017.dat' in the third row.
* Provide a name for the experiment and run the model.
        
2. Inversion experiment
* Go to the Inverse page.
* Download the 'Gutjahr_pH.csv' and 'Gutjahr_d13c.csv' from the [link](https://github.com/Shihan150/iloscar/tree/main/dat).
* In Step 1 table, set PALEO == 1, LOADFLAG == 1
* In Step 2 table, set pCO2_ref == 834, pCO2_initial == 834, silicate weathering0 = 7.5, carbonate weathering0 = 17.5, d13c volcanic == -1.5
* In Step 4 table, input './gutjahr2017.dat'
* Provide a name for the experiment and run the model.
* Success! 

<img width="836" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/2c7bd82d-a6c3-481f-8ae5-dc0ec13aa7f7">

  
        
#### 2.3 PTB experiment after [Wu et al., 2023](https://www.science.org/doi/full/10.1126/sciadv.abq4082)

1. Derive the steady state y0

* Go to the Forward page.
* In Step 1 table, set PALEO == 0, LOADFLAG == 0, Save ystart == 1
* In Step 2 table, set tfinal == 1e7, pCO2_ref == 425, pCO2_initial == 449, , fsh == 5, silicate weathering0 = 12, carbonate weathering0 = 17, d13c volcanic == -1.3, ca concentration == 0.013, mg concentration == 0.042
* In Step 4 table, input './wu2023.dat' into the third row.
* Provide a name for the experiment and run the model.
        
2. Inversion experiment 
* Go to the Inverse page.
* Download the 'wu_pco2.csv' and 'wu_d13c.csv' from the [link](https://github.com/Shihan150/iloscar/tree/main/dat).
* In Step 1 table, set PALEO == 0, LOADFLAG == 1
* In Step 2 table, set  pCO2_ref == 425, pCO2_initial == 449, fsh == 5, silicate weathering0 = 12, carbonate weathering0 = 17, d13c volcanic == -1.3, ca concentration == 0.013, mg concentration == 0.042, nsi == 0.4, ncc == 0.4
* In Step 3 table, set lower and higher boundaries as [-0.1, 1], which will accelerate the model
* In Step 4 table, input './wu2023.dat'
* Provide a name for the experiment and run the model.
* Success! 

<img width="400" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/6dba92a5-f5bf-4c04-a3c3-07060cb546b8">




## Benchmark
We welcome contributions from various operation systems and processors.  
|Experiment  |OS	| Processor  | Time (seconds)| Source|
| ----------- | ----------- | ---------------- | ----------- | ---------------- |
| 1.1 Paleo steady state tuning|Mac | Apple M1 8 cores @3.2 GHz  |  46  | This tutorial|
| 1.1 Paleo steady state tuning|Windows 11 Pro x64 | Intel Core i7-9700 CPU @ 3GHz with 8 cores  |  61  | User|
| 1.1  Paleo perturbation| Mac | Apple M1 8 cores @3.2 GHz  |  10  | This tutorial|
| 1.1 Paelo perturbation|Windows 11 Pro x64 | Intel Core i7-9700 CPU @ 3GHz with 8 cores  |  3  | User|
| 2.2 PETM Gutjahr2017 | Mac | Apple M1 8 cores @3.2 GHz  |  838  | This tutorial|
| 2.2 PETM Gutjahr2017 | Windows 11 Pro x64 | Intel Core i7-9700 CPU @ 3GHz with 8 cores  |  760  | User|
| 2.3 PTB Wu2023 | Mac | Apple M1 8 cores @3.2 GHz  |  816  | This tutorial|



## Troubleshooting

This section provides a summary of common issues that may arise while running the iLOSCAR model. It's important to note that this is not an exhaustive list and may be supplemented with additional information in the future. If the troubleshooting strategies outlined here do not resolve your problems, consider reaching out to shihan@tamu.edu for further assistance and discussion.  

#### No response from the forward model
Normally, a forward experiment should be completed within 2 to 3 minutes, depending on your machine. However,  if the experiment takes an excessively long time without yielding results, it could be due to an inappropriate selection of certain parameters.  This improper parameter choice might cause instability in the model and disrupt the solution process. For instance, altering the 'fsh' parameter to 10 in the default paleo settings can prevent the model from reaching a steady state. In such situations, follow these steps for troubleshooting:


i. Write down the parameter settings used in the current experiment.

ii. Interrupt the ongoing experiment by pressing Ctrl + C in the Terminal window.

iii. Restart the model by entering 'python app.py' in the Terminal window.

iv. Upon restart, the model parameters will revert to their default settings. Instead of applying all the previous parameters at once, adjust them individually. This step-by-step approach should help identify which specific parameter is causing instability.
        
 
#### Inversion algorithm fails to converge
If the inversion algorithm does not converge and you encounter an error message similar to the one shown in the figure below, consider the following steps to resolve the issue:

i. Ensure that the initial modeling proxy values (such as pH, pCO2, d13c) are aligned with the initial proxy records provided. 

ii. Modify the values in the second and third rows of Step 3 table as needed. A reliable approach is to increase the absolute values of these parameters. While this adjustment is generally safe, it is important to note that it may slow down the process. This balance between accuracy and computational efficiency needs to be considered when making adjustments.  
![image](https://user-images.githubusercontent.com/57557675/232137441-c1a4c47b-5420-46a0-a88f-2f6841de7991.png)


        
