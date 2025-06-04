"""Tests for edge cases in serialization and deserialization."""

import json
import uuid
from datetime import datetime, timezone

import pytest

from corelab_blockkit import BlockList, TextBlock, ImageBlock
from corelab_blockkit.blocks.base import BaseBlock
from corelab_blockkit.exceptions import SerializationError
from corelab_blockkit.meta import BlockMeta
from corelab_blockkit.ser.json_codec import (
    BlockJSONEncoder,
    serialize_to_json,
    deserialize_from_json,
)
from corelab_blockkit.ser.yaml_codec import (
    serialize_to_yaml,
    deserialize_from_yaml,
    _convert_uuids_to_strings,
)


class TestSerializationEdgeCases:
    """Tests for edge cases in serialization and deserialization."""

    def test_json_encoder_uuid(self):
        """Test JSON encoder with UUID."""
        test_uuid = uuid.uuid4()
        encoded = json.dumps(test_uuid, cls=BlockJSONEncoder)
        assert encoded == f'"{test_uuid}"'

    def test_json_encoder_datetime(self):
        """Test JSON encoder with datetime."""
        test_datetime = datetime(2023, 1, 1, tzinfo=timezone.utc)
        encoded = json.dumps(test_datetime, cls=BlockJSONEncoder)
        assert encoded == f'"{test_datetime.isoformat()}"'

    def test_json_encoder_basemodel(self):
        """Test JSON encoder with BaseModel."""
        meta = BlockMeta(is_favorite=True, tags=["test"])
        encoded = json.dumps(meta, cls=BlockJSONEncoder)
        assert '"is_favorite": true' in encoded
        assert '"tags": ["test"]' in encoded

    def test_json_serialization_error(self):
        """Test JSON serialization error."""

        class UnserializableObject:
            pass

        with pytest.raises(SerializationError):
            serialize_to_json(UnserializableObject())

    def test_json_deserialization_invalid_format(self):
        """Test JSON deserialization with invalid format."""
        with pytest.raises(SerializationError):
            deserialize_from_json("invalid json")

    def test_json_deserialization_invalid_block_list(self):
        """Test JSON deserialization with invalid block list format."""
        with pytest.raises(SerializationError):
            deserialize_from_json('{"not_blocks": []}')

    def test_json_deserialization_invalid_block(self):
        """Test JSON deserialization with invalid block format."""
        with pytest.raises(SerializationError):
            deserialize_from_json('{"blocks": [{"not_kind": "text"}]}')

    def test_json_deserialization_unknown_block_type(self):
        """Test JSON deserialization with unknown block type."""
        with pytest.raises(SerializationError):
            deserialize_from_json('{"blocks": [{"kind": "unknown_type"}]}')

    def test_json_deserialization_invalid_target_type(self):
        """Test JSON deserialization with invalid target type."""
        with pytest.raises(SerializationError):
            deserialize_from_json("{}", target_type=str)

    def test_yaml_serialization_error(self):
        """Test YAML serialization error."""

        class UnserializableObject:
            pass

        with pytest.raises(SerializationError):
            serialize_to_yaml(UnserializableObject())

    def test_yaml_serialization_unsupported_type(self):
        """Test YAML serialization with unsupported type."""
        with pytest.raises(SerializationError):
            serialize_to_yaml(123)  # Not a BaseBlock, BlockList, or list of BaseBlocks

    def test_yaml_deserialization_invalid_format(self):
        """Test YAML deserialization with invalid format."""
        with pytest.raises(SerializationError):
            deserialize_from_yaml("invalid: yaml: [")

    def test_yaml_deserialization_invalid_block_list(self):
        """Test YAML deserialization with invalid block list format."""
        with pytest.raises(SerializationError):
            deserialize_from_yaml("not_blocks: []")

    def test_yaml_deserialization_invalid_block(self):
        """Test YAML deserialization with invalid block format."""
        with pytest.raises(SerializationError):
            deserialize_from_yaml("blocks:\n- not_kind: text")

    def test_yaml_deserialization_unknown_block_type(self):
        """Test YAML deserialization with unknown block type."""
        with pytest.raises(SerializationError):
            deserialize_from_yaml("blocks:\n- kind: unknown_type")

    def test_yaml_deserialization_invalid_target_type(self):
        """Test YAML deserialization with invalid target type."""
        with pytest.raises(SerializationError):
            deserialize_from_yaml("{}", target_type=str)

    def test_convert_uuids_to_strings(self):
        """Test _convert_uuids_to_strings function."""
        test_uuid = uuid.uuid4()
        test_datetime = datetime.now()

        # Test with dict
        data_dict = {
            "id": test_uuid,
            "date": test_datetime,
            "nested": {
                "id": test_uuid,
                "date": test_datetime,
            },
            "list": [
                test_uuid,
                test_datetime,
                {"id": test_uuid},
            ],
        }
        _convert_uuids_to_strings(data_dict)
        assert data_dict["id"] == str(test_uuid)
        assert data_dict["date"] == test_datetime.isoformat()
        assert data_dict["nested"]["id"] == str(test_uuid)
        assert data_dict["nested"]["date"] == test_datetime.isoformat()
        assert data_dict["list"][0] == str(test_uuid)
        assert data_dict["list"][1] == test_datetime.isoformat()
        assert data_dict["list"][2]["id"] == str(test_uuid)

        # Test with list
        data_list = [
            test_uuid,
            test_datetime,
            {"id": test_uuid, "date": test_datetime},
            [test_uuid, test_datetime],
        ]
        _convert_uuids_to_strings(data_list)
        assert data_list[0] == str(test_uuid)
        assert data_list[1] == test_datetime.isoformat()
        assert data_list[2]["id"] == str(test_uuid)
        assert data_list[2]["date"] == test_datetime.isoformat()
        assert data_list[3][0] == str(test_uuid)
        assert data_list[3][1] == test_datetime.isoformat()
