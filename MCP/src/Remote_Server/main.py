from fastmcp import FastMCP

mcp = FastMCP(name="mcp-cal")

@mcp.tool
def add(a:int, b:int)->int:
    """Add two numbers together"""
    c = a + b
    return c


def main() -> None:
    mcp.run(transport="http", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()