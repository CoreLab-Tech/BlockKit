"""Tests for the BaseBlock class."""

import re
import uuid
from typing import Any, ClassVar, Dict

import pytest

from corelab_blockkit.blocks.base import BaseBlock
from corelab_blockkit.exceptions import BlockValidationError
from corelab_blockkit.meta import BlockMeta


class TestBaseBlock:
    """Tests for the BaseBlock class."""

    def test_create_base_block(self):
        """Test creating a BaseBlock instance."""
        block = BaseBlock(kind="test")
        assert block.kind == "test"
        assert isinstance(block.id, uuid.UUID)
        assert isinstance(block.meta, BlockMeta)
        assert block.payload == {}

    def test_create_with_custom_id(self):
        """Test creating a BaseBlock with a custom ID."""
        block_id = uuid.uuid4()
        block = BaseBlock(id=block_id, kind="test")
        assert block.id == block_id

    def test_create_with_custom_meta(self):
        """Test creating a BaseBlock with custom metadata."""
        meta = BlockMeta(is_favorite=True, tags=["test"])
        block = BaseBlock(kind="test", meta=meta)
        assert block.meta == meta
        assert block.meta.is_favorite is True
        assert block.meta.tags == ["test"]

    def test_create_with_payload(self):
        """Test creating a BaseBlock with a payload."""
        payload = {"text": "Hello world", "format": "markdown"}
        block = BaseBlock(kind="test", payload=payload)
        assert block.payload == payload

    def test_validate_kind_valid(self):
        """Test validating a valid kind value."""
        valid_kinds = ["text", "image", "video", "test_block", "my_custom_block"]
        for kind in valid_kinds:
            block = BaseBlock(kind=kind)
            assert block.kind == kind

    def test_validate_kind_invalid(self):
        """Test validating an invalid kind value."""
        invalid_kinds = ["", "Text", "IMAGE", "1text", "test-block", "test block"]
        for kind in invalid_kinds:
            with pytest.raises(BlockValidationError):
                BaseBlock(kind=kind)

    def test_model_validate_dict(self):
        """Test model_validate with a dictionary."""
        block_id = uuid.uuid4()
        meta = BlockMeta(is_favorite=True, tags=["test"])
        payload = {"text": "Hello world", "format": "markdown"}

        data = {
            "id": str(block_id),
            "kind": "test",
            "meta": meta.model_dump(),
            "payload": payload,
        }

        block = BaseBlock.model_validate(data)
        assert block.id == block_id
        assert block.kind == "test"
        assert block.meta.is_favorite is True
        assert block.meta.tags == ["test"]
        assert block.payload == payload

    def test_model_validate_non_dict(self):
        """Test model_validate with a non-dictionary value."""
        with pytest.raises(ValueError):
            BaseBlock.model_validate("not a dict")

    def test_model_validate_invalid_uuid(self):
        """Test model_validate with an invalid UUID."""
        data = {
            "id": "not-a-uuid",
            "kind": "test",
        }

        with pytest.raises(ValueError):
            BaseBlock.model_validate(data)

    def test_subclass_kind_inheritance(self):
        """Test that subclasses inherit the KIND class variable."""

        # Define a subclass without specifying KIND
        class TestBlock(BaseBlock):
            pass

        # The KIND should be automatically set based on the class name
        assert TestBlock.KIND == "test"

        # Create an instance and check the kind field
        block = TestBlock(kind=TestBlock.KIND)
        assert block.kind == "test"

    def test_subclass_with_explicit_kind(self):
        """Test a subclass with an explicitly set KIND."""

        class CustomBlock(BaseBlock):
            KIND: ClassVar[str] = "custom_type"

        assert CustomBlock.KIND == "custom_type"

        block = CustomBlock(kind=CustomBlock.KIND)
        assert block.kind == "custom_type"

    def test_subclass_with_block_suffix(self):
        """Test that _block suffix is removed from the KIND."""

        class TestBlockBlock(BaseBlock):
            pass

        assert TestBlockBlock.KIND == "test_block"
