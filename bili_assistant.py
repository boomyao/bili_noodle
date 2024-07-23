from dotenv import load_dotenv
load_dotenv('.env.local')

from bili_comment import fetch_comments
from embedding import create_embeddings
from vector_db import get_or_create_collection
import logging

class BiliAssistant:
  def __init__(self, model='ark'):
    self.model = model
    self.vector_collection = get_or_create_collection(name=f'bili_comment_{model}')

  def similar_comments(self, video_id: str, content: str, top_n=5, threshold=0.8):
    query_embeddings = create_embeddings([content], model=self.model)
    similar_comments = self.vector_collection.query(
      query_embeddings=query_embeddings,
      n_results=top_n,
      where={'vid': video_id},
    )
    return similar_comments

  def save_video_comments(self, video_id, max_page=1000):
    comment_generator = fetch_comments(video_id=video_id, max_page=max_page)

    for comments in comment_generator:
      comment_texts = [x['content'] for x in comments]
      ids = [str(x['rpid']) for x in comments]
      comment_embeddings = create_embeddings(comment_texts, model=self.model)
      self.vector_collection.upsert(
        ids=ids,
        documents=comment_texts,
        embeddings=comment_embeddings,
        metadatas=comments,
      )
      logging.info(f"Saved {len(comments)} comments")