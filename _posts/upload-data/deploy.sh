#!/bin/bash

# 오늘 날짜와 어제 날짜 설정
today=$(date +"%y%m%d")
yesterday=$(date -d "yesterday" +"%y%m%d")

echo "오늘 날짜: $today"
echo "어제 날짜: $yesterday"

# Git 작업 디렉토리로 이동
cd "/e/OneDrive/Github/inundata.github.io" || exit

# # Git LFS에서 오늘과 어제 파일 삭제
# for file in temperature_"$yesterday".xlsx temperature_wide_"$yesterday".xlsx temperature_"$today".xlsx temperature_wide_"$today".xlsx; do
#     if [ -f "$file" ]; then
#         git lfs rm --cached "$file"
#         rm "$file"
#     fi
# done

# 변경사항 커밋 및 푸시
git add .
git commit -m "자동 업데이트: $(date)"

# # Git LFS 및 히스토리 정리
# git lfs prune
# git reflog expire --expire=now --all
# git gc --prune=now

# GitHub로 Push
git push -u origin main

echo "Git 작업 완료!"
