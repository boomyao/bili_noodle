from volcenginesdkarkruntime import Ark
from openai import OpenAI
import os

ark_client = Ark(
  base_url=os.getenv('ARK_BASE_URL'),
  api_key=os.getenv('ARK_API_KEY'),
)
ark_embedding_model = os.getenv('ARK_EMBEDDING_MODEL')

openai_client = OpenAI()
openai_embedding_model = os.getenv('OPENAI_EMBEDDING_MODEL', 'text-embedding-3-small')

def create_embeddings(texts, model='ark'):
  client = ark_client if model == 'ark' else openai_client
  embedding_model = ark_embedding_model if model == 'ark' else openai_embedding_model
  embedding_res = client.embeddings.create(
    model=embedding_model,
    input=texts,
  )
  return [x.embedding for x in embedding_res.data]