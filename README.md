# Cooperage SDK

Lightweight helpers for writing [Cooperage](https://github.com/cooperage-io/cooperage)-compatible MCP servers.

## Install

```bash
pip install cooperage-sdk
```

## Usage

```python
from mcp.server.fastmcp import FastMCP
from cooperage_sdk import workspace, serve, register_docs

mcp = FastMCP("my-server", json_response=True, stateless_http=True)

@mcp.tool()
def process_data(input_file: str, output_file: str) -> str:
    """Process a data file from the workspace and write results."""
    data = workspace.path(input_file).read_text()
    workspace.path(output_file).write_text(data.upper())
    return f"Processed {input_file} → {output_file}"

register_docs(mcp)  # expose docs/ directory as MCP Resources
serve(mcp)
```

## API

### workspace

```python
from cooperage_sdk import workspace

# Get safe paths — blocks traversal, hides the env var
workspace.path("file.txt")              # returns a Path
workspace.path("file.txt").read_text()  # read
workspace.path("out.txt").write_text()  # write

# Works with any library
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

### register_docs

Expose a `docs/` directory as MCP Resources so the LLM can discover and read
server documentation on demand.

```python
from cooperage_sdk import register_docs

register_docs(mcp)              # scans docs/ directory (default)
register_docs(mcp, "manuals")   # custom directory
```

Each file in the directory becomes an MCP Resource:
- **URI**: `docs://<filename>` (e.g. `docs://quickstart.md`)
- **Name**: derived from filename (e.g. "Quickstart")
- **Description**: first line of the file — lets the LLM preview contents
  before reading

#### Example

```
my-server/
  server.py
  Dockerfile
  docs/
    quickstart.md          "Getting started with the image analyzer"
    scene-types.md         "Supported scene types: terrain, urban, coastal"
    api-reference.md       "Full API reference for all tools"
```

The LLM sees:
```
cooperage_list_server_resources("session-1", "my-server")
→ [
    {"uri": "docs://quickstart.md",     "name": "Quickstart",     "description": "Getting started with the image analyzer"},
    {"uri": "docs://scene-types.md",    "name": "Scene Types",    "description": "Supported scene types: terrain, urban, coastal"},
    {"uri": "docs://api-reference.md",  "name": "Api Reference",  "description": "Full API reference for all tools"},
  ]

cooperage_read_server_resource("session-1", "my-server", "docs://scene-types.md")
→ (full markdown content)
```

The LLM reads the descriptions, decides which docs are relevant, and only
pulls what it needs — no wasted context tokens.

## License

MIT
