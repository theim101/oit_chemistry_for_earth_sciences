#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 2018
Modules for extracting data from the Chronos database

@author: T.J. Heimovaara
"""
# %%
import sqlalchemy as sa
import pandas as pd
import numpy as np
import scipy as sp
import os
import subprocess, shlex
from collections import namedtuple
import seaborn as sns
import matplotlib.pyplot as plt


conn_str = 'mysql+pymysql://Guest_01:TUDelft01@localhost:3307/database_iDS05'

# %%
def wastebodyPropertiesWM(cellIdx):

    lFCode = np.array(['VP-06','VP-05a'])
    baseArea = np.array([26529,20118]) #m2
    topArea = np.array([7929,14013]) #m2

    # Heights of waste body estimated from the AHN data viewer    
    topHeight = np.array([10.5, 10.5])
    edgeHeight = np.array([-0.40, -0.40])
    baseHeight = np.array([-4.0, -4.0])
    
    slopeArea = baseArea-topArea
    slopeWidth = [47,52]
    slopeLength = slopeArea/slopeWidth
    lFHeightAboveGround = topHeight-edgeHeight
    lFHeightBelowGround = edgeHeight-baseHeight
    surfArea = slopeLength *slopeWidth + topArea
    
    lFVolume = lFHeightBelowGround * baseArea + lFHeightAboveGround * (0.5*slopeLength *slopeWidth + topArea)
    totVolume = sum(lFVolume)
    totWetWeight = [281083e3, 268407e3] #kg
    wetWeight = totWetWeight*lFVolume/totVolume;
    wetDensity = wetWeight/lFVolume;
    lFHeight = lFVolume / baseArea

    lFProp = {'code': lFCode[cellIdx],
              'volume': lFVolume[cellIdx],
              'wetWeight': wetWeight[cellIdx],
              'wetDensity': wetDensity[cellIdx],
              'surfArea': surfArea[cellIdx],
              'baseArea': baseArea[cellIdx],
              'height': lFHeight[cellIdx],
              'cl_height': 1.5}
    lF = pd.DataFrame(lFProp,index = [lFCode[cellIdx]])
    return lF

def wastebodyPropertiesBB(cellIdx):

    lFCode = np.array(['PP-11N','PP-11Z','PP-12'])
    baseArea = np.array([34802,35188,30000]) #m2 From GIS
    topArea = np.array([20778,24365,16303]) #m2
    topHeight = np.array([9.4, 9, 9.2])
    edgeHeight = np.array([-0.40, -0.40, -0.40])
    baseHeight = np.array([-2.5, -3.5, -3.5])
    slopeArea = baseArea-topArea
    slopeWidth = 28
    slopeLength = slopeArea/slopeWidth
    lFHeightAboveGround = topHeight-edgeHeight
    lFHeightBelowGround = edgeHeight-baseHeight
    surfArea = slopeLength *slopeWidth + topArea
    lFVolume = lFHeightBelowGround * baseArea + lFHeightAboveGround * (0.5*slopeLength *slopeWidth + topArea)
    totVolume = sum(lFVolume)
    totWetWeight = 1216723e3 #kg
    wetWeight = totWetWeight*lFVolume/totVolume
    wetDensity = wetWeight/lFVolume
    lFHeight = lFVolume / baseArea

    lFProp = {'code': lFCode[cellIdx],
          'volume': lFVolume[cellIdx],
          'wetWeight': wetWeight[cellIdx],
          'wetDensity': wetDensity[cellIdx],
          'surfArea': surfArea[cellIdx],
          'baseArea': baseArea[cellIdx],
          'height': lFHeight[cellIdx],
          'cl_height': 1.5
        }
    lF = pd.DataFrame(lFProp,index = [lFCode[cellIdx]])
    return lF

def wastebodyPropertiesKR(cellIdx):

    lFCode = np.array(['KR3','KR4'])
    #topArea = np.array([49700,59750]) #m2
    #baseArea = np.array([56750, 59750]) #m2
    topArea = np.array([57593.0,61012.0]) #m2
    baseArea = np.array([56137.0, 58206.0]) #m2
    
    baseLevel = np.array([5.04, 5.01]) # m
    wasteVolume = np.array([851561.0, 622421.0]) #m3 obtained from Attero
    ClHeight = 0.5

    #slopeArea = baseArea-topArea
    #slopeWidth = 60
    #slopeLength = slopeArea/slopeWidth
    #lFHeight = wasteVolume/baseArea + 0.5
    #surfArea = slopeLength *slopeWidth + topArea
    lFHeight = wasteVolume / baseArea
    lFVolume = wasteVolume + 0.5*topArea  # assume a coverlayer of 50 cm

    wetWeight = wasteVolume*1300.0 + 0.5*topArea*1800 #kg wet waste density of 1300 kg/m3 and wet soil density of 1800 (20 % moisture)
    wetDensity = wetWeight/lFVolume

    drainWidth = [159, 147] # [m]width of base liner in order to calculate the storage volume in the drainage system
    #drainLength = np.array([0,24,82,96,215,344]) # cumulative length of drain sections in drainage system
    #drainHeight = np.array([5.15, 5.85, 6.20, 6.35, 6.85, 6.85]) # cumulative height of drain sections in drainage system (with respect to NAP)
    drainLength = np.array([-6., 0., 22., 208., 325., 347., 353.]) # cumulative length of drain sections in drainage system
    drainHeight = np.array([8., 5.192, 5.920, 6.841, 6.948, 6.948, 8.]) # cumulative height of drain sections in drainage system (with respect to NAP)
    drainPor = 0.3 # porosity in drainage system
    # include rectangles for earlier sections...
   


    lFProp = {'code': lFCode[cellIdx],
          'volume': lFVolume[cellIdx],
          'wetWeight': wetWeight[cellIdx],
          'wetDensity': wetDensity[cellIdx],
          'surfArea': topArea[cellIdx],
          'baseArea': baseArea[cellIdx],
          'height': lFHeight[cellIdx],
          'drainWidth': drainWidth[cellIdx],
          'drainLength': drainLength,
          'drainHeight': drainHeight,
          'drainPor': drainPor,
          'ClHeight': ClHeight,
          }
    lF = pd.Series(lFProp)
    return lF


def download_sens_data_Kragge (pklfiles):
    # function checks if pklfile[0] exists, if not it will run a query on Chronos and download the relevant data and
    # save the data to the pklfile (in the format defined by the calling function)

    ## Index to sensor names in the data base

    #   | Cell     | type      | code |
    #   | -------- | --------- | ---- |
    #   |Kragge 4: |flow meter |CF014, CF_014_o |
    #   |          |level meter|CL014, CL_014_o|
    #   |          |temperature|CT015|
    #   |          |EC         |CQ001|
    #   |Kragge 3: |flow meter |CF013, CF_013_o||
    #   |          |level meter|CL012, CL_012_o|
    #   |          |level meter BB002| CL008|
    #   |Kragge 2: |flowmeter |CF015 |     
    #   |PumpPit 3:|level meter |CL008|
    #   |          |EC| CQ002|
    #   |PumpPit 4:|level meter| CL003| 
    #   |Infil Pit | level meter| CL007|
    #   |          |temperature |CT008|
    
    # select the data for the different sensors per group
    
    flow_sensnm = "'CF013', 'CF_013_o', 'CF014', 'CF_014_o', 'CF001', 'CF015'"
    level_sensnm = "'CL012', 'CL_012_o', 'CL014', 'CL_014_o', 'CL008'"
    infil_sensnm = "'CF001', 'CF001_1', 'CF001_2', 'CF001_2', 'CF001_3', 'CF001_4', 'CF001_5', 'CF001_6', 'CF001_7', 'CF001_8'"

    sql_query = ("select fs.sensorno, fs.sensorname, sm.datetime, sm.componentno, "\
                "c.name_nl as cname, sm.value, u.name_nl as uname "\
                "from fieldsensor as fs, sensormeas as sm, component as c, "
                "unit as u where fs.sensorno = sm.sensorno and "\
                "sm.unitno = u.unitno and sm.componentno=c.componentno "\
                "and fs.sensorname in (" + flow_sensnm + ") and sm.componentno = 22701 "\
                "and sm.datetime >= '2011-01-01 00:00:00'") 

    #import the data in to a dataframe
    if not (os.path.exists(pklfiles['cumflow'])):
        db_engine = sa.create_engine(conn_str)

        df_cumflow = pd.read_sql_query(sql_query,db_engine)
        df_cumflow.to_pickle(pklfiles['cumflow'], compression='infer')
    else:
        # if the first file exists, we assume the second does as well
        df_cumflow = pd.read_pickle(pklfiles['cumflow'])
    
    # Instantaneous Flow data
    sql_query = ("select fs.sensorno, fs.sensorname, sm.datetime, sm.componentno, "\
                "c.name_nl as cname, sm.value, u.name_nl as uname "\
                "from fieldsensor as fs, sensormeas as sm, component as c, "
                "unit as u where fs.sensorno = sm.sensorno and "\
                "sm.unitno = u.unitno and sm.componentno=c.componentno "\
                "and fs.sensorname in (" + flow_sensnm + ") and sm.componentno = 22728 "\
                "and sm.datetime >= '2011-01-01 00:00:00'") 

    #import the data in to a dataframe
    if not (os.path.exists(pklfiles['flow'])):
        db_engine = sa.create_engine(conn_str)

        df_flow = pd.read_sql_query(sql_query,db_engine)        
        df_flow.to_pickle(pklfiles['flow'], compression='infer')
    else:
        # if the first file exists, we assume the second does as well
        df_flow = pd.read_pickle(pklfiles['flow'])
    
    # Level data
    sql_query = ("select fs.sensorno, fs.sensorname, sm.datetime, sm.componentno, "\
                "c.name_nl as cname, sm.value, u.name_nl as uname "\
                "from fieldsensor as fs, sensormeas as sm, component as c, "
                "unit as u where fs.sensorno = sm.sensorno and "\
                "sm.unitno = u.unitno and sm.componentno=c.componentno "\
                "and fs.sensorname in (" + level_sensnm + ") "\
                "and sm.datetime >= '2011-01-01 00:00:00'") 

    if not (os.path.exists(pklfiles['level'])):
        db_engine = sa.create_engine(conn_str)

        df_level = pd.read_sql_query(sql_query,db_engine)        
        df_level.to_pickle(pklfiles['level'], compression='infer')
    else:
        # if the first file exists, we assume the second does as well
        df_level = pd.read_pickle(pklfiles['level'])
    

    sql_query = ("select fs.sensorno, fs.sensorname, sm.datetime, sm.componentno, "\
                "c.name_nl as cname, sm.value, u.name_nl as uname "\
                "from fieldsensor as fs, sensormeas as sm, component as c, "
                "unit as u where fs.sensorno = sm.sensorno and "\
                "sm.unitno = u.unitno and sm.componentno=c.componentno "\
                "and fs.sensorname in (" + infil_sensnm + ") and sm.componentno = 22701 "\
                "and sm.datetime >= '2011-01-01 00:00:00'") 

    #import the data in to the dataframe df_inline
    if not (os.path.exists(pklfiles['infil'])):
        db_engine = sa.create_engine(conn_str)

        df_cum_infil = pd.read_sql_query(sql_query,db_engine)     
        df_cum_infil.to_pickle(pklfiles['infil'], compression='infer')
    else:
        # if the first file exists, we assume the second does as well
        df_cum_infil = pd.read_pickle(pklfiles['infil'])
    
    
    
    ## create pivot tables for easy handling
    # old cumflow data are given in 
    #df_cumflow.loc[(df_cumflow['sensorname']=='CF_013_o'),'value'] *= 0.01
    #df_cumflow.loc[(df_cumflow['sensorname']=='CF_014_o'),'value'] *= 0.01

    #df_level.loc[(df_level['sensorname']=='CL_012_o'),'value'] *= 0.001
    #df_level.loc[(df_level['sensorname']=='CL_014_o'),'value'] *= 0.001

    cumflow_data = pd.pivot_table(df_cumflow, values='value', index=['datetime'],
                    columns=['sensorname'], aggfunc='mean')
    flow_data = pd.pivot_table(df_flow, values='value', index=['datetime'],
                    columns=['sensorname'], aggfunc='mean')
    level_data = pd.pivot_table(df_level, values='value', index=['datetime'],
                    columns=['sensorname'], aggfunc='mean')

    cum_infil_data = pd.pivot_table(df_cum_infil, values='value', index=['datetime'],
                    columns=['sensorname'], aggfunc='mean')

    return cumflow_data, flow_data, level_data, cum_infil_data


def download_sens_data_BB (pklfiles, sens_names):
    # function checks if pklfile[0] exists, if not it will run a query on Chronos and download the relevant data and
    # save the data to the pklfile (in the format defined by the calling function)

    ## Index to sensor names in the data base
    # 4	Flow_VP-06Cum	cumulative flow	2001-01-01		3327	VP-06		leachate flow	3327	VP-06
    # 13	Level_VP-06	peil	2001-01-01		3327	VP-06		level sensor	3327	VP-06   

    # select the data for the different sensors per group
    flow_sensnm = sens_names['flowsens']
    level_sensnm = sens_names['levelsens']
        
    sql_query = ("select fs.sensorno, fs.sensorname, sm.datetime, sm.componentno, "\
                "c.name_nl as cname, sm.rawvalue, u.name_nl as uname "\
                "from fieldsensor as fs, sensormeas as sm, component as c, "
                "unit as u where fs.sensorno = sm.sensorno and "\
                "sm.unitno = u.unitno and sm.componentno=c.componentno "\
                "and fs.sensorname in ('" + flow_sensnm + "') and sm.componentno = 22701 "\
                "and sm.datetime >= '2012-06-01 00:00:00'") 

    #import the data in to a dataframe
    if not (os.path.exists(pklfiles['cumflow'])):
        db_engine = sa.create_engine(conn_str)

        df_cumflow = pd.read_sql_query(sql_query,db_engine)
        df_cumflow.to_pickle(pklfiles['cumflow'], compression='infer')
    else:
        # if the first file exists, we assume the second does as well
        df_cumflow = pd.read_pickle(pklfiles['cumflow'])
    
    # Level data
    sql_query = ("select fs.sensorno, fs.sensorname, sm.datetime, sm.componentno, "\
                "c.name_nl as cname, sm.value, u.name_nl as uname "\
                "from fieldsensor as fs, sensormeas as sm, component as c, "
                "unit as u where fs.sensorno = sm.sensorno and "\
                "sm.unitno = u.unitno and sm.componentno=c.componentno "\
                "and fs.sensorname in ('" + level_sensnm + "') "\
                "and sm.datetime >= '2012-06-01 00:00:00'") 

    if not (os.path.exists(pklfiles['level'])):
        db_engine = sa.create_engine(conn_str)

        df_level = pd.read_sql_query(sql_query,db_engine)        
        df_level.to_pickle(pklfiles['level'], compression='infer')
    else:
        # if the first file exists, we assume the second does as well
        df_level = pd.read_pickle(pklfiles['level'])
    

    cumflow_data = pd.pivot_table(df_cumflow, values='rawvalue', index=['datetime'],
                    columns=['sensorname'], aggfunc='mean')
    level_data = pd.pivot_table(df_level, values='value', index=['datetime'],
                    columns=['sensorname'], aggfunc='mean')

    return cumflow_data, level_data


def download_watertreatment_dataKR_dilution(pklfiles):
    # function to download sensordata for watertreatment plant KR
    # function uses downloaded data to calcualate daily dilution factor for concentration
    # infiltrated water
    # Assumpution: very short residence time in WT plant, dilution factor directly applied
    # to concentration drainage

    # Suppletion 	|flowmeter 	|CF007 	|m3/hr|
    # Nitratation 	|flowmeter 	|CF008 	|m3/hr|
    # Nitratation to slibbuffer |flowmeter 	|CF009 	|m3/hr|
    # Demon 	flowmeter 	|CF010 	|m3/hr|
    # Demon to infilpit 	|flowmeter 	|CF010_1 	|m3/hr|
    # Demon to effluent 	flowmeter 	|CF010_2| 	|m3/hr|
    # Demon to slibbuffer 	|flowmeter |CF010_3 	|m3/hr|
    
    # flow in water treatment plant (to estimate dilution and discharge? in m3/hour)
    wt_sensnm = "'CF007', 'CF008', 'CF009', 'CF010', 'CF010_1', 'CF010_2', 'CF010_3', 'CF001', 'CF013' "
    
    sql_query = ("select fs.sensorno, fs.sensorname, sm.datetime, sm.componentno, "\
                "c.name_nl as cname, sm.value, u.name_nl as uname "\
                "from fieldsensor as fs, sensormeas as sm, component as c, "
                "unit as u where fs.sensorno = sm.sensorno and "\
                "sm.unitno = u.unitno and sm.componentno=c.componentno "\
                "and fs.sensorname in (" + wt_sensnm + ") and sm.componentno = 22728 "\
                "and sm.datetime >= '2018-01-01 00:00:00'") 

    #import the data in to the dataframe df_inline

    if not (os.path.exists(pklfiles['water_treatment'])):
        db_engine = sa.create_engine(conn_str)

        df_wt_flow = pd.read_sql_query(sql_query,db_engine)     
        df_wt_flow.to_pickle(pklfiles['water_treatment'], compression='infer')
    else:
        # if the first file exists, we assume the second does as well
        df_wt_flow = pd.read_pickle(pklfiles['water_treatment']) 
    
        
    
    # sensors give flow rates in m3/hour, we need to cumulate and
    # extract daily cumulative flows
    
    # create a pivot_table from dt_wt_flow
    df_wt = df_wt_flow.pivot_table(index='datetime',columns='sensorname',
                                  values='value',aggfunc='mean')
    selidx = df_wt.isna()
    df_wt[selidx] = 0
    selidx = df_wt < 0
    df_wt[selidx] = 0
    
    if df_wt.index.dtype == '<M8[us]':
        units_per_sec = 1e6
    else:
        units_per_sec = 1e9

    # calculate time step between measureemnts, translate to hours
    delta_t = df_wt.index.diff().values.astype(float)/(units_per_sec*3600)

    # calculate hourly cumulative flow
    df_cum_wt = np.cumsum(df_wt.iloc[:-1] * delta_t.reshape(len(delta_t),1)[1:])

    df_cum_wt = df_cum_wt - df_cum_wt.iloc[0] 
    
    # create final result dataframe to store daily interpolated values    
    # We obtain the days from one of the dataseries...
    
    trange = df_cum_wt.index.floor('1d').unique()

    # initialze wt_totF for daily flow and dilution
    wt_totF = pd.DataFrame(index=trange)
    for sensnm in df_cum_wt.columns:

        finter = sp.interpolate.interp1d(
            df_cum_wt.index.astype(np.int64),
            df_cum_wt[sensnm].values, fill_value="extrapolate")

        totF_val = finter(trange.astype(np.int64))
        wt_totF[sensnm] = totF_val - totF_val[0]  
    
    # estimate total infiltration and correct for discharge
    wt_totF['suppletion_to_infil'] = wt_totF['CF007']
    wt_totF['demon_to_infil'] = wt_totF['CF010_1']
    wt_totF['nitrat_to_infil'] = (wt_totF['CF008']-wt_totF['CF009'])

    suppletion = wt_totF['suppletion_to_infil'].diff()
    demon = wt_totF['demon_to_infil'].diff()
    nitrat = wt_totF['nitrat_to_infil'].diff()

    # replace nitrat to infil should be >= 0!
    selidx = nitrat < 0
    nitrat.loc[selidx] = 0

    selidx = demon < 0
    demon.loc[selidx] = 0

    wt_totF['dilution_factor'] = (nitrat + demon) / (suppletion + nitrat + demon + 1e-20)

    sel_idx = wt_totF['dilution_factor'].isna()
    wt_totF.loc[sel_idx,'dilution_factor'] = 1.0

    
    return wt_totF    
     
            
def download_sens_data_WM (pklfiles):
    # function checks if pklfile[0] exists, if not it will run a query on Chronos and download the relevant data and
    # save the data to the pklfile (in the format defined by the calling function)

    ## Index to sensor names in the data base
    # 4	Flow_VP-06Cum	cumulative flow	2001-01-01		3327	VP-06		leachate flow	3327	VP-06
    # 13	Level_VP-06	peil	2001-01-01		3327	VP-06		level sensor	3327	VP-06   

    # select the data for the different sensors per group
    
    flow_sensnm = "'Flow_VP-06Cum'"
    level_sensnm = "'Level_VP-06'"
    
    sql_query = ("select fs.sensorno, fs.sensorname, sm.datetime, sm.componentno, "\
                "c.name_nl as cname, sm.rawvalue, u.name_nl as uname "\
                "from fieldsensor as fs, sensormeas as sm, component as c, "
                "unit as u where fs.sensorno = sm.sensorno and "\
                "sm.unitno = u.unitno and sm.componentno=c.componentno "\
                "and fs.sensorname in (" + flow_sensnm + ") and sm.componentno = 22701 "\
                "and sm.datetime >= '2011-01-01 00:00:00'") 

    #import the data in to a dataframe
    if not (os.path.exists(pklfiles['cumflow'])):
        db_engine = sa.create_engine(conn_str)

        df_cumflow = pd.read_sql_query(sql_query,db_engine)
        df_cumflow.to_pickle(pklfiles['cumflow'], compression='infer')
    else:
        # if the first file exists, we assume the second does as well
        df_cumflow = pd.read_pickle(pklfiles['cumflow'])
    
    # Level data
    sql_query = ("select fs.sensorno, fs.sensorname, sm.datetime, sm.componentno, "\
                "c.name_nl as cname, sm.value, u.name_nl as uname "\
                "from fieldsensor as fs, sensormeas as sm, component as c, "
                "unit as u where fs.sensorno = sm.sensorno and "\
                "sm.unitno = u.unitno and sm.componentno=c.componentno "\
                "and fs.sensorname in (" + level_sensnm + ") "\
                "and sm.datetime >= '2011-01-01 00:00:00'") 

    if not (os.path.exists(pklfiles['level'])):
        db_engine = sa.create_engine(conn_str)

        df_level = pd.read_sql_query(sql_query,db_engine)        
        df_level.to_pickle(pklfiles['level'], compression='infer')
    else:
        # if the first file exists, we assume the second does as well
        df_level = pd.read_pickle(pklfiles['level'])
    

    
    ## create pivot tables for easy handling
    # old cumflow data are given in 
    #df_cumflow.loc[(df_cumflow['sensorname']=='CF_013_o'),'value'] *= 0.01
    #df_cumflow.loc[(df_cumflow['sensorname']=='CF_014_o'),'value'] *= 0.01

    #df_level.loc[(df_level['sensorname']=='CL_012_o'),'value'] *= 0.001
    #df_level.loc[(df_level['sensorname']=='CL_014_o'),'value'] *= 0.001

    cumflow_data = pd.pivot_table(df_cumflow, values='rawvalue', index=['datetime'],
                    columns=['sensorname'], aggfunc='mean')
    level_data = pd.pivot_table(df_level, values='value', index=['datetime'],
                    columns=['sensorname'], aggfunc='mean')

    return cumflow_data, level_data

def download_lab (pump_code,pklfile):
    # function checks if pklfile[0] exists, if not it will run a query on Chronos and download the relevant data and
    # save the data to the pklfile (in the format defined by the calling function)

    # components: 
    # Cl:508, 
    # NH4: 289
    # NH4 as N: 290, 
    # NH4 as NH4: 291
    # Br:391, 
    # TOC: 1574, 
    # DOC: 684
    clist = '508, 289,290,291,391, 1574, 684, 2631'

    '''
    684     DOC
    965	    Koolstof (totaal)
    1313	Opgelost organisch koolstof (DOC)
    1318	Organisch koolstof
    1572	Totaal anorganisch koolstof (TIC)
    1574	Totaal organisch koolstof (TOC)
    2631    DOC uitloogbaar
    999811	totaal organisch koolstof
    999867	particulair organisch koolstof
    999879	organisch koolstof
    999949	opgelost organisch koolstof
    '''

    if pump_code =='PP-11N':
        measpointno = '3033'
    elif pump_code =='PP-11Z':
        measpointno = '3034'
    elif pump_code =='PP-12':
        measpointno = '3032'
    elif pump_code == 'VP-06':
        measpointno = '9638'
    elif pump_code == 'KR_cell3':
        measpointno = '9726'
    elif pump_code == 'KR_cell4':
        measpointno = '9728'

    # check if pickel file exists
    if not (os.path.exists(pklfile)):
        # Need to query the data base for online sensor and manual gas measurements
        # Open a connection
        db_engine = sa.create_engine(conn_str)

        ## Read the inline measurements from the database
        # define the query, we need to extract data from the tables: fieldsensor,
        # sensormeas, component and unit. We explicitly select the sensor numbers
        # of the inline sensors. Please note the list of sensor-
        # numbers can be found by querying the database...
        sql_query = ("select s.date, s.measpointno, mp.measpointname, "
            "a.componentno, avg(a.value) as value, c.name_nl as cname, u.name_nl as uname "
            "from measurement_point mp, sample s, analysis a, component c, unit u "
            "where s.measpointno = mp.measpointno "
            "and s.sampleno = a.sampleno and a.componentno = c.componentno "
            "and a.unitno = u.unitno "
            "and s.measpointno = " + measpointno + " "
            "and a.componentno in (" + clist +") "
            "group by s.measpointno, s.date, a.componentno")

        # import the data in to the dataframe df_inline
        df_lab = pd.read_sql_query(sql_query, db_engine)
        # save df_inline to a pickle file
        df_lab.to_pickle(pklfile, compression='infer')
    else:
        # if the first file exists, we assume the second does as well
        df_lab = pd.read_pickle(pklfile)

    return df_lab


def download_meteoKNMI (t_range, weather_station, pklfile):
    # This function runs a command line argument to download data from
    # the KNMI website. The meteo station code is given in weather_station
    # the time range for the data is given in the tuple t_range

    # two meteo stations:
    # 249:         4.979       52.644      -2.50  BERKHOUT
    # 269:         5.526       52.458      -4.00  LELYSTAD

    # 340: Woensdrecht
    # 350: Gilze-Rijen
    # download rainfall data in t_range to 0DailyDataRLT.txt
    #http://projects.knmi.nl/klimatologie/daggegevens/getdata_dag.cgi
    #!wget -O 0DailyDataRLT.txt --post-data="stns=249:269&vars=ALL&start=20000101&end20180915" http://projects.knmi.nl/klimatologie/daggegevens/getdata_dag.cgi
    # check if pickel file exists
    
    #wget -O bestand --no-check-certificate --post-data="variabele=waarde&variabele=waarde&...." https://www.daggegevens.knmi.nl/klimatologie/daggegevens
    if not (os.path.exists(pklfile)):
        my_command = 'wget -O 0DailyDataRLT.txt --no-check-certificate --post-data="stns=' + weather_station \
            + '&vars=ALL&start=' + t_range[0] + '&end=' + t_range[1] \
            + '"  https://www.daggegevens.knmi.nl/klimatologie/daggegevens'

        my_args = shlex.split(my_command)

        subprocess.run(my_args)  # doesn't capture output

        m_dat = pd.read_csv('0DailyDataRLT.txt', sep=',', header=None, engine='c',
                   comment='#', parse_dates=True,
                   names= ['STN','YYYYMMDD','DDVEC','FHVEC','FG','FHX','FHXH',
                           'FHN','FHNH','FXX','FXXH','TG','TN','TNH','TX','TXH', 
                           'T10N','T10NH','SQ','SP','Q','DR','RH','RHX','RHXH',
                           'PG','PX','PXH','PN','PNH','VVN','VVNH','VVX','VVXH',   
                           'NG','UG','UX','UXH','UN','UNH','EV24'])
                   
        m_out = pd.DataFrame()
        m_out['datetime'] = pd.to_datetime(m_dat['YYYYMMDD'],format='%Y%m%d')
        m_out['rain'] = m_dat['RH']
        m_out['rain'] = m_out['rain'].replace(-1,0.25)
        m_out['rain'] = m_out['rain']/1e4
        m_out['pEV'] = m_dat['EV24']/1e4
        m_out['temp'] = m_dat['TG']/10
        m_out.set_index('datetime',inplace=True)

        # we only require rainfall data and potential evaporation
        # we also want change the YYYYMMDD column to a pandas datetime

        m_out.to_pickle(pklfile,compression='infer')
    else:
        m_out = pd.read_pickle(pklfile)
    return(m_out)

def remove_outliers_inline(inline_par):
    #inline_par.index = pd.to_datetime(inline_par.index)
    # resample from totalflow to daily data
    tmpF = inline_par.dropna(subset=['totalflow']).copy()
    #delt = np.diff(tmpF.index).astype('float64')/(1e9 * 3600)
    tmpF['diffFlow']=tmpF['totalflow'].diff()
    tmpF['flowR'] = tmpF['diffFlow']

    cidx = tmpF.columns == 'flowR'
    tmpF.iloc[0,cidx] = 0
    #tmpF[['totalflow','flowR','level']].plot(subplots=True,style='.-',grid=True)

    max_flow_ini = np.amax(tmpF['flowR'].iloc[0:20000])
    # Identify outliers using z-score
    zscore = (tmpF['flowR'] - tmpF['flowR'].mean())/tmpF['flowR'].std(ddof=0)
    tmpF['outliers_zscore'] = np.abs(zscore) > 3

    outlieridx = np.where(tmpF.outliers_zscore==True)[0]
    rngidx = np.where(tmpF['flowR'].iloc[outlieridx[1]:outlieridx[1]+10000]> 5*max_flow_ini)
    lastidx = outlieridx[1] + rngidx[0][-1]

    # slope of flowR between outlieridx[0] and outlieridx[1] is 50 times to high
    # slope of flowR between outlieridx[1] and lastidx is 10 times to high

    tmpF['cFlowR'] = tmpF['flowR']
    cidx = np.where(tmpF.columns == 'cFlowR')[0][0]
    tmpF.iloc[outlieridx[0]:outlieridx[1],cidx] = tmpF['flowR'].iloc[outlieridx[0]:outlieridx[1]]/50
    tmpF.iloc[outlieridx[1]:lastidx,cidx] = tmpF['flowR'].iloc[outlieridx[1]:lastidx]/10
    tmpF.iloc[outlieridx[0],cidx] = tmpF['cFlowR'].iloc[outlieridx[0]-1]
    tmpF.iloc[outlieridx[1],cidx] = tmpF['cFlowR'].iloc[outlieridx[1]-1]
    tmpF['totF'] = tmpF['cFlowR'].cumsum()

    totF = tmpF['totF']

    return totF

def remove_outliers_inlineBB(inline_par):
    #inline_par.index = pd.to_datetime(inline_par.index)
    # resample from totalflow to daily data
    tmpF = inline_par.dropna(subset=['totalflow']).copy()
    #delt = np.diff(tmpF.index).astype('float64')/(1e9 * 3600)
    tmpF['diffFlow']=tmpF['totalflow'].diff()
    tmpF['flowR'] = tmpF['diffFlow']

    cidx = tmpF.columns == 'flowR'
    tmpF.iloc[0,cidx] = 0
    #tmpF[['totalflow','flowR','level']].plot(subplots=True,style='.-',grid=True)

    # Identify outliers using z-score
    zscore = (tmpF['flowR'] - tmpF['flowR'].mean())/tmpF['flowR'].std(ddof=0)
    tmpF['outliers_zscore'] = np.abs(zscore) > 3

    outlieridx = np.where(tmpF.outliers_zscore==True)[0]
    # rngidx = np.where(tmpF['flowR'].iloc[outlieridx[1]:outlieridx[1]+10000]> 5*max_flow_ini)
    # lastidx = outlieridx[1] + rngidx[0][-1]

    # # slope of flowR between outlieridx[0] and outlieridx[1] is 50 times to high
    # # slope of flowR between outlieridx[1] and lastidx is 10 times to high

    tmpF['cFlowR'] = tmpF['flowR']
    cidx = np.where(tmpF.columns == 'cFlowR')[0][0]
    # tmpF.iloc[outlieridx[0]:outlieridx[1],cidx] = tmpF['flowR'].iloc[outlieridx[0]:outlieridx[1]]/50
    # tmpF.iloc[outlieridx[1]:lastidx,cidx] = tmpF['flowR'].iloc[outlieridx[1]:lastidx]/10
    tmpF.iloc[outlieridx,cidx] = tmpF['cFlowR'].iloc[outlieridx-1]
    
    # There have been moments when the settings of the pump were wrong,
    # leading too high or too low pumprates. This needs to be corrected manually
    # for each sensor
    
    ## PP-11N
    
    tmpF['totF'] = tmpF['cFlowR'].cumsum()

    totF = tmpF['totF']

    return totF

# def remove_outliers_inlineBB(totF0, level_data, t_range):

#     # %% Correct totalflow (remove drops in data set):
#     # replace nan in totflow column by interpolated values
#     totF1 = totF0[slice(t_range[0],t_range[1])].interpolate()
#     #totF1 = totF0
#     # difference in level
#     dlev = level_data.diff()

#     # cumulative drop in level...
#     dlev2 = np.cumsum(dlev*(dlev<0))

#     # Step 1
#     # Find the first negative flow,
#     # then correct the value based on the cumulative level change
#     # which has been calibrated using the level change from a
#     # time period of 4 days before the point of correction.
#     # We calibrate the level change by relating the total level change
#     # over 4 days with the cumulative pumped volume in these four days...
#     # correction is carried out on all subsequent data...

#     totF2 = totF1.copy()
#     # find the negative values in the gradient of the cumulative flow data set
#     idx1 = np.where(totF1['totalflow'].diff()<0)[0]

#     # create time series of four days before idx1
#     for ii in np.arange(len(idx1)):
#         irange = np.arange(idx1[ii]-24*4*4,idx1[ii])
#         cumQ = totF2['totalflow'].iloc[irange[-20]]-totF2['totalflow'].iloc[irange[0]]
#         dLevtot = dlev2[irange[-20]]-dlev2[irange[0]]
#         effSurf = -cumQ/dLevtot

#         # coordinate with negative diff value: idx1[0]
#         # replace value with
#         dQFlow = totF2['totalflow'].iloc[idx1[ii]-1] - \
#             totF2['totalflow'].iloc[idx1[ii]] + \
#             (dlev2[idx1[ii]-1]-dlev2[idx1[ii]])*effSurf

#         # add correction from dlev2: (dlev2[idx1[0]]-dlev2[idx1[0]])*effSurf

#         totF2['totalflow'].iloc[idx1[ii]:] += dQFlow

#     # Step 2

#     totF3 = totF2.copy()
#     # find the negative values in the gradient of the cumulative flow data set
#     idx2 = np.where(totF3['totalflow'].diff()>1000*totF3['totalflow'].diff().mean())[0]

#     for ii in np.arange(len(idx2)):
#         irange = np.arange(idx2[ii]-24*4*4,idx2[ii])
#         cumQ = totF3['totalflow'].iloc[irange[-20]]-totF3['totalflow'].iloc[irange[0]]
#         dLevtot = dlev2[irange[-20]]-dlev2[irange[0]]
#         effSurf = -cumQ/dLevtot

#         # coordinate with negative diff value: idx1[0]
#         # replace value with
#         dQFlow = totF3['totalflow'].iloc[idx2[ii]-1] - \
#             totF3['totalflow'].iloc[idx2[ii]] + \
#             (dlev2[idx2[ii]-1]-dlev2[idx2[ii]])*effSurf

#         # add correction from dlev2: (dlev2[idx1[0]]-dlev2[idx1[0]])*effSurf

#         totF3['totalflow'].iloc[idx2[ii]:] += dQFlow


#     return totF3['totalflow']

def download_meteoKNMI_etmgeg (t_range, weather_station, pklfile, inpfile):
    # This function runs a command line argument to download data from
    # the KNMI website. The meteo station code is given in weather_station
    # the time range for the data is given in the tuple t_range

    # two meteo stations:
    # 249:         4.979       52.644      -2.50  BERKHOUT
    # 269:         5.526       52.458      -4.00  LELYSTAD

    # 340: Woensdrecht
    # 350: Gilze-Rijen
    # download rainfall data in t_range to 0DailyDataRLT.txt
    #http://projects.knmi.nl/klimatologie/daggegevens/getdata_dag.cgi
    #!wget -O 0DailyDataRLT.txt --post-data="stns=249:269&vars=ALL&start=20000101&end20180915" http://projects.knmi.nl/klimatologie/daggegevens/getdata_dag.cgi
    # check if pickel file exists
    if not (os.path.exists(pklfile)):
        m_dat = pd.read_csv(inpfile, sep=',', header=None, engine='c',
               na_values='     ', comment='#', parse_dates=True, 
               infer_datetime_format=True, skiprows=48,
               names=['STN', 'YYYYMMDD', 'DDVEC', 'FHVEC', 'FG', 'FHX', 'FHXH',  
                      'FHN', 'FHNH', 'FXX', 'FXXH', 'TG', 'TN', 'TNH', 'TX', 'TXH', 
                      'T10N', 'T10NH', 'SQ', 'SP', 'Q', 'DR', 'RH', 'RHX', 'RHXH', 
                      'PG', 'PX', 'PXH', 'PN', 'PNH', 'VVN', 'VVNH', 'VVX', 'VVXH',
                      'NG', 'UG', 'UX', 'UXH', 'UN', 'UNH', 'EV24'])

        m_out = pd.DataFrame()
        m_out['datetime'] = pd.to_datetime(m_dat['YYYYMMDD'],format='%Y%m%d')
        m_out['rain'] = m_dat['RH']
        m_out['rain'] = m_out['rain'].replace(-1,0.25)
        m_out['rain'] = m_out['rain']/1e4
        m_out['pEV'] = m_dat['EV24']/1e4
        m_out['temp'] = m_dat['TG']/10
        m_out.set_index('datetime',inplace=True)

        # we only require rainfall data and potential evaporation
        # we also want change the YYYYMMDD column to a pandas datetime

        m_out.to_pickle(pklfile,compression='infer')
    else:
        m_out = pd.read_pickle(pklfile)
    return(m_out)
# %%
#-------# def remove_outliers(df, column):-----------
#     Q1, Q3 = df[column].quantile([0.25, 0.75])
#     IQR = Q3 - Q1
#     lower_bound, upper_bound = Q1 - 1. * IQR, Q3 + 1. * IQR
#     return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
#--------------------------------------------------------------------------------
def remove_outliers(df, column):
    """
    Removes outliers by keeping only the 1st-99th percentile range
    (the central 98%) in 'column'.
    """
    lower_bound, upper_bound = df[column].quantile([0.01, 0.99])
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
