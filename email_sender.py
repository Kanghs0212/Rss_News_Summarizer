import smtplib
import os
from email.message import EmailMessage
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def send_email():
    # HTML 파일 읽기
    try:
        with open("summary_report.html", "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        print("❌ 보낼 파일(summary_report.html)이 없습니다.")
        return

    msg = EmailMessage()
    today_date = datetime.now().strftime("%Y-%m-%d")
    
    msg['Subject'] = f"Tech & AI Briefing ({today_date})"
    msg['From'] = os.getenv("GMAIL_USER")
    msg['To'] = os.getenv("GMAIL_USER") # 받는 사람 이메일
    
    # ★ 핵심 변경 사항: add_alternative를 사용하여 HTML로 설정 ★
    msg.add_alternative(html_content, subtype='html')

    try:
        print("📮 HTML 메일 발송 중...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv("GMAIL_USER"), os.getenv("GMAIL_APP_PASSWORD"))
            smtp.send_message(msg)
        print("✅ 전송 완료! 메일함을 확인하세요.")
    except Exception as e:
        print(f"❌ 전송 실패: {e}")

if __name__ == "__main__":
    send_email()