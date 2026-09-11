import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.core import Root
# from snowflake.cortex import Complete
from snowflake.snowpark.functions import lit, call_builtin
import config
import prompt_builder

def fetch_rag_context(session) -> tuple[str,str]:
    inventory_df = session.table(f"{config.DATABASE_NAME}.{config.SCHEMA_NAME}.{config.INVENTORY_TABLE}").to_pandas()
    inventory_context = inventory_df.to_string(index=False)
            
    schedule_df = session.table(f"{config.DATABASE_NAME}.{config.SCHEMA_NAME}.{config.SCHEDULE_TABLE}").to_pandas()
    schedule_context = schedule_df.to_string(index=False)

    return inventory_context, schedule_context

st.title("Pharma company AI assistant")

session = get_active_session()
root = Root(session)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input("E.g. What drugs do we produce?")
if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            # we use 2 tables and build the propmt with their info
            inventory_context, schedule_context = fetch_rag_context(session)
        
            search_service = root.databases[config.DATABASE_NAME].schemas[config.SCHEMA_NAME].cortex_search_services[config.SEARCH_SERVICE_NAME]
            search_results = search_service.search(user_prompt, columns=["FILE_NAME", "CHUNK_TEXT"], limit=config.MAX_SEARCH_RESULTS)
            
            rag_context = "\n\n".join(
                [f"Source: {row['FILE_NAME']}\n{row['CHUNK_TEXT']}" for row in search_results.results]
            ) if search_results.results else ""
            
            system_prompt = prompt_builder.build_system_prompt(inventory_context, schedule_context, rag_context)
            full_prompt = f"{system_prompt}\n\nUser Question: {user_prompt}"

            # preeviously it was just session.sql...
            # ai_answer = Complete(config.COMPLETION_MODEL, full_prompt) # 403 error

            # don't call REST API, but use the session
            df_result = session.range(1).select(
                call_builtin("SNOWFLAKE.CORTEX.COMPLETE", lit(config.COMPLETION_MODEL), lit(full_prompt))
            ).collect()
            
            ai_answer = df_result[0][0]
            
            st.markdown(ai_answer)
            st.session_state.messages.append({"role": "assistant", "content": ai_answer})