from sentence_transformers import SentenceTransformer

# Load a pre-trained AI model designed for semantic similarity.
# "all-MiniLM-L6-v2" is chosen because it is very fast and lightweight,
# making it perfect for running on a standard laptop (CPU).
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(text: str):
    """
    Converts a text string into a vector (list of floating point numbers).
    
    Args:
        text (str): The input text to convert.
        
    Returns:
        numpy.ndarray: An array of 384 numbers representing the semantic meaning.
    """
    # The .encode() method processes the text through the transformer network.
    return model.encode(text)