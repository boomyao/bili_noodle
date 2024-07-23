import requests
import re
import time
import logging

logger = logging.getLogger(__name__)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


def get_video_id(bv):
    url = f'https://www.bilibili.com/video/{bv}'
    html = requests.get(url, headers=headers)
    html.encoding = 'utf-8'
    content = html.text
    aid_regx = '"aid":(.*?),"bvid":"{}"'.format(bv)
    video_aid = re.findall(aid_regx, content)[0]
    return video_aid

def create_comment_info(comment, video_id, level=0, comment_to=''):
  comment_info = {
      'rpid': comment['rpid'],
      'vid': video_id,
      'oid': comment['oid'],
      'content': comment['content']['message'],
      'level': level,
      'comment_to': comment_to,
      'like_count': comment['like'],
      'replied_at': comment['ctime'],
      'member_mid': comment['mid'],
      'member_uname': comment['member']['uname'],
      'member_sex': comment['member']['sex'],
      'member_sign': comment['member']['sign'],
  }
  return comment_info

def fetch_comment_replies(video_id, comment_id, parent_user_name, max_pages=1000):
    replies = []
    preLen = 0
    for page in range(1, max_pages + 1):
        url = f'https://api.bilibili.com/x/v2/reply/reply?oid={video_id}&type=1&root={comment_id}&ps=10&pn={page}'
        try:
            # 添加超时设置
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data and data.get('data') and 'replies' in data['data']:
                    for reply in data['data']['replies']:
                        reply_info = create_comment_info(reply, video_id=video_id, level=1, comment_to=parent_user_name)
                        replies.append(reply_info)
                    if preLen == len(replies):
                        break
                    preLen = len(replies)
                else:
                    return replies
        except requests.RequestException as e:
            print(f"请求出错: {e}")
            break
        # 控制请求频率
        time.sleep(1)
    return replies


def fetch_comments(video_id, max_page=1000):
    for page in range(1, max_page + 1):
        url = f'https://api.bilibili.com/x/v2/reply?pn={page}&type=1&oid={video_id}&sort=3'
        try:
            # 添加超时设置
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data and 'replies' in data['data']:
                    replies = data['data']['replies']
                    logger.info(f"Found {len(replies)} comments in page {page}")
                    if not replies:
                        break
                    comments = []
                    for comment in replies:
                        comment_info = create_comment_info(comment, video_id=video_id)
                        comments.append(comment_info)
                        # replies = fetch_comment_replies(video_id, comment['rpid'], comment['member']['uname'])
                        # comments.extend(replies)
                    yield comments
                else:
                    break
            else:
                break
        except requests.RequestException as e:
            print(f"请求出错: {e}")
            break
        # 控制请求频率
        time.sleep(1)
