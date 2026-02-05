import rss_collector
import summarizer
import email_sender
import time

def main():
    print("🚀 뉴스 요약 자동화 시스템을 시작합니다.")
    
    # 1. RSS 수집
    print("\n[Step 1] RSS 데이터 수집")
    rss_data = rss_collector.fetch_rss_feeds()
    rss_collector.save_to_json(rss_data)
    
    # 2. AI 요약 및 HTML 생성
    print("\n[Step 2] AI 요약 및 HTML 디자인")
    html_report = summarizer.generate_summary()
    
    if html_report:
        # 3. 이메일 발송
        print("\n[Step 3] 이메일 발송")
        email_sender.send_email()
        print("\n✨ 모든 작업이 성공적으로 끝났습니다!")
    else:
        print("\n❌ 요약 생성 실패로 메일을 보내지 않습니다.")

if __name__ == "__main__":
    main()