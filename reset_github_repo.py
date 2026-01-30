import requests
import os
import time
import subprocess
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# GitHub 설정
GITHUB_USER = "Inundata"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = "inundata.github.io"

# GitHub API 헤더
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}


def delete_github_repo():
    """ 기존 GitHub 레포지토리를 삭제하고 삭제 여부를 확인하는 함수 """
    delete_url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}"
    
    # 최대 10번 재시도
    for attempt in range(10):
        response = requests.delete(delete_url, headers=headers)
        
        if response.status_code == 204:
            print(f"✅ GitHub 저장소 삭제 완료: {REPO_NAME}")
            break
        elif response.status_code == 404:
            print(f"✅ GitHub 저장소가 이미 존재하지 않음.")
            break
        else:
            print(f"⚠️ GitHub 저장소 삭제 실패 (시도 {attempt + 1}/10): {response.status_code}")
            time.sleep(5)
    else:
        print("❌ 최대 재시도 횟수를 초과하여 삭제 실패")
        return False

    # 삭제 확인 (최대 10회 재시도)
    for attempt in range(10):
        check_response = requests.get(delete_url, headers=headers)
        if check_response.status_code == 404:
            print("✅ GitHub 저장소 삭제가 확인됨.")
            return True
        print(f"⌛ 삭제 확인 중... (시도 {attempt + 1}/10)")
        time.sleep(5)
    
    print("❌ GitHub 저장소 삭제 확인 실패")
    return False


def create_github_repo():
    """ 새로운 GitHub 저장소를 생성하는 함수 """
    create_url = "https://api.github.com/user/repos"
    payload = {"name": REPO_NAME, "private": False}

    response = requests.post(create_url, json=payload, headers=headers)
    if response.status_code == 201:
        print(f"🟢 새로운 GitHub 저장소 생성 완료: {REPO_NAME}")
        return True
    else:
        print(f"❌ GitHub 저장소 생성 실패: {response.status_code}, {response.text}")
        return False


def run_command(command, cwd=None):
    """ 안전하게 시스템 명령어 실행하는 함수 (UTF-8 인코딩 적용) """
    result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        print(f"⚠ Command execution failed: {command}")  # 영어 메시지 변경
        print(result.stderr)
    return result


def setup_local_repo():
    """ 로컬 Git 저장소 초기화 및 GitHub 원격 연결 """
    repo_path = f"E:\\OneDrive\\Github\\{REPO_NAME}"

    # 기존 .git 폴더 삭제 (안전한 초기화)
    if os.path.exists(os.path.join(repo_path, ".git")):
        run_command("rmdir /s /q .git", cwd=repo_path)

    run_command("git init", cwd=repo_path)

    print("✅ 로컬 Git 저장소 초기화 완료")


def setup_git_lfs():
    """ Git LFS 설정 """
    run_command("git lfs install")
    run_command('git lfs track "*.xlsx"')

    print("✅ Git LFS 설정 완료")


def commit_and_push():
    """ 변경 사항 커밋 및 GitHub에 푸시 """
    repo_path = f"E:\\OneDrive\\Github\\{REPO_NAME}"
    
    # git 연결 및 최초 commit
    run_command("git add .", cwd=repo_path)  # cwd 추가 필요 (안전성 확보)
    run_command('git commit -m "Initial commit"', cwd=repo_path) # cwd 추가 필요

    # 기본 브랜치를 `main`으로 변경
    run_command("git branch -M main", cwd=repo_path)

    # [수정 핵심] URL에 GITHUB_USER와 GITHUB_TOKEN을 직접 포함시킴
    # 형식: https://<USER>:<TOKEN>@github.com/<USER>/<REPO>.git
    remote_url = f"https://{GITHUB_USER}:{GITHUB_TOKEN}@github.com/{GITHUB_USER}/{REPO_NAME}.git"
    
    # 보안상 로그에는 토큰을 제외하고 출력하거나, 아예 출력을 생략하는 것이 좋음
    run_command(f"git remote add origin {remote_url}", cwd=repo_path)

    # GitHub에 푸시
    run_command("git push -u origin main", cwd=repo_path)
    print("🚀 GitHub Pages 푸시 완료")



# 실행 순서
if __name__ == "__main__":
    if delete_github_repo():
        time.sleep(5)
        if create_github_repo():
            time.sleep(5)
            setup_local_repo()
            time.sleep(5)
            setup_git_lfs()
            time.sleep(5)
            commit_and_push()
            print("✅ 모든 작업 완료!")
        else:
            print("❌ 저장소 생성 실패로 중단됨.")
    else:
        print("❌ 저장소 삭제 실패로 중단됨.")
