# Cooperage SDK

Lightweight helpers for building tools that run on [Cooperage](https://github.com/cooperage-io/cooperage).

## Install

```bash
pip install cooperage-sdk
```

## Two ways to build tools

### Option A: Write a full server (maximum control)

Use the SDK to build a Docker image with custom tools. You get full control over dependencies, runtime, and behavior.

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

register_docs(mcp)
serve(mcp)
```

Package in a Dockerfile, register with `cooperage register --name my-server --image my-server:latest`.

### Option B: Write a function, skip the Docker image

Write plain Python functions that use the SDK's workspace helpers, then register them with a YAML config. Cooperage wraps them automatically — no Dockerfile, no MCP boilerplate.

```python
# tools.py
from cooperage_sdk import workspace

def analyze_csv(input_path: str) -> str:
    """Analyze a CSV file from the workspace."""
    import pandas as pd
    df = pd.read_csv(workspace.path(input_path))
    summary = df.describe().to_json()
    workspace.path("summary.json").write_text(summary)
    return "Summary written to /workspace/summary.json"

def merge_files(file_a: str, file_b: str) -> str:
    """Merge two workspace files."""
    a = workspace.path(file_a).read_text()
    b = workspace.path(file_b).read_text()
    workspace.path("merged.txt").write_text(a + "\n" + b)
    return "Merged to /workspace/merged.txt"
```

```yaml
# tools.yaml
name: my-tools
type: python
source: /workspace/tools.py
python_tools:
  - name: analyze_csv
    function: analyze_csv
    description: Analyze a CSV file
    params:
      input_path: {type: string, description: "Path to CSV in workspace"}
  - name: merge_files
    function: merge_files
    description: Merge two text files
    params:
      file_a: {type: string}
      file_b: {type: string}
```

```bash
cooperage register --from tools.yaml
```

The SDK's `workspace` helper works in both modes — whether your code runs in a custom Docker image or inside the adapter container.

## API

### workspace

Safe interface to the shared `/workspace` volume. Handles path resolution, traversal protection, and the `COOPERAGE_WORKSPACE` env var.

```python
from cooperage_sdk import workspace

# Get safe paths
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

Start the MCP server. Reads `PORT` from the environment (default 8000).

```python
from cooperage_sdk import serve

serve(mcp)                              # start on port 8000
serve(mcp, port=9000)                   # custom port
```

### register_docs

Expose a `docs/` directory as MCP Resources so the LLM can discover and read server documentation on demand.

```python
from cooperage_sdk import register_docs

register_docs(mcp)              # scans docs/ directory (default)
register_docs(mcp, "manuals")   # custom directory
```

Each file becomes an MCP Resource with a `docs://` URI. The LLM reads descriptions first and only pulls what it needs — no wasted context.

## License

MIT
