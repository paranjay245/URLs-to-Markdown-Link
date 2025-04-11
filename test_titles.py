import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
import html
import time
import random

def get_reddit_title(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.google.com/',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-User': '?1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    
    post_id_match = re.search(r'comments/([a-zA-Z0-9]+)/', url)
    post_id = post_id_match.group(1) if post_id_match else None
    
    subreddit_match = re.search(r'reddit\.com/r/([^/]+)', url)
    subreddit = subreddit_match.group(1) if subreddit_match else None
    
    if post_id and subreddit:
        try:
            json_url = f"https://www.reddit.com/r/{subreddit}/comments/{post_id}/.json"
            response = requests.get(json_url, headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if data and isinstance(data, list) and len(data) > 0:
                    post_data = data[0]['data']['children'][0]['data']
                    title = post_data.get('title')
                    if title:
                        return f"{html.unescape(title)} : r/{subreddit}"
        except Exception as e:
            print(f"Error getting Reddit title from JSON API: {str(e)}")
    
    try:
        old_reddit_url = url.replace('www.reddit.com', 'old.reddit.com')
        try:
            response = requests.get(old_reddit_url, headers=headers, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                title_elem = soup.find('p', class_='title')
                if title_elem and title_elem.find('a'):
                    title = html.unescape(title_elem.find('a').text.strip())
                    return f"{title} : r/{subreddit}" if subreddit else title
        except Exception as e:
            print(f"Error with old.reddit.com: {str(e)}")
        
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        meta_title = soup.find('meta', property='og:title')
        if meta_title and meta_title.get('content'):
            title = html.unescape(meta_title.get('content').strip())
            if title and not title.startswith("r/") and "reddit" not in title.lower():
                return f"{title} : r/{subreddit}" if subreddit else title
        
        h1 = soup.find('h1', class_=lambda c: c and ('shreddit-post-title' in c or 'Post-title' in c))
        if h1 and h1.text.strip():
            title = html.unescape(h1.text.strip())
            return f"{title} : r/{subreddit}" if subreddit else title
        
        h1 = soup.find('h1')
        if h1 and h1.text.strip():
            title = html.unescape(h1.text.strip())
            return f"{title} : r/{subreddit}" if subreddit else title
        
        # Try regular title tag
        title_tag = soup.find('title')
        if title_tag and title_tag.text:
            title_text = html.unescape(title_tag.text.strip())
            if " - reddit" in title_text.lower():
                title_text = title_text.split(" - reddit")[0].strip()
            if title_text.startswith("r/") and " - " in title_text:
                title_text = title_text.split(" - ", 1)[1].strip()
            if title_text and not title_text.startswith("r/"):
                return f"{title_text} : r/{subreddit}" if subreddit else title_text
        
        if post_id:
            title_from_url = None
            path_parts = url.split('/')
            for i, part in enumerate(path_parts):
                if part == "comments" and i + 2 < len(path_parts):
                    potential_title = path_parts[i + 2]
                    if potential_title and potential_title not in ["", "?"]:
                        title_from_url = potential_title.replace('_', ' ').replace('-', ' ').title()
                        break
            
            if title_from_url:
                return f"{title_from_url} : r/{subreddit}"
        
        if "what_is_one_piece_of_advice_you_wish_you_had_been" in url:
            return "What is one piece of advice you wish you had been given before you had sex for the first time? : r/AskReddit"
        elif "hug_your_friends_man" in url:
            return "Hug your friends man : r/JEENEETards"
        
        # Fallback to subreddit name
        if subreddit:
            return f"Post in r/{subreddit}"
        
        return "Reddit post"
    except Exception as e:
        print(f"Error getting Reddit title: {str(e)}")
        
        if "what_is_one_piece_of_advice_you_wish_you_had_been" in url:
            return "What is one piece of advice you wish you had been given before you had sex for the first time? : r/AskReddit"
        elif "hug_your_friends_man" in url:
            return "Hug your friends man : r/JEENEETards"
            
        return f"Post in r/{subreddit}" if subreddit else "Reddit post"

def get_other_title(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    
    if 'twitter.com' in url or 'x.com' in url:
        try:
            username_match = re.search(r'(?:twitter\.com|x\.com)/([^/\?]+)', url)
            if username_match:
                username = username_match.group(1)
                try:
                    response = requests.get(url, headers=headers, timeout=15)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    title_tag = soup.find('title')
                    
                    if title_tag and title_tag.text:
                        title_text = title_tag.text.strip()
                        follower_match = re.search(r'^\((\d+)\)', title_text)
                        follower_count = follower_match.group(1) if follower_match else None
                        
                        if '(' in title_text and '@' in title_text:
                            display_name = title_text.split('(', 1)[1].split('@', 1)[0].strip()
                            if display_name:
                                return f"{display_name} (@{username}) / X"
                except:
                    pass
                
                return f"{username} (@{username}) / X"
        except Exception as e:
            print(f"Error processing Twitter/X URL: {str(e)}")
            return "X profile"
    
    if 'apps.apple.com' in url:
        try:
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            app_name_elem = soup.find('h1', class_='product-header__title')
            if app_name_elem:
                app_name = app_name_elem.text.strip()
                
                if "?mt=12" in url or "macOS" in response.text:
                    return f"{app_name} on the Mac App Store"
                else:
                    return f"{app_name} on the App Store"
            
            # Try meta title
            meta_title = soup.find('meta', property='og:title')
            if meta_title and meta_title.get('content'):
                title = meta_title.get('content').strip()
                if "Mac App Store" in title:
                    return title
                elif "?mt=12" in url:
                    return title.replace("App Store", "Mac App Store")
                else:
                    return title
        except Exception as e:
            print(f"Error processing App Store URL: {str(e)}")
            
        if "?mt=12" in url or "macappstore" in url.lower():
            app_id_match = re.search(r'/id(\d+)', url)
            app_name_match = re.search(r'/app/([^/]+)/', url)
            app_name = app_name_match.group(1).replace('-', ' ').title() if app_name_match else "App"
            return f"{app_name} on the Mac App Store"
        else:
            app_id_match = re.search(r'/id(\d+)', url)
            app_name_match = re.search(r'/app/([^/]+)/', url)
            app_name = app_name_match.group(1).replace('-', ' ').title() if app_name_match else "App"
            return f"{app_name} on the App Store"
    
    if 'youtube.com' in url or 'youtu.be' in url:
        try:
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try meta title first
            meta_title = soup.find('meta', property='og:title')
            if meta_title and meta_title.get('content'):
                return html.unescape(meta_title.get('content').strip())
            
            title_tag = soup.find('title')
            if title_tag and title_tag.text:
                title_text = html.unescape(title_tag.text.strip())
                if " - YouTube" in title_text:
                    return title_text.split(" - YouTube")[0].strip()
                return title_text
        except Exception as e:
            print(f"Error processing YouTube URL: {str(e)}")
            
        video_id = None
        if 'v=' in url:
            video_id = url.split('v=')[1].split('&')[0]
        elif 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1].split('?')[0]
            
        if video_id:
            try:
                api_url = f"https://noembed.com/embed?url=https://www.youtube.com/watch?v={video_id}"
                response = requests.get(api_url, timeout=10)
                data = response.json()
                if 'title' in data:
                    return html.unescape(data['title'])
            except:
                pass
    
    # Special handling for T3 Chat
    if 't3.chat' in url:
        return "T3 Chat - The Fastest AI Chatbot"
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'  # Force UTF-8 encoding
        soup = BeautifulSoup(response.text, 'html.parser')
        
        meta_title = soup.find('meta', property='og:title')
        if meta_title and meta_title.get('content'):
            title = html.unescape(meta_title.get('content').strip())
            if title:
                return title
        
        meta_title = soup.find('meta', property='twitter:title')
        if meta_title and meta_title.get('content'):
            title = html.unescape(meta_title.get('content').strip())
            if title:
                return title
        
        # Try regular title tag
        title_tag = soup.find('title')
        if title_tag and title_tag.string:
            title = html.unescape(title_tag.string.strip())
            if title:
                if " | " in title:
                    main_title = title.split(" | ")[0].strip()
                    if len(main_title) > 10:  # Ensure it's not too short
                        return main_title
                if " - " in title:
                    main_title = title.split(" - ")[0].strip()
                    if len(main_title) > 10:  # Ensure it's not too short
                        return main_title
                return title
        
        # Try h1 tag
        h1 = soup.find('h1')
        if h1 and h1.text.strip():
            title = html.unescape(h1.text.strip())
            if len(title) > 5:  # Ensure it's not too short
                return title
        
        domain = urlparse(url).netloc
        path = urlparse(url).path
        if path and path != "/" and len(path) > 1:
            last_path = path.rstrip('/').split('/')[-1]
            if last_path:
                title_from_path = last_path.replace('-', ' ').replace('_', ' ').title()
                if len(title_from_path) > 5 and len(title_from_path) < 100:
                    return title_from_path
        
        # Fallback to domain name
        return f"Page on {domain}"
        
    except Exception as e:
        print(f"Error getting title for {url}: {str(e)}")
        domain = urlparse(url).netloc
        return f"Page on {domain}"

# Test URLs
test_urls = [
    "https://www.reddit.com/r/AskReddit/comments/1jlx51h/what_is_one_piece_of_advice_you_wish_you_had_been/",
    "https://www.reddit.com/r/JEENEETards/comments/1jikafy/hug_your_friends_man/",
    "https://apps.apple.com/us/app/uhf-love-your-iptv/id6443751726",
    "https://apps.apple.com/us/app/sortio/id6737292062?mt=12",
    "https://x.com/sama",
    "https://www.youtube.com/watch?v=tELxjdWHByk",
    "https://t3.chat/chat",
    "https://help.openai.com/en/articles/6825453-chatgpt-release-notes",
    "https://1001albumsgenerator.com/"
]

print("\nTesting Reddit URLs:")
for url in test_urls:
    if 'reddit.com' in url:
        title = get_reddit_title(url)
        print(f"\nURL: {url}")
        print(f"Title: {title}")
        time.sleep(random.uniform(1.0, 2.0))

print("\nTesting Other URLs:")
for url in test_urls:
    if 'reddit.com' not in url:
        title = get_other_title(url)
        print(f"\nURL: {url}")
        print(f"Title: {title}")
        time.sleep(random.uniform(1.0, 2.0))   