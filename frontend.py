import streamlit as st
import requests
import os

# CONFIGURATION
# If your backend is running locally on port 8000
# If running in Docker, use the service name 'backend'. 
# If running locally, default to localhost.
API_BASE_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# Page Config
st.set_page_config(
    page_title="RAG Document Assistant",
    page_icon="📄",
    layout="wide"
)

st.title("RAG Document Assistant")
st.markdown("Upload documents, search them, or ask the AI questions.")

# ==========================================
# SIDEBAR: USER MANAGEMENT
# Endpoints: POST /users
# ==========================================
with st.sidebar:
    st.header("User Management")
    
    #1 Create User
    with st.expander("Register new user"):
        new_id=st.text_input("ID")
        new_name=st.text_input("Name")
        if st.button("Create User"):
            try:
                payload={"id":new_id,"name":new_name}
                res=requests.post(f"{API_BASE_URL}/users",json=payload)
                if(res.status_code==200 or res.status_code==201):
                    st.success(f"Created! ID: {res.json().get('id')}")
                else:
                    st.error(f"Error: {res.text}")
            except Exception as e:
                st.error(f"Conn Error: {e}")
            
    st.markdown("---")
    
    #session USER ID (Global for other tabs)
    st.subheader("Current Session")
    user_id=st.text_input("Enter User ID for Actions:", value="u1")
    st.info("This ID is used for uploads and fetching docs.")


# Create three tabs for main functionality
tab_files, tab_chat, tab_search,tab_admin = st.tabs(["📂 My Files", "💬 Chat with AI", "🔍 Search","🛠️ Admin / Debug"])

# ==========================================
# TAB 1: FILES (Upload & List)
# Endpoints: POST /documents/upload, GET /users/{id}/documents
# ==========================================
with tab_files:
    col1, col2 = st.columns(2)
    
    #Section A : Upload (POST /documents/upload)
    with col1:
        st.subheader("Upload Document")
        uploaded_file = st.file_uploader("Choose PDF/Image", type=["pdf","png","jpg"])
        
        if st.button("Upload file", type="primary"):
            if uploaded_file and user_id:
                with st.spinner("Uploading & Indexing..."):
                    try:
                        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                        data = {"user_id": user_id}
                        res = requests.post(f"{API_BASE_URL}/documents/upload", files=files, data=data)
                        if res.status_code == 201:
                            st.success("Uploaded!")
                            st.json(res.json())
                        else:
                            st.error(res.text)
                    except Exception as e:
                        st.error(str(e))

# Section B: List Documents (GET /users/{user_id}/documents)
    with col2:
        st.subheader("📋 My Documents")
        if st.button("Refresh List"):
            try:
                res = requests.get(f"{API_BASE_URL}/users/{user_id}/documents")
                if res.status_code == 200:
                    docs = res.json()
                    if docs:
                        for d in docs:
                            with st.expander(f"📄 {d.get('filename', 'Doc')} (ID: {d.get('id')})"):
                                st.write(f"**Created:** {d.get('created_at')}")
                                st.text(d.get('extracted_text')[:100] + "...")
                    else:
                        st.info("No documents found for this user.")
                else:
                    st.error(res.text)
            except Exception as e:
                st.error(str(e))


