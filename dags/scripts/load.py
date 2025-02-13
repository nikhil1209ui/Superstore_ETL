from snowflake.connector import connect

def load_data(df):

    # Snowflake connection authorization

    conn = connect(

           user = 'Nikhil',
           password = 'Nappi7carter#',
           account = 'lp28715.me-central2.gcp',
           warehouse = 'COMPUTE_WH',
           database = 'SUPERSTORE',
           schema = 'SALES'
    )

    # Loading data into snowflake

    cursor = conn.cursor()
    cursor.execute("PUT file://sales_cleaned.csv @%Superstore_Sales")
    cursor.execute("""
                   COPY INTO Superstore_Sales
                   FROM @%Superstore_Sales/sales_cleaned.csv.gz
                   FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' FIELD_DELIMITER = ',' SKIP_HEADER = 1 ERROR_ON_COLUMN_COUNT_MISMATCH = false)
                   ON_ERROR = 'CONTINUE'
                   """)