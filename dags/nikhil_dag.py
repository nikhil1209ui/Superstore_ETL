from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta

import pandas as pd
import logging

from snowflake.connector import connect
#from scripts.extract import extract_data
#from scripts.transform import transform_data
#from scripts.load import load_data


def extract_data():

    df = pd.read_csv('/opt/airflow/Data/SSales.csv', encoding='latin1')
    
    # Saving extracted data to a temporary file instead of returning full dict
    file_path = "/opt/airflow/Data/extracted_data.csv"
    df.to_csv(file_path, index=False)

    logging.info(f"Data Extracted Successfully! File saved at: {file_path}")

    return file_path  # Return file path instead of full DataFrame
    #print("Data Extracted Successfully !")
    #return df.to_dict()




def transform_data(**context):
     
    file_path = context['ti'].xcom_pull(task_ids='extract_data')  # Get file path
    df = pd.read_csv(file_path)  # Read data from file instead of XCom

    #renaming columns to appropiate naming convention

    df.columns = df.columns.str.replace(" ", "_")

    # converting date columns to datetime format

    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    df['Ship_Date'] = pd.to_datetime(df['Ship_Date'])

    # Adding calculated columns

    df['Order_Month'] = df['Order_Date'].dt.month 
    df['Order_Year'] = df['Order_Date'].dt.year

    # Removing unnecessary columns

    df = df.drop('Row_ID', axis=1)
    
    # Saving transformed data to another file instead of returning full dict
    transformed_file_path = "/opt/airflow/Data/transformed_data.csv"
    df.to_csv(transformed_file_path, index=False, header=True)

    logging.info(f"Data Transformed Successfully! File saved at: {transformed_file_path}")

    return transformed_file_path  # Return file path instead of full dict
    #print("Data Transformed Successfully !")
    #return df.to_dict()



def load_data(**context):
    
    file_path = context['ti'].xcom_pull(task_ids='transform_data')  # Get transformed file path

    #df = pd.DataFrame(file_path)
    # Snowflake connection authorization

    conn = connect(

           user = 'your username',
           password = 'your password',
           account = 'your account identifier',
           warehouse = 'COMPUTE_WH',
           database = 'SUPERSTORE',
           schema = 'SALES'
    )

    # Creating cursor

    cursor = conn.cursor()
    
    # Inserting data into Snowflake
    cursor.execute(f"PUT file://{file_path} @%SUPERSTORE_SALES")
    cursor.execute("TRUNCATE TABLE SUPERSTORE_SALES")  # Clears old data
    cursor.execute(f"""
                   COPY INTO SUPERSTORE_SALES
                   FROM @%SUPERSTORE_SALES/{file_path.split('/')[-1]}
                   FILE_FORMAT = (TYPE = 'CSV' 
                   FIELD_OPTIONALLY_ENCLOSED_BY = '"' 
                   FIELD_DELIMITER = ',' 
                   SKIP_HEADER = 1)
                   ON_ERROR = ABORT_STATEMENT
                   PURGE = TRUE
                   """)
    
    # Committing and closing connection

    conn.commit()
    cursor.close()
    conn.close()
    
    logging.info("Data Loaded to Snowflake Successfully!")
    #print("Data Loaded to Snowflake Successfully !")

# Default arguments for DAG
default_args = {
        
        'owner' : 'airflow',
        'depends_on_past' : False,
        'start_date' : datetime(2023, 2, 8, 20, 40, 0),
        'retries' : 1,
        'retry_delay' : timedelta(minutes=5), 
}

# Defining DAG

dag = DAG(
    'superstore_sale_ETL',
    default_args = default_args,
    description = 'ETL Pipeline for Superstore Sales Data',
    schedule_interval = '@daily',
)

# Task 1 (Data-Extraction)
extraction_task = PythonOperator(
    task_id = 'extract_data',
    python_callable = extract_data,
    dag = dag
)

# Task 2 (Data-Transformation)
transformation_task = PythonOperator(
    task_id = 'transform_data',
    python_callable = transform_data,
    provide_context=True,  # Ensures context is passed properly
    dag = dag,
)

# Task 3 (Data-Loading)
loading_task = PythonOperator(
    task_id = 'loading_data',
    python_callable = load_data,
    provide_context=True,  # Ensures context is passed properly
    dag = dag,
)

# Defining Task Dependencies

extraction_task >> transformation_task >> loading_task




