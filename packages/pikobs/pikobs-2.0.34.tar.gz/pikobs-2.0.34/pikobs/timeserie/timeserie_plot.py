#!/usr/bin/env python3
#============================================
#---------------
# time_series
#---------------
#
#  Auteur : Pierre Koclas Aout 2021
#  But:
#         faire des graphes(images)
#         de series temporelles
#         a partir de fichiers  csv
#         generes par des scripts SQL.
#
#
import numpy as np
import sys
import csv
import dateutil
from datetime import datetime
#import matplotlib.dates as dates2
from matplotlib.dates import date2num
import pikobs
import math
from matplotlib.dates import MONDAY,MO, TU, WE, TH, FR, SA, SU
from matplotlib.dates import  DateFormatter, WeekdayLocator,DayLocator

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as pyplot
import sqlite3
def timeserie_plot(pathwork,
              datestart,
              dateend,
              fonctions,
              flag_type,
              family,
              region,
              fig_title,
              vcoord, 
              id_stn,
              varnos,
              files,
              names):
   
   mpl.style.use('classic')
   mpl.rcParams['lines.linewidth'] = 1.0
   mpl.rcParams['lines.dashed_pattern'] = [6, 6]
   mpl.rcParams['lines.dashdot_pattern'] = [3, 5, 1, 5]
   mpl.rcParams['lines.dotted_pattern'] = [1, 3]
   mpl.rcParams['lines.scale_dashes'] = False
   if isinstance(varnos, int):
       varnos = [varnos]

   for fonction in fonctions:
    for varno in varnos:
       FNAM, FNAMP, SUM, SUM2 = pikobs.type_boxes(fonction)
       
    
       Colors = ['#1f77b4',
                 '#ff7f0e',
                 '#2ca02c',
                 '#d62728',
                 '#9467bd',
                 '#8c564b',
                 '#e377c2',
                 '#7f7f7f',
                 '#bcbd22',
                 '#17becf',
                 '#1a55FF']
       num_lines=9
       #couleurs= [pyplot.cm.spectral(i) for i in np.linspace(0, 1, num_lines)]
       couleurs= [pyplot.cm.Set1(i) for i in np.linspace(0, 1, num_lines)]
       GREEN='#009900'
       BLUE='#0276FD'
       BLACK='#000000'
       RED='#D00000'
       couleurs[0]=BLUE
       couleurs[0]=RED
       #couleurs=Colors
       #---------
       Misgv=-999.
       MisgvN=0
       #---------
       
       vcotype={'PRESSION(Hpa)':'Pressure Hpa', 'HAUTEUR':'Height Km' ,  'CANAL':'Channel' , 'Surface':'Surface' , 'Surface_raob':'Surface_raob'}
       graphe_nomvar ={'11012':'WIND SPEED(10M)','11215':'U COMPONENT OF WIND (10M)','11216':'V COMPONENT OF WIND (10M)','12004':'DRY BULB TEMPERATURE AT 2M','10051':'PRESSURE REDUCED TO MEAN SEA LEVEL','10004':'PRESSURE','12203':'DEW POINT DEPRESSION (2M)','12001':'TEMPERATURE/DRY BULB','11003':'U COMPONENT OF WIND','11004':'V COMPONENT OF WIND','12192':'DEW POINT DEPRESSION','12163':'BRIGHTNESS TEMPERATURE','15036':'ATMOSPHERIC REFRACTIVITY','12101':'TEMPERATURE/DRY BULB','12239':'DEW POINT DEPRESSION'}
       
       # Ordre des colonnes par defaut generes par mes scripts SQL est;"
       #
       #SQL csv="select date , VARNO, Nrej,  Nacc , avg, avg2,std,std2,N, '1', VCORD"
       #                 0      1     2      3       4    5    6    7  8   9    10
       #                 0      1     2      3       4         5       6   7    8 
       graphe_colonnes ={'O-P':(4,6),'O-A':(5,7),'O-F':(4,6),'REJ':(2,8),'OBS':(4,6), 'P':(4,6),'O-P/P':(4,6),'O-A/P':(5,7),'O-A/A':(5,7)}
       
       variable_name, units, vcoord_type = pikobs.type_varno(varno)
       graphe1  =[]
       nfichiers= 1
       vcoord  = vcoord
       try:
          vcoord = int(vcoord)
       except ValueError:
          vcoord = vcoord 
       famille = f'Family:{family} id_stn:{id_stn} vcoord:{(vcoord)}'
       REGION1 = region
       varno   = varno 
       label   = f'Region:{region}'
       fonction= fonction
    #   fonction= 'omp'
       graphe1.append(fonction.strip)
       if varno  in graphe_nomvar :
         Nom=graphe_nomvar[varno]
       else:
         Nom=varno
       nfichiers=0
       if nfichiers >1:
        files.append(LARG[9])
        famille2 =LARG[10]
        REGION2  =LARG[11]
        varno2   =LARG[12]
        label2=   LARG[13]
        fonction2=LARG[14]
        graphe1.append(fonction2.strip)
        if varno2  in graphe_nomvar :
          Nom2=graphe_nomvar[varno]
        else:
          Nom2=varno
       
       VCO=[vcoord]
       
       vcoord_type=f'{variable_name} {units}'
       vcoord_type_e=vcoord_type
       
      # vcoord=''
       if  ( len(VCO) >1):
        vco1=VCO[1]
        if  ( len(VCO) ==3):
         vco2=VCO[2]
         vcoord=vco1
         if ( vco2 != ''):
          if ( vco1 != vco2):
           A=' To '
           vcoord=vco1+A+vco2
        else:
         vcoord=vco1
       
       ColB=5
       ColS=7
       ColN=9
       
       left = 0.1
       width = 0.8
       width = 0.9
       pyplot.close('all')

       fig = pyplot.figure(figsize=(18,6))
       fig = pyplot.figure(figsize=(14,5))
       ax1 = pyplot.axes([left, 0.58, width, 0.35])
       ax2 = pyplot.axes([left, 0.21, width, 0.25])
       ax3 = pyplot.axes([left, 0.01, width, 0.15])
       
       ax1.grid(True)
       ax2.grid(True)
       ax3.grid(True)
       
       # ticks at the top of the top plot
       ax1.xaxis.tick_bottom()
       
       # remove ticks for ax2 and ax3
       ax2.xaxis.set_visible(True)
       ax3.xaxis.set_visible(False)
       ax3.yaxis.set_visible(False)
       
       #2013-03-02 12:00:00        50000.0          1           589         0.4         2.4         589
       
       filenumb=0
       barwidth=[0.25,.15]
       TITRE=[]
       #files= [1, 1]
       for file in files :
        Bomp2=[] ; Somp2=[]
        Nomb2=[]
        Nrejets=[]
        Dates2=[]
       
        L1=[]
        rownum1 = 0
       
       # if graphe1[filenumb]   in graphe_colonnes :
       #  ColB,ColS=graphe_colonnes[graphe1[filenumb]]
       
      #  else :
      #   ColB,ColS=(5,7)
        ColB,ColS=(5,7)
    
       
       #filenumb=filenumb+1
        #hdl1 = open (file,'r') # Open file for reading
        #reader1 = csv.reader(hdl1,delimiter=",")
        #for row in reader1:
        #  L1.append( row ) 
        #  rownum1 += 1
       # exit()
        path_output_work=f'{pathwork}/timeserie_{datestart}_{dateend}_{fonction}_{flag_type}_{family}.db'
        conn = sqlite3.connect(file)
        # Create a cursor to execute SQL queries
        FNAM, FNAMP, SUM, SUM2 = pikobs.type_boxes(fonction)
        cursor = conn.cursor()
        cursor.execute("PRAGMA TEMP_STORE=memory")

        if id_stn =='join' and vcoord=='join' :
          crite ="  "
        if id_stn =='join' and vcoord!='join' :
          crite = f" and  vcoord = {vcoord} "

        if id_stn !='join' and vcoord=='join' :
          crite = f"and  id_stn= '{id_stn}'    "

        if id_stn !='join' and vcoord!='join' :
          crite = f"  and  vcoord = {vcoord} and id_stn= '{id_stn}'  "



 
        query = f"""
               SELECT
                   DATE,  --0
                   varno, --1
                   Nrej,  --2
                   Nacc,  --3
                   SUM({SUM})/SUM(CAST(N AS FLOAT)) AVG,    --4
                   SQRT(SUM({SUM2})/SUM(CAST(N AS FLOAT)) - SUM({SUM})/SUM(CAST(N AS FLOAT))*SUM({SUM})/SUM(CAST(N AS FLOAT))) STD, --5
                   SUM(sumstat)/SUM(CAST(N AS FLOAT)) BCORR,  --6
                   count(flag) --7
                   
               FROM
                   timeserie
                WHERE
                    varno='{varno}'
                    {crite}
                     
                GROUP BY
                    DATE;"""
        cursor.execute(query)
        results = cursor.fetchall() 
        Dates2  = np.array([row[0] for row in results])  #Dates
        Nrejets = np.array([row[2] for row in results])  #Chans
        Bomp2   = np.array([row[4] for row in results])  #AvgOMA
        Somp2   = np.array([row[5] for row in results])  #AvgOMP
        Nomb2  = np.array([row[3] for row in results])  #StdOMA
        bcorr  = np.array([row[6] for row in results])  #StdOMP
    
    
    
       #  print (  row )
       # L1.sort(key=lambda tup: tup[0])  
       # Dates2  =[da[0]   for da in L1]
       # Nrejets =[x[2]    for x  in L1]
       # Bomp2   =[x[ColB] for x  in L1]
       # Somp2   =[x[ColS] for x  in L1]
       # Nomb2   =[x[8]    for x  in L1]
       # Nprofils=[x[9]    for x  in L1]
       # Nomb2   =[x[9]    for x  in L1]
       # Nomb2   =[x[9]    for x  in L1]
       # bcorr   =[x[10]    for x  in L1]
       
        
    
        Sbcorr=np.zeros(len(Somp2))
        Sbcorr=[float(x) for x in bcorr]
       
        Snrej=np.zeros(len(Somp2))
        Snrej=[float(x) for x in Nrejets]
       
        Nb=np.zeros(len(Somp2))
        Nb=[float(x) for x in Nomb2]
       
        B1=np.zeros(len(Bomp2))
        B1=[float(x) for x in Bomp2]
       
        S1=np.zeros(len(Somp2))
        S1=[float(x) for x in Somp2]
        
    
        dates = [dateutil.parser.parse(s) for s in Dates2]
        
        debutD=Dates2[0]
        finD =Dates2[-1]
        debut=dates[0]
        debutD=debut.strftime("%Y-%m-%d-%H")
        
        fin  =dates[-1]
        finD=fin.strftime("%Y-%m-%d-%H")
        PERIODE=' From ' + debutD +'   to ' + finD
        LABEL1=label
        TITRE.append(PERIODE)

        legendlist=['μ' ,'σ']
        famille1=famille
        period=date2num(fin) - date2num(debut)  + .25
        if ( period <=6.):
         interval=1
        else:
         interval=4
        
       #----------------------------------------------------------------------
       
        x=date2num(dates)
       
        y1_values    = np.array(B1)
        Bomp2_masked = np.ma.masked_where(y1_values <= Misgv , y1_values)
        Bias=np.ma.compressed(Bomp2_masked)
       
        y1_values    = np.array(S1)
        Somp2_masked = np.ma.masked_where(y1_values <= Misgv ,  y1_values)
        Sigma=np.ma.compressed(Somp2_masked)
       
        y1_values    = np.array(Nb)
        NB_masked=np.ma.masked_where(y1_values <= MisgvN  ,  y1_values)
        Nomb=np.ma.compressed(NB_masked)
       
        y1_values    = np.ma.array(Snrej)
        SNrej_masked=np.ma.masked_where(y1_values <= Misgv ,  y1_values)
        NREJ=np.ma.compressed(SNrej_masked)
       
        y1_values    = np.array(Sbcorr)
        Bcorr_masked = np.ma.masked_where(y1_values <= Misgv , y1_values)
        Bcorr=np.ma.compressed(Bcorr_masked)
       
        Serie1=fonction
       
        xmi=x[0]
        xma=x[-1]
        ax1.set_xlim([xmi, xma])
       #=================================================================================================
        ax1.plot(x, Bomp2_masked, linestyle='--',marker='o', markersize=3,color=couleurs[filenumb-0],lw=2) 
        ax1.plot(x, Somp2_masked, linestyle='-', marker='p', markersize=4,color=couleurs[filenumb-0],lw=2) 
        if ( fonction == 'BIAS_CORR' or  fonction == 'OBS_ERROR' ):
           ax1.plot(x, Bcorr_masked, linestyle='-', marker='p', markersize=4,color='g',lw=2) 
        if ( fonction == 'NOBS' or  fonction == 'DENS'  ):
       #   ax1.plot(x, NB_masked, linestyle='-', marker='p', markersize=4,color='g',lw=2) 
           ax1.plot(x, NB_masked,drawstyle='steps',color='g')
       #=================================================================================================
       
        MdFmt = DateFormatter('%m-%d')
        for tick in ax1.xaxis.get_major_ticks():
             tick.label1.set_fontsize(10)

        ax1.xaxis.set_major_formatter(MdFmt)
        ax1.xaxis.set_major_locator(DayLocator(interval=interval))
       
       
       #ax1.xaxis.set_major_locator(mondays)
        ax1.xaxis_date()
       #ax1.set_ylabel(Serie1,color=couleurs[filenumb-1],bbox=dict(facecolor='w',boxstyle='round'),fontsize =10)
       
       #----------------------------------------------------------------------
       
       #======================================================================
        xmi=x[0]
        xma=x[-1]
        ax2.set_xlim([xmi, xma])
       #a ax2.set_ylim([0,100000])
        ax2.plot(x,NB_masked, linestyle='-',marker='o', drawstyle='steps', markersize=3 , color=couleurs[filenumb-0],lw=2)  
      #  ax2.plot(x,Nb,drawstyle='steps',color=couleurs[filenumb-0])
     #   ax1.set_ylim([-0.5, 5])
        ax2.plot(x,SNrej_masked, linestyle='--',marker='p',drawstyle='steps',markersize=4, color=couleurs[filenumb-0],lw=2)
       #======================================================================
        #ax2.plot(x,NREJ, linestyle='--', drawstyle='steps',color=couleurs[filenumb-0])
        
        MdFmt = DateFormatter('%m-%d')
        for tick in ax2.xaxis.get_major_ticks():
             tick.label1.set_fontsize(10)
        ax2.xaxis.set_major_formatter(MdFmt)
        ax2.xaxis.set_major_locator(DayLocator(interval=interval))
    
        ax2.xaxis_date()
       #======================================================================
        del(Bomp2) ; del(Somp2)
        del(Nomb2) 
        del(Nrejets)
        del(L1)
        del(Dates2)
       
        if len(Nomb) >0:
         
         Mu=sum(Bias*Nomb)/sum(Nomb)
       # Mu=sum(Bomp2_masked*NB_masked)/sum(NB_masked)
         Sx2=(Sigma*Sigma +Bias*Bias)*Nomb
       # Sx2=(Somp2_masked*Somp2_masked +Bomp2_masked*Bomp2_masked)*NB_masked
         Sig=math.sqrt(sum(Sx2)/sum(Nomb)  -Mu*Mu)
       
       
         STRING=f'{fonction} μ:{round(Mu,3)} σ:{round(Sig,3)} Nobs:{int(sum(Nomb))}'
         textstr=STRING
       
         ONMAP=int(sum(Nomb))
       # textstr = '$\mu=%.2f\sigma=%.2f$Nobs=%.2i'%(Mu, Sig, ONMAP)
       # textstr=STRING
         ax1.text(0.45, 1.12+(filenumb-0)/9., textstr, transform=ax1.transAxes, fontsize=11,
               verticalalignment='top', color=couleurs[filenumb])
       
        ax1.text(.00, 1.040, names[0]+' ',fontsize =11, color=couleurs[0], transform=ax1.transAxes)
        ax1.text( .1, 1.040, TITRE[0]+' ',fontsize =11, color=couleurs[0], transform=ax1.transAxes)
       
        ax3.text(.01 ,0.24, famille1     , fontsize =12, color=couleurs[0], transform=ax3.transAxes)
        #   ax3.text(.13, 0.24, REGION1        ,fontsize =12,color=couleurs[0],transform=ax3.transAxes)
        ax3.text(.32, 0.24,  vcoord_type_e ,fontsize =12,color=couleurs[0],transform=ax3.transAxes)
        #  ax3.text(.48, 0.24,                ,fontsize =12,color=couleurs[0],transform=ax3.transAxes)
        #  ax3.text(.58, 0.24, vcoord         ,fontsize =12,color=couleurs[0],transform=ax3.transAxes)
        ax3.text(.75, 0.24, LABEL1         ,fontsize =12,color=couleurs[0],transform=ax3.transAxes)
        import matplotlib.pyplot as plt
        from matplotlib.lines import Line2D
        l2=ax1.legend(legendlist, columnspacing=1, fancybox=True, ncol=2, shadow = False, loc = (0.80, +1.030))
       # plt.setp(l2.get_texts(), color='b')
        custom_line = Line2D([0], [0], color='g', lw=2, marker='o', markersize=3)  # Color verde en la leyenda
        l2.legendHandles[0].set_color('black')
        l2.legendHandles[1].set_color('black')
        legendlist2=['Nobs', 'Nrej']
        l3=ax2.legend(legendlist2, columnspacing=1, fancybox=True, ncol=2, shadow = False, loc = (0.80, +1.030))
        #plt.setp(l3.get_texts(), color='b')
        l3.legendHandles[0].set_color('black')
        l3.legendHandles[1].set_color('black')

         
        filenumb=filenumb +1
       
       if filenumb ==2:
        Serie2=names[1]
        LABEL2='aaa'#label2
    
        ax1.text(.00, 1.030 +.056*filenumb  , Serie2+' '  ,fontsize =11,color=couleurs[filenumb-1],transform=ax1.transAxes)
        ax1.text(.1, 1.030 +.056*filenumb  , TITRE[1]+' ',fontsize =11,color=couleurs[filenumb-1],transform=ax1.transAxes)
       
        ax3.text(.01 ,0.016 +.30*filenumb   ,famille     ,fontsize =12,color=couleurs[filenumb-1],transform=ax3.transAxes)
        #  ax3.text(.13, 0.015 +.30*filenumb   ,REGION1     ,fontsize =12,color=couleurs[filenumb-1],transform=ax3.transAxes)
        ax3.text(.32, 0.016 +.30*filenumb    ,vcoord_type_e       ,fontsize =12,color=couleurs[filenumb-1],transform=ax3.transAxes)
       
        #  ax3.text(.48, 0.016 +.30*filenumb, vcoord_type_e  ,fontsize =12,color=couleurs[filenumb-1],transform=ax3.transAxes)
        #  ax3.text(.58, 0.016 +.30*filenumb, vcoord         ,fontsize =12,color=couleurs[filenumb-1],transform=ax3.transAxes)
        ax3.text(.75, 0.016 +.30*filenumb ,LABEL1         ,fontsize =12,color=couleurs[filenumb-1] ,transform=ax3.transAxes)
       
       
       pyplot.savefig(f'{pathwork}/timeserie/timeserie_{fonction}_id_stn{id_stn}_vcoord{(vcoord)}_varno{varno}.png',format='png',dpi=100,bbox_inches='tight')
