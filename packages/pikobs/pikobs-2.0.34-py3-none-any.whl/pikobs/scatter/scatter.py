"""
Description
------------

This module allows for the computation of various statistical metrics over adjustable tiles on the globe, averaged over a specified time period. These metrics include:

- **omp (Observation minus Prediction)**: The difference between observed meteorological data and model predictions.
- **oma (Observation minus Analysis)**: The difference between observed meteorological data and the analysis field.
- **des (Density)**: The density of observations within a specified region.
- **obs (Observations)**: Recorded meteorological observations from various stations.
- **bcorr (Bias Correction)**: Applicable to radiances, it represents the bias corrections applied across different datasets.

These calculations are essential for:

1. Evaluating the quality and accuracy of meteorological observations.
2. Creating detailed maps for specific meteorological experiments.
3. Generating comparative maps to analyze differences between control experiments and evaluation experiments.

Details of Calculations for a Single Experiment
-----------------------------------------------

1. **omp (Observation minus Prediction)**:
   - Shows the difference between observed meteorological data and the model-predicted field.
   - It is crucial for understanding the performance of predictive models and identifying areas where model predictions deviate from actual observations.

   .. image:: ../../../docs/source/_static/omp1.png
      :alt: omp Plot

2. **oma (Observation minus Analysis)**:
   - Similar to the 'omp' metric, but compares observations with the analysis field rather than predictions.
   - This helps in assessing how well the analysis represents the observed data.

   .. image:: ../../../docs/source/_static/oma1.png
      :alt: oma Plot

3. **obs (Observations)**:
   - Displays recorded meteorological observations from various stations.
   - A color scale is used to highlight significant observations, aiding in the detection of patterns, anomalies, and overall trends in the data.

   .. image:: ../../../docs/source/_static/obs1.png
      :alt: obs Plot

4. **dens (Density)**:
   - Visualizes the density of observations within a specified region.
   - This metric uses a color scale to indicate variations in observation density, providing a clear picture of areas with higher and lower concentrations of data.

   .. image:: ../../../docs/source/_static/dens1.png
      :alt: dens Plot

5. **bcorr (Bias Correction of Radiances)**:
   - Depicts the bias corrections applied to radiance data across different datasets.
   - The color scale in this plot shows the magnitude and direction of bias corrections, which is essential for assessing and adjusting discrepancies in radiance data.

   .. image:: ../../../docs/source/_static/bcorr1.png
      :alt: bcorr Plot

Generate Scatter for Radiance Assimilation Analysis
****************************************************

To start an interactive session for generating scatter plots, use the following qsub command:

.. code-block:: bash

    qsub -I -X -l select=4:ncpus=80:mpiprocs=80:ompthreads=1:mem=185gb -l place=scatter -l walltime=6:0:0

Generating Scatter Plots for a Single Experiment
------------------------------------------------

To generate scatter plots for a single experiment using the `pikobs` module, use the following command format:

.. code-block:: bash

    python -c 'import pikobs; pikobs.scatter.arg_call()' \

         --path_experience_files /home/dlo001/data_maestro/ppp5/maestro_archives/E22SLT50BGCK/monitoring/banco/postalt/ \

         --experience_name E22SLT50BGCK \

         --pathwork work_to_amsua_allsky_scatter_omp_version2 \

         --datestart 2022060100 \

         --dateend 2022060200 \

         --region Monde \

         --family atms_allsky \

         --flags_criteria assimilee \

         --function omp oma obs dens bcorr \

         --boxsizex 2 \

         --boxsizey 2 \

         --projection robinson \

         --id_stn all \

         --channel all \

         --n_cpu 80

Comparative Analysis Between Control and Evaluation Experiments
---------------------------------------------------------------

This section provides an overview of how to generate comparative maps to analyze differences between control and evaluation experiments. The visual representations illustrate the functionality and significance of each metric.

1. **omp (Observation minus Prediction)**:
   - Displays the difference between average meteorological observations and model-predicted fields for the specified time period across two experiments (control and experimental).
   - This plot helps in visualizing deviations between observed data and model predictions.

   .. image:: ../../../docs/source/_static/omp2.png
      :alt: omp Plot

2. **oma (Observation minus Analysis)**:
   - Illustrates the difference between average meteorological observations and the analysis field for the specified time period in both control and experimental experiments.
   - This plot aids in understanding deviations between observed data and analyzed predictions.

   .. image:: ../../../docs/source/_static/oma2.png
      :alt: oma Plot

3. **obs (Observations)**:
   - Shows average recorded meteorological observations from stations during the specified time period for both control and experimental experiments.
   - Utilizes a color scale to highlight significant observations, facilitating pattern and anomaly detection.

   .. image:: ../../../docs/source/_static/obs2.png
      :alt: obs Plot

4. **dens (Density)**:
   - Visualizes average observation density within a defined region for the specified time period across control and experimental experiments.
   - Uses a color scale to depict variations in observation density, providing insights into spatial concentration.

   .. image:: ../../../docs/source/_static/dens2.png
      :alt: dens Plot

5. **bcorr (Bias correction of radiances)**:
   - Depicts bias corrections applied to average radiance data across different datasets for the specified time period in both control and experimental experiments.
   - Displays bias correction magnitude and direction using a color scale, aiding in data quality assessment and adjustment.

   .. image:: ../../../docs/source/_static/bcorr2.png
      :alt: bcorr Plot

Generating Comparative Scatter Plots
------------------------------------

To generate comparative scatter plots between control and evaluation experiments using the `pikobs` module, use the following command format:

.. code-block:: bash

    python -c 'import pikobs; pikobs.scatter.arg_call()' \

         --path_control_files /home/dlo001/data_maestro/ppp5/maestro_archives/E22SLT50/monitoring/banco/postalt/ \

         --control_name E22SLT50 \

         --path_experience_files /home/dlo001/data_maestro/ppp5/maestro_archives/E22SLT50BGCK/monitoring/banco/postalt/ \

         --experience_name E22SLT50BGCK \

         --pathwork work_to_amsua_allsky_scatter_omp_version2 \

         --datestart 2022060100 \

         --dateend 2022060200 \

         --region Monde \

         --family atms_allsky \

         --flags_criteria assimilee \

         --function omp oma obs dens bcorr \

         --boxsizex 2 \

         --boxsizey 2 \

         --projection robinson \

         --id_stn all \

         --channel all \

         --n_cpu 80
"""
#!/usr/bin/python3

