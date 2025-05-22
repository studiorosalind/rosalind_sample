from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("docs")

USER_AGENT = "doce-app/1.0"
SERPER_URL = ""

docs_urls = {
    "langchain": "python.langchain.com/docs",
    "llama-index": "docs.llamaindex.ai/en/stable",
    "openai": "platform.openai.com/docs",
}

def main():
    print("Hello from mcp-documentation!")

def search_web():
    ...

def fetch_url():
    ...

@mcp.tool()
def get_docs():
    ...

if __name__ == "__main__":
    main()
