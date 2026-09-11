USE ROLE ACCOUNTADMIN; -- need this instead of SYSADMIN to create the cortex services!!! this role was granted perms
USE DATABASE PHARMA_COPILOT;
USE SCHEMA PHARMA_DATA;

CREATE OR REPLACE CORTEX SEARCH SERVICE SOP_SEARCH_SERVICE
ON chunk_text
ATTRIBUTES file_name
WAREHOUSE = COMPUTE_WH -- warehouse, could be outside of snowflake at AWS
TARGET_LAG = '1 minute'
AS (
    SELECT 
        file_name,
        chunk_text
    FROM DOC_CHUNKS
);