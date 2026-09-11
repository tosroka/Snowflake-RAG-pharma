-- we loaded the data though UI and now there are two tables available

-- we create a new column for difference in SN to get the pool

USE ROLE SYSADMIN;
USE DATABASE PHARMA_COPILOT;
USE SCHEMA PHARMA_DATA;

CREATE OR REPLACE VIEW SN_POOL_SUBTRACT AS
SELECT 
    g.DRUG_NAME, -- reduced to only drug namea for less token consumption
    (g.END_SN - g.START_SN) + 1 AS AVAILABLE_SN_COUNT
FROM SN_POOL g;