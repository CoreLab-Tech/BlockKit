#!/usr/bin/env python3
"""Minimal example of using blockkit."""

import uuid
from datetime import datetime

from corelab_blockkit import BlockList, TextBlock, ImageBlock, toggle_favorite
from corelab_blockkit.meta import BlockMeta


def main():
    """Create and serialize a simple block list."""
    # Create a block list
    blocks = BlockList()

    # Add a text block
    text_block = TextBlock(
        text="Hello **world**! This is a *markdown* formatted text block.",
        format="markdown",
    )
    blocks = blocks.add(text_block)

    # Add an image block
    image_block = ImageBlock(
        url="https://example.com/image.jpg",
        alt_text="An example image",
        caption="Figure 1: Example image",
    )
    blocks = blocks.add(image_block)

    # Create a block with custom metadata
    custom_meta = BlockMeta(
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_favorite=True,
        tags=["example", "custom"],
        extra={"author": "John Doe"},
    )

    text_block_with_meta = TextBlock(
        text="This block has custom metadata.",
        meta=custom_meta,
    )
    blocks = blocks.add(text_block_with_meta)

    # Toggle favorite on a block
    block = blocks.find_by_id(text_block.id)
    new_meta = toggle_favorite(block.meta)

    # Create a new block with the updated metadata
    # (since blocks are immutable, we need to create a new one)
    updated_block = TextBlock(
        id=block.id,
        text=block.text,
        format=block.format,
        meta=new_meta,
    )

    # Replace the old block with the updated one
    blocks = blocks.remove(block.id).add(updated_block)

    # Serialize to JSON and print
    json_str = blocks.to_json(indent=2)
    print(json_str)

    # Serialize to YAML
    yaml_str = blocks.to_yaml()
    print("\nYAML representation:")
    print(yaml_str)

    # Demonstrate round-trip serialization
    deserialized = BlockList.from_json(json_str)
    print(f"\nDeserialized {len(deserialized)} blocks")

    # Access block properties
    for i, block in enumerate(deserialized):
        print(f"Block {i+1} kind: {block.kind}")
        if block.kind == "text":
            print(f"  Text: {block.text[:30]}...")
        elif block.kind == "image":
            print(f"  Image URL: {block.url}")
        print(f"  Is favorite: {block.meta.is_favorite}")


if __name__ == "__main__":
    main()
