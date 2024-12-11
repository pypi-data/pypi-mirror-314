import pandas as pd
import sqlite3
import glob
from dask import delayed, compute
from dask.diagnostics import ProgressBar
from dask.distributed import Client

import pandas as pd
import sqlite3
import glob
from dask import delayed, compute
from dask.diagnostics import ProgressBar
from dask.distributed import Client

@delayed
def process_and_insert(file_path, new_db_filename, varno, criteria_id_stn, flag_criteria, latloncrit, vcocrit):
    """
    Procesa un archivo SQLite, calcula las métricas requeridas en pandas,
    e inserta directamente los resultados en una tabla SQLite.
    """
    try:
        # Procesar el archivo
        with sqlite3.connect(file_path) as conn:
            # Cargar datos desde las tablas
            data = pd.read_sql_query("SELECT VCOORD,OMP,OMA,BIAS_CORR,VARNO, ID_OBS FROM data", conn)
            header = pd.read_sql_query("SELECT DATE,ID_OBS,ID_STN FROM header", conn)

        # Combinar las tablas
        combined = pd.merge(header, data, on="ID_OBS", how='inner')  # Ajusta según el esquema real

        # Filtrar por VARNO y aplicar otros criterios
        filtered = combined[
            (combined["VARNO"] == varno) &
            (combined["OMP"].notnull())
        ]
        # Aplicar criterios adicionales
        if criteria_id_stn:
            filtered = filtered.query(criteria_id_stn)
        if flag_criteria:
            filtered = filtered.query(flag_criteria)
        if latloncrit:
            filtered = filtered.query(latloncrit)
        if vcocrit:
            filtered = filtered.query(vcocrit)

        # Calcular las métricas
        grouped = filtered.groupby(["VCOORD", "ID_STN"]).agg(
            DATE=("DATE", "first"),  # O ajusta según sea necesario
            Ntot=("OMP", "size"),
            AvgOMP=("OMP", "mean"),
            AvgOMA=("OMA", "mean"),
            StdOMP=("OMP", "std"),
            StdOMA=("OMA", "std"),
            AvgBCOR=("BIAS_CORR", "mean")
        ).reset_index()

        grouped["VARNO"] = varno

        # Insertar resultados en la base de datos SQLite
        with sqlite3.connect(new_db_filename, uri=True, isolation_level=None, timeout=99999) as new_db_conn:
            grouped.to_sql("serie_vdedr", new_db_conn, if_exists="append", index=False)
        print(f"Procesado e insertado: {file_path}")

    except Exception as e:
        print(f"Error procesando {file_path}: {e}")


def process_files_and_insert(input_dir, new_db_filename, varno, criteria_id_stn="", flag_criteria="", latloncrit="", vcocrit=""):
    """
    Procesa todos los archivos en el directorio, calcula las métricas y las inserta directamente en SQLite.
    """
    sqlite_files = glob.glob(f"{input_dir}/*_cris")

    # Crear tareas para procesar e insertar cada archivo
    tasks = [
        process_and_insert(file, new_db_filename, varno, criteria_id_stn, flag_criteria, latloncrit, vcocrit)
        for file in sqlite_files
    ]

    # Ejecutar tareas en paralelo con ProgressBar
    with ProgressBar():
        compute(*tasks)


if __name__ == "__main__":
    # Parámetros de entrada
    input_directory = "/home/ata000/data_maestro/ppp5/maestro_archives/G2901H24_post/monitoring/banco/postalt/"
    new_db_filename = "serie_vdedr.db"
    varno = 12163  # Ejemplo de VARNO
    criteria_id_stn = "ID_STN == 'NOAA20'"
    flag_criteria = ""  # Agrega tus criterios
    latloncrit = ""     # Agrega tus criterios
    vcocrit = ""        # Agrega tus criterios

    # Configurar cliente Dask
    with Client(processes=True, threads_per_worker=1, n_workers=40, silence_logs=40) as client:
        print(client)  # Muestra información del cliente
        process_files_and_insert(
            input_directory, new_db_filename, varno,
            criteria_id_stn, flag_criteria, latloncrit, vcocrit
        )



