from fastmcp import FastMCP
from db_helper.sqlitestorage import storage

mcp = FastMCP('mcp_service')

@mcp.tool('add', description="Add two numbers and return the result")
def add(a, b):
    """Add two numbers and return the result"""
    return a + b
# The FastMCP ``resource`` decorator requires the URI template to contain at least
# one parameter. Need to add a dummy ``{unused}`` placeholder and accept it in the
# function signature (it is not used by the implementation).
@mcp.resource('sqlite://resources/list')
def get_recruitments():
    """Return the list of recruitment entries.

    The ``unused`` argument satisfies FastMCP's requirement for a URI
    parameter but is otherwise ignored.
    """
    try:
        result = storage.get_recruitment_list()
    except Exception as e:
        print(e)
    return result

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000, path="/mcp")