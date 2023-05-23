#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: shihan
"""


"""

Author: Shihan Li

Original reference:
   Zeebe, R. E., Zachos, J. C., and Dickens, G. R. Carbon dioxide
   forcing alone insufficient to explain Paleocene-Eocene Thermal
   Maximum warming. Nature Geoscience, doi:10.1038/NGEO578 (2009)

Based on the .c version
"""

import pandas as pd
import numpy as np
from numba import jit
import sys

import dash
from dash import html, dcc
from style import *

import timeit
import plotly.graph_objects as go


from scipy import interpolate
from scipy.optimize import root_scalar, toms748


from scipy.integrate import solve_ivp

from os.path import join, exists
from os import makedirs






def init_start(params):
    # input: front-end user input
    # output: running information to the website

    # retrieve parameters from params
    global exp_name
    exp_name = params['exp_name']

    # table 1

    global FTYS, FSED, LOADFLAG, FSEDCC, RUN_TYPE, tsnsflag, svstart
    FTYS = params['FTYS']
    FSED = params['FSED']
    LOADFLAG = params['LOADFLAG']
    RUN_TYPE = params['RUN_TYPE']   # AUTOMATICALLY Determined BY THE WEBSITE
    tsnsflag = params['tsnsflag']

    if RUN_TYPE == 2:
        global target_type, target_file, target_file2, toms_low, toms_high
        target_type = params['target']
        target_file = params['target_file']
        target_file2 = params['target_file2']
        LOADFLAG = 1
        toms_low = params['toms_low']
        toms_high = params['toms_high']



    try:
        svstart = params['svstart']
    except:
        svstart = 0
    # if LOADFLAG == 1:
    #     svstart = 0

    if FSED:
        FSEDCC = 1
    else:
        FSEDCC = 0

    # table 2
    global t0, tfinal, pref, pcsi, fepl, eph0, rrain, fsh, fvc0, finc0, d13cin, d13cvc, thc0, cac, mgc, sclim, nsi, ncc
    t0 = params['t0']
    tfinal = params['tfinal']
    pref = params['pref']
    pcsi = params['pcsi']
    fepl = params['fepl']
    eph0 = params['eph']
    rrain = params['rrain']
    fsh = params['fsh']
    fsi0 = params['fsi0']*1e12
    finc0 = params['finc0']*1e12

    d13cin = params['d13cin']
    d13cvc = params['d13cvc']
    thc0 = params['thc']
    cac = params['cac']
    mgc = params['mgc']
    sclim = params['sclim']
    nsi = params['nsi']
    ncc = params['ncc']



    # table 3
    global cinpflag
    cinpflag = params['cinpflag']


    global RST
    RST = 0.011

    global rccinp, frccinp
    if cinpflag !=0 :
        global fcinp, frccinp


    if cinpflag == 1:

        cinp = params['cinp']
        dccinp = params['dccinp']
        rccinp = ((dccinp/1e3)+1)*RST
        tcin0 = params['tcin0']
        tcspan = params['tcspan']
        fcinp = interpolate.interp1d([tcin0, tcin0+tcspan],[cinp/tcspan, cinp/tcspan], fill_value=(0,0), bounds_error=False)
        frccinp = interpolate.interp1d([tcin0, tcin0+tcspan],[rccinp, rccinp], fill_value=(0,0), bounds_error=False)

    # table 4
    if LOADFLAG == 1:
        global initfile
        initfile = params['initfile']

    if RUN_TYPE == 2:

        dccinp = params['dccinp']
        rccinp = (dccinp/1e3+1)*RST


    if cinpflag == 2 or cinpflag == 3:
        cinpfile = params['cinpfile']

        try:
            co2_emi = np.loadtxt(cinpfile)
            tems = co2_emi[:,0]
            ems = co2_emi[:,1]

            if cinpflag == 2:
                dccinp = params['dccinp']
                rccinp = (dccinp/1e3+1)*RST
                frccinp = interpolate.interp1d([t0, tfinal],[rccinp, rccinp], fill_value=(0,0), bounds_error=False)
            else:
                dccinp = co2_emi[:,2]
                rccinp = (dccinp/1e3+1)*RST
                frccinp = interpolate.interp1d(tems,rccinp, fill_value=(0,0), bounds_error=False)


            fcinp = interpolate.interp1d(tems, ems, fill_value = (0,0), bounds_error = False)

        except:
            # to be incorporated into the website
            info_start = html.Div(children=[
    html.Div(style = Home_STYLE, children =[
    html.P("Please provide the right file name for the argument emission_file. "),
    html.Br(),
    html.P(["The data in the provided file should be two/three columns in shape without a header line",]),
    ])

])
            return info_start, 'Fail'

    if svstart == 1:
        global svfile
        svfile = params['svfile']



    ### globalize the constants
    load_const()

    """ =========     Silicate Weathering: volc degass   ======="""


    # Note: 5e12 is steady-state degassing @280 uatm,
    # balanced by steady-state Si weathering @280 uatm.
    # change fvc(t) in later

    fvc0 = (fsi0/AOC) * (pcsi/pref)**nsi
    """ ========      CaCO3 in-flux  ========= """

    finc0 = ((finc0) * (pcsi/pref)**ncc)/AOC # mol C /m2/year riverine flux



    # initialize model and y0
    model_initialize()

    # print out the model settings
    wo_params()

    # return initialization infomation to the front-end

    h0 = ''
    if LOADFLAG == 0 and cinpflag != 0:
        h0 = '\n@ Warning: the perturbation simulation does not start from the steady state. \n Please switch the LOADFLAG to 1.'

    if FTYS:
        h1 = "\n@ This is the PALEO setup including Tethys"
    else:
        h1 = "\n@ This is the MODERN setup"

    h2 = []

    if RUN_TYPE == 1:
        if LOADFLAG:
            h2 = "\n@ Loaded initial values are used"
        else:
            h2 = "\n@ Default initial values are used"

    if RUN_TYPE == 1:
        if cinpflag:
            h3 = "\n@ The carbon injection is ON"
        else:
            h3 = "\n@ The carbon injection is OFF"

    elif RUN_TYPE == 2:
        h3 = '\n@ This experiment calculates the carbon emission scenario inversely.'

    h4 = f'\n@ The experiment name      : {exp_name}'
    h5 = "\n@ No. ocean basins         : %d" %NOC
    h6 = "\n@ No. ocean boxes          : %d" %NB
    h7 = "\n@ No. ocean tracers        : %d" % NOCT
    h8 = "\n@ Atmospheric Carbon       : %d" % NCATM
    h9 = "\n@ Atmospheric Carbon-13    : %d" % NCCATM
    h10 = "\n@ No. sediment depth levels: %d" % NSD
    h11 = "\n@ No. sediment C-13 levels : %d" % NSDCC
    h12 = "\n@ No. equations            : %d" % NEQ
    h13 = []
    h14 = []
    if RUN_TYPE == 1:
        h13 = "\n@ Starting integration\n"
        h14 = "[tstart  tfinal]=[%.2e  %.2e]\n" % (t0, tfinal)
    elif RUN_TYPE == 2:
        h13 = "\n@ Starting inversion"

    info_start = html.Div(children=[
    html.Div(children =[
    html.P(h0, style = {'color': '#cc3300'}),
    html.P([h1,h2,h3]),
    html.Br(),
    html.P([h4,h5,h6,h7,h8,h9,h10,h11,h12]),
    html.Br(),
    html.P([h13,h14])
    ])

])
    return info_start, 'Success'


def model_run(set_progress):

    global RUN_TYPE
    if RUN_TYPE == 1:
        start_time = timeit.default_timer()


        hpls = np.ones(NB) * HGUESS

        ysol = solve_ivp(derivs, (t0, tfinal), ystart, args = [set_progress, hpls], method = 'LSODA')

        elapse = timeit.default_timer() - start_time

        h0 = ''
        if svstart:
            yfinal = np.copy(ysol['y'][:,-1])
            yfinal[3*NB:4*NB] *= TSCAL
            np.savetxt(svfile, yfinal)
            h0 = (f'System variables at t={tfinal:.2e} has been saved to ', svfile)


        info = html.Div([
                        html.P('Integration finished.'),
                        html.P(f'{elapse: .2f}s used.'),

                        html.P('Starting to save the modeling results.'),
                        html.P(h0),])


        return info, ysol['y'], ysol['t']

    if RUN_TYPE == 2:
        start_time = timeit.default_timer()
        tracer_type = target_type
        target = pd.read_csv(target_file).dropna().to_numpy()

        global t_target
        t_target = target[:,0]
        tracer_target = target[:,1]

        tracer_eval = np.zeros(len(t_target))

        global f_target, y0
        f_target = interpolate.interp1d(t_target, tracer_target, bounds_error=False, fill_value=(tracer_target[0], tracer_target[-1]))

        global frccinp

        if tracer_type == 'pCO2':

            if cinpflag == 0:


                frccinp = interpolate.interp1d([t_target[0], t_target[-1]],[rccinp, rccinp], fill_value=(0,0), bounds_error=False)


            for i in range(len(t_target)-1):
                if i:
                    y0 = np.loadtxt('inv_ystart.dat')
                    y0[3*NB:4*NB] /= TSCAL
                else:
                    y0 = ystart



                tems = t_target[i:i+2]
                ems = tracer_eval[i]

                n = int((tems[-1]-t_target[0])/(t_target[-1]-t_target[0])*100)
                set_progress((str(n), str(100)))


                if i:
                    init_guess = 2 * tracer_eval[i] - tracer_eval[i-1]
                else:
                    init_guess = tracer_eval[i]

                hpls = np.ones(NB) * HGUESS

                # ems_new = fmin(cost_function, init_guess, args = (tracer_type, hpls, tems, ems), disp = True)
                # ems_new = root_scalar(cost_function, x0 = init_guess, x1 = init_guess+0.01, method = 'secant',
                #                       args = (tracer_type, hpls, tems, ems))
                # ems_new = ems_new.root
                ems_new, results = toms748(cost_function, toms_low , toms_high,
                                        args = (tracer_type, hpls, tems, ems),
                                        xtol = 1e-4, rtol = 1e-8,
                                        full_output = True)

                tracer_eval[i] = ems_new

                # write out the ysol as the initial values for the next loop
                ysol = solve_ivp(derivs, (tems[0], tems[1]), y0, t_eval = [tems[1]],args = [0, hpls],  method = 'LSODA')
                yfinal = ysol['y'][:,-1]
                yfinal[3*NB:4*NB] *= TSCAL
                np.savetxt('inv_ystart.dat', yfinal)

            elapse = timeit.default_timer() - start_time
            print(f'{elapse: .2f}s used.')



            global fcinp
            fcinp = interpolate.interp1d(t_target, tracer_eval, bounds_error=False, fill_value=0, kind = 'zero')




            tt = np.concatenate((t_target, t_target[1:]-1))
            tt = np.sort(tt)
            emi_c = fcinp(tt)

            ts = tt[1:]-tt[0:-1]

            emi_interval = np.concatenate([[0],ts * emi_c[0:-1]])
            #np.concatenate([[0], (emi_c[0:-1]+emi_c[1:])/2 * ts])

            emi_c_cum = np.cumsum(emi_interval)

            emi_scenario = pd.DataFrame(np.vstack([tt, emi_c, emi_c_cum]).T)
            emi_scenario.columns = ['Age', 'Carbon_emission_Gt', 'total_carbon_emission_Gt']
            emi_scenario.to_csv('inverse_emission_from_pco2.csv')



            ysol = solve_ivp(derivs, (t_target[0]-500, t_target[-1]), ystart, args = [0, hpls], method = 'LSODA')

            info = html.Div([
                            html.P(f'{elapse: .2f}s used.'),
                            html.P('The calculated emission scenario has been saved to inverse_emission_from_pco2.csv'),

                            html.P('Starting to save the modeling results.'),
                            ])


            return info, ysol['y'], ysol['t']

        elif tracer_type == 'd13c':

            frccinp = interpolate.interp1d([t_target[0], t_target[-1]],[rccinp, rccinp], fill_value=(0,0), bounds_error=False)






            for i in range(len(t_target)-1):
                if i:
                    y0 = np.loadtxt('inv_ystart.dat')
                    y0[3*NB:4*NB] /= TSCAL
                else:
                    y0 = ystart

                tems = t_target[i:i+2]
                ems = tracer_eval[i]

                n = int((tems[-1]-t_target[0])/(t_target[-1]-t_target[0])*100)
                set_progress((str(n), str(100)))

                if i:
                    init_guess = tracer_eval[i-1]
                else:
                    init_guess = -20

                # if (np.abs(fcinp(tems))<0.005).all():
                #     try:
                #         tracer_eval[i] = tracer_eval[i-1]
                #     except:
                #         tracer_eval[i] = -20
                #
                # else:

                hpls = np.ones(NB) * HGUESS
                # ems_d13c_new = fmin(cost_function, init_guess, args = (tracer_type, hpls, tems, ems_d13c), disp = True)

                # ems_d13c_new = root_scalar(cost_function, x0 = init_guess, x1 = init_guess+10, method = 'secant',
                #              args = (tracer_type, hpls, tems, ems_d13c))
                # ems_d13c_new = ems_d13c_new.root

                ems_new, results = toms748(cost_function, tom_low, toms_high,
                                        args = ('d13c_for_emi', hpls, tems, ems),
                                        xtol = 1e-4, rtol = 1e-8,
                                        full_output = True)


                tracer_eval[i]= ems_new


                # write out hte ysol as the initial values for next loop

                ysol = solve_ivp(derivs, (tems[0], tems[1]), y0, args = [0, hpls], t_eval = [tems[1]], method = 'LSODA')
                yfinal = ysol.y[:,-1]
                yfinal[3*NB:4*NB] *= TSCAL
                np.savetxt('inv_ystart.dat', yfinal)

            elapse = timeit.default_timer() - start_time
            print(f'{elapse: .2f}s used.')

            # tt = np.linspace(t_target[0], t_target[-1]-10, int((t_target[-1]-t_target[0])/100))
            #
            # RUN_TYPE = 3
            #
            # frccinp = interpolate.interp1d(t_target, (tracer_eval/1e3+1)*RST, bounds_error=False, fill_value=((tracer_eval[0]/1e3+1)*RST,0), kind = 'zero')
            #
            # emi_d13c = (frccinp(tt)/RST-1)*1e3
            #
            # emi_d13c_scenario = pd.DataFrame(np.vstack([tt, emi_d13c]).T)
            # emi_d13c_scenario.columns = ['Age', 'd13C_of_carbon_emission']
            # emi_d13c_scenario.to_csv('inverse_emission_d13c_results.csv')


            fcinp = interpolate.interp1d(t_target, tracer_eval, bounds_error=False, fill_value=0, kind = 'zero')

            tt = np.concatenate((t_target, t_target[1:]-1))
            tt = np.sort(tt)

            emi_c = fcinp(tt)

            ts = tt[1:]-tt[0:-1]

            emi_interval = np.concatenate([[0],ts * emi_c[0:-1]])

            emi_c_cum = np.cumsum(emi_interval)

            emi_scenario = pd.DataFrame(np.vstack([tt, emi_c, emi_c_cum]).T)
            emi_scenario.columns = ['Age', 'Carbon_emission_Gt', 'total_carbon_emission_Gt']
            emi_scenario.to_csv('inverse_emission_from_d13c.csv')

            RUN_TYPE = 3

            ysol = solve_ivp(derivs, (t_target[0], t_target[-1]), ystart, args = [0, hpls], method = 'LSODA')

            info = html.Div([
                            html.P(f'{elapse: .2f}s used.'),
                            html.P('The calculated emission scenario has been saved to inverse_emission_from_d13c.csv'),

                            html.P('Starting to save the modeling results.'),
                            ])


            return info, ysol['y'], ysol['t']



        elif tracer_type == 'GSpH':

            if cinpflag == 0:


                frccinp = interpolate.interp1d([t_target[0], t_target[-1]],[rccinp, rccinp], fill_value=(0,0), bounds_error=False)


            for i in range(len(t_target)-1):
                if i:
                    y0 = np.loadtxt('inv_ystart.dat')
                    y0[3*NB:4*NB] /= TSCAL
                else:
                    y0 = ystart



                tems = t_target[i:i+2]
                ems = tracer_eval[i]

                n = int((tems[-1]-t_target[0])/(t_target[-1]-t_target[0])*100)
                set_progress((str(n), str(100)))

                if i:
                    init_guess = 2 * tracer_eval[i] - tracer_eval[i-1]

                else:
                    init_guess = tracer_eval[i]


                hpls = np.ones(NB) * HGUESS

                # ems_new = fmin(cost_function, init_guess, args = (tracer_type, hpls,tems, ems), disp = True)


                # ems_new = root_scalar(cost_function, x0 = init_guess, x1 = init_guess+diff_init_guess, method = 'secant', options ={'disp': True},
                #                      args = (tracer_type, hpls, tems, ems))

                ems_new, results = toms748(cost_function, toms_low, toms_high,
                                        args = (tracer_type, hpls, tems, ems),
                                        xtol = 1e-4, rtol = 1e-8,
                                        full_output = True)




                tracer_eval[i] = ems_new

                # write out the ysol as the initial values for the next loop
                ysol = solve_ivp(derivs, (tems[0], tems[1]), y0, t_eval = [tems[1]],args = [0, hpls],  method = 'LSODA')
                yfinal = ysol['y'][:,-1]
                yfinal[3*NB:4*NB] *= TSCAL
                np.savetxt('inv_ystart.dat', yfinal)

            elapse = timeit.default_timer() - start_time
            print(f'{elapse: .2f}s used.')

            # emi_scenario = np.vstack([t_target, tracer_eval]).T
            # np.savetxt('inverse_emission_from_ph.dat', emi_scenario)


            fcinp = interpolate.interp1d(t_target, tracer_eval, bounds_error=False, fill_value=0, kind = 'zero')
            tt = np.concatenate((t_target, t_target[1:]-1))
            tt = np.sort(tt)

            emi_c = fcinp(tt)

            ts = tt[1:]-tt[0:-1]

            emi_interval = np.concatenate([[0],ts * emi_c[0:-1]])


            emi_c_cum = np.cumsum(emi_interval)

            # emi_c_cum = np.cumsum(emi_c)
            emi_scenario = pd.DataFrame(np.vstack([tt, emi_c, emi_c_cum]).T)
            emi_scenario.columns = ['Age', 'Carbon_emission_Gt', 'total_carbon_emission_Gt']
            emi_scenario.to_csv('inverse_emission_from_ph.csv')


            ysol = solve_ivp(derivs, (t_target[0]-500, t_target[-1]), ystart, args = [0, hpls], method = 'LSODA')

            info = html.Div([
                            html.P(f'{elapse: .2f}s used.'),
                            html.P('The calculated emission scenario has been saved to inverse_emission_from_ph.csv'),

                            html.P('Starting to save the modeling results.'),
                            ])


            return info, ysol['y'], ysol['t']


        elif tracer_type == 'pCO2_d13c':
            if cinpflag == 0:
                frccinp = interpolate.interp1d([t_target[0], t_target[-1]],[rccinp, rccinp], fill_value=(0,0), bounds_error=False)


            for i in range(len(t_target)-1):
                if i:
                    y0 = np.loadtxt('inv_ystart.dat')
                    y0[3*NB:4*NB] /= TSCAL
                else:
                    y0 = ystart



                tems = t_target[i:i+2]
                ems = tracer_eval[i]

                n = int((tems[-1]-t_target[0])/(t_target[-1]-t_target[0])*100)/2
                set_progress((str(n), str(100)))


                if i:
                    init_guess = 2 * tracer_eval[i] - tracer_eval[i-1]
                else:
                    init_guess = tracer_eval[i]

                hpls = np.ones(NB) * HGUESS

                # ems_new = fmin(cost_function, init_guess, args = ('pCO2', hpls, tems, ems), disp = True)
                # ems_new = root_scalar(cost_function, x0 = init_guess, x1 = init_guess+0.01, method = 'secant',
                #                       args = ('pCO2', hpls, tems, ems))
                # ems_new = ems_new.root

                ems_new, results = toms748(cost_function, toms_low, toms_high,
                                        args = ('pCO2', hpls, tems, ems),
                                        xtol = 1e-4, rtol = 1e-8,
                                        full_output = True)


                tracer_eval[i] = ems_new

                # write out the ysol as the initial values for the next loop
                ysol = solve_ivp(derivs, (tems[0], tems[1]), y0, t_eval = [tems[1]],args = [0, hpls],  method = 'LSODA')
                yfinal = ysol['y'][:,-1]
                yfinal[3*NB:4*NB] *= TSCAL
                np.savetxt('inv_ystart.dat', yfinal)



            # emi_scenario = np.vstack([t_target, tracer_eval]).T
            # np.savetxt('inverse_emission_from_pco2.dat', emi_scenario)

            # aa = np.loadtxt('inverse_emission_from_pco2.dat')
            # t_target = aa[:,0]
            # tracer_eval = aa[:,1]
            fcinp = interpolate.interp1d(t_target, tracer_eval, bounds_error=False, fill_value=0, kind = 'zero')


            tt = np.concatenate((t_target, t_target[1:]-1))
            tt = np.sort(tt)

            emi_c = fcinp(tt)

            ts = tt[1:]-tt[0:-1]

            emi_interval = np.concatenate([[0],ts * emi_c[0:-1]])

            emi_c_cum = np.cumsum(emi_interval)
            emi_scenario = pd.DataFrame(np.vstack([tt, emi_c, emi_c_cum]).T)
            emi_scenario.columns = ['Age', 'Carbon_emission_Gt', 'total_carbon_emission_Gt']
            emi_scenario.to_csv('double_inversion_emission.csv')

            # inverse the d13c
            target_d13c = pd.read_csv(target_file2).dropna().to_numpy()

            t_target_d13c = target_d13c[:,0]
            d13c_target = target_d13c[:,1]

            d13c_eval = np.zeros(len(t_target_d13c))

            f_target = interpolate.interp1d(t_target_d13c, d13c_target, bounds_error=False, fill_value=(d13c_target[0],d13c_target[-1]))



            for i in range(len(t_target_d13c)-1):
                if i:
                    y0 = np.loadtxt('inv_ystart.dat')
                    y0[3*NB:4*NB] /= TSCAL
                else:
                    y0 = ystart

                tems_d13c = t_target_d13c[i:i+2]
                ems_d13c = d13c_eval[i]

                n = int((tems_d13c[-1]-t_target_d13c[0])/(t_target_d13c[-1]-t_target_d13c[0])*100)/2 + 50
                set_progress((str(n), str(100)))

                if i:
                    init_guess = d13c_eval[i-1]
                else:
                    init_guess = -20



                if (np.abs(fcinp(tems_d13c))<0.005).all():
                    try:
                        d13c_eval[i] = d13c_eval[i-1]
                    except:
                        d13c_eval[i] = -20


                else:
                    hpls = np.ones(NB) * HGUESS
                    # ems_d13c_new = fmin(cost_function, init_guess, args = ('d13c', hpls, tems_d13c, ems_d13c), disp = True)
                    ems_d13c_new = root_scalar(cost_function, x0 = init_guess, x1 = init_guess+5, method = 'secant',
                                            xtol = 1e-4, rtol = 1e-8,
                                          args = ('d13c', hpls, tems_d13c, ems_d13c))

                    ems_d13c_new = ems_d13c_new.root
                    # if ems_d13c_new > 10:
                    #     ems_d13c_new = 10
                    # elif ems_d13c_new < -60:
                    #     ems_d13c_new = -60


                    d13c_eval[i]= ems_d13c_new


                # write out hte ysol as the initial values for next loop

                ysol = solve_ivp(derivs, (tems_d13c[0], tems_d13c[1]), y0, args = [0, hpls], t_eval = [tems_d13c[1]], method = 'LSODA')
                yfinal = ysol.y[:,-1]
                yfinal[3*NB:4*NB] *= TSCAL
                np.savetxt('inv_ystart.dat', yfinal)

            elapse = timeit.default_timer() - start_time
            print(f'{elapse: .2f}s used.')


            RUN_TYPE = 3
            frccinp = interpolate.interp1d(t_target_d13c, (d13c_eval/1e3+1)*RST, bounds_error=False, fill_value=((d13c_eval[0]/1e3+1)*RST,0), kind = 'zero')
            # emi_d13c_scenario = np.vstack([t_target_d13c, d13c_eval]).T
            # np.savetxt('inverse_emission_d13c_results.dat', emi_d13c_scenario)
            t_end = np.minimum(tt[-1], t_target_d13c[-1])
            t_start = np.minimum(tt[0], t_target_d13c[0])
            tt = np.concatenate((t_target_d13c, t_target_d13c[1:]-1))
            tt = np.sort(tt)
            # np.linspace(t_target_d13c[0], t_target_d13c[-1]-10, int((t_target[-1]-t_target[0])/100))
            emi_d13c = (frccinp(tt)/RST-1)*1e3

            emi_d13c_scenario = pd.DataFrame(np.vstack([tt, emi_d13c]).T)
            emi_d13c_scenario.columns = ['Age', 'd13C_of_carbon_emission']
            emi_d13c_scenario.to_csv('double_inversion_emission_d13c.csv')



            ysol = solve_ivp(derivs, (t_start-500, t_end), ystart, args = [0, hpls], method = 'LSODA')

            info = html.Div([
                            html.P(f'{elapse: .2f}s used.'),
                            html.P('The calculated emission scenario has been saved to double_inversion_emission.csv and double_inversion_emission_d13c.csv'),

                            html.P('Starting to save the modeling results.'),
                            ])


            return info, ysol['y'], ysol['t']

        elif tracer_type == 'pH_d13c':
            if cinpflag == 0:
                frccinp = interpolate.interp1d([t_target[0], t_target[-1]],[rccinp, rccinp], fill_value=(0,0), bounds_error=False)


            for i in range(len(t_target)-1):
                if i:
                    y0 = np.loadtxt('inv_ystart.dat')
                    y0[3*NB:4*NB] /= TSCAL
                else:
                    y0 = ystart



                tems = t_target[i:i+2]
                ems = tracer_eval[i]


                n = int((tems[-1]-t_target[0])/(t_target[-1]-t_target[0])*100)/2
                set_progress((str(n), str(100)))


                if i:
                    init_guess = 2 * tracer_eval[i] - tracer_eval[i-1]
                else:
                    init_guess = tracer_eval[i]

                hpls = np.ones(NB) * HGUESS

                # ems_new = fmin(cost_function, init_guess, args = ('GSpH', hpls, tems, ems), disp = True)
                # ems_new = root_scalar(cost_function, x0 = init_guess, x1 = init_guess+0.01, method = 'secant',
                #                       args = ('GSpH', hpls, tems, ems))
                #
                # ems_new = ems_new.root
                ems_new, results = toms748(cost_function, toms_low, toms_high,
                                        args = ('GSpH', hpls, tems, ems),
                                        xtol = 1e-4, rtol = 1e-8,
                                        full_output = True)


                tracer_eval[i] = ems_new

                # write out the ysol as the initial values for the next loop
                ysol = solve_ivp(derivs, (tems[0], tems[1]), y0, t_eval = [tems[1]],args = [0, hpls],  method = 'LSODA')
                yfinal = ysol['y'][:,-1]
                yfinal[3*NB:4*NB] *= TSCAL
                np.savetxt('inv_ystart.dat', yfinal)



            # emi_scenario = np.vstack([t_target, tracer_eval]).T
            # np.savetxt('inverse_emission_from_pco2.dat', emi_scenario)

            # aa = np.loadtxt('inverse_emission_from_pco2.dat')
            # t_target = aa[:,0]
            # tracer_eval = aa[:,1]
            fcinp = interpolate.interp1d(t_target, tracer_eval, bounds_error=False, fill_value=0, kind = 'zero')


            tt = np.concatenate((t_target, t_target[1:]-1))
            tt = np.sort(tt)

            emi_c = fcinp(tt)

            ts = tt[1:]-tt[0:-1]

            emi_interval = np.concatenate([[0],ts * emi_c[0:-1]])

            emi_c_cum = np.cumsum(emi_interval)

            emi_scenario = pd.DataFrame(np.vstack([tt, emi_c, emi_c_cum]).T)
            emi_scenario.columns = ['Age', 'Carbon_emission_Gt', 'total_carbon_emission_Gt']
            emi_scenario.to_csv('double_inversion_emission_pH.csv')

            # inverse the d13c
            target_d13c = pd.read_csv(target_file2).dropna().to_numpy()

            t_target_d13c = target_d13c[:,0]
            d13c_target = target_d13c[:,1]

            d13c_eval = np.zeros(len(t_target_d13c))




            d13c_eval = np.zeros(len(t_target_d13c))

            f_target = interpolate.interp1d(t_target_d13c, d13c_target, bounds_error=False, fill_value=(d13c_target[0],d13c_target[-1]))



            for i in range(len(t_target_d13c)-1):
                if i:
                    y0 = np.loadtxt('inv_ystart.dat')
                    y0[3*NB:4*NB] /= TSCAL
                else:
                    y0 = ystart

                tems_d13c = t_target_d13c[i:i+2]
                ems_d13c = d13c_eval[i]

                n = int((tems_d13c[-1]-t_target_d13c[0])/(t_target_d13c[-1]-t_target_d13c[0])*100)/2 + 50
                set_progress((str(n), str(100)))



                if i:
                    init_guess = d13c_eval[i-1]
                else:
                    init_guess = -20

                if (np.abs(fcinp(tems_d13c))<0.0001).all():
                    try:
                        d13c_eval[i] = d13c_eval[i-1]
                    except:
                        d13c_eval[i] = -20

                else:


                    hpls = np.ones(NB) * HGUESS
                    # ems_d13c_new = fmin(cost_function, init_guess, args = ('d13c', hpls, tems_d13c, ems_d13c), disp = True)
                    ems_d13c_new = root_scalar(cost_function, x0 = init_guess, x1 = init_guess+5, method = 'secant',
                                          xtol = 1e-4, rtol = 1e-8,
                                          args = ('d13c', hpls, tems_d13c, ems_d13c))


                    ems_d13c_new = ems_d13c_new.root

                    # if ems_d13c_new > 10:
                    #     ems_d13c_new = 10
                    # elif ems_d13c_new < -60:
                    #     ems_d13c_new = -60

                    d13c_eval[i]= ems_d13c_new







                # write out hte ysol as the initial values for next loop

                ysol = solve_ivp(derivs, (tems_d13c[0], tems_d13c[1]), y0, args = [0, hpls], t_eval = [tems_d13c[1]], method = 'LSODA')
                yfinal = ysol.y[:,-1]
                yfinal[3*NB:4*NB] *= TSCAL
                np.savetxt('inv_ystart.dat', yfinal)

            elapse = timeit.default_timer() - start_time
            print(f'{elapse: .2f}s used.')


            RUN_TYPE = 3
            frccinp = interpolate.interp1d(t_target_d13c, (d13c_eval/1e3+1)*RST, bounds_error=False, fill_value=((d13c_eval[0]/1e3+1)*RST,0), kind = 'zero')
            # emi_d13c_scenario = np.vstack([t_target_d13c, d13c_eval]).T
            # np.savetxt('inverse_emission_d13c_results.dat', emi_d13c_scenario)
            t_end = np.minimum(t_target[-1], t_target_d13c[-1])
            t_start = np.minimum(t_target[0], t_target_d13c[0])
            tt = np.concatenate((t_target_d13c, t_target_d13c[1:]-1))
            tt = np.sort(tt)
            # np.linspace(t_target_d13c[0], t_target_d13c[-1]-10, int((t_target[-1]-t_target[0])/100))
            emi_d13c = (frccinp(tt)/RST-1)*1e3

            emi_d13c_scenario = pd.DataFrame(np.vstack([tt, emi_d13c]).T)
            emi_d13c_scenario.columns = ['Age', 'd13C_of_carbon_emission']
            emi_d13c_scenario.to_csv('double_inversion_emission_d13c_pH.csv')



            ysol = solve_ivp(derivs, (t_start-500, t_end), ystart, args = [0, hpls], method = 'LSODA')

            info = html.Div([
                            html.P(f'{elapse: .2f}s used.'),
                            html.P('The calculated emission scenario has been saved to double_inversion_emission_pH.csv and double_inversion_emission_d13c_pH.csv'),

                            html.P('Starting to save the modeling results.'),
                            ])


            return info, ysol['y'], ysol['t']













def cost_function(ems_new, tracer_type, hpls, tems, ems):
    if tracer_type == 'pCO2':
        ems = np.array([ems_new, ems_new])

        global fcinp
        fcinp = interpolate.interp1d([tems[0], tems[1]], [ems[0], ems[1]], bounds_error=False, fill_value=0)

        ysol = solve_ivp(derivs, (tems[0], tems[1]), y0, t_eval = [tems[1]], args = [0, hpls], method = 'LSODA')

        index = NOCT * NB

        tracer_sol = ysol.y[index,:]/PPMTOMMSQ/CNTI

        errors = tracer_sol[-1]-f_target(tems[-1])


        return errors

    if tracer_type == 'd13c_for_emi':
        ems = np.array([ems_new, ems_new])
        fcinp = interpolate.interp1d([tems[0], tems[1]], [ems[0], ems[1]], bounds_error=False, fill_value=0)
        ysol = solve_ivp(derivs, (tems[0], tems[1]), y0, t_eval = [tems[1]], args = [0, hpls], method = 'LSODA')
        dic = ysol.y[0:NB,:]
        dicc = ysol.y[5*NB:6*NB,:] * CNTI*1e3/RHO
        temp = dicc/(dic*1e3/RHO)/RST
        d13c_mol = np.transpose((temp-1)*1e3)
        d13c_surf = np.sum(d13c_mol[:, kkv] * vb[kkv],axis = 1)/np.sum(vb[kkv])

        errors = (d13c_surf-f_target(tems[-1]))/np.abs(f_target(tems[-1]))

        return errors[0]



    if tracer_type == 'd13c':
        global rccinp
        # ems = np.array([(arg[0]/1e3 + 1) *RST, (ems_new[0]/1e3 + 1) * RST])
        rccinp = (ems_new/1e3+1)*RST
        # frccinp = interpolate.interp1d([tems[0], tems[1]], [ems[0], ems[1]], bounds_error=False, fill_value=0, kind = 'zero')

        ysol = solve_ivp(derivs, (tems[0], tems[1]), y0, t_eval = [tems[1]], args = [0, hpls],method = 'LSODA')
        dic = ysol.y[0:NB,:]
        dicc = ysol.y[5*NB:6*NB,:] * CNTI*1e3/RHO
        temp = dicc/(dic*1e3/RHO)/RST
        d13c_mol = np.transpose((temp-1)*1e3)
        d13c_surf = np.sum(d13c_mol[:, kkv] * vb[kkv],axis = 1)/np.sum(vb[kkv])

        errors = (d13c_surf-f_target(tems[-1]))/np.abs(f_target(tems[-1]))


        return errors

    if tracer_type == 'GSpH':

        ems = np.array([ems_new, ems_new])

        fcinp = interpolate.interp1d([tems[0], tems[1]], [ems[0], ems[1]], bounds_error=False, fill_value=0)
        ysol = solve_ivp(derivs, (tems[0], tems[1]), y0, t_eval = [tems[1]], args = [0, hpls], method = 'LSODA')

        t = ysol.t
        ysol = ysol.y


        dic = ysol[0:NB, :]
        alk = ysol[NB:2*NB,:]
        tcb = ysol[3*NB:4*NB]*TSCAL

        salv_cal = salv.reshape(NB,1)*np.ones((1,len(t)))
        prsv_cal = prsv.reshape(NB,1)*np.ones((1,len(t)))
        hgssv = np.ones(NB*len(t))* HGUESS

        co2, pco2, co3, hpls, ph, kh, o2sat = fcsys(dic.flatten()/RHO, alk.flatten()/RHO, hgssv, tcb.flatten(), salv_cal.flatten(), prsv_cal.flatten(), cac, mgc)
        ph = np.array(ph).reshape(NB, len(t))
        surface_ph = np.sum(np.transpose(ph)[:, kkv] * vb[kkv],axis = 1)/np.sum(vb[kkv])


        errors = surface_ph - f_target(tems[-1])

        #/np.abs(f_target(tems[-1])

        return errors[0]







def wo_results(y, t):
    """
        FILE.dat  UNIT     VARIABLE
        -----------------------------------------------------------------
        time       (y)           time
        tcb       (deg C)   OCN temperature
        dic       (mmol/kg) OCN total dissolved inorganic carbon
        alk       (mmol/kg) OCN total alkalinity
        po4       (umol/kg) OCN phosphate
        dox       (mol/m3)  OCN dissolved oxygen
        dicc      (mmol/kg) OCN DIC-13
        d13c      (per mil) OCN delta13C(DIC)
        d13ca     (per mil) ATM delta13C(atmosphere)
        pco2a     (ppmv)    ATM atmospheric pCO2
        co3       (umol/kg) OCN carbonate ion concentration
        ph        (-)       OCN pH (total scale)
        pco2ocn   (uatm)    OCN ocean pCO2
        omegaclc  (-)       OCN calcite saturation state
        omegaarg  (-)       OCN aragonite saturation state
        fca       (-)       SED calcite content Atlantic
        fci       (-)       SED calcite content Indian
        fcp       (-)       SED calcite content Pacific
        fct       (-)       SED calcite content Tethys (PALEO only)
        ccda      (m)       SED calcite compens. depth Atlantic
        ccdi      (m)       SED calcite compens. depth Indian
        ccdp      (m)       SED calcite compens. depth Pacific
        ccdt      (m)       SED calcite compens. depth Tethys (PALEO only)

        surface d13c        OCN surface delta13c(dic)
        Total C   (mol)     Total carbon in the ocean
        Total ALK (mol)     Total alkalinity in the ocean

        ------------------------------------------------------------------
        """

    ysol = np.array(y)

    dir_name = f'./{exp_name}'

    folder = exists(dir_name)
    if not folder:
        makedirs(dir_name)

    # time.dat
    np.savetxt(join(dir_name,"time.dat"), t)

    # dic, alk, po4.dat

    dic = ysol[0:NB,:]

    alk = ysol[NB:2*NB,:]
    po4 = ysol[2*NB:3*NB,:]  # po4 convert to mol/m3


    total_c = np.sum(np.transpose(dic) * vb, axis = 1)
    total_alk = np.sum(np.transpose(alk) * vb, axis = 1)

    surface_dic = np.sum(np.transpose(dic*1e3/RHO)[:, kkv] * vb[kkv],axis = 1)/np.sum(vb[kkv])
    surface_alk = np.sum(np.transpose(alk*1e3/RHO)[:, kkv] * vb[kkv],axis = 1)/np.sum(vb[kkv])

    if FTYS:
        col_name = ['LA', 'LI', 'LP', 'IA', 'II', 'IP', 'DA', 'DI', 'DP', 'H',  'LT', 'IT', 'DT' ]
    else:
        col_name = ['LA', 'LI', 'LP', 'IA', 'II', 'IP', 'DA', 'DI', 'DP', 'H']

    pd_dic = pd.DataFrame(np.transpose(dic*1e3/RHO), index = t)
    pd_dic.columns = col_name
    pd_dic.index.name = 'Age'
    pd_dic.to_csv(join(dir_name, "dic.csv"))

    pd_alk = pd.DataFrame(np.transpose(alk*1e3/RHO), index = t)
    pd_alk.columns = col_name
    pd_alk.index.name = 'Age'
    pd_alk.to_csv(join(dir_name, "alk.csv"))

    pd_po4 = pd.DataFrame(np.transpose(po4*1e3/RHO), index = t)
    pd_po4.columns = col_name
    pd_po4.index.name = 'Age'
    pd_po4.to_csv(join(dir_name, "po4.csv"))


    pd_ocean_inventory = pd.DataFrame({
        'total carbon': total_c,
        'total alkalinity': total_alk
        }, index = t)
    pd_ocean_inventory.index.name = 'Age'
    pd_ocean_inventory.to_csv(join(dir_name, "Carbon_inventory.csv"), float_format = '%.4e')





    # np.savetxt(join(dir_name, "dic.dat"), np.transpose(dic*1e3/RHO), fmt='%18.15f')
    # np.savetxt(join(dir_name, "alk.dat"), np.transpose(alk*1e3/RHO), fmt='%18.15f')
    # np.savetxt(join(dir_name, "po4.dat"), np.transpose(po4*1e3/RHO), fmt='%18.15f')
    # np.savetxt(join(dir_name, "tc_ocn.dat"), total_c, fmt='%18.15f')
    # np.savetxt(join(dir_name, "talk_ocn.dat"), total_alk, fmt='%18.15f')
    # np.savetxt(join(dir_name, "surface_dic.dat"), surface_dic, fmt = '%18.15f')
    # np.savetxt(join(dir_name, "surface_alk.dat"), surface_alk, fmt = '%18.15f')


    # tcb.dat
    if NOCT >= 4:
        tcb = ysol[3*NB:4*NB,:]*TSCAL

        pd_tcb = pd.DataFrame(np.transpose(tcb), index = t)
        pd_tcb.columns = col_name
        pd_tcb.index.name = 'Age'
        pd_tcb.to_csv(join(dir_name, "tcb.csv"))

        # np.savetxt(join(dir_name, "tcb.dat"), np.transpose(tcb), fmt = "%18.15f")

    # dox.dat
    if NOCT >= 5:
        dox = ysol[4*NB:5*NB,:]
        pd_dox = pd.DataFrame(np.transpose(dox), index = t)
        pd_dox.columns = col_name
        pd_dox.index.name = 'Age'
        pd_dox.to_csv(join(dir_name, "dox.csv"))
        # np.savetxt(join(dir_name , "dox.dat"), np.transpose(dox), fmt = "%18.15f")

    if NOCT >= 6:
        dicc = ysol[5*NB:6*NB,:] * CNTI*1e3/RHO   #->mmol/kg
        pd_dicc = pd.DataFrame(np.transpose(dicc), index = t)
        pd_dicc.columns = col_name
        pd_dicc.index.name = 'Age'
        pd_dicc.to_csv(join(dir_name, "dicc.csv"))
        # np.savetxt(join(dir_name , "dicc.dat"), np.transpose(dicc), fmt = "%18.15f")

        temp = dicc/(dic*1e3/RHO)/RST
        pd_d13c = pd.DataFrame(np.transpose((temp-1)*1e3), index = t)
        pd_d13c.columns = col_name
        pd_d13c.index.time = 'Age'
        pd_d13c.to_csv(join(dir_name, "d13c.csv"))

        # np.savetxt(join(dir_name , "d13c.dat"), np.transpose((temp-1)*1e3), fmt='%18.15f')

        d13c_mol = np.transpose((temp-1)*1e3)
        d13c_surf = np.sum(d13c_mol[:, kkv] * vb[kkv],axis = 1)/np.sum(vb[kkv])



        # np.savetxt(join(dir_name , "d13c_surf.dat"), d13c_surf, fmt='%18.15f')



    if NCATM == 1:
        pco2a = ysol[NOCT*NB,:] / PPMTOMMSQ/CNTI  #atmospheric co2, scaling /CNTI
        # np.savetxt(join(dir_name , "pco2a.dat"), pco2a, fmt='%18.15f')

    if NCCATM == 1:
        temp = ysol[NOCT*NB+1]/(pco2a*PPMTOMMSQ)/RST           # not scaled

        pd_atm = pd.DataFrame(
            {'pCO2': pco2a,
             'pCO2_d13c': (temp-1)*1e3
                },
            index = t
            )
        pd_atm.index.name = 'Age'
        pd_atm.to_csv(join(dir_name, "pCO2_d13c.csv"))

        # np.savetxt(join(dir_name , "d13ca.dat"), (temp-1)*1e3, fmt='%18.15f')

    if FSED:
        fcva = ysol[NOATM: NOATM+NSD]
        fcvi = ysol[NOATM+NSD : NOATM+2*NSD]
        fcvp = ysol[NOATM+2*NSD : NOATM + 3*NSD]

        pd_fca = pd.DataFrame(np.transpose(fcva), index =t)
        pd_fca.columns = dsv
        pd_fca.index.name = 'Age'
        pd_fca.to_csv(join(dir_name, 'fca.csv'))

        pd_fci = pd.DataFrame(np.transpose(fcvi), index =t)
        pd_fci.columns = dsv
        pd_fci.index.name = 'Age'
        pd_fci.to_csv(join(dir_name, 'fci.csv'))

        pd_fcp = pd.DataFrame(np.transpose(fcvp), index =t)
        pd_fcp.columns = dsv
        pd_fcp.index.name = 'Age'
        pd_fcp.to_csv(join(dir_name, 'fcp.csv'))

        # np.savetxt(join(dir_name , "fca.dat"), np.transpose(fcva), fmt = "%.15e")
        # np.savetxt(join(dir_name , "fci.dat"), np.transpose(fcvi), fmt = "%.15e")
        # np.savetxt(join(dir_name , "fcp.dat"), np.transpose(fcvp), fmt = "%.15e")

        fcca = ysol[NOATM + (3+KTY)*NSD + 0 * NSD : NOATM + (3+KTY)*NSD + 1 * NSD] * CNTI
        fcci = ysol[NOATM + (3+KTY)*NSD + 1 * NSD : NOATM + (3+KTY)*NSD + 2 * NSD] * CNTI
        fccp = ysol[NOATM + (3+KTY)*NSD + 2 * NSD : NOATM + (3+KTY)*NSD + 3 * NSD] * CNTI

        pd_fcca = pd.DataFrame(np.transpose(fcca), index = t)
        pd_fcca.columns = dsv
        pd_fcca.index.name = 'Age'
        pd_fcca.to_csv(join(dir_name, 'fcca.csv'))

        pd_fcci = pd.DataFrame(np.transpose(fcci), index = t)
        pd_fcci.columns = dsv
        pd_fcci.index.name = 'Age'
        pd_fcci.to_csv(join(dir_name, 'fcci.csv'))

        pd_fccp = pd.DataFrame(np.transpose(fccp), index = t)
        pd_fccp.columns = dsv
        pd_fccp.index.name = 'Age'
        pd_fccp.to_csv(join(dir_name, 'fccp.csv'))

        # np.savetxt(join(dir_name , "fcca.dat"), np.transpose(fcca), fmt = "%.15e")
        # np.savetxt(join(dir_name , "fcci.dat"), np.transpose(fcci), fmt = "%.15e")
        # np.savetxt(join(dir_name , "fccp.dat"), np.transpose(fccp), fmt = "%.15e")

        if FTYS:
            fcvt = ysol[NOATM+3*NSD:NOATM+4*NSD]

            pd_fct = pd.DataFrame(np.transpose(fcvt), index =t)
            pd_fct.columns = dsv
            pd_fct.index.name = 'Age'
            pd_fct.to_csv(join(dir_name, 'fct.csv'))

            # np.savetxt(join(dir_name , "fct.dat"), np.transpose(fcvt), fmt = "%.15e")

            fcct = ysol[NOATM + (3+KTY)*NSD + 3 * NSD : NOATM + (3+KTY)*NSD + 4 * NSD] * CNTI
            pd_fcct = pd.DataFrame(np.transpose(fcct), index = t)
            pd_fcct.columns = dsv
            pd_fcct.index.name = 'Age'
            pd_fcct.to_csv(join(dir_name, 'fcct.csv'))

            # np.savetxt(join(dir_name , "fcct.dat"), np.transpose(fcct), fmt = "%.15e")

    hgssv = np.ones(NB) * HGUESS
    salv0 = salv.reshape(NB,1) * np.ones((1, len(t)))
    prsv0 = prsv.reshape(NB,1) * np.ones((1, len(t)))
    hgssv = np.ones(NB*len(t)) * HGUESS

    co2, pco2, co3, hpls, ph, kh, o2sat = fcsys(dic.flatten()/RHO, alk.flatten()/RHO, hgssv, tcb.flatten(), salv0.flatten(), prsv0.flatten(), cac, mgc)

    kspc = fkspc(tcb.flatten(), salv0.flatten(), prsv0.flatten(), cac, mgc)
    kspa = fkspa(tcb.flatten(), salv0.flatten(), prsv0.flatten(), cac, mgc)

    co3 = np.array(co3*1e6).reshape(NB, len(t))
    ph = np.array(ph).reshape(NB, len(t))
    pco2 = np.array(pco2).reshape(NB, len(t))
    kspc = np.array(kspc).reshape(NB, len(t))
    kspa = np.array(kspa).reshape(NB, len(t))

    surface_ph = np.sum(np.transpose(ph)[:, kkv] * vb[kkv],axis = 1)/np.sum(vb[kkv])

    pd_surface = pd.DataFrame(
        {'surface_dic': surface_dic,
         'surface_alk': surface_alk,
         'surface_d13c': d13c_surf,
         'surface_pH': np.transpose(surface_ph)
            },
        index = t
        )
    pd_surface.index.name = 'Age'
    pd_surface.to_csv(join(dir_name, "Surface_dic_alk_d13c_ph.csv"), float_format = '%.4f')

    pd_co3 = pd.DataFrame(np.transpose(co3), index = t)
    pd_co3.columns = col_name
    pd_co3.index.name = 'Age'
    pd_co3.to_csv(join(dir_name , "co3.csv"))

    pd_ph = pd.DataFrame(np.transpose(ph), index = t)
    pd_ph.columns = col_name
    pd_ph.index.name = 'Age'
    pd_ph.to_csv(join(dir_name , "ph.csv"))

    pd_pco2ocn = pd.DataFrame(np.transpose(pco2), index = t)
    pd_pco2ocn.columns = col_name
    pd_pco2ocn.index.name = 'Age'
    pd_pco2ocn.to_csv(join(dir_name , "pco2ocn.csv"))

    pd_omegaclc = pd.DataFrame(np.transpose(co3/1e6*cac/kspc), index = t)
    pd_omegaclc.columns = col_name
    pd_omegaclc.index.name = 'Age'
    pd_omegaclc.to_csv(join(dir_name , "omegaclc.csv"))

    pd_omegaarg = pd.DataFrame(np.transpose(co3/1e6*cac/kspa), index = t)
    pd_omegaarg.columns = col_name
    pd_omegaarg.index.name = 'Age'
    pd_omegaarg.to_csv(join(dir_name , "omegaarg.csv"))

    # np.savetxt(join(dir_name , "co3.dat"), np.transpose(co3), fmt = "%18.15f")

    # np.savetxt(join(dir_name , "ph.dat"), np.transpose(ph), fmt = "%18.15f")

    # np.savetxt(join(dir_name , "surface_ph.dat"), np.transpose(surface_ph), fmt = "%18.15f")

    # np.savetxt(join(dir_name , "pco2ocn.dat"), np.transpose(pco2), fmt = "%18.15f")

    # np.savetxt(join(dir_name , "omegaclc.dat"), np.transpose(co3/1e6*cac/kspc), fmt = "%18.15f")

    # np.savetxt(join(dir_name , "omegaarg.dat"), np.transpose(co3/1e6*cac/kspa), fmt = "%18.15f")

    # calculate the CCD
    fccd = FCCD
    faca = np.zeros((len(zv), len(t)))
    fica = np.zeros((len(zv), len(t)))
    fpca = np.zeros((len(zv), len(t)))
    if FTYS:
        ftca = np.zeros((len(zv), len(t)))

    for i in range(len(t)):
        fa = interpolate.interp1d(dsv, fcva[:,i],  fill_value="extrapolate")
        faca[:,i] = fa(zv)
        fi = interpolate.interp1d(dsv, fcvi[:,i],  fill_value="extrapolate")
        fica[:,i] = fi(zv)
        fp = interpolate.interp1d(dsv, fcvp[:,i],  fill_value="extrapolate")
        fpca[:,i] = fp(zv)

        if FTYS:

            ft = interpolate.interp1d(dsv, fcvt[:,i],  fill_value="extrapolate")
            ftca[:,i] = ft(zv)


    faca = np.abs(faca-fccd)
    fica = np.abs(fica-fccd)
    fpca = np.abs(fpca-fccd)
    if FTYS:
        ftca = np.abs(ftca-fccd)



    # np.savetxt(join(dir_name , "ccda.dat"), np.argmin(faca, axis = 0), fmt = "%7.2f")
    # np.savetxt(join(dir_name , "ccdi.dat"), np.argmin(fica, axis = 0), fmt = "%7.2f")
    # np.savetxt(join(dir_name , "ccdp.dat"), np.argmin(fpca, axis = 0), fmt = "%7.2f")

    if FTYS:
        pd_ccd = pd.DataFrame(
                {
                    'Atlantic': np.argmin(faca, axis = 0),
                'Indian':np.argmin(fica, axis = 0),
                'Pacific':np.argmin(fpca, axis = 0),
                'Tetheys': np.argmin(ftca, axis = 0)
                },
                index = t
                )

        # np.savetxt(join(dir_name , "ccdt.dat"), np.argmin(ftca, axis = 0), fmt = "%7.2f")
    else:
        pd_ccd = pd.DataFrame(
                {
                    'Atlantic': np.argmin(faca, axis = 0),
                'Indian':np.argmin(fica, axis = 0),
                'Pacific':np.argmin(fpca, axis = 0)
                },
                index = t
                )
    pd_ccd.index.name = 'Age'
    pd_ccd.to_csv(join(dir_name , "ccd.csv"))



    h_surf_ph = html.P()
    h_surf_d13c = html.P()

    # if svstart:
    h_surf_ph = html.P(['The final average surface pH is: ', round(surface_ph[-1],2)])
    h_surf_d13c =  html.P(['The final average surface d13c is: ', round(d13c_surf[-1],2)])
    h_pco2 =  html.P(['The final pCO2 is: ', round(pco2a[-1],2)], 'uatm')

    return html.Div(
        [html.P(f'Modeling results have been saved to {exp_name} folder.'),
         html.P('The experiment succeeds. Congratulations!'),
         h_surf_ph,
         h_surf_d13c,
         h_pco2
         ]
        )




 ### globalize the constants
def load_const():
    # load model constants
    global NEQ, NB, MMTOM, NOCT, TSCAL, CNTI, NCATM, NCCATM, PPMTOMMSQ, NOATM, NSD, NOC, NLS, RHO, RHOS, MOOK, REDPC, REDNC, REDO2C, PMMK, MTOKGCACR, CAM, MGM, AOC, KTY, PMMV, PMM0, KMMOX, ALPKC, MZER, HAV,\
        SALOCN, YTOSEC, HGUESS, VOC, KOC, NSDCC, HIMAX, TKLV, BORT, FCCD

    CNTI = 0.01        # scaling

    if FTYS:
        NOC = 4    # Oceans 4: A,I,P,T
        NB  = 13   # of ocean boxes
        NLS = 4    # of low-lat surf boxes
        KTY = 1    # shift 13C sed index
    else:
        NOC = 3    # Oceans 3: A,I,P
        NB  = 10   # of ocean boxes
        NLS = 3    # of low-lat surf boxes
        KTY = 0    # shift 13C sed index

    KOC = NOC + KTY
    NOCT  = 6      # ocean tracers: dic, alk, po4, tcb, dox, dicc
    NCATM = 1      # C atmosphere 1
    NCCATM = 1     # CC atmosphere 1
    NHS = 1        # high-lat surf boxes
    NTS = NLS + NHS # total surf boxes
    NOATM = NOCT*NB + NCATM + NCCATM  # of equations for ocean and atm

    # sediment
    if FSED:
        NSD = 13   # sed boxes per OCN
    else:
        NSD = 0

    FCCD = 0.1 # caco3 fraction at CCD

    # 13C
    if FSEDCC:
        NSDCC = NSD
    else:
        NSDCC = 0

    # of DEQS
    NEQ = NOCT * NB + NCATM + NCCATM + NOC * NSD + NOC * NSDCC

    # oceans
    VOC = 1.2918235e18   # m3 volume ocean
    AOC = 3.49e14        # m2 area ocean
    HAV = VOC/AOC        # m average depth
    RHO = 1.025e3        # kg/m3 seawater
    RHOS = 2.50e3        # kg/m3 sediment
    SALOCN = 34.72       # psu ocean salinity

    # conversions
    YTOSEC = 3600*24*365 # years to secs
    MMTOM = 1e-3         # mmol to mol
    PPMTOMMSQ = 2.2e15/12/AOC # ppmv to mol/m2
    MTOKGCACR = 100/1e3  # mol C to kg CaCO3


    # biological pump
    REDPC = 1/130        # Redfield P:C
    REDNC = 15/130       # Redfield N:C
    REDO2C = 165/130     # Redfield O2:C


    # co2 chemistry
    TKLV = 273.15        # TC -> TKelvin
    HGUESS = 1e-8        # H+ first guess
    HIMAX = 50           # H+ max iterations
    HCONV = 1e-4         # H+ rel. accuracy
    NCSWRT = 5           # calc csys output vars
    HALK2DIC = 1.6       # high alk/dic ratio
    BORT = 432.5         # 416 DOE94, 432.5 Lee10

    # Ca,Mg
    CAM = 10.3e-3        # mol/kg modern Ca
    MGM = 53.0e-3        # mol/kg modern Mg
    ALPKC = 0.0833       # Slope Mg/Ca on Kspc



    # ocn tEMP CHANGE (X DEG C PER 2*CO2)
    # Temp relax times (y) surf, interm, deep
    global TAUS, TAUI, TAUD
    TAUS = 20
    TAUI = 200
    TAUD = 1000
    # scale temperature to oder 1 (*1/TSCAL)
    TSCAL = 10

    # MM kinetics highlat p04 uptake
    PMMK = 0.1e-3        # mol/m3
    PMM0 = 0.1e-3
    PMMV = 1 + PMM0/PMMK

    # MM kinetics dissovled oxygen
    KMMOX = 1e-3         # mol/m3

    # Carbon-13(dicc,ccatm)
    ALPRSTHA13_CHOICE = 'MOOK' # else: Zhang

    # order of magnitude for comparison
    MZBH = 1e2           # box height
    MZOM = 1.0           # omega
    MZER = 1e-4          # erosion

    # co2 gas exchange reference
    MOOK = 1   # 0:Zhang et al.1995, 1: Mook 1986




def model_initialize():
    global ab, alpcorg, asva, asvi, asvp, cac, dsv, epscorg, fc0a, fc0i, fc0p, fcc0a, fcc0i, fcc0p, fconv, fcsml, fdapi, fkrg, frei, frrf, fsh, \
            gp, gtha, gthi, hb, hsl, jsh, kiv, kkv, klid, kssd, m1, m2, m3, mgc, mhd, mxv, ncc, ncsd, nlid, nsi, nuwd, nz, oi, pcsi, phi0, phi1, phiia, phiii, phiip, prsv, \
                rincc, rkrgcc, rvccc, salv, tcb0, tcb0c, thbra, thbri, thc, tso, tto, vb, ystart, zv

    if FTYS:
        global fsht, asvt, klidt, fc0t, phiit

    if FTYS:
        #area fractions      A    I     P   T
        fanoc = np.array([0.15,0.14,0.52,0.09])


    else:
        fanoc = np.array([0.26,0.18,0.46])


    fdvol = np.array([ 0.16,0.16,0.68])  #deep volume fractions
    fhl = 0.1  # high box area fraction


    # height          L   I     D
    hlid = np.array([100,900,HAV-1000])


    """ =======     Temperature     =========         """
    if FTYS:
        tc3 = np.array([25,16,12])  #AIP
        tct = np.array([18,14,12])  #TETHYS
    else:
        tc3 = np.array([20,10,2])   #AIP, modern


    """ ======   Mixing paratmeters =======       """
    if FTYS:
        mv0 = np.array([3.5,3.5,7.0,3.2,2])*1e6  # low <-> intermediate box
        mhd0 = np.array([4.0,4.0,6,0.7])*1e6     # deep boxes <--> H-box
    else:
        mv0 = np.array([5.5,4.5,6.5]) *1e6
        mhd0 = np.array([3.0,2.0,8.0])*1e6


    """ ======  fraction EHP, remineralized in deep A I P boxes ====="""
    gp0 = np.array([0.3,0.3,0.4])

    if FSED:
        # sediment box depth
        dsv0 = np.array([.1,.6,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6.5])  #(km) depth
        # area fractions A,I,P,T (2*2 deg, Karen Bice)
        if FTYS:
            asva = np.array([1.1407, 10.0216,  8.7160,
                     6.3724,  4.7915,  3.4973,
                     12.2935,10.7438,  8.4983,
                    11.4134, 11.0948, 11.4167, 1e-6])/100
            asvi = np.array([ .2501,  5.5345,  5.5145,
                     8.9550,  4.6283,  6.5361,
                     11.7221, 12.6050, 14.6295,
                     13.8384,  8.0807,  7.7057, 1e-6])/100
            asvp = np.array([ 0.1673,  2.8333,  3.0599,
                     2.5389,  1.4218,  5.0153,
                     9.8023,  14.0117, 10.1975,
                     20.0019, 13.7155, 17.2346, 1e-6])/100
            asvt = np.array([7.0534, 46.5363, 22.4068,
                     7.1501,  2.4261,  3.9946,
                     2.7063,  0.8532,  0.9814,
                     3.0802,  2.3583,  0.4533, 1e-6])/100
        else:
            # Menard & Smith, 1966
            asva  = np.array([7.0297,  5.1729,  1.9106,
                      2.3882,  4.2988,  4.2988,
                      9.6711,  9.6711, 16.2389,
                      16.2389, 11.1712, 11.1712,  0.7388])/100
            asvi  = np.array([3.5710,  2.6844,  1.5907,
                      1.9884,  5.0146,  5.0146,
                      12.6299, 12.6299, 18.3221,
                      18.3221,  8.4957,  8.4957,  1.2407])/100
            asvp  = np.array([1.6358,  2.5901,  1.4484,
                      1.8105,  3.4372,  3.4372,
                      10.9275, 10.9275, 17.5411,
                      17.5411, 13.4784, 13.4784, 1.7468])/100




    if FTYS:
        fconv = 3
        thc = thc0 * 1e6 * YTOSEC  # m3/y Conveyor transport
        tto = 2e6 * YTOSEC   # m3/y Tethys Transport
    else:
        fconv = 1
        thc =thc0 * 1e6 * YTOSEC
        tto = 0

    # PETM: add SO to NPDW
    tso = 0
    # TH branches
    thbra = 0.2 # 0.2 upwelled into intermdt Atl
    thbri = 0.2 # 0.2 upwelled into intermdt Ind
    gtha = 1 - thbra         # export into deep Ind
    gthi = 1 - thbra - thbri # export into deep Pac




    # fcsml, numerics: linear f_calcite drop
    # during dissolution if fc< fcsml. 0.05
    fcsml = 0.05

    # allocate globals
    ystart = np.zeros(NEQ, dtype = 'float64')     # ystart
    vb = np.zeros(NB,dtype = 'float64')           # volume boxes
    ab = np.zeros(NB,dtype = 'float64')           # areas
    hb = np.zeros(NB,dtype = 'float64')           # height boxes
    gp = np.zeros(NB,dtype = 'float64')           # H-frac remineralized in AIP
    tcb0 = np.zeros(NB, dtype = 'float64')        # temperature boxes init
    tcb0c = np.zeros(NB)                          # temperature boxes init cntrl
    salv = np.ones(NB)                            # salinity boxes
    prsv = np.zeros(NB)                           # pressure boxes
    fdapi = np.zeros(3)                                     # # init fdapi. change initial dic, alk, po4, see later initstart()

    """

    AL, IL, PL: 0,1,2
    AI, II, PI: 3,4,5
    AD, ID, PD: 6,7,8
    H: 9
    TL, TI, TD: 10,11,12

    """
    #areas
    ab[0:3] = fanoc[0:3] * AOC
    ab[3:6] = fanoc[0:3] * AOC
    ab[6:9] = fanoc[0:3]* AOC
    ab[9] = fhl * AOC

    if FTYS:
        ab[10:13] = fanoc[3]*AOC

    # height
    hb[0:3] = hlid[0]
    hb[3:6] = hlid[1]
    hb[6:9] = hlid[2]
    hb[9] = 250

    if FTYS:
        hb[10], hb[11] = hlid[0:2]
        hb[12] = 200

    # final volume and height
    if FTYS:
        # residual volume
        vres = VOC - (hlid[0]+hlid[1])*(1-fhl)*AOC-hb[9]*ab[9]-hb[12]*ab[12]
        # distribute into deep AIP
        hb[6:9] = vres * fdvol/ab[6:9]
        vb = ab * hb
    else:
        vb = ab * hb
        # now add to deep boxes: the volume below H box = ab[9]*(HAV-hb[9])
        vb[6:9] += ab[9] * (HAV-hb[9]) / 3
        hb = vb/ab

    # set box indices
    # kkv: surface: low-lat（NLS） + High(1)
    # kiv: interm
    if FTYS:
        kkv = np.array([0,1,2,9,10], dtype = 'int8')
    else:
        kkv = np.array([0,1,2,9], dtype = 'int8')

    if FTYS:
        kiv = np.array([3,4,5,11], dtype = 'int8')
    else:
        kiv = np.array([3,4,5], dtype = 'int8')

    """ =====      temp, sal, pressure, Mg, Ca   =========="""
    # set interal default
    # temp (deg C)  L I D

    tcb0[0:3] = tc3[0]
    tcb0[3:6] = tc3[1]
    tcb0[6:9] = tc3[2]
    tcb0[9] = 2          # H-box

    if FTYS:
        tcb0[10],tcb0[11],tcb0[12] = tct[0],tct[1],tct[2]
        tcb0[9] = 12

    tcb0c = tcb0
    # salinity
    salv = salv * SALOCN

    # pressure
    prsv[0:3] =  0.5 * hb[0:3]                                          * 0.1  # surf
    prsv[3:6] = (0.5 * hb[3:6] + hb[0:3])                     * 0.1  # interm
    prsv[6:9] = (0.5 * hb[6:9] + hb[0:3] + hb[3:6]) * 0.1  # deep
    prsv[9] = 0.5 * hb[9] * 0.1

    if FTYS:
        k = 10
        prsv[k]   =  0.5 * hb[k]                                          * 0.1   # surf
        prsv[k+1] = (0.5 * hb[k+1] + hb[k])                     * 0.1   # interm
        prsv[k+2] = (0.5 * hb[k+2] + hb[k] + hb[k+1]) * 0.1   # deep


    # store SP to matrix
    spm = np.vstack((salv,prsv))  # Salinity Pressure matrix


    # set Ca Mg


    """============        mixing parameters          ==========="""
    mxv = 3.8 * YTOSEC * mv0         #Sv -> m3/year  3.8: tuning
    mhd = 1.3 * YTOSEC * mhd0        #Sv -> m3/year  1.3: tuning

    """===========        Biological pump           =========="""
    global eph
    eph = eph0 * ab[9]    # mol/y 1.8 H export, mol C/m2/y * A = mol/year

    if FSED:
        nuwd = 0.31      # water column dissolution
    else:
         nuwd = 0.0


    frei = 0.78          # fraction EPL, remineralized in I boxes
    oi = 1 - frei


    # fraction EPH, remineralized in deep A,I,P boxes
    gp[6:9] = gp0







    # Some of the values ofor the C-Cycle parameters below
    # are only loosely constrained, some have been be tuned
    # within reasonable ranges. A few references that provide
    # ranges are given in brackets:
    # WK92 = WalkerKasting92, Berner = GEOCARN 123
    # KA99 = KumpArthur99, Veizer = VeizerEtAl99
    # Hayes = HayesEtAl99


    # kerogen oxidation, tuded to match d13c-sw results with observations
    if FTYS:
        fkrg = 7e12/AOC    # mol C/m2/y 7 [WK92, Berner]
    else:
        fkrg = 10e12/AOC

    # long C-Cycle fluxes 13C
    if FTYS:

        d13ckrg = -23.2    # -23.2 kerogen [WK92/tuned]
        epscorg = -33      # -33   eps(Corg-DIC) [tuned_Berner, Hayes]

    else:
        d13ckrg = -21.0
        epscorg = -27.7

    alpcorg = epscorg/1e3 + 1  # eps(Corg-DIC) [tuned_Berner, Hayes]

    rvccc = (d13cvc/1e3 + 1) * RST
    rincc = (d13cin/1e3 + 1) * RST
    rkrgcc = (d13ckrg/1e3 + 1) * RST
    """ =========   allocate values for the sediment boxes  ========"""
    if FSED:

        fc0a  = np.zeros(NSD, dtype = 'float64')
        fc0i  = np.zeros(NSD, dtype = 'float64')
        fc0p  = np.zeros(NSD, dtype = 'float64')
        phiia = np.zeros(NSD, dtype = 'float64')
        phiii = np.zeros(NSD, dtype = 'float64')
        phiip = np.zeros(NSD, dtype = 'float64')




    if FTYS:
        klidt = np.zeros(NSD, dtype = 'int8')
        fc0t  = np.zeros(NSD)
        phiit = np.zeros(NSD)
    if FSEDCC:
        fcc0a = np.zeros(NSD)
        fcc0i = np.zeros(NSD)
        fcc0p = np.zeros(NSD)
    if FTYS:
        fcc0t = np.zeros(NSD)

    # rain of remainder
    frrf = 0.35                 # g/cm2/ky remainder
    frrf = frrf * 1e4/1e3/1e3   # -> kg/m2/y


    # sediments
    # dissolution parameter
    # ~ fc ^ 0.5 * (cs-c)  Kd defined in DEQ
    ncsd = 2.4                  # calc dissolution order
    kssd = 20.36e10             # mol/m2/y


    # shelf/deep rain

    if FTYS:
        nsht = 0.4              # 0.4 Tethy exponent
        fsht = fsh ** nsht


    jsh = 2                     # shelf/deep rain partitioning


    # sediment box depths
    dsv = dsv0 * 1e3           # km -> m

    # depth variable (0< = z <= dsv[NSD])
    nz = 6500+1
    zv = np.arange(dsv[-1]+1, dtype = int)


    # klid: assign sediment to ocean boxes
    # low, interm or deep
    kl = np.where(dsv <= hlid[0])
    ki = np.where((dsv > hlid[0]) &
              (dsv <= (hlid[0]+hlid[1])))
    kd = np.where(dsv>(hlid[0]+hlid[1]))
    klid = np.zeros(len(dsv),dtype = int)
    klid[kl] = 0
    klid[ki] = 3
    klid[kd] = 6

    if FTYS:
        klidt[kl] = 10
        klidt[ki] = 11
        klidt[kd] = 12
    nlid = np.array([len(dsv[kl]),len(dsv[ki]),len(dsv[kd])])




    # porosity
    phi0 = 0.85    # porosity max 0.85
    gam  = 0.23    # porosity delta 0.23
    phi1 = phi0-gam # porosity min

    hsl = 0.08

    if FTYS:
        m1 = np.array([0,1,2,10])
        m2 = np.array([0,1,2,8])
        m3 = np.array([0,1,2,6])
    else:
        m1 = np.array([0,1,2])
        m2 = np.array([0,1,2])
        m3 = np.array([0,1,2])




    """ =========     Initialize y-start values (default or load) ===="""
    """
    sequence of tracers:
        ocn: 1 = dic; 2 = alk; 3 = po4; 4 = tcb; 5 = dox; 6 = dicc
        Catm, C13atm
    sediment:
        NOATM + 1 = fc ATL
        NOATM +1*NSD + 1 = fc IND
        NOATM +2*NSD + 1 = fc PAC
        (NOATM) + 3 * NSD + 1 = fc TETH

        NOATM+(3+KTY)*NSD+1... = fcc ATL
        NOATM+(4+KTY)*NSD+1... = fcc IND
        NOATM+(5+KTY)*NSD+1... = fcc PAC
        NOATM+(6+KTY)*NSD+1... = fcc TETH

        where KTY = 0 modern, KTY = 1 paleo

    """

    # init DIC
    dic0 = np.ones(NB) * 2.3 * 1e-3 * RHO    # 2.3 mmol/kg -> mol/m3

    # init alk
    alk0 = np.ones(NB) * 2.4 * 1e-3 * RHO    # 2.4 mmol/kg -> mol/m3

    # init po4
    if FTYS:
        po4pe = 0.87 * 1.0133122
        po40 = np.ones(NB) * 2.50 * 1e-3 * po4pe # mol/kg (po4 at t = 0)
    else:
        po40 = np.ones(NB) * 2.50 * 1e-3 * 0.87

    po40 = po40 * RHO                        # -> mol/m3

    # init dicc
    if NOCT >=6:
        d13c0 = np.hstack((2.35* np.ones(3), 0.5* np.ones(3), 0.67* np.ones(3), 1.63))
    if FTYS:
        d13c0 = np.hstack((d13c0, 2.35,0.5,0.67))
    rccb0 = (d13c0/1e3 +1)* RST
    dicc0 = rccb0 * dic0

    # copy all to ystart
    ystart[0:3*NB] = np.hstack((dic0,alk0,po40))


    # copy tcb0 to ystart

    ystart[3*NB:4*NB] = tcb0/TSCAL


    # dox

    ystart[4*NB : 5*NB] = 0.2   # mol/m3


    # dicc
    if NOCT>=6:
        ystart[5*NB : 6*NB] = dicc0/CNTI


    # nocatm
    if NCATM == 1:
        catm0 = 280*PPMTOMMSQ # ppmv -> mol/m2 atm co2 inventory
                           # 1 ppmv = 2.2 Pg C
        ystart[NOCT*NB] = catm0*CNTI


    # atmospheric d13co2
    if NCCATM == 1:
        d13catm0 = -6.45
        ccatm0 = catm0 * (d13catm0/1e3 + 1) * RST
        ystart[NOCT*NB +1] = ccatm0




    """ ======== Sediment setting ========== """
    if FSED:
        mc0a = np.zeros(NSD)
        mc0i = np.zeros(NSD)
        mc0p = np.zeros(NSD)
        if FTYS:
            mc0t = np.zeros(NSD)

    # set initial fraction
        fc0a = np.ones(NSD) * 0.46
        fc0i = np.ones(NSD) * 0.46
        fc0p = np.ones(NSD) * 0.46

        if FTYS:
            fc0t = np.ones(NSD) * 0.46
    #   copy all to ystart
    ystart[NOATM: NOATM + 3 * NSD] = np.hstack((fc0a,fc0i,fc0p))

    if FTYS:
        ystart[NOATM+3*NSD: NOATM+4*NSD] = fc0t

# initial porosities and CaCO3 mass
    ffphi = (phi1-phi0)/(1-phi1)
    phiia = (phi0 + ffphi*fc0a)/(1+ffphi*fc0a)
    phiii = (phi0 + ffphi*fc0i)/(1+ffphi*fc0i)
    phiip = (phi0 + ffphi*fc0p)/(1+ffphi*fc0p)
    mc0a = fc0a * RHOS * (1-phiia)
    mc0i = fc0i * RHOS * (1-phiii)
    mc0p = fc0p * RHOS * (1-phiip)
    if FTYS:
        phiit = (phi0 + ffphi*fc0t)/(1+ffphi*fc0t)
        mc0t = fc0t * RHOS * (1-phiit)
    if FSEDCC:
        fcc0a = rincc * fc0a
        fcc0i = rincc * fc0i
        fcc0p = rincc * fc0p
    if FTYS:
        fcc0t = rincc * fc0t

    # copy all to ystart
    ystart[NOATM + (3 + KTY) * NSD: NOATM + (6+KTY) * NSD ] = np.hstack((fcc0a/CNTI, fcc0i/CNTI, fcc0p/CNTI))
    if FTYS:
        ystart[NOATM + (6+KTY) *NSD: NOATM +(7+KTY) * NSD] = fcc0t/CNTI










    ### ------  Alternatively, load restart  ---------------###
    if LOADFLAG:

        ystart = np.loadtxt(initfile)

        if len(ystart) != NEQ:
            print('Wrong restart values')


        if NOCT >= 4:

            ystart[3*NB:4*NB] /= TSCAL
            tcb0 = ystart[3*NB:4*NB] * TSCAL

        if FSED:
            # fc0 and phii need to be recalculated during restart
            fc0a = ystart[NOATM       : NOATM+NSD]
            fc0i = ystart[NOATM+NSD   : NOATM+2*NSD]
            fc0p = ystart[NOATM+2*NSD : NOATM+3*NSD]
            if FTYS:
                fc0t = ystart[NOATM+3*NSD : NOATM+4*NSD]

            # porosities
            phiia = (phi0 + ffphi * fc0a)/(1+ffphi*fc0a)
            phiii = (phi0 + ffphi * fc0i)/(1+ffphi*fc0i)
            phiip = (phi0 + ffphi * fc0p)/(1+ffphi*fc0p)
            if FTYS:
                phiit = (phi0 + ffphi * fc0t)/(1+ffphi*fc0t)



            # apply fdapi (change initial dic, alk, po4)
            # only control file modifies fdapi. default 0
            ystart[0:NB] *= (1+fdapi[0]*CNTI)
            ystart[NB:2*NB] *= (1+fdapi[1]*CNTI)
            ystart[2*NB:3*NB] *= (1+fdapi[2]*CNTI)

            if NOCT>=6:
                ystart[5*NB:6*NB] *= (1+fdapi[0]*CNTI)


def wo_params():
    dir_name = f'./{exp_name}'

    folder = exists(dir_name)
    if not folder:
        makedirs(dir_name)

    fpout = open(join(dir_name, "params.out"),"w")
    fpout.write("%e sclim   \n" %sclim)
    for i in range(3):
        fpout.write(f'{fdapi[i]:.6e} fdapi[{i}]\n' )
    fpout.write(f'{fcsml:.6e} fcmsl  \n')

    for k in range(NB):
        fpout.write(f'{vb[k]:.6e} vb[{k}] \n')
    for k in range(NB):
        fpout.write(f'{ab[k]:.6e} ab[{k}] \n')
    for k in range(NB):
        fpout.write(f'{hb[k]:.6e} hb[{k}] \n')
    for k in range(NB):
        fpout.write(f'{tcb0[k]:.6e} tcb0[{k}] \n')
    for k in range(NB):
        fpout.write(f'{salv[k]:.6e} salv[{k}] \n')
    for k in range(NB):
        fpout.write(f'{prsv[k]:.6e} prsv[{k}] \n')
    fpout.write(f'{t0:.6e} t0 \n')
    fpout.write(f'{tfinal:.6e} tfinal \n' )

    fpout.write(f'{pcsi:.6e} pcsi \n')
    fpout.write(f'{thc:.6e} thc \n')
    fpout.write(f'{thbra:.6e} thbra \n' )
    fpout.write(f'{fepl:.6e} fepl \n')
    fpout.write(f'{eph:.6e} eph \n')
    fpout.write(f'{rrain:.6e} rrain \n')
    if FSED:
        fpout.write(f'{fsh:.6e} fsh \n')
        fpout.write(f'{fvc0:.6e} fvc0 \n')
        fpout.write(f'{finc0:.6e} finc0 \n')
        fpout.write(f'{fkrg:.6e} fkrg \n')
        fpout.write(f'{cac:.6e} cac \n')
        fpout.write(f'{mgc:.6e} mgc \n')
    for k in range(KOC):
        fpout.write(f'{mxv[k]:.6e} mxv[{k}] \n')
    for k in range(NOC):
        fpout.write(f'{mhd[k]:.6e} mhd[{k}] \n')
    if FSED:
        fpout.write(f'{ncsd:.6e} ncsd \n')
        fpout.write(f'{kssd:.6e} kssd \n')
    for k in range(NSD):
        fpout.write(f'{dsv[k]:.6e} dsv[{k}] \n')
    for k in range(NSD):
        fpout.write(f'{asva[k]:.6e} asva[{k}] \n')
    for k in range(NSD):
        fpout.write(f'{asvi[k]:.6e} asvi[{k}] \n')
    for k in range(NSD):
        fpout.write(f'{asvp[k]:.6e} asvp[{k}] \n')
    if FTYS:
        for k in range(NSD):
            fpout.write(f'{asvt[k]:.6e} asvt[{k}] \n')
    for k in range(NSD):
        fpout.write(f'{klid[k]:d} klid[{k}] \n')
    if FTYS:
        for k in range(3):
            fpout.write(f'{nlid[k]:d} nlid[{k}] \n')
    if FTYS:
        for k in range(NSD):
            fpout.write(f'{klidt[k]:d} klidt[{k}] \n')
    for k in range(NSD):
        fpout.write(f'{phiia[k]:.6e} phiia[{k}] \n')
    for k in range(NSD):
        fpout.write(f'{phiii[k]:.6e} phiii[{k}] \n')
    for k in range(NSD):
        fpout.write(f'{phiip[k]:.6e} phiip[{k}] \n')
    fpout.close()

    # # dsv.out
    # fpout = open("dsv.out","w")
    # for k in range(NSD):
    #     fpout.write(f'{dsv[k]:.6e} \n')
    # fpout.close()

    # # zv.out
    # if FTYS:
    #     fpout = open("zv.out", "w")
    #     for k in range(nz):
    #         fpout.write(f'{zv[k]:.6e} \n')
    # fpout.close()

    # # ystart.out
    # fpout = open('ystart.out','w')
    # for k in range(NEQ):
    #     fpout.write(f'{ystart[k]:.6e}, ystart[{k}] \n')
    # fpout.close()

# @jit(nopython = True)
def derivs(t, y, set_progress, hpls):
    yp = np.zeros(NEQ)


    # if RUN_TYPE == 1:
    #     n = int((t-t0)/(tfinal-t0)*100)
    #     set_progress((str(n), str(100)))


    # read tracer values from y
    # dydt default: all to zero
    dic = y[0:NB]
    dicp = np.zeros(NB)
    alk = y[NB:2*NB]
    alkp = np.zeros(NB)
    po4 = y[2*NB:3*NB]*MMTOM  # po4 convert to mol/m3
    po4p = np.zeros(NB)


    # warning if high-lat po4 < 0
    if po4[9]<0:
        print('\n HighLat PO4 = {po4[9]:.e} mol/m3')
        print("derivs(): HighLat PO4 is negative. Increase initial PO4?")

    if NOCT >= 4:
        tcb = y[3*NB:4*NB]*TSCAL
        tcbp = np.zeros(NB)
    else:
        tcb = tcb0
    if NOCT >= 5:
        dox = y[4*NB:5*NB]
        doxp = np.zeros(NB)

        if dox.any() < 0:
            print('\n Dissolved Oxygen: dox[{k:.d} = {dox[k]:.e} mol/m3')
            print("derivs(): Diss. O2 is negative (<anoxic). Reduce CBIOH?")

    if NOCT >= 6:
        dicc = y[5*NB:6*NB] * CNTI   #->mol/m3
        diccp = np.zeros(NB)
        rccb = dicc/dic

    if NCATM == 1:
        pco2a = y[NOCT*NB] / PPMTOMMSQ/CNTI  #atmospheric co2, scaling /CNTI
        catmp = 0

    if NCCATM == 1:
        pcco2a = y[NOCT*NB+1]/PPMTOMMSQ           # not scaled
        ccatmp = 0.0

    if FSED:
        fcva = y[NOATM: NOATM+NSD]
        fcvi = y[NOATM+NSD : NOATM+2*NSD]
        fcvp = y[NOATM+2*NSD : NOATM + 3*NSD]
        if FTYS:
            fcvt = y[NOATM+3*NSD:NOATM+4*NSD]
        fcvap = np.zeros(NSD)
        fcvip = np.zeros(NSD)
        fcvpp = np.zeros(NSD)
        if FTYS:
            fcvtp = np.zeros(NSD)
        if FSEDCC:
            fccva = y[NOATM+(KTY+3)*NSD:NOATM+(KTY+4)*NSD]*CNTI
            fccvi = y[NOATM+(KTY+4)*NSD:NOATM+(KTY+5)*NSD]*CNTI
            fccvp = y[NOATM+(KTY+5)*NSD:NOATM+(KTY+6)*NSD]*CNTI
            if FTYS:
                fccvt = y[NOATM+(KTY+6)*NSD:NOATM+(KTY+7)*NSD]*CNTI
            fccvap = np.zeros(NSD)
            fccvip = np.zeros(NSD)
            fccvpp = np.zeros(NSD)
            if FTYS:
                fccvtp = np.zeros(NSD)
        # fc0flag = 0
        # fcc0flag = 0
        # fc1flag = 0
        # if FTYS:
        #     if fcva.any()<0 or fcvi.any()<0 or fcvp.any()<0 or fcvt.any()<0:
        #         fc0flag = 1

        #     if FSEDCC:
        #         if fccva.any()<0 or fccvi.any()<0 or fccvp.any()<0 or fcvt.any()<0:
        #             fcc0flag = 1

        # if fcva.any()<0 or fcvi.any()<0 or fcvp.any()<0:
        #     fc0flag = 1

        # if FSEDCC:
        #     if fccva.any()<0 or fccvi.any()<0 or fccvp.any()<0:
        #         fcc0flag = 1

        # if fc0flag == 1:
        #     print(f'\n\n @ at t = {t:e} \n')
        #     print("derivs(): fc < 0.0. Reduce EPSLV? Raise FCSML?")

        # if fcc0flag == 1:
        #     print(f'\n\n @ at t = {t:e} \n')
        #     print("x")

        # # warning if any fc > 1.0
        # if fcva.any()>1 or fcvi.any()>1 or fcvp.any()>1:
        #     fc1flag = 1

        # if fc1flag == 1:
        #     print(f'derivs(): fc > 1 at t={t:.3e}. Check final fc values.')

        # sed boxes low and low+interm

        ns1 = nlid[0]
        ns2 = nlid[0] + nlid[1]


    # init locals
    eplv = np.zeros(NLS)
    ealv = np.zeros(NLS)
    enlv = np.zeros(NLS)
    pplv = np.zeros(NLS)
    eclv = np.zeros(NLS)
    exlv = np.zeros(NLS)
    co2 =  np.zeros(NB)
    pco2 = np.zeros(NB)
    co3 =  np.zeros(NB)

    ph =  np.zeros(NB)
    kh =  np.zeros(NB)
    o2sat =  np.zeros(NB)
    kasv0 =  np.zeros(NB)
    kasv =  np.zeros(NB)
    vask0 =  np.zeros(NB)
    vask =  np.zeros(NB)
    fmmo =  np.zeros(NB)
    alpdb =  np.zeros(NB)
    alpdg =  np.zeros(NB)
    alpcb =  np.zeros(NB)
    eplvcc = np.zeros(NLS)
    ealvcc = np.zeros(NLS)
    eclvcc = np.zeros(NLS)
    exlvcc = np.zeros(NLS)
    fkrgccb = np.zeros(NB)

    if FSED:





        rscva = np.zeros(NSD)
        rscvi = np.zeros(NSD)
        rscvp = np.zeros(NSD)





        rdva = np.zeros(NSD)
        rdvi = np.zeros(NSD)
        rdvp = np.zeros(NSD)



        wcva = np.zeros(NSD)
        wcvi = np.zeros(NSD)
        wcvp = np.zeros(NSD)

        fba = np.zeros(NSD)
        fbi = np.zeros(NSD)
        fbp = np.zeros(NSD)

        gsda = np.zeros(NSD)
        gsdi = np.zeros(NSD)
        gsdp = np.zeros(NSD)

        #jja = np.zeros(NSD) # allocated later
        #jji = np.zeros(NSD)
        #jjp = np.zeros(NSD)



        if FTYS:

            rscvt = np.zeros(NSD)

            #disst = np.zeros(NSD)
            rdvt  = np.zeros(NSD)

            #lett  = np.zeros(NSD)
            wcvt  = np.zeros(NSD)
            fbt   = np.zeros(NSD)
            gsdt  = np.zeros(NSD)


        dissm = np.full((NOC,NSD),np.nan)

        if FSEDCC:

            rscvacc = np.zeros(NSD)
            rscvicc = np.zeros(NSD)
            rscvpcc = np.zeros(NSD)

            rdvacc = np.zeros(NSD)
            rdvicc = np.zeros(NSD)
            rdvpcc = np.zeros(NSD)

            wcvacc = np.zeros(NSD)
            wcvicc = np.zeros(NSD)
            wcvpcc = np.zeros(NSD)

            if FTYS:


                rscvtcc = np.zeros(NSD)
                rdvtcc = np.zeros(NSD)
                wcvtcc = np.zeros(NSD)

            dissmcc = np.full((NOC,NSD),0)
    # co2 system and o2 of boxes (surface 0:LA 1:LI 3:LP 9:H )
    # requires mol/kg

    co2, pco2, co3, hpls, ph, kh, o2sat = fcsys(dic/RHO, alk/RHO, hpls, tcb, salv, prsv, cac, mgc)



    # air-sea co2 exchange coeff

    kasv0[kkv] = 0.06
    vask0[kkv] = 3*365
    kasv = kasv0 * ab
    vask = vask0 * ab

    # air-sea 13co2 alphas
    alpdb[kkv], alpdg[kkv], alpcb[kkv] = falpha(tcb[kkv])


    if MOOK:
        alpu = 0.9995
    else:
        alpu = 0.9991



    """---------------------- Biological pump -------------------------"""

    eplv = fepl * mxv[0:NLS] * po4[kiv]/REDPC
    ealv = eplv *2 /rrain     # ALK mol/year
    pplv = eplv * REDPC       # PO4 mol/year
    enlv = eplv * REDNC       # NO3 mol/year

    # total carbon: Corg + CaCO3
    eclv = eplv + 0.5 * ealv


    # high lat export

    eah = 0                      ##  2*eph/init.rrain   ###???? 0000?
    pph = eph * REDPC
    enh = eph * REDNC
    # total carbon
    ech = eph+0.5*eah


    if NOCT >= 6 :

        eplvcc[0:3] = alpcorg * rccb[0:3] * eplv[0:3]
        ealvcc[0:3] =           rccb[0:3] *ealv[0:3]
        eclvcc[0:3] = eplvcc[0:3] + 0.5 * ealvcc[0:3]

        ephcc = alpcorg*rccb[9]*eph
        eahcc =         rccb[9]*eah
        echcc = ephcc+0.5*eahcc

        if FTYS:
            eplvcc[3] = alpcorg * rccb[10] * eplv[3]
            ealvcc[3] =           rccb[10] *ealv[3]
            eclvcc[3] = eplvcc[3] + 0.5 * ealvcc[3]


    if po4[9] < PMMK:
        if po4[9]<0:
            pph = 0
        else:
            pph = pph * PMMV * po4[9] /(PMM0 + po4[9])

    if NOCT >= 5:
        # MM kinetic dissolved oxygen
        fmmo = dox/(dox+KMMOX)
        fmmo [np.where(fmmo<0)] = 0


    if FSED:


        rscva, rscvacc, rdva, rdvacc, wcva, wcvacc, gsda, dissa, dissmcca, fba =  funcsed(ealv[0], ealvcc[0], eah, eahcc, ab[0], fccva, fcva, fc0a, asva, phiia, tcb, co3, gp[6], 1, 0)
        rscvi, rscvicc, rdvi, rdvicc, wcvi, wcvicc, gsdi, dissi, dissmcci, fbi =  funcsed(ealv[1], ealvcc[1], eah, eahcc, ab[1], fccvi, fcvi, fc0i, asvi, phiii, tcb, co3, gp[7], 1, 1)
        rscvp, rscvpcc, rdvp, rdvpcc, wcvp, wcvpcc, gsdp, dissp, dissmccp, fbp =  funcsed(ealv[2], ealvcc[2], eah, eahcc, ab[2], fccvp, fcvp, fc0p, asvp, phiip, tcb, co3, gp[8], 0.5, 2)


        if FTYS:
            rscvt, rscvtcc, rdvt, rdvtcc, wcvt, wcvtcc, gsdt, disst, dissmcct, fbt =  funcsedt(ealv[3], ealvcc[3], eah, eahcc, ab[10], fccvt, fcvt, fc0t, asvt, phiit, tcb, co3, 0, 6)
            dissm = np.vstack((dissa, dissi, dissp, disst))
            dissmcc = np.vstack((dissmcca, dissmcci, dissmccp, dissmcct))

        else:
            dissm = np.vstack((dissa, dissi, dissp))
            dissmcc = np.vstack((dissmcca, dissmcci, dissmccp))





    # ----- Long C-Cycle fluxes ---------

    # CaSiO3 weathering


    fsi = fvc0* (pco2a/pcsi) ** nsi
    # CaCO3 weathering
    finc = finc0 * (pco2a/pcsi) ** ncc


    # long c-cycle fluxes 13c

    fsicc = rincc*fsi
    fincc = rincc*finc
    fkrgccb = alpcorg*fkrg*rccb




    # sediment flags
    if FSED:
        exlv = 1.0 * eplv
        exh = eph
        if NOCT >= 6:
            exlvcc = eplvcc * 1.0
            exhcc = ephcc
        sdn  = 0
    else:
        exlv = eclv * 1.0
        exh = ech
        if NOCT>=6:
            exlvcc = 1.0 * eclvcc
            exhcc = echcc
        sdn = 1



    """

    Right-hand side of DEQs
    Units ocean tracer: mol/m3/y

    """


    # =========================== DIC ===================================

    # TH and mixing

    dicp = thmfun(dic,fconv,thc,tso,tto,mxv,mhd,vb,gtha,thbra,gthi,thbri)


    # air-sea
    if NCATM == 1:
        dicp[kkv] = dicp[kkv] + kasv[kkv] * (pco2a-pco2[kkv])/vb[kkv]


    # bio pump Corg

    dicp[m1] = dicp[m1] - eclv/vb[m1]
    dicp[m2+3] = dicp[m2+3] + frei*exlv/vb[m2+3]
    dicp[m3+6] = dicp[m3+6] + oi*exlv/vb[m3+6]
    dicp[m3+6] = dicp[m3+6] + 0.5*nuwd*ealv/vb[m3+6]


    dicp[9] = dicp[9] - ech/vb[9]

    dicp[6:9] = dicp[6:9] + exh/vb[6:9]*gp[6:9] + 0.5*nuwd*eah/vb[6:9]*gp[6:9]



    if FSED:
        dicp[m1] += 2 * finc*AOC/vb[m1]/NOC
        dicp[m1] += 2 * fsi *AOC/vb[m1]/NOC
        dicp[m1] -= 1 * fkrg*AOC/vb[m1]/NOC

        dicp[m1] += np.sum(dissm[np.arange(NOC), 0:ns1], axis = 1)/vb[m1]
        dicp[m2+3] += np.sum(dissm[np.arange(NOC), ns1:ns2], axis = 1)/vb[m2+3]
        dicp[m3+6] += np.sum(dissm[np.arange(NOC), ns2:NSD], axis = 1)/vb[m3+6]







    # =========================== ALK ===================================
    # TH and mixing
    alkp = thmfun(alk,fconv,thc,tso,tto,mxv,mhd,vb,gtha,thbra,gthi,thbri)
    # bio pump

    alkp[m1] += -ealv/vb[m1] + enlv/vb[m1]
    alkp[m2+3] += frei*(sdn*ealv/vb[m2+3] - enlv/vb[m2+3])
    alkp[m3+6] += oi * (sdn*ealv/vb[m3+6]-enlv/vb[m3+6]) + nuwd*ealv/vb[m3+6]
    alkp[9] += -eah/vb[9] + enh/vb[9]

    alkp[6:9] += (sdn*eah/vb[6:9] - enh/vb[6:9])*gp[6:9] + nuwd*eah/vb[6:9] * gp[6:9]

    if FSED:
        alkp[m1] += 2*finc*AOC/vb[m1]/NOC
        alkp[m1] += 2*fsi*AOC/vb[m1]/NOC
        alkp[m1] += 2 * np.sum(dissm[:,0:ns1],axis=1)/vb[m1]
        alkp[m2+3] += 2 * np.sum(dissm[:,ns1:ns2],axis=1)/vb[m2+3]
        alkp[m3+6] += 2 * np.sum(dissm[:,ns2:NSD],axis=1)/vb[m3+6]

    # =========================== PO4 ===================================
    # TH and mixing
    po4p = thmfun(po4,fconv,thc,tso,tto,mxv,mhd,vb,gtha,thbra,gthi,thbri)
    # bio pump Porg
    po4p[m1] -= pplv/vb[m1]
    po4p[m2+3] += frei*pplv/vb[m2 + 3]
    po4p[m3+6] += oi*pplv/vb[m3 + 6]

    po4p[9] -= pph/vb[9]

    po4p[6:9] += pph/vb[6:9]*gp[6:9]


    # =========================== Temp ===================================
    # Ocean temp change, using simple climate sensitivity (Archer,2005)
    # TAU: relax times(y): surf, interm, deep

    if NOCT>=4:


        if ((tsnsflag == 1) and (pco2a >= 150)):
            tmp = sclim*np.log(pco2a/pcsi)/np.log(2)
            tcbp[m1] = (tcb0[m1] + tmp-tcb[m1])/TAUS
            tcbp[m2+3] = (tcb0[m2+3]+tmp-tcb[m2+3])/TAUI
            tcbp[m3+6] = (tcb0[m3+6]+tmp-tcb[m3+6])/TAUD
            tcbp[9] = (tcb0[9]+tmp-tcb[9])/TAUS


   # =========================== Oxygen ===================================
    if NOCT >= 5:
        doxp = thmfun(dox,fconv,thc,tso,tto,mxv,mhd,vb,gtha,thbra,gthi,thbri)
        # air-sea, o2sat = o2 at saturation(atm)
        doxp[kkv] += vask[kkv] * (o2sat[kkv]-dox[kkv])/vb[kkv]

        # bio pump o2
        doxp[m1] += eplv*REDO2C/vb[m1]
        doxp[m2+3] -= frei*fmmo[m2+3]*eplv*REDO2C/vb[m2+3]
        doxp[m3+6] -= oi*fmmo[m3+6]*eplv*REDO2C/vb[m3+6]
        doxp[9] += eph*REDO2C/vb[9]

        doxp[6:9] -= gp[6:9]*fmmo[6:9]*eph*REDO2C/vb[6:9]


    # =========================== DICC:13C ===================================
    if NOCT >= 6:
        # TH and mixing
        diccp = thmfun(dicc,fconv,thc,tso,tto,mxv,mhd,vb,gtha,thbra,gthi,thbri)
        # air-sea
        if NCCATM == 1:
            tmp = alpdg[kkv]*pcco2a-alpdb[kkv]*rccb[kkv]*pco2[kkv]
            diccp[kkv] += kasv[kkv]*alpu*tmp/vb[kkv]

        # bio pump Corg
        diccp[m1] += -eclvcc/vb[m1]
        diccp[m2+3] += frei*exlvcc/vb[m2+3]
        diccp[m3+6] += oi*exlvcc/vb[m3+6] + 0.5*nuwd*ealvcc/vb[m3+6]
        diccp[9] -= echcc/vb[9]

        diccp[6:9] += exhcc/vb[6:9] * gp[6:9] + 0.5*nuwd*eahcc/vb[6:9] * gp[6:9]

        if FSEDCC:
            # riverine and sediment fluxes
            diccp[m1] += 2*fincc * AOC/vb[m1]/NOC
            diccp[m1] += 2*fsicc * AOC/vb[m1]/NOC
            diccp[m1] -= 1*fkrgccb[m1]*AOC/vb[m1]/NOC
            diccp[m1] += np.sum(dissmcc[:,0:ns1],axis=1)/vb[m1]
            diccp[m2+3] += np.sum(dissmcc[:,ns1:ns2],axis=1)/vb[m2+3]
            diccp[m3+6] += np.sum(dissmcc[:,ns2:NSD],axis=1)/vb[m3+6]



    # ===========================   C atm   ===================================
    if NCATM == 1:
        catmp -= np.sum(kasv[kkv]*(pco2a-pco2[kkv])/AOC)

        if FSED:
            fvc = fvc0
            catmp += fvc - finc - 2*fsi + fkrg



    # ===========================  13C atm  ===================================
    if NCCATM == 1:
        tmp = alpdg[kkv]*pcco2a-alpdb[kkv]*rccb[kkv]*pco2[kkv]
        ccatmp-= np.sum(kasv[kkv]*alpu*tmp/AOC)
        if FSED:
            fvccc = rvccc*fvc
            fkrgcc = rkrgcc*fkrg
            ccatmp +=fvccc - fincc - 2*fsicc +fkrgcc



    # cabon input scenarios
    if cinpflag or RUN_TYPE == 2 or RUN_TYPE == 3:

        cinp = fcinp(t)



        catmp += cinp*1e15/12/AOC
        # dicp[m1] += cinp*1e15/12/vb[m1]/NOC
        #
        # diccp[m1] += cinp*1e15/12*frccinp(t)/vb[m1]/NOC

        if RUN_TYPE == 2 and (target_type == 'd13c' or target_type == 'pCO2_d13c' or target_type == 'pH_d13c'):

            ccatmp += rccinp*cinp*1e15/12/AOC

        else:
            ccatmp+=frccinp(t)*cinp*1e15/12/AOC


        # except:
        #     ccatmp+=rccinp*fcinp(t)*1e15/12/AOC
    # ========================= all to yp   ===================================
    yp[0    : NB]   = dicp
    yp[NB   : 2*NB] = alkp
    yp[2*NB : 3*NB] = po4p/MMTOM      #convert back to mmol/m3
    if NOCT>=4:
        yp[3*NB : 4*NB] = tcbp/TSCAL  #Temp: scale to order 1

    if NOCT>=5:
        yp[4*NB : 5*NB] = doxp

    if NOCT>=6:
        yp[5*NB : 6*NB] = diccp/CNTI

    if NCATM == 1:
        yp[NOCT*NB] = catmp*CNTI

    if NCCATM == 1:
        yp[NOCT*NB+1] = ccatmp



    # ===========================   sed boxes   ===============================
    if FSED:
        fcvap = fba*rscva - fba*rdva - wcva
        fcvap /= gsda
        fcvip = fbi*rscvi - fbi*rdvi - wcvi
        fcvip /= gsdi
        fcvpp = fbp*rscvp - fbp*rdvp - wcvp
        fcvpp /= gsdp

        if FTYS:
            fcvtp = fbt*rscvt - fbt*rdvt - wcvt
            fcvtp /= gsdt

        # all to yp
        yp[NOATM:NOATM+NSD] = fcvap
        yp[NOATM+NSD:NOATM+2*NSD] = fcvip
        yp[NOATM+2*NSD:NOATM+3*NSD] = fcvpp

        if FTYS:
            yp[NOATM+3*NSD:NOATM+4*NSD] = fcvtp

        # sediment 13C
        if FSEDCC:
            fccvap = fba*rscvacc - fba*rdvacc -wcvacc
            fccvap /= gsda
            fccvip = fbi*rscvicc - fbi*rdvicc -wcvicc
            fccvip /= gsdi
            fccvpp = fbp*rscvpcc - fbp*rdvpcc - wcvpcc
            fccvpp /=gsdp
            if FTYS:
                fccvtp = fbt*rscvtcc -fbt*rdvtcc - wcvtcc
                fccvtp /= gsdt

            yp[NOATM+(3+KTY)*NSD : NOATM+(4+KTY)*NSD] = fccvap/CNTI
            yp[NOATM+(4+KTY)*NSD : NOATM+(5+KTY)*NSD] = fccvip/CNTI
            yp[NOATM+(5+KTY)*NSD : NOATM+(6+KTY)*NSD] = fccvpp/CNTI

            if FTYS:
                yp[NOATM+(6+KTY)*NSD : NOATM+(7+KTY)*NSD] = fccvtp/CNTI

    # if t==0:
    #     np.savetxt('derivs_test.dat', yp)
    #     sys.exit()


    return yp

"""
/*============================================================*/
/*==================== derivs() END ==========================*/
/*============================================================*/
 """


@jit(nopython = True)
# @jit(nopython = True , nogil = True)
def funcsed(ealv, ealvcc, eah, eahcc, ab, fccv, fcv, fc0, asv, phii, tcb, co3,gp, coef, i):
    # input
    # ealv: caco3 export * 2
    # ealvcc: d13 of caco3 export
    # eah: high-latitude caco3 input, 0
    # eahcc, d13 of high-latitude caco3 input
    # ab: areas of each ocean
    # fccv: sediment d13
    # fcv: sediment box calcite fraction
    # fc0: initial calcite fraction
    # asv: areas of the sediment boxes in each ocean
    # phii: initial porosity
    # tcb: temperature
    # co3: co32- concentration of the deep box
    # coef: adjust the clay amount

    # Return
    # rscv: clay rain rate
    # rdv: dissolution rate
    # wcv: calcite burial rate
    # gsd: dphi/df
    # diss, dissmcc: dissolution


    # CaCO3 export AIP mol/y
    # eaa = ealv[0] + eah * gp[6]
    ea = ealv + eah * gp

    # CaCO3 rian to sediments, mol/m2/yr
    fpr = (1 - nuwd) * ea * 0.5/ ab

    fprv = np.ones(NSD) * fpr

    # clay remainder rain to sediments AIP
    frrfaip = np.ones(NSD) * frrf * coef

    if FSEDCC:
       rccs = fccv/fcv
       eacc = ealvcc + eahcc * gp
       fprcc = np.ones(NSD) * (1-nuwd) * eacc * 0.5/ab

    # shelf/deep rain partitioning
    fdr = (1-fsh*np.sum(asv[0:jsh]))/np.sum(asv[jsh:NSD])

    fshv = np.zeros(NSD)

    fshv[0:jsh] = fsh
    fshv[jsh:NSD] = fdr

    # shelf/deep: modify clay rain
    fprv = fshv*fprv

    # shelf/deep: modify clay rain
    frrfaip = fshv*frrfaip

    if FSEDCC:
       fprcc = fshv * fprcc

    # calc. saturation at sediment levels
    tsedv = tcb[klid[np.arange(NSD)]+i]
    ssedv = salv[klid[np.arange(NSD)]+i]
    kspcsed = fkspc(tsedv, ssedv, 0.1*dsv, cac, mgc)
    co3satm = kspcsed/cac

    omv = co3[klid[np.arange(NSD)]+i]/co3satm


    # sort out the supersaturation layers
    kd = np.arange(NSD) + 1

    kd[np.where(omv<1)] = 0

    # porosities as functions of fc
    ffphi = (phi1-phi0) / (1-phi1)
    phi = (phi0 + ffphi * fcv)/(1 + ffphi * fcv)

    # sed rate, m/y (kg/m2/y/(kg*m3)) -> m/yr
    rscv = fprv * MTOKGCACR / RHOS / (1-phi1)

    # remainder clay
    rsrv = frrfaip / RHOS / (1-phi0)

    # caco3 + clay
    rsv = rscv + rsrv

    if FSEDCC:
       rscvcc = fprcc * MTOKGCACR / RHOS / (1-phi1)


    diss = np.zeros(NSD)

    # correction for Ca,Mg effect on kinetics
    rcak = (cac/CAM) * (1/(1-ALPKC*(MGM/CAM - mgc/cac)))

    # dissolution mol/m2/y
    dk = np.zeros(NSD)
    index = np.where(kd == 0)
    dk[index] = kssd * ((co3satm[index]-co3[klid[index]+i])*rcak) ** ncsd
    diss[index] = np.sqrt((fcv[index])) * dk[index]

    # numerics (avoid negative fc and NaN):
    # linear drop in fc as fc -> 0
    jj = np.arange(1, NSD+1, 1)
    jj[np.where((fcv-fcsml)/fcsml >= 0)] = 0

    bbf = np.sqrt(1/fcsml)

    temp = np.intersect1d(np.argwhere(kd == 0), np.argwhere(jj != 0))
    diss[temp] = fcv[temp] * dk[temp] * bbf

    # diss rate, m/y [(mol/m2/y)*kg/mol/kg*m3 = m/y]
    rdv = diss * MTOKGCACR /RHOS / (1-phi1)

    wv = rsv - rdv

    # find erosion indices
    le = np.arange(NSD) + 1
    le[np.where((wv-0)/MZER >= 0)] = 0

    # calcite burial (w>0)
    wcv = fcv*wv*(1-phi)/(1-phi1)

    # flags default: 1, erosion:0
    fb = np.ones(NSD)

    # calcite erosion (w<0)
    # Note on signs
    temp = np.where(le != 0)
    wcv[temp] = -(1-fc0[temp])*wv[temp]*(1-phii[temp])/(1-phi0)
    wcv[temp] += rsrv[temp]
    fb[temp] = 0.0

    # dphi/dfc
    tmp = ffphi*(1-phi0)/(1+ffphi*fcv)/(1+ffphi*fcv)
    gsd = hsl*(1-phi-fcv*tmp)/(1-phi1)

    # dissloution(w>0) in mol/m2/y
    # dissolution(w<0) in mol/m2/y

    temp = np.where(le != 0 ) # erosion boxes
    diss[temp] = (rsv[temp] - wv[temp]) * (1-phi1) * RHOS/MTOKGCACR

    if FSEDCC:
        dissmcc = np.zeros(NSD)
        # dissolution rate
        rdvcc = rccs * rdv

        # burial rate
        wcvcc = rccs * wcv
        dissmcc = rccs*diss*asv*ab





    return rscv, rscvcc, rdv, rdvcc, wcv, wcvcc, gsd, diss*asv*ab, dissmcc, fb

@jit(nopython = True)
# @jit(nopython = True , nogil = True)
def funcsedt(ealv, ealvcc, eah, eahcc, ab, fccv, fcv, fc0, asv, phii, tcb, co3, gp, coef):
    # input
    # ealv: caco3 export * 2
    # ealvcc: d13 of caco3 export
    # eah: high-latitude caco3 input, 0
    # eahcc, d13 of high-latitude caco3 input
    # ab: areas of each ocean
    # fccv: sediment d13
    # fcv: sediment box calcite fraction
    # fc0: initial calcite fraction
    # asv: areas of the sediment boxes in each ocean
    # phii: initial porosity
    # tcb: temperature
    # co3: co32- concentration of the deep box
    # coef: adjust the clay amount

    # Return
    # rscv: clay rain rate
    # rdv: dissolution rate
    # wcv: calcite burial rate
    # gsd: dphi/df
    # diss, dissmcc: dissolution


    # CaCO3 export AIP mol/y
    # eaa = ealv[0] + eah * gp[6]
    ea = ealv + eah * gp

    # CaCO3 rian to sediments, mol/m2/yr
    fpr = (1 - nuwd) * ea * 0.5/ ab

    fprv = np.ones(NSD) * fpr

    # clay remainder rain to sediments AIP
    frrfaip = np.ones(NSD) * frrf * coef

    if FSEDCC:
       rccs = fccv/fcv
       eacc = ealvcc + eahcc * gp
       fprcc = np.ones(NSD) * (1-nuwd) * eacc * 0.5/ab

    # shelf/deep rain partitioning

    fdr = (1-fsht*np.sum(asv[0:jsh]))/np.sum(asv[jsh:NSD])

    fshv = np.zeros(NSD)
    fshv[0:jsh] = fsht

    fshv[jsh:NSD] = fdr

    # shelf/deep: modify clay rain
    fprv = fshv*fprv

    # shelf/deep: modify clay rain
    frrfaip = fshv*frrfaip

    if FSEDCC:
       fprcc = fshv * fprcc

    # calc. saturation at sediment levels

    tsedv = tcb[klidt[np.arange(NSD)]]
    ssedv = salv[klidt[np.arange(NSD)]]

    kspcsed = fkspc(tsedv, ssedv, 0.1*dsv, cac, mgc)
    co3satm = kspcsed/cac


    omv = co3[klidt[np.arange(NSD)]]/co3satm



    # sort out the supersaturation layers
    kd = np.arange(NSD) + 1

    kd[np.where(omv<1)] = 0

    # porosities as functions of fc
    ffphi = (phi1-phi0) / (1-phi1)
    phi = (phi0 + ffphi * fcv)/(1 + ffphi * fcv)

    # sed rate, m/y (kg/m2/y/(kg*m3)) -> m/yr
    rscv = fprv * MTOKGCACR / RHOS / (1-phi1)

    # remainder clay
    rsrv = frrfaip / RHOS / (1-phi0)

    # caco3 + clay
    rsv = rscv + rsrv

    if FSEDCC:
       rscvcc = fprcc * MTOKGCACR / RHOS / (1-phi1)


    diss = np.zeros(NSD)

    rcak = (cac/CAM) * (1/(1-ALPKC*(MGM/CAM - mgc/cac)))

    # dissolution mol/m2/y
    dk = np.zeros(NSD)
    index = np.where(kd == 0)

    dk[index] = kssd * ((co3satm[index] - co3[klidt[index]])*rcak) ** ncsd

    diss[index] = np.sqrt((fcv[index])) * dk[index]

    # numerics (avoid negative fc and NaN):
    # linear drop in fc as fc -> 0
    jj = np.arange(1, NSD+1, 1)
    jj[np.where((fcv-fcsml)/fcsml >= 0)] = 0

    bbf = np.sqrt(1/fcsml)

    temp = np.intersect1d(np.argwhere(kd == 0), np.argwhere(jj != 0))
    diss[temp] = fcv[temp] * dk[temp] * bbf

    # diss rate, m/y [(mol/m2/y)*kg/mol/kg*m3 = m/y]
    rdv = diss * MTOKGCACR / RHOS / (1-phi1)

    wv = rsv - rdv

    # find erosion indices
    le = np.arange(NSD) + 1
    le[np.where((wv-0)/MZER >= 0)] = 0

    # calcite burial (w>0)
    wcv = fcv*wv*(1-phi)/(1-phi1)

    # flags default: 1, erosion:0
    fb = np.ones(NSD)

    # calcite erosion (w<0)
    # Note on signs
    temp = np.where(le != 0)
    wcv[temp] = -(1-fc0[temp])*wv[temp]*(1-phii[temp])/(1-phi0)
    wcv[temp] += rsrv[temp]
    fb[temp] = 0.0

    # dphi/dfc
    tmp = ffphi*(1-phi0)/(1+ffphi*fcv)/(1+ffphi*fcv)
    gsd = hsl*(1-phi-fcv*tmp)/(1-phi1)

    # dissloution(w>0) in mol/m2/y
    # dissolution(w<0) in mol/m2/y

    temp = np.where(le != 0 )
    diss[temp] = (rsv[temp] - wv[temp]) * (1-phi1) * RHOS/ MTOKGCACR

    if FSEDCC:
        dissmcc = np.zeros(NSD)
        # dissolution rate
        rdvcc = rccs * rdv

        # burial rate
        wcvcc = rccs * wcv
        dissmcc = rccs*diss*asv*ab





    return rscv, rscvcc, rdv, rdvcc, wcv, wcvcc, gsd, diss*asv*ab, dissmcc, fb




@jit(nopython=True)
def fcsys(dic,alk,hgss,tc,sal,prs,calc,mgcl):


    tk = tc + TKLV
    bor =(BORT * (sal/35))*1e-6  # 416 DOE94, 432.5 Lee10

    hx = hgss

    khx = fkh(tk,sal)

    k1,k2  = fk1k2(tk,sal)
    kb  = fkb(tk,sal)
    kw  = fkw(tk,sal)
    o2x = fo2(tk,sal)




  #---------------------------------------------------------------------
    # pressure correction
    pcorrk = fpcorrk(tk, prs)
    k1 *= pcorrk[0,:]
    k2 *= pcorrk[1,:]
    kb *= pcorrk[2,:]
    kw *= pcorrk[3,:]


    # for i in range(NB):
    #     if prs[i] > 0:
    #         pcorrk = fpcorrk(tk[i],prs[i])
    #         k1[i] *= pcorrk[0]
    #         k2[i] *= pcorrk[1]
    #         kb[i] *= pcorrk[2]
    #         kw[i] *= pcorrk[3]
    #kspc = kspc*pcorrk[4]
    #kspa = kspa**pcorrk[5]


    # Ca, Mg corrections
    if calc!=CAM or mgcl != MGM:


        k1 = k1 + fdelk1(k1, calc, mgcl)
        k2 = k2 + fdelk2(k2, calc, mgcl)



    PRINTCSU = 0
    # iterative solution for H+, Follows et al. 2006

    for i in range(HIMAX):
        hgss = hx
        boh4g = bor*kb/(hgss+kb)
        fg = -boh4g-(kw/hgss) + hgss
        calkg = alk + fg
        gam = dic/calkg
        tmp = (1-gam)*(1-gam)*k1*k1 - 4 *k1 *k2 *(1-2*gam)

        hx = 0.5 *((gam-1)*k1+np.sqrt(tmp))

        if (np.fabs(hx-hgss).all() <= (hgss*1e-4)).all() :
            break



              # if PRINTCSU:
              #     print(f'\n {i:d} i')


       # if i == HIMAX:
       #     print(f'\n [H+] = {hx:.e}]')
       #     print(f'\n [H+] iteration did not converge after {HIMAX:.d} steps')
       #     if hx<0:
       #         print('\n [H+] < 0. Your ALK/DIC ratio may be too high')
       #         print('csys(): check co2 system input')


    co2 = dic/(1+k1/hx + k1*k2/hx/hx)
    pco2 = co2 * 1e6/khx
    co3 = dic/(1+hx/k2 + hx*hx/k1/k2)
    h = hx
    ph = - np.log10(hx)
    kh = khx
    o2sat = o2x



    if PRINTCSU:
         print("%20.15e  kh\n",khx)
         print("%20.15e  k1\n",k1)
         print("%20.15e  k2\n",k2)
         print("%20.15e  kb\n",kb)
         print("%20.15e  kw\n",kw)
         print("%20.15e  O2  \n",o2x)


    return co2, pco2, co3, h, ph, kh, o2sat


# =========================== fcsys() end ===================================


@jit(nopython=True)
def fkspc(tc,sal, prs, calc, mgcl):
    #------Kspc (calcite)  --------
    # Apparent solubility product of calcite
    # Kspc = [Ca2+][coe2-]T   T:total, free ions + ion pairs
    # Mucci 1983 mol/kg(solution)
    tk = tc + TKLV
    tmp1 = -171.9065-0.077993*tk+2839.319/tk+71.595*np.log10(tk)
    tmp2 = (-0.77712 + 0.0028426 * tk + 178.34/tk) * np.sqrt(sal)
    tmp3 = -0.07711*sal+0.0041249* (sal **1.5)
    log10kspc = tmp1 + tmp2 +tmp3

    kspc = 10**log10kspc


    # pressure correction
    kspc = kspc*fpcorrk(tk,prs)[4,:]
    # if prs>0:
    #     kspc = kspc*fpcorrk(tk,prs)[4]

    # Ca, Mg corrections
    if ((np.fabs((calc-CAM)/CAM))>0) or ((np.fabs((mgcl-MGM)/MGM))>0):
        kspc *= 1-ALPKC * (MGM/CAM - mgcl/calc)

    return kspc
# =========================== fkspc() end ===================================

@jit(nopython=True)
def fkspa(tc,sal, prs, calc, mgcl):
    #------Kspc (calcite), Kspa(arogonite)  --------
    # Apparent solubility product of calcite
    # Kspc = [Ca2+][coe2-]T   T:total, free ions + ion pairs
    # Mucci 1983 mol/kg(solution)
    tk = tc + TKLV

    tmp1 = -171.945 - 0.077993*tk + 2903.293/tk + 71.595*np.log10(tk)
    tmp2 = +(-0.068393+0.0017276*tk +88.135/tk)*np.sqrt(sal)
    tmp3 = -0.10018*sal+0.0059415*(sal**1.5)
    log10kspa = tmp1 + tmp2 + tmp3

    kspa = 10 ** (log10kspa)

    # pressure correction

    kspa = kspa*fpcorrk(tk,prs)[5,:]
    # Ca, Mg corrections


    return kspa

# =========================== fkspa() end ===================================

    #-------kh (K Henry)-----
    #
    # CO2(g) <-> CO2 (aq.)
    # kh  =  [co2]/pco2
    # Weiss 1974, mol/kg/atm

@jit(nopython=True)
def fkh(tk,sal):
    tmp = 9345.17/tk - 60.2409 + 23.3585*np.log(tk/100)
    nkhwe74 = tmp + sal * (0.023517 - 2.3656e-4 * tk + 0.0047036e-4 * tk * tk)

    khx = np.exp(nkhwe74)
    return khx

# ===========================  khx() end  ===================================


    #--------k1,k2-------
    # first, second acidity constant
    # pH-scale: total
    # Mehrbach et al. 1973, efit by Lueker et al.(2000)
@jit(nopython=True)
def fk1k2(tk,sal):
    pk1mehr = 3633.86/tk - 61.2172 + 9.6777 * np.log(tk)-0.011555* sal + 1.152e-4*sal*sal
    k1 = 10**(-pk1mehr)

    pk2mehr = 471.78/tk +25.9290 - 3.16967 * np.log(tk) - 0.01781 * sal + 1.122e-4*sal*sal
    k2 = 10**(-pk2mehr)

    return k1,k2

# =========================== fk1k2() end ===================================

    #-------kb-----------
    #Kbor = [H+][B(OH)4-]/[B(OH)3] = kp7/km7
    #(Dickson, 1990 in Dickson and Goyet, 1994, Chapter 5)
    #pH-scale: total mol/kg -soln
@jit(nopython=True)
def fkb(tk,sal):
    tmp1 = (-8966.90-2890.53*np.sqrt(sal)-77.942*sal+1.728*sal**1.5 - 0.0996 *sal*sal)
    tmp2 = 148.0248 + 137.1942 * np.sqrt(sal) + 1.62142*sal
    tmp3 = (-24.4344-25.085*np.sqrt(sal)-0.2474*sal)*np.log(tk)
    lnkb = tmp1/tk +tmp2 +tmp3+0.053105*np.sqrt(sal)*tk

    kb = np.exp(lnkb)
    return kb

# =========================== fkb() end ===================================


    #--------kwater----------
    #
    # Millero(1995) (in Dickson and Goyet (1994, Chapter 5))
    # $K_w$ in mol/kg-soln
    # pH -scale: total scal
@jit(nopython=True)
def fkw(tk,sal):
    tmp1 = -13847.26/tk + 148.96502 - 23.6521 * np.log(tk)
    tmp2 = (118.67/tk -5.977 +1.0495 * np.log(tk)) * np.sqrt(sal) - 0.01615 * sal
    lnkw = tmp1 + tmp2
    kw = np.exp(lnkw)

    return kw
# =========================== fkw() end ===================================


    #------solubility of O2 （ml/l = l/m3)--
    #
    # Weiss 1970 DSR,17, p.721
@jit(nopython=True)
def fo2(tk,sal):

    # ml/kg
    #A = np.array([-177.7888,255.5907,146.4813,-22.2040])
    #B = np.array([-0.037362,0.016504,-0.0020564])


    A = np.array([-173.4292,249.6339,143.3483,-21.8492])
    B = np.array([-0.033096, 0.014259, -0.0017000])
    lno2 = A[0] + A[1] * 100/tk + A[2]*np.log(tk/100) + A[3]* (tk/100)+ sal * (B[0] + B[1]*tk/100 +B[2] * ((tk/100)**2))

    o2x = np.exp(lno2)/22.4 # -> mol/m3
    return o2x

# =========================== fo2() end ===================================

@jit(nopython=True)
def fpcorrk(tk,prs):

    n = len(tk)
        ### pressure effect on K's (Millero, 1995)###

    R = 83.131            # J mol-1 deg-1 (Perfect Gas)
                          # conversion cm3 -> m3 1e-6
                          #            bar -> Pa = N/m-2 1e5
                          #                => 1/10
    # index: k1 1, k2 2, kb 3, kw 4,  kspc 5, kspa 6


    #----- note: there is an error in Table 9 of Millero, 1995
    #----- The coefficents -b0 and b1 have to be multiplied by 1e-3
    #                k1,   k2,     kb,     kw,      kspc,    kspa

    a0 = -np.array([25.5 , 15.82,  29.48,  25.60,   48.76,   46])

    a1 = np.array([0.1271, -0.0219,0.1622, 0.2324, 0.5304,  0.5304])

    a2 = np.array([0.0,    0.0,    -2.608, -3.6246, 0     ,  0])*1e-3

    b0 = -np.array([3.08, -1.13,    2.84,  5.13,    11.76,   11.76])*1e-3

    b1 = np.array([0.0877, -0.1475, 0.0,   0.0794,  0.3692,  0.3692])*1e-3
    #b2 = np.zeros(len(a0))
    tc = tk - TKLV

    deltav = a0.reshape(6,1) * np.ones((1,n)) + a1.reshape(6,1) * tc.reshape((1,n)) + \
             a2.reshape(6,1) * tc.reshape((1,n)) * tc.reshape((1,n))
    deltak = b0.reshape(6,1) * np.ones((1,n)) + b1.reshape(6,1) * tc.reshape((1,n)) #+ b2 * tc * tc
    lnkpok0 = -(deltav / (R*tk)) * prs + (0.5 * deltak/(R*tk)) * prs * prs

    pcorrk = np.exp(lnkpok0)

    return pcorrk


# =========================== fpcorrkksp() end ===================================
@jit(nopython=True)
def fdelk1(k1, calc, mgcl):
    sk1ca =  33.73e-3
    sk1mg = 155.00e-3

    #/* add Ca,Mg correction K* (Ben-Yaakov & Goldhaber, 1973) */
    delk1ca = sk1ca*k1*(calc/CAM-1.)
    delk1mg = sk1mg*k1*(mgcl/MGM-1.)

    delk1   = delk1ca+delk1mg

    return delk1

# =========================== fdelk1() end ===================================
@jit(nopython=True)
def fdelk2(k2, calc, mgcl):
    # /* sensitivity parameters for Ca,Mg effect on K* */
    sk2ca =  38.85e-3
    sk2mg = 442.00e-3

     #/* add Ca,Mg correction K* (Ben-Yaakov & Goldhaber, 1973) */
    delk2ca = sk2ca*k2*(calc/CAM-1.)
    delk2mg = sk2mg*k2*(mgcl/MGM-1.)

    delk2   = delk2ca+delk2mg;

    return delk2

# =========================== fdelk2() end ===================================

@jit(nopython=True)
def falpha(tcb):
    # 13C alphas for co2 gas exchange
    # Mook 1986 or Zhang et al. 1995
    tkb = tcb+TKLV
    if MOOK:
        epsdb = -9866/tkb +24.12
        epsdg = -373/tkb + 0.19
        epscb = -867/tkb + 2.52
    else:
        epsbg = -0.141 * tcb + 10.78
        epsdg = 0.0049 * tcb - 1.31
        epscg = -0.052 * tcb + 7.22
        epsdb = (epsdg-epsbg)/(1+epsbg/1e3)
        epscb = (epscg-epsbg)/(1+epsbg/1e3)
    alpdb = epsdb/1e3 + 1
    alpdg = epsdg/1e3 + 1
    alpcb = epscb/1e3 + 1

    return alpdb,alpdg,alpcb

# =========================== falpha() end ===================================

@jit(nopython=True)
def thmfun(y, fconvl, thcl, tsol, ttol, mvl, mhdl, vb, ga, ta, gi, ti):




    fa = 0.4
    fi = 0.3
    fp = 0.3


    if FTYS==0:
        ttol = tsol
        tsol = ttol

    yp = np.zeros(NB)

    if fconvl == 1:
        yp[3] = (ga*thcl*y[4] + ta*thcl*y[6] - thcl*y[3])/vb[3]    # IA
        yp[4] = (gi*thcl*y[5] + ti*thcl*y[7] - ga*thcl*y[4])/vb[4] # II
        yp[5] = gi*thcl*(y[8]-y[5])/vb[5]                          # IP

        yp[6] = thcl*(y[9]-y[6])/vb[6]                             # DA
        yp[7] = ga*thcl*(y[6]-y[7])/vb[7]                          # DI
        yp[8] = gi*thcl*(y[7]-y[8])/vb[8]                          # DP

        yp[9] = thcl*(y[3]-y[9])/vb[9]                             # H-box

    elif fconvl == 2:
        yp[5] = (ga*thcl*y[4] + ta*thcl*y[8] - thcl*y[5])/vb[5]    # IP
        yp[4] = (gi*thcl*y[3] + ti*thcl*y[7] - ga*thcl*y[4])/vb[4] # II
        yp[3] = gi*thcl*(y[6]-y[3])/vb[3]                          # IA
        yp[8] = thcl*(y[9]-y[8])/vb[8]                             # DP
        yp[7] = ga*thcl*(y[8]-y[7])/vb[7]                          # DI
        yp[6] = gi*thcl*(y[7]-y[6])/vb[6]                          # DA
        yp[9] = thcl*(y[5]-y[9])/vb[9]                            # H

        yp[3] = yp[3] + fa*tsol*(y[6]-y[3])/vb[3]                  # IA
        yp[4] = yp[4] + fi*tsol*(y[7]-y[4])/vb[4]                  # II
        yp[5] = yp[5] + fp*tsol*(y[8]-y[5])/vb[5]                  # IP
        yp[6] = yp[6] + fa*tsol*(y[9]-y[6])/vb[6]                  # DA
        yp[7] = yp[7] + fi*tsol*(y[9]-y[7])/vb[7]                  # DI
        yp[8] = yp[8] + fp*tsol*(y[9]-y[8])/vb[8]                  # DP
        yp[9] = yp[9] + (fa*tsol*(y[3]-y[9]) + fi*tsol*(y[4]-y[9]) + fp*tsol*(y[5]-y[9]))/vb[9]

    elif fconvl == 3:
        yp[3] = fa*thcl*(y[6]-y[3])/vb[3]
        yp[4] = fi*thcl*(y[7]-y[4])/vb[4]
        yp[5] = fp*thcl*(y[8]-y[5])/vb[5]
        yp[6] = fa*thcl*(y[9]-y[6])/vb[6]
        yp[7] = fi*thcl*(y[9]-y[7])/vb[7]
        yp[8] = fp*thcl*(y[9]-y[8])/vb[8]
        yp[9] = (fa*thcl*(y[3]-y[9]) + fi*thcl*(y[4]-y[9]) + fp*thcl*(y[5]-y[9]))/vb[9]

    if FTYS:
        yp[10] = ttol*(y[1]-y[10])/vb[10]
        yp[12] = ttol*(y[10]-y[12])/vb[12]
        yp[7] = yp[7] + ttol*(y[12]-y[7])/vb[7]
        yp[4] = yp[4] + ttol*(y[7]-y[4])/vb[4]
        yp[1] = yp[1] + ttol*(y[4]-y[1])/vb[1]

    # mixing AIP H
    # for k in range(3):
    #     yp[k] = yp[k] + mvl[k]*(y[k+3]-y[k])/vb[k]
    #     yp[k+3] = yp[k+3] + mvl[k]*(y[k]-y[k+3])/vb[k+3]
    #     yp[k+6] = yp[k+6] + mhdl[k]*(y[9]-y[k+6])/vb[k+6]
    #     yp[9] = yp[9] + mhdl[k]*(y[k+6]-y[9])/vb[9]
    yp[0:3] = yp[0:3] + mvl[0:3]*(y[3:6]-y[0:3])/vb[0:3]
    yp[3:6] = yp[3:6] + mvl[0:3]*(y[0:3]-y[3:6])/vb[3:6]
    yp[6:9] = yp[6:9] + mhdl[0:3]*(y[9]-y[6:9])/vb[6:9]
    yp[9] = yp[9] + np.sum(mhdl[0:3]*(y[6:9]-y[9])/vb[9])

    if FTYS:
        yp[11] = mvl[3]*(y[10]-y[11])/vb[11]
        yp[10] = yp[10] + mvl[3]*(y[11] -y[10])/vb[10]
        yp[11] = yp[11] + mvl[4]*(y[4]-y[11])/vb[11]
        yp[4] = yp[4] + mvl[4]*(y[11]-y[4])/vb[4]
        yp[10] = yp[10] + mhdl[3]*(y[12]-y[10])/vb[10]
        yp[12] = yp[12] + mhdl[3]*(y[10]-y[12])/vb[12]

    return yp
