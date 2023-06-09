# iLOSCAR
A web-based interactive carbon cycle model, built upon the classic LOSCAR model. Forward and inverse mode included.  
 
 Author  
 Shihan Li | Department of Oceanography, Texas A&M University, College Station, Texas, 77843, USA
 
 Contributors  
 Dr. Richard E. Zeebe | Department of Oceanography, University of Hawaii, Manoa Honolulu, Hawaii, 96822, USA  
 Dr. Shuang Zhang | Department of Oceanography, Texas A&M University, College Station, Texas, 77843, USA  
 
 For any questions, please contact shihan@tamu.edu
 
---
- [Install](#install)
  * [0. Anaconda install](#0-anaconda-install)
  * [1. Create a virtual environment and run the model](#1-create-a-virtual-environment-and-run-the-model)
- [Model description](#model-description)
  * [Smoothing function](#smoothing-function)
  * [Output files](#output-files)
  * [External file requirement](#external-file-requirement)
- [Example](#example)
  * [1. Forward model example](#1-forward-model-example)
  * [2. Inverse model example](#2-inverse-model-example)


## Install  


***To successfully install iLOSCAR, please follow the tutorial provided. Note that the 'pip' command installation method is not effective in this case.***

To avoid the potential inconvenience caused by the Python package inconsistency, we highly recommend downloading the code directly from <a href="https://github.com/Shihan150/iloscar" target='_blank'>https://github.com/Shihan150/iloscar</a> and setting up an Anaconda virtual environment to run iLOSCAR. 

![image](https://github.com/Shihan150/iloscar/assets/57557675/76247891-d631-47bf-82b5-abe3bf14ff92)
<br>

### 0. Anaconda install  
Please refer to the [Anaconda_install.md](https://github.com/Shihan150/iloscar/blob/main/Anaconda_install.md) file for detailed instructions on installing Anaconda. If you already have Anaconda installed, you can proceed to the next step.

### 1. Create a virtual environment and run the model

#### Mac system
1. Open the Terminal and go to the iloscar main directory downloaed in the previous step. One example is shown below and you need to specify your own path.

<img width="478" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/8359350e-6ebc-4d94-9455-4e31128eefeb">
<br>

2. Type ***conda env create -f iloscar_mac.yml*** to install the iloscar environment. It may take ~1 - 5 min.

<img width="460" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/98e28f3a-121b-4b64-949b-e01100a64981">
<br>

3. Type ***conda activate iloscar***

<img width="434" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/e38d5d20-9da2-4889-88da-fdee7b4c940a">
<br>

4. Go to the code file by typing ***cd iloscar*** 

<img width="365" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/424b2eeb-a9aa-4b74-a179-265bd576845e">
<br>

5. Type ***python app.py*** and open [http://127.0.0.1:7777/](http://127.0.0.1:7777/) in your browser to run the model. It may take several to tens of seconds, depending on your machine.

<img width="387" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/eca0100f-7c9e-4fa8-a455-57d8ee86cc6e">
<img width="1844" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/99778982-9208-47d6-a1a9-7da45d5c6747">   
Succeed!

<br>
<br>
<br>

----

#### Windows 10
1. Open the start menu and look for **Anaconda Prompt**. 
<img width="960" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/e5742f3d-11a9-4dff-872e-69620e491d64">


2. Go to the iloscar main directory downloaed in the previous step. One example is shown below and you need to specify your own path.

3. Type ***conda env create -f iloscar_win.yml*** to install the iloscar environment. It may take ~1-2 mins.
![image](https://github.com/Shihan150/iloscar/assets/57557675/4d85dae4-7816-4496-8850-cebf2541a2b7)


4. Type ***conda activate iloscar***
![image](https://github.com/Shihan150/iloscar/assets/57557675/30bf756c-7ef8-4c92-90c5-d3164c91d952)

5. Type ***python app.py*** and open [http://127.0.0.1:7777/](http://127.0.0.1:7777/) in your browser to run the model.
![image](https://github.com/Shihan150/iloscar/assets/57557675/2e28f0cf-8c84-4e21-9ab0-cab5edd5e642)

Succeed!
<br>
<br>
<br>

## Model description
For the details of iLOSCAR, including the relevant processes, the physical meanings of parameters, model structure and derivation of equations, please refer to our paper (in preparation) and [Zeebe, 2012, GMD](https://gmd.copernicus.org/articles/5/149/2012/).

### Smoothing function
A LOWESS smoothing function is available within the module. Users have the flexibility to upload data files and manually adjust the hyperparamter that controls the windown fraction used in the LOWESS algorithm. Note that the default temporal resolution for output data is 0.2 kyr. For a comprehensive explanation of the smoothing algorithm, please refer to the following link: [LOWESS Smoothing Algorithm](https://www.statsmodels.org/dev/generated/statsmodels.nonparametric.smoothers_lowess.lowess.html). 

### Output files
In each experiment, the model will output following data files.

| File.csv    | Unit        | Variable         |
| ----------- | ----------- | ---------------- |
| tcb    |  (deg C)  | OCN temperature|
| dic    |   (mmol/kg) | OCN total dissolved inorganic carbon|
|  alk    |  (mmol/kg)| OCN total alkalinity|
|  po4   |    (umol/kg)| OCN phosphate|
|  dox   |    (mol/m3) | OCN dissolved oxygen|
|   dicc  |    (mmol/kg) |OCN DIC-13|
|  d13c   |   (per mil)| OCN delta13C(DIC)|
|  d13ca   |  (per mil) |ATM delta13C(atmosphere)|
|   pco2a_d13c   |  (ppmv, per mil)   | ATM atmospheric pCO2 and d13c|
|    co3      | (umol/kg) |OCN carbonate ion concentration|
|   ph      |  (-)      | OCN pH (total scale)|
|    pco2ocn |  (uatm)   | OCN ocean pCO2|
|    omegaclc | (-)     |  OCN calcite saturation state|
|    omegaarg | (-)     |  OCN aragonite saturation state|
|     fca     |  (-)    |   SED calcite content Atlantic|
|    fci    |   (-)     |  SED calcite content Indian|
|    fcp     |  (-)     |  SED calcite content Pacific|
|    fct     |  (-)     |  SED calcite content Tethys (PALEO only)|
|    ccda   |   (m)     |  SED calcite compens. depth Atlantic|
|    ccdi   |   (m)     |  SED calcite compens. depth Indian|
|    ccdp   |   (m)     |  SED calcite compens. depth Pacific|
|     ccdt    |  (m)     |  SED calcite compens. depth Tethys (PALEO only)|
| Surface_dic_alk_d13c_ph | (-) |  Mean OCN surface DIC, ALK, d13c, and pH|
|        Carbon_inventory |   (mol)   |  Total carbon and alkalinty in the ocean|
        
        

### External file requirement
Some external files are required to run the model.

| Mode      | File usage| Format | Requirement
| ----------- | ----------- | ------- | -------
| Forward    | Initial y0   | .dat | 1 column, 140 (for modern) or 184  rows; <br /> y0 satisfies dy0/dt = F(t=t0, y0) = 0 
|            | Emission file | .dat | When LOADFLAG == 2, two columns (age (yr) + emission mass (Gt/yr)).<br /> When LOADFLAG == 3, three columns (age (yr) + emission mass (Gt/yr)+d13c of input (per mil)).
|            | Save yfinal  | .dat | When Save ystart == 1, y(t=tfinal) will be saved into the according |
| Inverse | pCO2 data for inversion | .csv | 2 column with headline, age (yr) + pCO2 (ppmv)
|          | mean surface pH data for inversion | .csv | 2 column with headline, age (yr) + pH |
|          | mean surface d13c data for inversion | .csv | 2 column with headline, age (yr) + d13c |
| Function | data to be smoothed | .csv | 2 column with headline, age (yr) + data |


## Example
(Example data files could be downloaded [here](https://github.com/Shihan150/iloscar/tree/main/dat).).    

For all tables, the first column can be adjusted manually.

### 1. Forward model example
The general workflow is as follows:   
    1. Select the desired version in Table 1;    
    2. Tune relevant parameters in Table 2 and turn off the carbon emission in Table 3;   
    3. Change the t0 and tfinal in Table 3 and spin up the model for 2 Ma. Check if the steady state is achieved;  
    4. Utilize the final steady state achieved in the previous step as the initial condition (y0). Enable the carbon emissions and run the model.  
    
To assist users in familiarizing themselves with the process of running iLOSCAR in a forward manner, an example is provided.

#### 1.1 Origninal PETM example from [Zeebe et al., 2009](https://www.nature.com/articles/ngeo578). 

Please note that this specific implementation does not include the prolonged carbon release following the main emission event or the inferred reverse circulation described in the original study by Zeebe et al., 2009.

##### Tuning the steady state
Please note that if you intend to run the default model, you can skip this part as the initial y0 values are provided in our package (preind_steady.dat and petm_steady.dat), which can be used directly.

    1. Go to the Forward page   
![image](https://github.com/Shihan150/iloscar/assets/57557675/1a9ea74e-718d-482b-984e-ad074916be60)



    2. Set the PALEO parameter to '1', LOADFLAG to '0', and Save ystart to '1'.
    The model parameters in Table 2 will adjust automatically to the palaeo settings.
    Save ystart determines if the model will export the y values at t=tfinal. 
    The export file name can be manually specified in Table 4. In this example, we use the 'petm_steady.dat'.
    
    
 ![image](https://github.com/Shihan150/iloscar/assets/57557675/fb654bff-d91a-4b0f-a294-1788638cd85e)
    
   
    3. Turn off carbon emissions by changing 'emission pattern' to 0 in Table 3.
    
![image](https://github.com/Shihan150/iloscar/assets/57557675/00f621d3-d1fc-435f-bc3d-b396a66d16c7)


    4. Modify 'tfinal' to '2e7' in Table 2.
![image](https://github.com/Shihan150/iloscar/assets/57557675/362a0071-4355-4f7d-a917-fba1570f967a)


    
    5. Provide a name for your experiment and run it. I name it as Zeebe2009 here.
![image](https://github.com/Shihan150/iloscar/assets/57557675/1171abab-39c3-4999-9415-fa96c20f1fcb)

    6. The running information will be displayed in the following chunck. 
<img width="926" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/b32fb30d-6b34-4eeb-8a72-3d5d6c8fc83b">

    7. Once the integration is complete, the final steady state will be saved to the file specified in Table 4 ('petm_steady.dat' in this case). 
    The exported file can be used as the initial y0 for perturbation experiments later.
<img width="794" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/dba35d27-b377-4943-8c7c-05f95377fbb3">

##### Perturbation experiment
    1. Stay on the same page. In table 1, set LOADFALG  to '1' and Save ystart to '0'.
![image](https://github.com/Shihan150/iloscar/assets/57557675/0481554b-a6db-49e8-8162-25faa08cbe83)

    2. In table 2, change 'tfinal' to '2e5'.
 ![image](https://github.com/Shihan150/iloscar/assets/57557675/d08149a5-d8c1-47db-ac80-42b0db5e3e00)
    
    3. Select the carbon emission scenario in Table 3. In this example, set:
    'emission pattern' == 1, 'emission amount' == 3000, 
    'd13c emission' == -55, 'emission start' == 0, 
    'emission duration' == 6000.
    
![image](https://github.com/Shihan150/iloscar/assets/57557675/ca30ed7c-a9f4-4c4f-a9a7-1af2471b9100)


    
    4. Run the model. 
    Optionally, you can click the 'Clean the output' button to clear the experiment information from the previous run. 
    However, this step is optional, and you can proceed to run the next experiment directly.
![image](https://github.com/Shihan150/iloscar/assets/57557675/96f94b67-62ed-4d99-8ddf-2c3f33178344)


    6. Once the integration is complete, the modeling results will be saved in the exp_name folder (e.g., 'Zeebe2009').
    The folder will be located in the same directory where you ran your Python code. 
    Modeling mean surface DIC, ALK, pH and d13c, pCO2, and CCD for each ocean basin will be displayed when integration succeeds. 

![image](https://github.com/Shihan150/iloscar/assets/57557675/3bf77e45-77af-4c92-9fa2-e375fc50ec24)


### 2. Inverse model example
The general workflow for the inverse model is as follows:  
1. Tune the parameters and obtain the initial steady state y0 using the forward model page.
2. Go to the inverse model page and specify the file names that contain the target records.
3. Adjust the parameters based on the tuning results obtained from the forward model.
4. Run the inverse model.

#### 2.1 Inverse twin experiment 

To evaluate the performance of the inverse algorithm, an identical twin test can be conducted. In this type of test, a preliminary run of the forward model is performed to generate a synthetic 'truth' dataset that can be used for subsequent inversion experiments. This allows for a straightforward assessment of the accuracy of the inverse algorithm.

2.1.1. Preliminary run  

    * In the Forward page, maintain all the default settings in Table 1 and 2, except for setting 'tfinal' to '4e4'.   

    
    * Set the 'emission pattern' to 3 in Table 3, and input 'pulse_emi.dat' in the second row of Table 4. 
    Note that the file name should be provided as a relative path.
    
    * 'puluse_emi.dat' file represents two emission events:  
    a fast and short event (3000 Gt in 3 kyr) and a slow and long event (10000 Gt in 35 kyr).  
     This dataset serves as an excellent example for checking the performance of the inversion algorithm. 
    
    * Provide a name for the experiment and run it.
    
![image](https://user-images.githubusercontent.com/57557675/232114536-3d65cadb-fcea-45e9-9e52-c1cbb66c1bae.png)

2.1.2. Prepare data for inversion   

    * Navigate to the twin_exp folder.
    * Locate the pCO2 results in the pCO2_d13c.csv file.
    * Select the desired pCO2 values and save them as twin_pco2_for_inv.csv. 
    * Keep in mind that the modeling results may have a high temporal resolution, so it is recommended to select a subset of data to ensure reasonable inversion times.
    * Repeat the same process for the mean surface pH and surface d13C results. Select the relevant values and save them accordingly for use in the inversion experiment.
    
2.1.3. Inverse experiment (457.08s used)    

    * Go to the Inverse page.    
    From the dropdown menu, select 'pCO2 + mean surface d13c'.
    Manually input the target file names.
    
![image](https://github.com/Shihan150/iloscar/assets/57557675/abc338e4-00df-4eee-8ef0-35a53e87289d)

    * In Table 3, specify the boundary values for the Toms748 root-finding algorithm. 
    These values represent the expected minimum and maximum degassing rates. 
    The closer the range, the faster the experiment will run, but there is a higher chance of failure. 
    The default values of -0.1 and 2 Gt/yr should be suitable for most applications.
![image](https://github.com/Shihan150/iloscar/assets/57557675/2914c095-10c2-45f0-b20c-6983096e272e)

    
    
    * Provide a name for the experiment and run the model.
    
    * If you need to terminate the ongoing experiment, simply click the 'Cancel' button.
![image](https://github.com/Shihan150/iloscar/assets/57557675/8fda005f-e110-484e-b072-6222f2b9ecfe)

    
    * If you encounter an error similar to the figure below, it means that some degassing rates exceed the default upper boundary in Table 3.
    Adjust the values in the second and third rows of Table 3 accordingly.
    
![image](https://user-images.githubusercontent.com/57557675/232137441-c1a4c47b-5420-46a0-a88f-2f6841de7991.png)
    
    * Once the inverse experiment is successful, the results will be displayed.
![image](https://github.com/Shihan150/iloscar/assets/57557675/db0604e2-b4c4-4d76-a4e9-68c93fa41cb8)

 
 

#### 2.2 PETM experiment after [Gutjahr et al., 2017](https://www.nature.com/articles/nature23646#Tab1)

1. Derive the steady state y0

    * Go to the Forward page.
    * In Table 1, set PALEO == 1, LOADFLAG == 0, Save ystart == 1
    * In Table 2, set tfinal == 1e7, pCO2_ref == 834, pCO2_initial == 834, silicate weathering0 = 7.5, carbonate weathering0 = 17.5, d13c volcanic == -1.5
    * In Table 4, input './gutjahr2017.dat' in the third row.
    * Provide a name for the experiment and run the model.
        
2. Inversion experiment (838s)
    * Go to the Inverse page.
    * Download the 'Gutjahr_pH.csv' and 'Gutjahr_d13c.csv' from the [link](https://github.com/Shihan150/iloscar/tree/main/dat).
    * In Table 1, set PALEO == 1, LOADFLAG == 1
    * In Table 2, set pCO2_ref == 834, pCO2_initial == 834, silicate weathering0 = 7.5, carbonate weathering0 = 17.5, d13c volcanic == -1.5
    * In Table 4, input './gutjahr2017.dat'
    * Provide a name for the experiment and run the model.
    * Succeed! 

<img width="836" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/2c7bd82d-a6c3-481f-8ae5-dc0ec13aa7f7">

  
        
#### 2.3 PTB experiment after [Wu et al., 2023](https://www.science.org/doi/full/10.1126/sciadv.abq4082)

1. Derive the steady state y0

    * Go to the Forward page.
    * In Table 1, set PALEO == 0, LOADFLAG == 0, Save ystart == 1
    * In Table 2, set tfinal == 1e7, pCO2_ref == 425, pCO2_initial == 449, , fsh == 5, silicate weathering0 = 12, carbonate weathering0 = 17, d13c volcanic == -1.3, ca concentration == 0.013, mg concentration == 0.042
    * In Table 4, input './wu2023.dat' into the third row.
    * Provide a name for the experiment and run the model.
        
2. Inversion experiment (s)
    * Go to the Inverse page.
    * Download the 'wu_pco2.csv' and 'wu_d13c.csv' from the [link](https://github.com/Shihan150/iloscar/tree/main/dat).
    * In Table 1, set PALEO == 0, LOADFLAG == 1
    * In Table 2, set  pCO2_ref == 425, pCO2_initial == 449, fsh == 5, silicate weathering0 = 12, carbonate weathering0 = 17, d13c volcanic == -1.3, ca concentration == 0.013, mg concentration == 0.042, nsi == 0.4, ncc == 0.4
    * In table 3, set lower and higher boundary as [-0.1, 1], which will accelerate the model
    * In Table 4, input './wu2023.dat'
    * Provide a name for the experiment and run the model.
    * Succeed! 
  ![image](https://user-images.githubusercontent.com/57557675/232583038-0837c29a-9568-4e22-8159-f001b92a6341.png)


## Common bugs
1. The age of target records must be in year unit.

        
        
