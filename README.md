# Superstore Sales ETL Project

This project is an end-to-end data architecture solution built to demonstrate skills in Python, SQL, data warehousing, workflow orchestration, containerization, and data visualization. The project uses the [Superstore Sales dataset](https://www.kaggle.com/jessemostipak/superstore) from Kaggle as its source data.

## Table of Contents

- [Project Overview](#Project-Overview)
- [Architecture & Technology Stack](#architecture--technology-stack)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [How to Run the ETL Pipeline](#how-to-run-the-etl-pipeline)
- [Business Insights SQL Queries](#business-insights-Queries)
- [Visualization with Power BI](#visualization-with-power-bi)
- [Challenges & Learnings](#challenges--learnings)

## Project Overview

This project extracts data from the Superstore Sales dataset, transforms it into a clean and analysis-ready format, and loads it into a Snowflake data warehouse. The entire ETL process is orchestrated using Apache Airflow running in Docker containers. Finally, Power BI is used to visualize the data by connecting directly to Snowflake via DirectQuery.

## Architecture & Technology Stack

- **Dataset:** Superstore Sales (Kaggle)
- **Data Warehouse:** Snowflake
- **Workflow Orchestration:** Apache Airflow
- **Containerization:** Docker (using `docker-compose.yaml`)
- **Data Transformation & ETL:** Python (pandas, Snowflake Connector)
- **Visualization:** Power BI (DirectQuery connection to Snowflake)

## Project Structure
```bash
superstore_etl_project/ 
├── Data/ 
│      └── SSales.csv # Original Superstore Sales dataset 
│      └──extracted_data.csv # Data extracted by Airflow DAG 
│      └── transformed_data.csv # Data after transformation step 
├── dags/
│ └── nikhil_dag.py # Airflow DAG for ETL (extract, transform, load) 
├── docker-compose.yaml # Docker Compose file to run Airflow services
├── .env # Environment variables (e.g., Snowflake credentials) 
└──  README.md # Project documentation (this file) 
```

## Setup & Installation

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)
- Git
- Python 3 (for local testing of ETL scripts)

### Steps
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your_username/superstore_etl_project.git
   cd superstore_etl_project
   ```

2. Create the Snowflake Table:

   Log in to your Snowflake account and open the Snowflake worksheet.
   Execute the following SQL script to create the SUPERSTORE_SALES table:
   ```sql
   CREATE OR REPLACE TABLE SUPERSTORE.SALES.SUPERSTORE_SALES (
    ORDERID VARCHAR(16777216),
    ORDERDATE DATE,
    SHIPDATE DATE,
    SHIPMODE VARCHAR(16777216),
    CUSTOMERID VARCHAR(16777216),
    CUSTOMERNAME VARCHAR(16777216),
    SEGMENT VARCHAR(16777216),
    COUNTRY VARCHAR(16777216),
    CITY VARCHAR(16777216),
    STATE VARCHAR(16777216),
    POSTALCODE NUMBER(38,0),
    REGION VARCHAR(16777216),
    PRODUCTID VARCHAR(16777216),
    CATEGORY VARCHAR(16777216),
    SUBCATEGORY VARCHAR(16777216),
    PRODUCTNAME VARCHAR(16777216),
    SALES FLOAT,
    QUANTITY NUMBER(38,0),
    DISCOUNT FLOAT,
    PROFIT FLOAT,
    ORDERMONTH NUMBER(38,0),
    ORDERYEAR NUMBER(38,0)
    );```
  -Verify that the table is created successfully before running the ETL pipeline.
3. Configure Environment Variables:
  - Create or update the .env file with your Snowflake credentials and any other required environment variables.
  - Start Apache Airflow Using Docker Compose:
   ```bash
   docker-compose up -d
   ```
4. Access the Airflow UI at `http://localhost:8080.`

## How to Run the ETL Pipeline
The ETL pipeline is defined in the Airflow DAG file dags/nikhil_dag.py and consists of the following steps:

### Extract:
- Reads the Superstore Sales CSV file from /opt/airflow/Data/SSales.csv.
- Saves the extracted data as extracted_data.csv.
### Transform:
- Reads the extracted CSV file.
- Renames columns to follow a consistent naming convention.
- Converts date columns to proper datetime formats.
- Adds new calculated columns (e.g., Order_Month, Order_Year).
- Drops unnecessary columns.
- Saves the transformed data as transformed_data.csv.
### Load:
- Connects to the Snowflake data warehouse using the Snowflake Connector.
- Uses Snowflake's PUT and COPY INTO commands to load the transformed data into the SUPERSTORE_SALES table.
- Clears previous data by truncating the table before loading new data.
- The DAG is scheduled to run daily. You can monitor and manage it from the Airflow UI.

## Visualization with Power BI
After the data is loaded into Snowflake, the project uses Power BI (via DirectQuery mode) to create interactive dashboards. 
The DArch.pbix file in the repository is a sample Power BI report that visualizes key metrics from the Superstore Sales dataset.

## Business Insight Queries [queries](https://github.com/nikhil1209ui/Superstore_ETL/blob/main/Snowflake_SQL_Queries/Business%20Queries)
After loading the data into Snowflake, several SQL queries were executed to gain business insights.

## Ensuring Connections

Additionally, a test insert was performed to verify the DirectQuery connection in Power BI.
```sql
insert into superstore_sales(ORDERID,ORDERDATE,SHIPDATE,SHIPMODE,CUSTOMERID,CUSTOMERNAME,SEGMENT,COUNTRY,CITY,STATE,POSTALCODE,REGION,PRODUCTID,CATEGORY,SUBCATEGORY,PRODUCTNAME,SALES,QUANTITY,DISCOUNT,PROFIT,ORDERMONTH,ORDERYear)
values('IN-2018-000012','2018-01-07','2018-02-10','First Class','NK-12079','NIKHIL KUSHWAHA','Consumer','India','Jhansi','Uttar Pradesh',284003,'East','ON-AI-20883390','Sport Supplies','Sport','Baseball 1204',12.01,1,0,5.746,1,2018)

SELECT * FROM SUPERSTORE_SALES
where customername = 'NIKHIL KUSHWAHA'

select count(*) from superstore_sales
```

## Challenges & Learnings
- Self-Learning New Tools:
This project was my first hands-on experience with Snowflake, Apache Airflow, and Docker. I navigated the learning curve by using official documentation, online tutorials, and community forums.
- ETL Pipeline Complexity:
Building an end-to-end ETL pipeline required integrating multiple technologies. I learned the importance of data quality checks, effective logging, and error handling.
- DirectQuery Limitations:
Working with Power BI in DirectQuery mode introduced some limitations (e.g., report view restrictions and inability to create new measures), which I addressed by designing a robust data model in Snowflake.