import sqlite3
import pikobs
import re
import os
from  dask.distributed import Client
import numpy as np
import sqlite3
import os
import re
import sqlite3


def create_and_populate_moyenne_table(family, 
                                      new_db_filename,
                                      existing_db_filename,
                                      region_seleccionada,
                                      selected_flags, 
                                      FONCTION,
                                      boxsizex,
                                      boxsizey,
                                      varnos,
                                      channel,
                                      id_stn):
      
   
       
       pattern = r'(\d{10})'
       match = re.search(pattern, existing_db_filename)
   
       if match:
           date = match.group(1)
          
       else:
           print("No 10 digits found in the string.")
       
       
       # Connect to the new database
     
       new_db_conn = sqlite3.connect(new_db_filename, uri=True, isolation_level=None, timeout=999)
       new_db_cursor = new_db_conn.cursor()
       FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)
       if varnos:
           element=",".join(varnos)
       if channel=='join':
           VCOORD='  vcoord '
       if channel=='join' and  id_stn=='all':
           group_channel = ' "join" as Chan,    '
           group_id_stn  = ' id_stn as id_stn, '
           group_id_stn_vcoord = ' group by 2, 3, 4, 5, id_stn'
       if channel=='all' and  id_stn=='join':
           group_channel = f' {VCOORD} as  Chan, '
           group_id_stn  = ' "join" as id_stn, '
           group_id_stn_vcoord = f' group by 2, 3, 4, 5,{VCOORD}'
       if channel=='all' and  id_stn=='all':
           group_channel = f'  {VCOORD} as Chan,'
           group_id_stn  = ' id_stn as id_stn, '
           group_id_stn_vcoord = f' group by 2, 3, 4, 5, id_stn, {VCOORD}'
       if channel=='join' and  id_stn=='join':
           group_channel = ' "join" as Chan, '
           group_id_stn  =  ' "join" as id_stn,  '
           group_id_stn_vcoord = 'group by 2, 3, 4, 5, date '


       LAT1, LAT2, LON1, LON2 = pikobs.regions(region_seleccionada)
       LATLONCRIT = pikobs.generate_latlon_criteria(LAT1, LAT2, LON1, LON2)
       flag_criteria = pikobs.flag_criteria(selected_flags)
       STNID = f"floor(360. / {boxsizex} ) * floor(lat / {boxsizey} ) + floor(MIN(179.99, lon) / {boxsizex}) "
       LAT = f"floor(lat / {boxsizey})  * {boxsizey} + {boxsizey} / 2."
       LON = f"floor(MIN(179.99, lon) / {boxsizex} ) * {boxsizex} + {boxsizex} / 2. "
       # Attach the existing database
       new_db_cursor.execute(f"PRAGMA journal_mode = OFF;")
       new_db_cursor.execute(f"PRAGMA journal_mode = MEMORY;")
       new_db_cursor.execute(f"PRAGMA synchronous = OFF;")
       new_db_cursor.execute(f"PRAGMA foreign_keys = OFF;")
       new_db_cursor.execute(f"ATTACH DATABASE '{existing_db_filename}' AS db;")
       # Create the 'moyenne' table in the new database if it doesn't exist
       new_db_cursor.execute("""
           CREATE TABLE IF NOT EXISTS moyenne (
               Nrej INTEGER,
               Nacc INTEGER,
               Nprofile INTEGER,
               DATE INTEGER,
               lat FLOAT,
               lon FLOAT,
               boite INTEGER,
               id_stn TEXT,
               varno INTEGER,
               vcoord FLOAT,   -- INTEGER FLOAT canal
               sumx FLOAT,
               sumy FLOAT,
               sumz FLOAT,
               sumStat FLOAT,
               sumx2 FLOAT,
               sumy2 FLOAT,
               sumz2 FLOAT,
               sumStat2 FLOAT,
               n INTEGER,
               flag integer           );
       """)
   
       # Execute the data insertion from the existing database
       qr = f"""
       INSERT INTO moyenne (
           DATE,
           lat,
           lon,
           boite, 
           varno, 
           vcoord, 
           sumx, 
           sumy, 
           sumz,
           sumStat,
           sumx2, 
           sumy2, 
           sumz2, 
           sumStat2,
           n,
           Nrej,
           Nacc,
           Nprofile,
           id_stn,
           flag
   
       )
       SELECT
           {date},
           {LAT},   --2
           {LON},   --3
           {STNID}, --4
           VARNO,   --5
           {group_channel} --6
           sum(omp),
           sum(oma),
           sum(obsvalue), 
           sum(bias_corr),
           sum(omp*omp),
           sum(oma*oma),
           sum(obsvalue*obsvalue),
           sum(bias_corr*bias_corr),
           COUNT(*),
           sum(flag & 512=512),
           sum(flag & 4096-4094),
           count(distinct id_obs),
           {group_id_stn}
           flag
           
   
       FROM
           db.header
       NATURAL JOIN
           db.DATA
       WHERE
           varno IN ({element}) and 
           obsvalue IS NOT NULL
           {flag_criteria}
           {LATLONCRIT}
           {VCOCRIT}
       {group_id_stn_vcoord} 
       """
       new_db_cursor.execute(qr)
   
       # Commit changes and detach the existing database
       #new_db_cursor.execute("DETACH DATABASE db;")
       new_db_conn.commit()
   
   
   
   
       # Commit changes and detach the existing database
       #new_db_cursor.execute("DETACH DATABASE db;")
   
   
       # Close the connections
       new_db_conn.close()
