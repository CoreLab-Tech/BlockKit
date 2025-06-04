"""Tests for the BlockTypeRegistry."""

import pytest

from corelab_blockkit.blocks.base import BaseBlock
from corelab_blockkit.exceptions import RegistryError
from corelab_blockkit.registry import BlockTypeRegistry


class TestBlockTypeRegistry:
    """Tests for the BlockTypeRegistry."""

    def test_register_and_get(self):
        """Test registering and getting a block type."""
        registry = BlockTypeRegistry()

        # Create a test block class
        class TestBlock(BaseBlock):
            KIND = "test_block"

        # Register the block class
        registry.register(TestBlock)

        # Get the block class
        retrieved_class = registry.get("test_block")
        assert retrieved_class == TestBlock

        # Check that it's in the list of types
        assert "test_block" in registry.list_types()

    def test_register_duplicate(self):
        """Test registering a duplicate block type."""
        registry = BlockTypeRegistry()

        # Create a test block class
        class TestBlock(BaseBlock):
            KIND = "test_block"

        # Register the block class
        registry.register(TestBlock)

        # Try to register another class with the same kind
        class AnotherTestBlock(BaseBlock):
            KIND = "test_block"

        with pytest.raises(RegistryError):
            registry.register(AnotherTestBlock)

    def test_register_no_kind(self):
        """Test registering a block class with no KIND defined."""
        registry = BlockTypeRegistry()

        # Create a mock block class with KIND set to None
        class MockBlock:
            KIND = None
            __name__ = "MockBlock"

        # Try to register the mock block class
        with pytest.raises(RegistryError):
            registry.register(MockBlock)

    def test_get_nonexistent(self):
        """Test getting a nonexistent block type."""
        registry = BlockTypeRegistry()

        with pytest.raises(RegistryError):
            registry.get("nonexistent")

    def test_list_types(self):
        """Test listing registered block types."""
        registry = BlockTypeRegistry()

        # Create and register some test block classes
        class TestBlock1(BaseBlock):
            KIND = "test_block1"

        class TestBlock2(BaseBlock):
            KIND = "test_block2"

        registry.register(TestBlock1)
        registry.register(TestBlock2)

        # List the types
        types = registry.list_types()
        assert "test_block1" in types
        assert "test_block2" in types
        assert len(types) == 2
