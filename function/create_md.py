import os
from datetime import datetime

def create_md(title, content, md_path):
    # 저장할 디렉토리 (GitHub Pages 저장소 내 경로)
    output_dir = str(os.getcwd())  # 실제 경로로 변경하세요

    # 오늘 날짜 가져오기
    today = datetime.today().strftime("%Y-%m-%d")

    # 파일명 설정
    md_name = f"{today}-temp.md"
    md_path = os.path.join(output_dir, md_name)

    # Markdown 파일 내용
    md_content = f"""---
title:  "{title}"
show_date: true
comments: true
layout: single
categories:
- data
tags: 
- data
toc: true
toc_sticky: true
published: true
---

    {content}
    """

    # 디렉토리 생성 (없을 경우)
    os.makedirs(output_dir, exist_ok=True)

    # 파일 생성 및 저장
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"md 파일 생성 완료")