from datetime import datetime, timedelta
   
def create_data_list(datestart1, 
                     dateend1,
                     family,
                     pathin, 
                     name, 
                     pathwork,
                     boxsizex, 
                     boxsizey, 
                     fonction, 
                     flag_criteria, 
                     region_seleccionada, 
                     varnos):
       data_list = []
       #print (datestart1, dateend1, family, pathin, pathwork, boxsizex, boxsizey, fonction, flag_criteria, region_seleccionada)
       # Convert datestart and dateend to datetime objects
       datestart = datetime.strptime(datestart1, '%Y%m%d%H')
       dateend = datetime.strptime(dateend1, '%Y%m%d%H')
   
       # Initialize the current_date to datestart
       current_date = datestart
   
       # Define a timedelta of 6 hours
       delta = timedelta(hours=6)
   
       # Iterate through the date range in 6-hour intervals
       while current_date <= dateend:
           # Format the current date as a string
           formatted_date = current_date.strftime('%Y%m%d%H')
   
           # Build the file name using the date and family
           filename = f'{formatted_date}_{family}'
           # Create a new dictionary and append it to the list
           data_dict = {
               'family': family,
               'filein': f'{pathin}/{filename}',
               'db_new': f'{pathwork}/scatter_{name}_{datestart1}_{dateend1}_bx{boxsizex}_by{boxsizey}_{flag_criteria}_{family}.db',
               'region': region_seleccionada,
               'flag_criteria': flag_criteria,
               'fonction': fonction,
               'boxsizex': boxsizex,
               'boxsizey': boxsizey,
               'varnos':varnos,
           }
           data_list.append(data_dict)
   
           # Update the current_date in the loop by adding 6 hours
           current_date += delta
   
       return data_list
   