# ==========================================
# TAB 2: CHAT WITH AI
# Endpoints: POST /ai/ask
# ==========================================
with tab_chat:
    st.header("Ask the AI")
    
    # Simple Chat Interface
    user_query = st.text_area("Enter your question:", height=100, placeholder="e.g., What does the HR policy say about remote work?")

    if st.button("Ask Question", type="primary"):
        if user_query:
            with st.spinner("Thinking..."):
                try:
                    # Payload matching 'AskRequest' in ai.py
                    payload = {"question": user_query}
                    
                    response = requests.post(f"{API_BASE_URL}/ai/ask", json=payload)

                    if response.status_code == 200:
                        data = response.json()
                        
                        # Display Answer
                        st.markdown(f"### Answer")
                        st.write(data.get("answer"))

                        # Display Metadata (Intent)
                        intent = data.get('intent', 'Unknown')
                        st.info(f"**Detected Intent:** {intent}")
                        
                        # Display Source Documents (if available)
                        sources = data.get("sources", [])
                        if sources and intent == "retrieve":
                            st.markdown("---")
                            st.markdown("### Source Documents")
                            st.caption(f"The answer above was generated using {len(sources)} relevant document chunk(s):")
                            
                            for idx, source in enumerate(sources, 1):
                                with st.expander(f"Source #{idx}"):
                                    st.text(source)
                        elif intent == "no_docs":
                            st.markdown("---")
                            st.warning("No relevant documents were found to answer this question.")
                    else:
                        st.error(f"Error {response.status_code}: {response.text}")

                except Exception as e:
                    st.error(f"Connection Error: {e}")
        else:
            st.warning("Please enter a question.")


# ==========================================
# TAB 3: SEMANTIC SEARCH (DEBUG)
# Endpoints: POST /search
# ==========================================
with tab_search:
    st.header("Debug: Semantic Search")
    st.write("See exactly which text chunks match your query.")

    search_query = st.text_input("Search phrase:", placeholder="e.g., refund policy")
    k_results = st.slider("Number of results to retrieve:", min_value=1, max_value=10, value=3)

    if st.button("Search Database"):
        if search_query:
            with st.spinner("Searching vector database..."):
                try:
                    # Payload matching your search endpoint
                    # Note: We send query params as query string or json depending on your implementation
                    # Based on your last code: POST /search?query=...&k=...
                    params = {"query": search_query, "k": k_results}
                    response = requests.post(f"{API_BASE_URL}/search", params=params)

                    if response.status_code == 200:
                        data = response.json()
                        results = data.get("results", [])

                        if not results:
                            st.info("No matching documents found.")
                        
                        for i, doc in enumerate(results):
                            with st.expander(f"Result #{i+1}"):
                                st.markdown(f"**Content:**\n{doc['text']}")
                                st.caption(f"Metadata: {doc['metadata']}")
                    else:
                        st.error(f"Search Failed: {response.text}")

                except Exception as e:
                    st.error(f"Connection Error: {e}")
                    
                    
# ==========================================
# TAB 4: ADMIN / DEBUG
# Endpoints: POST /documents (Manual Meta), POST /documents/index
# ==========================================
    
    # #1 create document metadata POST /documents
    # with col3:
    #     st.subheader("1. Register Metadata")
    #     meta_filename = st.text_input("Filename",value = "manual_doc.txt")
    #     meta_text = st.text_area("Extracted Text",height = 100)
    #     if st.button("Create DB Entry"):
    #         try:
    #             #schema matches DocumentCreate
    #             payload = {
    #                 "filename":meta_filename,
    #                 "extracted_text":meta_text,
    #                 "owner_id":int(user_id) if user_id.isdigit() else user_id
    #             }
    #             res=requests.post(f"{API_BASE_URL}/documents",json=payload)
    #             if res.status_code == 201:
    #                 st.success(f"Created! ID: {res.json().get('id')}")
    #             else:
    #                 st.error(res.text)
    #         except Exception as e:
    #             st.error(str(e))
                
                
# 2. Manual index (POST /documents/index)
# forces text into vector store manually
with tab_admin:
    st.warning("For Manual operations only")
    col3, col4 = st.columns(2)
    
    # Manual Indexing
    with col3:
        st.subheader("Manual Indexing")
        index_id = st.text_input("Document UUID to Index")
        index_text = st.text_area("Text to Index", height=100)
        
        if st.button("Force Index"):
            try: 
                res = requests.post(
                    f"{API_BASE_URL}/documents/index",
                    params={"doc_id": index_id, "text": index_text}
                )
                if res.status_code == 200:
                    st.success("Indexed Successfully!")
                else:
                    st.error(res.text)
            except Exception as e:
                st.error(str(e))