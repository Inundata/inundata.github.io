@echo off
chcp 65001 >nul
call db-pull.bat
"C:\Program Files\Git\bin\bash.exe" -c "/e/OneDrive/Github/inundata.github.io/_posts/upload-data/deploy.sh"