import sqlite3
import numpy as np

def get_id_stns(cursor, id_stn):
    """Obtiene la lista de id_stn desde la base de datos."""
    if id_stn == 'all':
        query = "SELECT DISTINCT id_stn FROM moyenne;"
        cursor.execute(query)
        return np.array([item[0] for item in cursor.fetchall()])
    return ['join']

def fetch_vcoords(cursor, criter):
    """Obtiene las coordenadas verticales y números de variable según el criterio dado."""
    query = f"SELECT DISTINCT vcoord, varno FROM moyenne {criter} ORDER BY vcoord ASC;"
    cursor.execute(query)
    return cursor.fetchall()

def fetch_channels_varno(cursor):
    """Obtiene los números de variable de todos los canales."""
    query = "SELECT DISTINCT varno FROM moyenne ORDER BY vcoord ASC;"
    cursor.execute(query)
    return [item[0] for item in cursor.fetchall()]

def create_data_list_plot(datestart1, dateend1, family, namein, pathwork, boxsizex, boxsizey,
                          fonction, flag_criteria, region_seleccionada, id_stn, channel):
    data_list_plot = []
    
    fileset = [f'{pathwork}/scatter_{namein[0]}_{datestart1}_{dateend1}_bx{boxsizex}_by{boxsizey}_{flag_criteria}_{family}.db']
    nameset = [namein[0]]

    if len(namein) > 1:
        fileb = f'{pathwork}/scatter_{namein[1]}_{datestart1}_{dateend1}_bx{boxsizex}_by{boxsizey}_{flag_criteria}_{family}.db'
        fileset.append(fileb)
        nameset.append(namein[1])

    with sqlite3.connect(fileset[0]) as conn:
        cursor = conn.cursor()
        id_stns = get_id_stns(cursor, id_stn)

        for idstn in id_stns:
            criter = '' if id_stn == 'join' else f'WHERE id_stn = "{idstn}"'
            
            if channel == 'all':

                vcoords = fetch_vcoords(cursor, criter)
                for vcoord, varno in vcoords:
                    data_list_plot.append({
                        'id_stn': idstn,
                        'vcoord': vcoord,
                        'files_in': fileset,
                        'varno': varno
                    })
            else:
                channels_varno = fetch_channels_varno(cursor)
                if channels_varno:
                    data_list_plot.append({
                        'id_stn': idstn,
                        'vcoord': 'join',
                        'files_in': fileset,
                        'varno': channels_varno
                    })
    return data_list_plot
 
