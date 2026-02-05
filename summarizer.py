import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def generate_summary():
    # outputs 폴더에서 읽기
    input_path = os.path.join("outputs", "rss_data.json")
    
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            articles = json.load(f)
    except FileNotFoundError:
        print(f"{input_path} 파일이 없습니다. 먼저 수집기를 실행하세요.")
        return None

    if not articles:
        return None

    today_str = datetime.now().strftime("%d %B %Y")

    # 2. Gemini 프롬프트 (HTML 디자인 지침 포함)
    prompt_text = f"""
    아래 뉴스 데이터를 바탕으로 **HTML 이메일 뉴스레터** 코드를 작성해줘.
    
    [데이터]
    {json.dumps(articles[:30], ensure_ascii=False)}

    [디자인 요구사항]
    1. 전체 스타일: 배경은 흰색, 글씨는 가독성 좋은 산세리프(Arial, sans-serif) 폰트.
    2. **헤더(Header)**:
       - 배경색: 다크 블루 (#2C3E50)
       - 글자색: 흰색 (#FFFFFF)
       - 내용: "Tech & AI Briefing - {today_str}" (가운데 정렬, 굵게)
       - 여백(padding): 20px
    3. **메인 타이틀**:
       - 내용: "🧠 Tech, AI & Cyber – Top Stories"
       - 색상: 붉은색 (#E74C3C)
       - 스타일: 텍스트 아래에 붉은색 밑줄(border-bottom) 2px
    4. **본문 내용**:
       - 카테고리(예: AI & Machine Learning)는 진한 검정색으로 굵게(h3 태그).
       - 뉴스 항목은 <ul>과 <li> 태그를 사용.
       - 각 뉴스는 한글로 2줄 요약.
       - 뉴스 끝에는 출처(Source)를 파란색(#3498db) 링크 텍스트로 표시. (링크 주소는 기사의 link 필드 사용)
    5. **제약 사항**:
       - <head>나 <style> 태그를 쓰지 말고, 모든 스타일은 태그 안에 **inline style** (예: <div style="color:red;">)로 작성해줘. (이메일 호환성 때문)
       - 오직 <body> 태그 안의 내용만 출력해줘 (```html 마크다운 없이).

    """

    print("Gemini가 HTML 뉴스레터를 디자인 중입니다...")
    
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-3-flash-preview')
    
    response = model.generate_content(prompt_text)
    html_content = response.text.replace("```html", "").replace("```", "") # 마크다운 제거

    # outputs 폴더에 저장 
    output_path = os.path.join("outputs", "summary_report.html")
    
    os.makedirs("outputs", exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"요약 완료! '{output_path}' 파일이 생성되었습니다.")
    return html_content

if __name__ == "__main__":
    generate_summary()