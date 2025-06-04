"""Tests for the BlockList class."""

import uuid
from typing import List

import pytest
from hypothesis import given, strategies as st

from corelab_blockkit import BlockList, TextBlock
from corelab_blockkit.exceptions import BlockDuplicateError, BlockNotFoundError


class TestBlockList:
    """Tests for the BlockList class."""

    def test_create_empty(self):
        """Test creating an empty block list."""
        blocks = BlockList()
        assert len(blocks) == 0
        assert list(blocks) == []

    def test_create_with_blocks(self):
        """Test creating a block list with blocks."""
        block1 = TextBlock(text="Block 1")
        block2 = TextBlock(text="Block 2")
        blocks = BlockList(blocks=[block1, block2])
        assert len(blocks) == 2
        assert blocks[0] == block1
        assert blocks[1] == block2

    def test_create_with_duplicate_ids(self):
        """Test creating a block list with duplicate IDs."""
        block_id = uuid.uuid4()
        block1 = TextBlock(id=block_id, text="Block 1")
        block2 = TextBlock(id=block_id, text="Block 2")
        with pytest.raises(BlockDuplicateError):
            BlockList(blocks=[block1, block2])

    def test_add(self):
        """Test adding a block."""
        blocks = BlockList()
        block = TextBlock(text="Test")
        new_blocks = blocks.add(block)
        assert len(new_blocks) == 1
        assert new_blocks[0] == block
        # Original list should be unchanged (immutability)
        assert len(blocks) == 0

    def test_add_with_index(self):
        """Test adding a block at a specific index."""
        block1 = TextBlock(text="Block 1")
        block2 = TextBlock(text="Block 2")
        blocks = BlockList(blocks=[block1, block2])
        block3 = TextBlock(text="Block 3")
        new_blocks = blocks.add(block3, index=1)
        assert len(new_blocks) == 3
        assert new_blocks[0] == block1
        assert new_blocks[1] == block3
        assert new_blocks[2] == block2

    def test_add_duplicate_id(self):
        """Test adding a block with a duplicate ID."""
        block1 = TextBlock(text="Block 1")
        blocks = BlockList(blocks=[block1])
        block2 = TextBlock(id=block1.id, text="Block 2")
        with pytest.raises(BlockDuplicateError):
            blocks.add(block2)

    def test_remove(self):
        """Test removing a block."""
        block1 = TextBlock(text="Block 1")
        block2 = TextBlock(text="Block 2")
        blocks = BlockList(blocks=[block1, block2])
        new_blocks = blocks.remove(block1.id)
        assert len(new_blocks) == 1
        assert new_blocks[0] == block2
        # Original list should be unchanged (immutability)
        assert len(blocks) == 2

    def test_remove_nonexistent(self):
        """Test removing a nonexistent block."""
        blocks = BlockList()
        with pytest.raises(BlockNotFoundError):
            blocks.remove(uuid.uuid4())

    def test_move(self):
        """Test moving a block."""
        block1 = TextBlock(text="Block 1")
        block2 = TextBlock(text="Block 2")
        block3 = TextBlock(text="Block 3")
        blocks = BlockList(blocks=[block1, block2, block3])
        new_blocks = blocks.move(block1.id, 2)
        assert len(new_blocks) == 3
        assert new_blocks[0] == block2
        assert new_blocks[1] == block3
        assert new_blocks[2] == block1

    def test_move_nonexistent(self):
        """Test moving a nonexistent block."""
        blocks = BlockList()
        with pytest.raises(BlockNotFoundError):
            blocks.move(uuid.uuid4(), 0)

    def test_move_invalid_index(self):
        """Test moving a block to an invalid index."""
        block = TextBlock(text="Test")
        blocks = BlockList(blocks=[block])
        with pytest.raises(ValueError):
            blocks.move(block.id, 1)

    def test_move_same_index(self):
        """Test moving a block to the same position returns the same list."""
        block1 = TextBlock(text="Block 1")
        block2 = TextBlock(text="Block 2")
        blocks = BlockList(blocks=[block1, block2])
        new_blocks = blocks.move(block1.id, 0)
        assert new_blocks is blocks
        assert list(new_blocks) == [block1, block2]

    def test_find_by_id(self):
        """Test finding a block by ID."""
        block1 = TextBlock(text="Block 1")
        block2 = TextBlock(text="Block 2")
        blocks = BlockList(blocks=[block1, block2])
        found = blocks.find_by_id(block1.id)
        assert found == block1

    def test_find_by_id_nonexistent(self):
        """Test finding a nonexistent block by ID."""
        blocks = BlockList()
        with pytest.raises(BlockNotFoundError):
            blocks.find_by_id(uuid.uuid4())

    @given(st.lists(st.integers()))
    def test_property_add_remove_inverse(self, items: List[int]):
        """Property test: adding and then removing a block is an identity operation."""
        blocks = BlockList()

        # Add all blocks first
        added_blocks = []
        for i, _ in enumerate(items):
            block = TextBlock(text=f"Block {i}")
            added_blocks.append(block)
            blocks = blocks.add(block)
            assert len(blocks) == i + 1

        # Then remove them one by one
        for i, block in enumerate(added_blocks):
            blocks = blocks.remove(block.id)
            assert len(blocks) == len(added_blocks) - i - 1
