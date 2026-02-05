import feedparser
import json
import os
from datetime import datetime
from time import mktime

# 1. 수집할 RSS 리스트 
RSS_URLS = [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.bleepingcomputer.com/feed/",
    "https://cloudblog.withgoogle.com/topics/threat-intelligence/rss/",
    "https://research.checkpoint.com/feed/",
    "https://www.darkreading.com/rss.xml",
    "https://isc.sans.edu/rssfeed_full.xml",
    "https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss.xml",
    "https://cvefeed.io/rssfeed/latest.xml",
    "https://www.ilsole24ore.com/rss/tecnologia--cybersicurezza.xml",
    "https://www.ilsole24ore.com/rss/tecnologia.xml",
    "https://www.cybersecurity360.it/feed/",
    "https://feeds.feedburner.com/eset/blog",
    "https://blog.talosintelligence.com/rss/",
    "https://www.marktechpost.com/feed/",
    "https://news.mit.edu/rss/topic/artificial-intelligence2",
    "https://research.google/blog/rss/",
    "https://openai.com/news/rss.xml",
    "https://nvidianews.nvidia.com/releases.xml",
    "https://developer.nvidia.com/blog/feed",
    "https://feeds.feedburner.com/nvidiablog"
]

def fetch_rss_feeds():
    all_articles = []
    
    print(f"총 {len(RSS_URLS)}개의 RSS 피드 수집을 시작합니다...")

    for url in RSS_URLS:
        try:
            # RSS 파싱
            feed = feedparser.parse(url)
            
            # 피드 제목 가져오기 
            source_name = feed.feed.get('title', url)
            print(f"   - 수집 중: {source_name}")

            # 각 피드에서 최신 글 5개만 가져오기
            for entry in feed.entries[:5]:
                # 날짜 처리 
                published_date = "Unknown Date"
                timestamp = 0
                
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    # 구조화된 시간 데이터를 읽어서 타임스탬프와 문자열로 변환
                    timestamp = mktime(entry.published_parsed)
                    published_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    timestamp = mktime(entry.updated_parsed)
                    published_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

                # 기사 정보 구조화
                article = {
                    "source": source_name,
                    "title": entry.get('title', 'No Title'),
                    "link": entry.get('link', ''),
                    "published": published_date,
                    "timestamp": timestamp, # 정렬용
                    "summary": entry.get('summary', entry.get('description', 'No Summary'))[:500] # 요약 너무 길면 자르기
                }
                all_articles.append(article)

        except Exception as e:
            print(f"❌ 오류 발생 ({url}): {e}")

    # 2. 날짜 최신순으로 정렬 
    all_articles.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return all_articles

def save_to_json(data, filename="rss_data.json"):
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    # 2. 경로 결합
    file_path = os.path.join(output_dir, filename)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"\n수집 완료! 총 {len(data)}개의 기사가 '{file_path}'에 저장되었습니다.")

if __name__ == "__main__":
    # 테스트용
    from rss_collector import fetch_rss_feeds
    data = fetch_rss_feeds()
    save_to_json(data)