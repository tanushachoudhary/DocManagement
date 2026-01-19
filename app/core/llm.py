from langchain_openai import AzureChatOpenAI
from app.core.config import get_settings

# Load settings once to access credentials
settings = get_settings()

# Initialize the Azure OpenAI Client
# We use temperature = 0 to ensure deterministic (consistent) answers,
# which is crucial for factual RAG applications.
llm = AzureChatOpenAI(
    azure_endpoint = settings.AZURE_OPENAI_ENDPOINT,
    api_key = settings.AZURE_OPENAI_API_KEY,
    api_version = settings.AZURE_OPENAI_API_VERSION,  
    deployment_name = settings.AZURE_OPENAI_DEPLOYMENT_NAME,
    temperature = 0
)