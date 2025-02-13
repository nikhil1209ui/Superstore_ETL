from snowflake.connector import connect
from tableauhyperapi import HyperException, Connection, SqlType, Telemetry, TableDefinition
import pandas as pd


# Connecting to Snowflake
conn = connect(

           user = 'Your Username',
           password = 'Your Password',
           account = 'Your Account Identifier',
           warehouse = 'COMPUTE_WH',
           database = 'SUPERSTORE',
           schema = 'SALES'
    )

# Fetching Data
query = """SELECT * FROM SUPERSTORE_SALES"""
df = pd.read_sql(query, conn)

#print(df.head())  #Testing

# Closing Connection
conn.close()

# Converting to Tableau Hyper Extract

hyper_file = "snowflake_data.hyper"



