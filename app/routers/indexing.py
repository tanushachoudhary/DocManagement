from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Document
from app.services.document_store import index_document
from app.services.vector_store import save_index

# Initialize the router ONLY ONCE
router = APIRouter()

# --- Endpoint 1: Manual Indexing ---
@router.post("/documents/index")
def index_document_api(doc_id: str, text: str):
    """
    Manually index a string of text under a specific ID.
    """
    index_document(doc_id, text)
    return {"message": "Document indexed successfully"}

# # --- Endpoint 2: System Sync (The Fix) ---
# @router.post("/system/sync-vectors")
# def sync_vectors_from_sql(db: Session = Depends(get_db)):
#     """
#     Emergency Fix: Reads all text from SQL and re-indexes it into FAISS.
#     Useful if the server restarted and the in-memory index was lost.
#     """
#     # 1. Get all documents from SQL
#     docs = db.query(Document).all()
    
#     count = 0
#     for doc in docs:
#         # Check if the document has text to index
#         if doc.extracted_text:
#             # 2. Re-chunk and Re-index
#             # We use the existing logic, passing the ID and the text
#             index_document(doc.id, doc.extracted_text)
#             count += 1
    
#     # 3. Force a save to disk so it survives the NEXT restart
#     save_index()
    
#     return {"message": f"Successfully re-synced {count} documents from SQL to Vector Store."}