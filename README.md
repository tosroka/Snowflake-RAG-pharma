# RAG Pharma helper

Simple project in Snowflake:
- uses structured (csv) and unstructured (pdf) data
- feeds relevant context using cortex semantic search
- instructs the LLM to refer to the provided documents to minimize hallucinations
- provides a simple GUI in Streamlit (directly deployed in Snowflake and viewed in Snowsight UI)

Demo of a complex question that reaches into multiple datasources at once:


https://github.com/user-attachments/assets/f01e93d5-d188-449b-b641-9f887b7db90f



## Setup

1. Create a warehouse and a compute pool for the app. Set max nodes = 2 for the compute pool, or make sure to turn off the notebook `4_chunk_pdfs.ipynb` later.
2. Run the `setup` files 1 and 2.
3. Create two tables `SN_POOL` and `SCHEDULE` from raw csv files
4. Create stage called `pharma_pdf_stage` with server side encryption and upload all the SOP pdfs there
5. continue the setup from 3 through 6, which prepares the semantic database and spins up the cortex search service
7. Deploy the streamlit app on the compute pool created at the beginning