def make_scatter(files_in,
                 names_in,  
                 pathwork, 
                 datestart,
                 dateend,
                 regions, 
                 familys, 
                 flag_criteria, 
                 fonction, 
                 varnos,
                 boxsizex, 
                 boxsizey, 
                 Proj, # Proj=='OrthoN'// Proj=='OrthoS'// Proj=='robinson' // Proj=='Europe' // Proj=='Canada' // Proj=='AmeriqueNord' // Proj=='Npolar' //  Proj=='Spolar' // Proj == 'reg'
                 mode,
                 Points,
                 id_stn,
                 channel,
                 n_cpu):
   
      """
       Perform scatter plot generation based on input parameters.
   
       Args:

        files_in (list): List of input file paths.

        names_in (list): List of input file names.

        pathwork (str): Working directory.

        datestart (str): Start date in YYYYMMDDHH format.

        dateend (str): End date in YYYYMMDDHH format.

        region (str): Region parameter description.

        family (str): Family parameter description.

        flag_criteria (str): Flags criteria.

        fonction (str): Function parameter description.

        boxsizex (int): Box size in X direction.

        boxsizey (int): Box size in Y direction.

        Proj (str or list): Projection type ('cyl', 'OrthoN', 'OrthoS', etc.).

        mode (str): Mode parameter description.

        Points (str): Points parameter description.

        id_stn (str): id_stn parameter description.

        channel (str): Channel parameter description.

        n_cpu (int): Number of CPUs to use.
   
       Returns:
       
         None
      """
      pikobs.delete_create_folder(pathwork)
      for family in familys:
       for region in regions:
        for file_in, name_in in zip(files_in, names_in):
          data_list = create_data_list(datestart,
                                       dateend, 
                                       family, 
                                       file_in,
                                       name_in,
                                       pathwork,
                                       boxsizex,
                                       boxsizey, 
                                       fonction, 
                                       flag_criteria, 
                                       region,
                                       varnos)
          import time
          import dask
          t0 = time.time()
          if n_cpu==1:
           print (f'in Serie files for {name_in} = {len(data_list)}')
           for  data_ in data_list:  
               create_and_populate_moyenne_table(data_['family'], 
                                                 data_['db_new'], 
                                                 data_['filein'],
                                                 data_['region'],
                                                 data_['flag_criteria'],
                                                 data_['fonction'],
                                                 data_['boxsizex'],
                                                 data_['boxsizey'],
                                                 data_['varnos'],
                                                 channel,
                                                 id_stn)
               
       
       
       
       
          else:
           print (f'Number of files used in calculating statistics for {name_in} = {len(data_list)}')
           with dask.distributed.Client(processes=True, threads_per_worker=1, 
                                              n_workers=n_cpu, 
                                              silence_logs=40) as client:
               delayed_funcs = [dask.delayed(create_and_populate_moyenne_table)(data_['family'], 
                                                 data_['db_new'], 
                                                 data_['filein'],
                                                 data_['region'],
                                                 data_['flag_criteria'],
                                                 data_['fonction'],
                                                 data_['boxsizex'],
                                                 data_['boxsizey'],
                                                 data_['varnos'],
                                                 channel,
                                                 id_stn)for data_ in data_list]
               results = dask.compute(*delayed_funcs)
        
        tn= time.time()
        print ('Total time for statistics:',tn-t0 )  
        data_list_plot = create_data_list_plot(datestart,
                                             dateend, 
                                             family, 
                                             names_in,
                                             pathwork,
                                             boxsizex,
                                             boxsizey, 
                                             fonction, 
                                             flag_criteria, 
                                             region,
                                             id_stn,
                                             channel)
        os.makedirs(f'{pathwork}/plot_{family}')
        t0 = time.time()
       # n_cpu=1
        if n_cpu==1:  
         print (f'in Serie plots = {len(data_list_plot)}')
         for  data_ in data_list_plot:  
           pikobs.scatter_plot(mode, 
                               region,
                               family, 
                               data_['id_stn'], 
                               datestart,
                               dateend, 
                               Points, 
                               boxsizex,
                               boxsizey,
                               Proj, 
                               pathwork,
                               flag_criteria, 
                               fonction,
                               data_['vcoord'],
                               data_['files_in'],
                               names_in, data_['varno'])
        else:
         print (f"in Paralle plots = {len(data_list_plot)}")
         with dask.distributed.Client(processes=True, threads_per_worker=1, 
                                          n_workers=n_cpu, 
                                          silence_logs=40) as client:
           delayed_funcs = [dask.delayed(pikobs.scatter_plot)(mode, 
                                                              region,
                                                              family, 
                                                              data_['id_stn'],
                                                              datestart,
                                                              dateend, 
                                                              Points, 
                                                              boxsizex,
                                                              boxsizey,
                                                              Proj, 
                                                              pathwork,
                                                              flag_criteria, 
                                                              fonction,
                                                              data_['vcoord'],
                                                              data_['files_in'],
                                                              names_in, data_['varno'])for data_ in data_list_plot]
   
           results = dask.compute(*delayed_funcs)
        print ('Total time:',time.time() - t0 )  
        print (f'check: {pathwork}')
    
   
   
   
