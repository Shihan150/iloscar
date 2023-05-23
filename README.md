# iloscar
 A web-based interactive carbon cycle model, built upon the classic LOSCAR model. Forward and inverse mode included.  
 
 Author  
 Shihan Li | Department of Oceanography, Texas A&M University, College Station, Texas, 77843, USA
 
 Contributors  
 Dr. Richard E. Zeebe | Department of Oceanography, University of Hawaii, Manoa Honolulu, Hawaii, 96822, USA  
 Dr. Shuang Zhang | Department of Oceanography, Texas A&M University, College Station, Texas, 77843, USA  
 
 For any questions, please contact shihan@tamu.edu

## Install  
To avoid the potential inconvenience caused by the Python package inconsistency, we highly recommend downloading the code directly from [https://github.com/Shihan150/iloscar](https://github.com/Shihan150/iloscar) and setting up an Anaconda virtual environment to run iLOSCAR. 

![image](https://github.com/Shihan150/iloscar/assets/57557675/76247891-d631-47bf-82b5-abe3bf14ff92)
<br>

### 0. Anaconda install  
Please refer to the [Anaconda_install.md](https://github.com/Shihan150/iloscar/blob/main/Anaconda_install.md) file for detailed instructions on installing Anaconda. If you already have Anaconda installed, you can proceed to the next step.

### 1. Create a virtual environment and run the model

#### Mac system
1. Open the Terminal and go to the iloscar main directory downloaed in the previous step. One example is shown below and you need to specify your own path.

<img width="478" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/8359350e-6ebc-4d94-9455-4e31128eefeb">
<br>

2. Type ***conda env create -f iloscar_mac.yml*** to install the iloscar environment. It may take ~1 min.

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



#### Windows 10
1. Open the start menu and look for **Anaconda Prompt**. 
<img width="960" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/e5742f3d-11a9-4dff-872e-69620e491d64">


2. Go to the iloscar main directory downloaed in the previous step. One example is shown below and you need to specify your own path.

3. Type ***conda env create -f iloscar_mac.yml*** to install the iloscar environment. It may take ~1-2 mins.
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
For the details of iLOSCAR, including model structure and derivation of equations, please refer to our paper (in preparation).

### Smoothing function
A LOWESS smoothing function is provided. Users are allowed to upload data files and tune the hyperparamter that controls the windown fraction used in LOWESS manually. Note that the default temporal resolution for output data is 0.2 kyr. For a full description of smoothing algorithm, refer to [https://www.statsmodels.org/dev/generated/statsmodels.nonparametric.smoothers_lowess.lowess.html](https://www.statsmodels.org/dev/generated/statsmodels.nonparametric.smoothers_lowess.lowess.html). 

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
        
        

## External file requirement
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
(Required data files could be downloaded [here](https://github.com/Shihan150/iloscar/tree/main/dat).)
For all tables, the first column can be adjusted manually.

### 1. Forward model
The general workflow follows: 
    1. choose the version control information in Table 1; 
    2. Tune relevant parameters in Table 2 and turn off the carbon emission in Table 3; 
    3. Change the t0 and tfinal in Table 3 and spin up the model for 2 Ma. Check if the steady state is achieved;
    4. using the final steady state from last step as y0 and turn on the carbon emission. Run the model.
    
Here one example is given to help users practice how to run the iLOSCAR forwardly.

#### 1.1 Origninal PETM example from [Zeebe et al., 2009](https://www.nature.com/articles/ngeo578). 

Note that the prolonged carbon leak after the major emission and the inferred reverse circulation are not incorporated here. 

##### Tune the steady state
Note that the initial y0 for the default parameter settings are given in our package (**preind_steady.dat** and **petm_steady.dat**), which can be used directly. Thus, if users want to run the default model, they can skip this part directly.

    1. Go to the Forward page   
![image](https://github.com/Shihan150/iloscar/assets/57557675/1a9ea74e-718d-482b-984e-ad074916be60)



    2. Turn the PALEO to '1', LOADFLAG to '0', and Save ystart to '1'.
    Save ystart decides if the model will export the y values at t=tfinal. 
    The export file name can be manually specified in Table 4. Here we use the 'petm_steady.dat'.
    Then the model parameters in Table 2 will adjust automatically to the palaeo settings.
    
 ![image](https://github.com/Shihan150/iloscar/assets/57557675/fb654bff-d91a-4b0f-a294-1788638cd85e)
    
   
    3. Turn off the carbon emission by changing 'emission pattern' to 0 in Table 3.
    
![image](https://github.com/Shihan150/iloscar/assets/57557675/00f621d3-d1fc-435f-bc3d-b396a66d16c7)


    4. Change tfinal to 2e7 in Table 2.
![image](https://github.com/Shihan150/iloscar/assets/57557675/362a0071-4355-4f7d-a917-fba1570f967a)


    
    5. Give a name to your experiment and run it. I name it as Zeebe2009 here.
![image](https://github.com/Shihan150/iloscar/assets/57557675/1171abab-39c3-4999-9415-fa96c20f1fcb)

    6. The running information will be given in the following chunck. 
<img width="926" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/b32fb30d-6b34-4eeb-8a72-3d5d6c8fc83b">

    7. When integration finished, the final steady state will be saved to the file specified in Table 4 ('petm_steady.dat' here).
    The export file can be used for perturbation experiments later.
<img width="794" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/dba35d27-b377-4943-8c7c-05f95377fbb3">

##### Perturbation experiment
    1. Stay in the same page. In table 1, set LOADFALG  to '1' and Save ystart to '0'.
![image](https://github.com/Shihan150/iloscar/assets/57557675/0481554b-a6db-49e8-8162-25faa08cbe83)

    2. In table 2, change tfinal to 2e5.
 ![image](https://github.com/Shihan150/iloscar/assets/57557675/d08149a5-d8c1-47db-ac80-42b0db5e3e00)
    
    3. Select the carbon emission scenario in Table 3. In this example, set:
    'emission pattern' == 1, 'emission amount' == 3000, 
    'd13c emission' == -55, 'emission start' == 0, 
    'emission duration' == 6000.
    
![image](https://github.com/Shihan150/iloscar/assets/57557675/ca30ed7c-a9f4-4c4f-a9a7-1af2471b9100)


    
    4. Run the model. 
Users can click the 'Clean the output' button, then the experiment information from the previous run will be cleared. But it is only optional and users can run the next experiment directly.

![image](https://github.com/Shihan150/iloscar/assets/57557675/96f94b67-62ed-4d99-8ddf-2c3f33178344)


    6. When integration finished, modeling results are saved to exp_name folder (Zeebe2009 here). 
    The folder will be in the same dictionary where you run your python code. 
    Modeling mean surface DIC, ALK, pH and d13c, pCO2, and CCD for each ocean basin will be displayed when integration succeeds. 

![image](https://github.com/Shihan150/iloscar/assets/57557675/3bf77e45-77af-4c92-9fa2-e375fc50ec24)


### 2. Inverse model

2.1 Inverse twin experiment 

To test the performance of inverse algorithm, an identical twin test is performed. In identical twin testing, a preliminary run of the forward model is used to generate a synthetic 'truth' data set which can subsequently be used in inversion experiments. It is straightfoward to check whether the inverse algorithm works correctly. 

1. Preliminary run
    * In Forward page, follow all the default settings in Table 1 and 2, except turn tfinal to 2e4.
    * Set 'emission pattern' as 3 in Step 3 and input 'pulse_emi.dat' in second row of Table 4. Note that relative path is required for the file name. 
    * 'puluse_emi.dat'  two emission events: fast and short (3000 Gt in 3 kyr) vs slow and long (10000 Gt in 35 kyr), thus serving an excellent example to check the inversion algorithm.
    * Name the model and run the experiment. 
    
    ![image](https://user-images.githubusercontent.com/57557675/232114536-3d65cadb-fcea-45e9-9e52-c1cbb66c1bae.png)

2. Prepare data for inversion
    * At twin_exp folder, select the pCO2 results from pCO2_d13c.csv file and save as twin_pco2_for_inv.csv. Note that the modeling results are of high temporal resolution and we take a slice to keep the inversion time reasonable.
    * Repeat the process for mean surface pH and surface d13C result.

3. Inverse experiment (457.08s used)
    * Navigate to the Inverse page. Select 'pCO2 + mean surface d13c' from the dropdown menu and input the target file names manually.
    
   ![image](https://user-images.githubusercontent.com/57557675/232131733-cedd0fb3-1246-43af-9c88-cb344e4517e0.png)
    * Name the experiment and run the model.
    * (If you meet an error similar to the following figure, which means some degassing rate is larger than the default higher boundary in Table 3. Try to adjust the values of second and third row in Table 3.)
    
    ![image](https://user-images.githubusercontent.com/57557675/232137441-c1a4c47b-5420-46a0-a88f-2f6841de7991.png)
    
    * Succeed! Note that when fcinp(t) = 0, inversed d13c may experience some fluctuation.
![image](https://user-images.githubusercontent.com/57557675/232155210-c4b169b7-e0ba-49dd-a5e6-d061ef85e2b1.png)

 
  

### 2. Example

2.1 [Gutjahr et al., 2017](https://www.nature.com/articles/nature23646#Tab1)

1. Derive the steady state y0

    * Navigate to the Forward page.
    * In Table 1, set PALEO == 1, LOADFLAG == 0, Save ystart == 1
    * In Table 2, set tfinal == 1e7, pCO2_ref == 834, pCO2_initial == 834, silicate weathering0 = 7.5, carbonate weathering0 = 17.5, d13c volcanic == -1.5
    * In Table 4, input './gutjahr2017.dat' into the third row.
    * Name the experiment and run the model.
        
2. Inversion experiment (878s)
    * Navigate to the Inverse page.
    * Download the 'Gutjahr_pH.csv' and 'Gutjahr_d13c.csv' from the [link](https://github.com/Shihan150/iloscar/tree/main/dat).
    * In Table 1, set PALEO == 1, LOADFLAG == 1
    * In Table 2, set pCO2_ref == 834, pCO2_initial == 834, silicate weathering0 = 7.5, carbonate weathering0 = 17.5, d13c volcanic == -1.5
    * In Table 4, input './gutjahr2017.dat'
    * Name the experiment and run the model
    * Succeed! 
  
        
        
3. Data interpretation
    * Refer to [TBD]

2.2 [Wu et al., 2023](https://www.science.org/doi/full/10.1126/sciadv.abq4082)

1. Derive the steady state y0

    * Navigate to the Forward page.
    * In Table 1, set PALEO == 0, LOADFLAG == 0, Save ystart == 1
    * In Table 2, set tfinal == 1e7, pCO2_ref == 425, pCO2_initial == 449, , fsh == 5, silicate weathering0 = 12, carbonate weathering0 = 17, d13c volcanic == -1.3, ca concentration == 0.013, mg concentration == 0.042
    * In Table 4, input './wu2023.dat' into the third row.
    * Name the experiment and run the model.
        
2. Inversion experiment (s)
    * Navigate to the Inverse page.
    * Download the 'wu_pco2.csv' and 'wu_d13c.csv' from the [link](https://github.com/Shihan150/iloscar/tree/main/dat).
    * In Table 1, set PALEO == 0, LOADFLAG == 1
    * In Table 2, set  pCO2_ref == 425, pCO2_initial == 449, fsh == 5, silicate weathering0 = 12, carbonate weathering0 = 17, d13c volcanic == -1.3, ca concentration == 0.013, mg concentration == 0.042, nsi == 0.4, ncc == 0.4
    * In table 3, set lower and higher boundary as [-0.1, 1], which will accelerate the model
    * In Table 4, input './wu2023.dat'
    * Name the experiment and run the model
    * Succeed! 
  ![image](https://user-images.githubusercontent.com/57557675/232583038-0837c29a-9568-4e22-8159-f001b92a6341.png)


## Common bugs
1. The age of target records must be in year unit.

        
        
