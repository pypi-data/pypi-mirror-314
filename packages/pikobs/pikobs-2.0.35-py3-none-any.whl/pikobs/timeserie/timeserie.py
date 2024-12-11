"""

Description
------------

This module calculates the number of observations over a period, for example:
  

    .. image:: ../../../docs/source/_static/timeserie.png
      :alt: Clasic time serie


"""
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


def create_timeserie_table(family, 
                           new_db_filename,
                           existing_db_filename, 
                           region_seleccionada, 
                           selected_flags,
                           varnos,
                           channel,
                           id_stn):
    """

    """

    
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
    LAT1, LAT2, LON1, LON2 = pikobs.regions(region_seleccionada)
    LATLONCRIT = pikobs.generate_latlon_criteria(LAT1, LAT2, LON1, LON2)
    flag_criteria = pikobs.flag_criteria(selected_flags)

    if varnos:
        element=",".join(varnos)
    if channel=='join':
           VCOORD='  vcoord '
    if channel=='join' and  id_stn=='all':
      group_channel = ' "join" as Chan,    '
      group_id_stn  = ' id_stn as id_stn, '
      group_id_stn_vcoord = ' group by date,id_stn,varno'
    if channel=='all' and  id_stn=='join':
      group_channel = f' {VCOORD} as  Chan, '
      group_id_stn  = ' "join" as id_stn, '
      group_id_stn_vcoord = f' group by date,{VCOORD},varno'
    if channel=='all' and  id_stn=='all':
      group_channel = f'  {VCOORD} as Chan,'
      group_id_stn  = ' id_stn as id_stn, '
      group_id_stn_vcoord = f' group by date,id_stn, {VCOORD},varno'

    if channel=='join' and  id_stn=='join':
      group_channel = ' "join" as Chan, '
      group_id_stn  =  ' "join" as id_stn,  '
      group_id_stn_vcoord = 'group by date,varno  '




    # Attach the existing database
    new_db_cursor.execute(f"ATTACH DATABASE '{existing_db_filename}' AS db;")
    # load extension CMC 
    new_db_conn.enable_load_extension(True)
    extension_dir = f'{os.path.dirname(pikobs.__file__)}/extension/libudfsqlite-shared.so'
    new_db_cursor.execute(f"SELECT load_extension('{extension_dir}')")
    new_db_cursor.execute(f"PRAGMA journal_mode = OFF;")
    new_db_cursor.execute(f"PRAGMA journal_mode = MEMORY;")
    new_db_cursor.execute(f"PRAGMA synchronous = OFF;")
    new_db_cursor.execute(f"PRAGMA foreign_keys = OFF;")

    # Create the 'moyenne' table in the new database if it doesn't exist
    new_db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS timeserie (
            DATE INTEGER, 
            varno INTEGER,
            Nrej  INTEGER,
            Nacc  INTIGER,
            SUMx  FLOAT,
            SUMx2 FLOAT,
            SUMy  FLOAT,
            SUMy2 FLOAT,
            SUMz  FLOAT,
            SUMz2 FLOAT,
            sumStat FLOAT,
            sumStat2 FLOAT,
            N INTEGER, 
            id_stn TEXT, 
            vcoord FLOAT,
            flag INTERGER
        );
    """)

    # Execute the data insertion from the existing database
    query = f"""
    INSERT INTO timeserie (
         DATE, 
         varno,
         Nrej,
         Nacc,
         SUMx,
         SUMx2, 
         SUMy,
         SUMy2,
         SUMz,
         SUMz2,
         sumStat,
         sumStat2,
         N, 
         id_stn, 
         VCOORD,
         flag

    )
    SELECT
        isodatetime({date}) AS DATE, 
        varno AS VARNO,
        count(*)- SUM(flag & 4096=4096) AS Nrej,
        SUM(flag & 4096=4096) AS Nacc,
        SUM(OMP)  AS SUMx,
        SUM(OMP*OMP) AS SUMx2,
        SUM(OMA)  AS SUMy,
        SUM(OMA*OMA) AS SUMy2,
        sum(obsvalue) AS SUMz, 
        sum(bias_corr) AS sumStat,
        sum(obsvalue*obsvalue) AS SUMz2,
        sum(bias_corr*bias_corr) AS sumStat,   
        --SUM(OMP) AS SUMx,
        --SUM(OMP*OMP) AS SUMx2,
        count(*) AS N,
        {group_id_stn}
        {group_channel}
        flag AS flag

    FROM
        db.header
    NATURAL JOIN
        db.DATA
    WHERE 
        varno IN ({element}) and 
        obsvalue IS NOT NULL
        --   AND ID_STN LIKE 'id_stn'
        --   AND vcoord IN (vcoord)
    
        {flag_criteria}
        {LATLONCRIT}
    --    {VCOCRIT}
   {group_id_stn_vcoord} 
  --  HAVING 
