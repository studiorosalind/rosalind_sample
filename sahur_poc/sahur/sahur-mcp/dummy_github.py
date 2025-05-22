# GitHub MCP 더미 래퍼
def get_github_file(path: str):
    # 현실적인 더미 파일 내용 반환
    if path == "app/main.py":
        return {
            "path": "app/main.py",
            "content": "def main():\n    print('Hello, SAHUR!')\n"
        }
    elif path == "app/handler.py":
        return {
            "path": "app/handler.py",
            "content": "def handler(event):\n    return {'status': 'ok'}\n"
        }
    else:
        return {
            "path": path,
            "content": "# 파일 없음 또는 더미 내용"
        }
