# Cooperage SDK

Lightweight helpers for writing [Cooperage](https://github.com/cooperage-io/cooperage)-compatible MCP servers.

## Install

```bash
pip install cooperage-sdk
```

## Usage

```python
from mcp.server.fastmcp import FastMCP
from cooperage_sdk import workspace, serve

mcp = FastMCP("my-server", json_response=True, stateless_http=True)

@mcp.tool()
def process_data(input_file: str, output_file: str) -> str:
    """Process a data file from the workspace and write results."""
    data = workspace.path(input_file).read_text()
    workspace.path(output_file).write_text(data.upper())
    return f"Processed {input_file} → {output_file}"

serve(mcp)
```

## API

### workspace

```python
from cooperage_sdk import workspace

# Get safe paths for any file operation
workspace.path("file.txt")             # returns Path, blocks traversal
workspace.path("file.txt").read_text() # read
workspace.path("out.txt").write_text() # write

# Works with any library that takes a path
Image.open(workspace.path("photo.png"))
pd.read_csv(workspace.path("data.csv"))
plt.savefig(workspace.path("chart.png"))

# Helpers
workspace.exists("file.txt")           # check existence
workspace.list()                        # list all files
workspace.list("subdir")               # list files in subdir
workspace.root                          # raw Path to /workspace
```

### serve

```python
from cooperage_sdk import serve

serve(mcp)                              # start on port 8000
serve(mcp, port=9000)                   # custom port
```

## License

MIT