--     SUM(OMP IS NOT NULL) >= 50;
    """
    new_db_cursor.execute(query)
    # Commit changes and detach the existing database
    new_db_conn.commit()
    new_db_cursor.execute("DETACH DATABASE db;")


    # Close the connections
    new_db_conn.close()
from datetime import datetime, timedelta

def create_data_list(datestart1, dateend1, family, pathin,namein, pathwork, flag_criteria, region, varnos):
    data_list = []
    # Convert datestart and dateend to datetime objects
    datestart = datetime.strptime(datestart1, '%Y%m%d%H')
    dateend = datetime.strptime(dateend1, '%Y%m%d%H')

    # Initialize the current_date to datestart
    current_date = datestart

    # Define a timedelta of 6 hours
    delta = timedelta(hours=6)
    FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)
    
    #flag_criteria = generate_flag_criteria(flag_criteria)

    element_array = np.array([float(x) for x in element.split(',')])  
    # Iterate through the date range in 6-hour intervals
    while current_date <= dateend: 
      # for varno in element_array:

        # Format the current date as a string
        formatted_date = current_date.strftime('%Y%m%d%H')

        # Build the file name using the date and family
        filename = f'{formatted_date}_{family}'
        # Create a new dictionary and append it to the list
        data_dict = {
            'family': family,
            'filein': f'{pathin}/{filename}',
            'db_new': f'{pathwork}/timeserie_{namein}_{datestart1}_{dateend1}_{flag_criteria}_{family}.db',
            'region': region,
            'flag_criteria': flag_criteria,
            'varnos': varnos,
          #  'varno'   : varno
        }
        data_list.append(data_dict)

        # Update the current_date in the loop by adding 6 hours
        current_date += delta

    return data_list

def create_data_list_plot(datestart1,
                          dateend1, 
                          family, 
                          namein, 
                          pathwork, 
                          flag_criteria, 
                          region_seleccionada, 
                          id_stn, 
                          channel):
    data_list_plot = []
    filea = f'{pathwork}/timeserie_{namein[0]}_{datestart1}_{dateend1}_{flag_criteria}_{family}.db'
    namea = namein[0]
    fileset = [filea]
    nameset = [namein[0]]
   
    if len(namein)>1:
          fileb = f'{pathwork}/timeserie_{namein[1]}_{datestart1}_{dateend1}_{flag_criteria}_{family}.db'
          fileset = [filea,fileb]
          nameset = [namein[0], namein[1]] 

    
    conn = sqlite3.connect(filea)
    cursor = conn.cursor()
    if id_stn=='all':
           query = "SELECT DISTINCT id_stn FROM timeserie;"
           cursor.execute(query)
           id_stns = np.array([item[0] for item in cursor.fetchall()])
    else:
           id_stns = ['join']
   
    for idstn in id_stns:
        if id_stn=='join':
            criter = '   '
        else:
            criter =f'where id_stn = "{idstn}"'
        if channel =='all': 
            query = f"SELECT DISTINCT vcoord, varno FROM timeserie {criter} ORDER BY vcoord ASC;"
            cursor.execute(query)
            vcoords = cursor.fetchall()
            for vcoord, varno in vcoords:
              data_dict_plot = {
               'id_stn': idstn,
               'vcoord': vcoord,
               'files_in':fileset,
               'varno':varno,
               'name_in':nameset}
              data_list_plot.append(data_dict_plot)
        else:
            query = f"SELECT DISTINCT  varno FROM timeserie ;"
            cursor.execute(query)
            channels_varno = []
            result = cursor.fetchall()
            if result:
                   channels_varno.append(result)
   
            for  varno in channels_varno[0]:
              data_dict_plot = {
               'id_stn': idstn,
               'vcoord': 'join',
               'files_in':fileset,
               'varno':varno,
               'name_in':nameset}
              data_list_plot.append(data_dict_plot)
    return data_list_plot


def make_timeserie(files_in,
                   names_in,  
                   pathwork, 
                   datestart,
                   dateend,
                   regions, 
                   familys, 
                   flag_criteria, 
                   fonction,
                   varnos,
                   id_stn,
                   channel,
                   n_cpu):


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
                                       flag_criteria, 
                                       region,
                                       varnos)
          

          import time
          import dask
          t0 = time.time()
          #n_cpu=1
          if n_cpu==1:
           for  data_ in data_list:  
               print (f"Serie for {name_in} ")
               create_timeserie_table(data_['family'], 
                                      data_['db_new'], 
                                      data_['filein'],
                                      data_['region'],
                                      data_['flag_criteria'],
                                      data_['varnos'],
                                      channel,
                                      id_stn)
               
       
       
       
       
          else:
           print (f'in Parallel for {name_in} = {len(data_list)}')
           with dask.distributed.Client(processes=True, threads_per_worker=1, 
                                              n_workers=n_cpu, 
                                              silence_logs=40) as client:
               delayed_funcs = [dask.delayed(create_timeserie_table)(data_['family'], 
                                                 data_['db_new'], 
                                                 data_['filein'],
                                                 data_['region'],
                                                 data_['flag_criteria'],
                                                 data_['varnos'],
                                                 channel,
                                                 id_stn)for data_ in data_list]
               results = dask.compute(*delayed_funcs)
    
          tn= time.time()
          print ('Total time:', round(tn-t0,2) )  
      data_list_plot = create_data_list_plot(datestart,
                                       dateend, 
                                       family, 
                                       names_in, 
                                       pathwork,
                                       flag_criteria, 
                                       region,
                                       id_stn,
                                       channel)

      os.makedirs(f'{pathwork}/timeserie')
      fig_title = ''
      t0 = time.time()

      if n_cpu==1:
           for  data_ in data_list_plot:  
               print ("Plotting in serie")

               pikobs.timeserie_plot(
                                  pathwork,
                     datestart,
                     dateend,
                     fonction,
                     flag_criteria,
                     family,
                     region,
                     fig_title,
                     data_['vcoord'], 
                     data_['id_stn'], 
                     data_['varno'],
                     data_['files_in'],
                     data_['name_in'])  
      else:
             print (f'Plotting in Parallel = {len(data_list_plot)}')
             with dask.distributed.Client(processes=True, threads_per_worker=1, 
                                              n_workers=n_cpu, 
                                              silence_logs=40) as client:
               delayed_funcs = [dask.delayed(pikobs.timeserie_plot)(
                                  pathwork,
                     datestart,
                     dateend,
                     fonction,
                     flag_criteria,
                     family,
                     region,
                     fig_title,
                     data_['vcoord'], 
                     data_['id_stn'], 
                     data_['varno'],
                     data_['files_in'],
                     data_['name_in'])for data_ in data_list_plot]

               results = dask.compute(*delayed_funcs)
      tn= time.time()
      print ('Total time:', round(tn-t0,2) )  
 



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
    parser.add_argument('--id_stn', default='all', type=str, help="id_stn") 
    parser.add_argument('--channel', default='all', type=str, help="channel")
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


    # Comment
    # Proj='cyl' // Proj=='OrthoN'// Proj=='OrthoS'// Proj=='robinson' // Proj=='Europe' // Proj=='Canada' // Proj=='AmeriqueNord' // Proj=='Npolar' //  Proj=='Spolar' // Proj == 'reg'
  

    #print("in")
    # Call your function with the arguments
    sys.exit(make_timeserie(files_in,
                            names_in, 
                            args.pathwork,
                            args.datestart,
                            args.dateend,
                            args.region,
                            args.family,
                            args.flags_criteria,
                            args.fonction, 
                            args.varnos,
                            args.id_stn,
                            args.channel,
                            args.n_cpus))

if __name__ == '__main__':
    args = arg_call()




