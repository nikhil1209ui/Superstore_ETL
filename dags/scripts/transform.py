import pandas as pd

def transform_data(df):

    #renaming columns to appropiate naming convention

    df.columns = df.columns.str.replace(" ", "_")

    # converting date columns to datetime format

    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    df['Ship_Date'] = pd.to_datetime(df['Ship_Date'])

    # Adding calculated columns

    df['Order_Month'] = df['Order_Month'].dt.month 
    df['Order_Year'] = df['Order_Year'].dt.year

    # Removing unnecessary columns

    df = df.drop('Row_ID', axis=1)

    print("Data Transformed Successfully !")

    return df