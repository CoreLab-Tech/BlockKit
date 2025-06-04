# Blockkit Plugin Example

This is an example plugin for the `blockkit` library that adds a new block type: `CodeBlock`.

## Installation

```bash
pip install -e .
```

## Usage

Once installed, the `CodeBlock` type will be automatically registered with the `blockkit` library through the entry point mechanism.

```python
from corelab_blockkit import BlockList
from blockkit_plugin_example import CodeBlock

# Create a block list
blocks = BlockList()

# Add a code block
code_block = CodeBlock(
    code="def hello_world():\n    print('Hello, world!')",
    language="python",
    line_numbers=True,
)
blocks = blocks.add(code_block)

# Serialize to JSON
json_str = blocks.to_json(indent=2)
print(json_str)
```

## How It Works

The plugin is registered with `blockkit` through the entry point mechanism. In `pyproject.toml`, we define:

```toml
[project.entry-points."blockkit.blocks"]
code_block = "blockkit_plugin_example:CodeBlock"
```

This tells `blockkit` to look for a `CodeBlock` class in the `blockkit_plugin_example` module when it loads entry points from the `blockkit.blocks` group.

The `BlockTypeRegistry` in `blockkit` will automatically discover and register this block type when it's installed.