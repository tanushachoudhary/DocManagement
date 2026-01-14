"""
Chunk Size (800 characters):
Optimal for LLM context windows: Most language models can process 800 characters efficiently without excessive token usage
Semantic coherence: 800 characters typically contains 2-4 complete paragraphs or 150-200 words, which is enough to maintain meaningful context
Manageable embeddings: Vector databases process ~800 char chunks efficiently for semantic search
Balance: Large enough to capture context, small enough to be specific for targeted retrieval

Chunk Overlap (150 characters):
Context preservation: 150 chars (~25-30 words) ensures important information at chunk boundaries isn't lost
Smooth transitions: When searching, overlapping chunks help catch relevant information that might fall at the edge between two chunks
Prevents semantic breaks: Without overlap, splitting a sentence across chunks could lose meaning
~19% overlap ratio: 150/800 = 18.75% is an industry-standard ratio for chunk-overlap balance (not too little, not excessive)
"""
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(
    text: str,
    chunk_size: int = 800,
    chunk_overlap: int = 150
) -> list[str]:
    """
    Splits long text into smaller chunks while preserving context.
    
    Why Recursive? 
    It tries to split on paragraphs (\n\n) first, then newlines (\n), 
    then spaces. This keeps related sentences together better than 
    splitting strictly by character count.
    
    Args:
        chunk_size: Target size of each chunk (characters).
        chunk_overlap: How much characters repeat between chunks (preserves context).
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""] # Priority order for splitting
    )
    return splitter.split_text(text)