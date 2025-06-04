"""Tests for serialization and deserialization."""

import json
import uuid
from datetime import datetime, timezone

import pytest

from corelab_blockkit import BlockList, TextBlock, ImageBlock
from corelab_blockkit.meta import BlockMeta
from corelab_blockkit.ser.json_codec import serialize_to_json, deserialize_from_json
from corelab_blockkit.ser.yaml_codec import serialize_to_yaml, deserialize_from_yaml


class TestSerialization:
    """Tests for serialization and deserialization."""

    def test_json_round_trip_single_block(self):
        """Test JSON round-trip serialization of a single block."""
        # Create a block with a fixed ID for deterministic testing
        block_id = uuid.UUID("12345678-1234-5678-1234-567812345678")
        created_at = datetime(2023, 1, 1, tzinfo=timezone.utc)
        updated_at = datetime(2023, 1, 2, tzinfo=timezone.utc)

        meta = BlockMeta(
            created_at=created_at,
            updated_at=updated_at,
            is_favorite=True,
            tags=["test", "example"],
            extra={"author": "Test Author"},
        )

        block = TextBlock(
            id=block_id,
            text="Hello **world**!",
            format="markdown",
            meta=meta,
        )

        # Serialize to JSON
        json_str = serialize_to_json(block)

        # Deserialize from JSON
        deserialized = deserialize_from_json(json_str, target_type=TextBlock)

        # Check that the deserialized block matches the original
        assert deserialized.id == block.id
        assert deserialized.kind == block.kind
        assert deserialized.text == block.text
        assert deserialized.format == block.format
        assert deserialized.meta.is_favorite == block.meta.is_favorite
        assert deserialized.meta.tags == block.meta.tags
        assert deserialized.meta.extra == block.meta.extra

    def test_json_round_trip_block_list(self):
        """Test JSON round-trip serialization of a block list."""
        # Create a block list with multiple blocks
        text_block = TextBlock(text="Hello **world**!")
        image_block = ImageBlock(
            url="https://example.com/image.jpg",
            alt_text="Example image",
        )

        blocks = BlockList(blocks=[text_block, image_block])

        # Serialize to JSON
        json_str = blocks.to_json()

        # Deserialize from JSON
        deserialized = BlockList.from_json(json_str)

        # Check that the deserialized block list matches the original
        assert len(deserialized) == len(blocks)
        assert deserialized[0].id == blocks[0].id
        assert deserialized[0].kind == blocks[0].kind
        assert deserialized[0].text == blocks[0].text
        assert deserialized[1].id == blocks[1].id
        assert deserialized[1].kind == blocks[1].kind
        assert deserialized[1].url == blocks[1].url

    def test_yaml_round_trip_single_block(self):
        """Test YAML round-trip serialization of a single block."""
        block = TextBlock(text="Hello **world**!")

        # Serialize to YAML
        yaml_str = serialize_to_yaml(block)

        # Deserialize from YAML
        deserialized = deserialize_from_yaml(yaml_str, target_type=TextBlock)

        # Check that the deserialized block matches the original
        assert deserialized.id == block.id
        assert deserialized.kind == block.kind
        assert deserialized.text == block.text

    def test_yaml_round_trip_block_list(self):
        """Test YAML round-trip serialization of a block list."""
        # Create a block list with multiple blocks
        text_block = TextBlock(text="Hello **world**!")
        image_block = ImageBlock(
            url="https://example.com/image.jpg",
            alt_text="Example image",
        )

        blocks = BlockList(blocks=[text_block, image_block])

        # Serialize to YAML
        yaml_str = blocks.to_yaml()

        # Deserialize from YAML
        deserialized = BlockList.from_yaml(yaml_str)

        # Check that the deserialized block list matches the original
        assert len(deserialized) == len(blocks)
        assert deserialized[0].id == blocks[0].id
        assert deserialized[0].kind == blocks[0].kind
        assert deserialized[0].text == blocks[0].text
        assert deserialized[1].id == blocks[1].id
        assert deserialized[1].kind == blocks[1].kind
        assert deserialized[1].url == blocks[1].url

    def test_json_invalid_format(self):
        """Test deserializing invalid JSON."""
        with pytest.raises(Exception):
            deserialize_from_json("invalid json")

    def test_yaml_invalid_format(self):
        """Test deserializing invalid YAML."""
        with pytest.raises(Exception):
            deserialize_from_yaml("invalid: yaml: [")
