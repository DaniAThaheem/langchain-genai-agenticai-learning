from fastmcp import FastMCP

mcp = FastMCP(name="mcp-cal")

@mcp.tool
def add(a:int, b:int)->int:
    """Add two numbers together"""
    c = a + b
    return c

if __name__ == "__main__":
    mcp.run(transport="stdio")