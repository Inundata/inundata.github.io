@echo off
chcp 65001 >nul

@REM REM 현재 날짜 가져오기
@REM for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value ^| find "LocalDateTime"') do set datetime=%%I
@REM set today=%datetime:~2,6%

@REM REM 어제 날짜 가져오기 (PowerShell 사용)
@REM for /f %%I in ('powershell -command "& {(Get-Date).AddDays(-1).ToString('yyMMdd')}"') do set yesterday=%%I

@REM echo 오늘 날짜: %today%
@REM echo 어제 날짜: %yesterday%

REM 1. Run Python 스크립트
"C:\Users\HERO\anaconda3\envs\db\python.exe" "E:\OneDrive\Github\inundata.github.io\_posts\upload-data\db-pull.py"


@REM REM 2. Git 작업 시작
@REM cd /d "E:\OneDrive\Github\inundata.github.io"

@REM REM Git LFS에서 오늘과 어제의 파일 삭제
@REM for %%F in (temperature_%yesterday%.xlsx temperature_wide_%yesterday%.xlsx temperature_%today%.xlsx temperature_wide_%today%.xlsx) do (
@REM     if exist "%%F" (
@REM         git lfs rm --cached "%%F"
@REM         del "%%F"
@REM     )
@REM )

@REM REM 변경사항 반영
@REM git add .
@REM git commit -m "자동 업데이트: %date% %time%"


@REM REM Git LFS에서 사용되지 않는 파일 정리
@REM echo y | git lfs prune

@REM REM Git 히스토리 정리 (LFS 파일 삭제 후 불필요한 기록 삭제)
@REM echo y | git reflog expire --expire=now --all
@REM echo y | git gc --prune=now

@REM REM GitHub로 Push
@REM git config --global credential.credentialStore dpapi
@REM git push -u origin main

@REM echo 작업 완료!
@REM pause
