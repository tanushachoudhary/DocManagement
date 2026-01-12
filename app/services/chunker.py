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