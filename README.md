# iloscar
 A web-based interactive carbon cycle model, built upon the classic LOSCAR model. Forward and inverse mode included.  
 
 Author: Shihan Li | Department of Oceanography, Texas A&M University, College Station, Texas, 77843, USA
 
 For any questions, please contact shihan@tamu.edu

## Install  
To avoid the potential inconvenience caused by the Python package inconsistency, we highly recommend downloading the code directly from [https://github.com/Shihan150/iloscar](https://github.com/Shihan150/iloscar) and setting up an Anaconda virtual environment to run iLOSCAR. 

### 0. Anaconda install  
Please refer to the [Anaconda_install.md](https://github.com/Shihan150/iloscar/blob/main/Anaconda_install.md) file for detailed instructions on installing Anaconda. If you already have Anaconda installed, you can proceed to the next step.

### 1. Create a virtual environment and running

#### Mac system
1. Open the Terminal and go to the iloscar main directory downloaed in the previous step. One example is shown below and you need to specify your own path.
<img width="422" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/fe677631-6469-4d00-a53d-8dcef8ba448c">

2. Type ***conda env create -f iloscar_mac.yml*** to install the iloscar environment. It may take ~1 min.
<img width="506" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/e0ed790a-e6b6-4028-a330-6de215db0490">

3. Type ***conda activate iloscar***
<img width="445" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/9a9765d1-4c6f-4398-a147-8d97e28cab7c">

4. Go to the code file by typing ***cd iloscar*** 
<img width="351" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/661d7c95-3d25-451a-b5f3-e703939e5884">

5. Type ***python app.py*** and open [http://127.0.0.1:7777/](http://127.0.0.1:7777/) to run the model.
<img width="414" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/a0c92e81-420b-4e6f-883a-a520ed82cd1a">

#### Windows 10
1. Open the start menu and look for **Anaconda Prompt**. 
<img width="960" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/e5742f3d-11a9-4dff-872e-69620e491d64">
<img width="1844" alt="image" src="https://github.com/Shihan150/iloscar/assets/57557675/99778982-9208-47d6-a1a9-7da45d5c6747">


2. Go to the iloscar main directory downloaed in the previous step. One example is shown below and you need to specify your own path.

3. 

```
## Model description
For the details of iLOSCAR, including model structure and derivation of equations, please refer to our paper (in preparation).

### Smoothing function
A LOWESS smoothing function is provided. Users are allowed to upload data files and tune the hyperparamter that controls the windown fraction used in LOWESS manually. Note that the default temporal resolution for output data is 0.2 kyr. For a full description of smoothing algorithm, refer to [https://www.statsmodels.org/dev/generated/statsmodels.nonparametric.smoothers_lowess.lowess.html](https://www.statsmodels.org/dev/generated/statsmodels.nonparametric.smoothers_lowess.lowess.html). 

### Output files
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
(Required dataset could be downloaded [here](https://github.com/Shihan150/iloscar/tree/main/dat).)

### 1. Benchmark

1.1 Origninal PETM example from [Zeebe et al., 2009](https://www.nature.com/articles/ngeo578).

    1. Go to the Forward page   

![image](https://user-images.githubusercontent.com/57557675/232100195-e47c4d51-dbba-4b5b-a82a-b60cb3870703.png)

    2. Turn the PALEO to '1'. Then the model parameters in Table 2 will adjust automatically to the palaeo settings, so skip the Step 2.

![image](https://user-images.githubusercontent.com/57557675/232095753-3edcd6d7-9a06-49cd-85f8-ecf19c4fca94.png)

    3. Select the carbon emission scenario in Table 3. In this example, set 'emission pattern' == 1, emission amount == 3000, 'd13c emission' == -55, 'emission start' == 0, 'emission duration' == 6000.

![image](https://user-images.githubusercontent.com/57557675/232096837-51e2d08a-5f5c-48c5-b0dd-ac867f97327a.png)

    4. Give a name to your experiment and run it. I name it as Zeebe2009 here.

![image](https://user-images.githubusercontent.com/57557675/232097501-d03a8807-07e3-4e6f-bef9-ca7bb1eb8770.png)

    5. The running information will be given in the following chunck. A progress bar is displayed to track the experiment running. 

![image](https://user-images.githubusercontent.com/57557675/232097903-6d2d0c27-6d90-464b-9359-8d42d0d9bded.png)

    6. When integration finished, modeling results are saved to exp_name folder (Zeebe2009 here). The folder will be in the same dictionary where you run your python code. 44Modeling Mean surface DIC, ALK, pH and d13c, pCO2, and CCD for each ocean basin will be displayed when integration succeeds. 

![image](https://user-images.githubusercontent.com/57557675/232099371-c2bac20e-fd1c-4c16-8acb-88f4de7e7815.png)

1.2 Inverse twin experiment 

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

        
        