def arg_call():

    import argparse
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_control_files', default='undefined', type=str, help="Directory where input sqlite files are located")
    parser.add_argument('--control_name', default='undefined', type=str, help="Directory where input sqlite files are located")
    parser.add_argument('--path_experience_files', default='undefined', type=str, help="Directory where input sqlite files are located")
    parser.add_argument('--experience_name', default='undefined', type=str, help="Directory where input sqlite files are located")
  

    
    parser.add_argument('--pathwork', default='undefined', type=str, help="Working directory")
    parser.add_argument('--datestart', default='undefined', type=str, help="Start date")
    parser.add_argument('--dateend', default='undefined', type=str, help="End date")
    parser.add_argument('--region', nargs="+", default='undefined', type=str, help="Region")
    parser.add_argument('--family', nargs="+", default='undefined', type=str, help="Family")
    parser.add_argument('--flags_criteria', default='undefined', type=str, help="Flags criteria")
    parser.add_argument('--fonction', nargs="+", default='undefined', type=str, help="Function") 
    parser.add_argument('--varnos', nargs="+", default='undefined', type=str, help="Function")
    parser.add_argument('--boxsizex', default='undefined', type=int, help="Box size in X direction")
    parser.add_argument('--boxsizey', default='undefined', type=int, help="Box size in Y direction")
    parser.add_argument('--projection', nargs="+", default='cyl', type=str, help="Projection type (cyl, OrthoN, OrthoS, robinson, Europe, Canada, AmeriqueNord, Npolar, Spolar, reg)")
    parser.add_argument('--mode', default='SIGMA', type=str, help="Mode")
    parser.add_argument('--Points', default='OFF', type=str, help="Points")
    parser.add_argument('--id_stn', default='one_per_plot', type=str, help="id_stn") 
    parser.add_argument('--channel', default='one_per_plot', type=str, help="channel")
    parser.add_argument('--n_cpus', default=1, type=int, help="Number of CPUs")

    args = parser.parse_args()

    for arg in vars(args):
       print (f'--{arg} {getattr(args, arg)}')
    # Check if each argument is 'undefined'
    if args.path_control_files == 'undefined':
        files_in = [args.path_experience_files]
        names_in = [args.experience_name]
    else:    
        if args.path_experience_files == 'undefined':
            raise ValueError('You must specify --path_experience_files')
        if args.experience_name == 'undefined':
            raise ValueError('You must specify --experience_name')
        else:

            files_in = [args.path_control_files, args.path_experience_files]
            names_in = [args.control_name, args.experience_name]
    if args.varnos == 'undefined':
        args.varnos = []
    if args.pathwork == 'undefined':
        raise ValueError('You must specify --pathwork')
    if args.datestart == 'undefined':
        raise ValueError('You must specify --datestart')
    if args.dateend == 'undefined':
        raise ValueError('You must specify --dateend')
    if args.region == 'undefined':
        raise ValueError('You must specify --region')
    if args.family == 'undefined':
        raise ValueError('You must specify --family')
    if args.flags_criteria == 'undefined':
        raise ValueError('You must specify --flags_criteria')
    if args.fonction == 'undefined':
        raise ValueError('You must specify --fonction')
    if args.boxsizex == 'undefined':
        raise ValueError('You must specify --boxsizex')
    if args.boxsizey == 'undefined':
        raise ValueError('You must specify --boxsizey')


    # Comment
    # Proj='cyl' // Proj=='OrthoN'// Proj=='OrthoS'// Proj=='robinson' // Proj=='Europe' // Proj=='Canada' // Proj=='AmeriqueNord' // Proj=='Npolar' //  Proj=='Spolar' // Proj == 'reg'
  

    #print("in")
    # Call your function with the arguments
    sys.exit(make_scatter(files_in,
                          names_in,    
                          args.pathwork,
                          args.datestart,
                          args.dateend,
                          args.region,
                          args.family,
                          args.flags_criteria,
                          args.fonction,
                          args.varnos,
                          args.boxsizex,
                          args.boxsizey,
                          args.projection,
                          args.mode,
                          args.Points,
                          args.id_stn,
                          args.channel,
                          args.n_cpus))
