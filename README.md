# RAG Pharma helper

Simple project in Snowflake:
- uses structured (csv) and unstructured (pdf) data
- feeds relevant context using cortex semantic search
- instructs the LLM to refer to the provided documents to minimize hallucinations


## Setup

1. Create a warehouse and a compute pool for the app. Set max nodes = 2 for the compute pool, or make sure to turn off the notebook `4_chunk_pdfs.ipynb` later.
2. Create database with files
3. Create two tables `SN_POOL` and `SCHEDULE` from raw csv files
4. Create stage called `pharma_pdf_stage` with server side encryption and upload all the SOP pdfs there
5. Create cortex service with `6_cortex_service.sql`
6. Deploy the streamlit app on the compute pool created at the beginning
