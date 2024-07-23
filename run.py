from bili_assistant import BiliAssistant
import logging
import argparse

logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  
  subparsers = parser.add_subparsers(dest='command')

  dl_parser = subparsers.add_parser('dl')
  dl_parser.add_argument('--video_id', type=str, help='video id', required=True)
  dl_parser.add_argument('--model', type=str, help='model', default='ark')

  query_parser = subparsers.add_parser('query')
  query_parser.add_argument('--video_id', type=str, help='video id', required=True)
  query_parser.add_argument('--content', type=str, help='content', required=True)
  query_parser.add_argument('--model', type=str, help='model', default='ark')
  query_parser.add_argument('--top_n', type=int, help='top_n', default=5)
  
  args = parser.parse_args()

  if args.command is None:
    parser.print_help()
  elif args.command == 'dl':
    video_id = args.video_id
    assistant = BiliAssistant(model=args.model)
    assistant.save_video_comments(video_id)
  elif args.command == 'query':
    video_id = args.video_id
    content = args.content
    assistant = BiliAssistant(model=args.model)
    # tip: ark的embedding模型提供指令效果更佳(如: 为这个句子生成表示以用于检索相关文章：)，详情请参考文档 https://www.volcengine.com/docs/82379/1285467
    similar_comments = assistant.similar_comments(video_id, content, top_n=args.top_n)
    documents = similar_comments['documents'][0]
    distances = similar_comments['distances'][0]
    for i in range(len(documents)):
      print(f"content: {documents[i]}, distance: {distances[i]}")