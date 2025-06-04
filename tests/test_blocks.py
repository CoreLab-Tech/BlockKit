"""Tests for block types."""

import uuid
from datetime import datetime, timezone

import pytest

from corelab_blockkit import (
    AudioBlock,
    BlockList,
    DownloadBlock,
    GlossaryBlock,
    ImageBlock,
    QuoteBlock,
    SupplementBlock,
    TextBlock,
    VideoBlock,
)
from corelab_blockkit.enums import AudioFormat, MimeType, TextFormat, VideoProvider
from corelab_blockkit.meta import BlockMeta
from corelab_blockkit.ser.json_codec import serialize_to_json, deserialize_from_json
from corelab_blockkit.ser.yaml_codec import serialize_to_yaml, deserialize_from_yaml


class TestBlockTypes:
    """Tests for block types."""

    def test_text_block(self):
        """Test TextBlock creation and properties."""
        block = TextBlock(text="Hello **world**!", format=TextFormat.MARKDOWN)
        assert block.text == "Hello **world**!"
        assert block.format == TextFormat.MARKDOWN
        assert block.kind == "text"

        # Test with string format
        block = TextBlock(text="Hello world!", format="plain")
        assert block.format == TextFormat.PLAIN

        # Test serialization/deserialization
        json_str = serialize_to_json(block)
        deserialized = deserialize_from_json(json_str, target_type=TextBlock)
        assert deserialized.text == block.text
        assert deserialized.format == block.format

    def test_image_block(self):
        """Test ImageBlock creation and properties."""
        block = ImageBlock(
            url="https://example.com/image.jpg",
            alt_text="Example image",
            caption="Figure 1",
            width=800,
            height=600,
        )
        assert block.url == "https://example.com/image.jpg"
        assert block.alt_text == "Example image"
        assert block.caption == "Figure 1"
        assert block.width == 800
        assert block.height == 600
        assert block.kind == "image"

        # Test serialization/deserialization
        json_str = serialize_to_json(block)
        deserialized = deserialize_from_json(json_str, target_type=ImageBlock)
        assert deserialized.url == block.url
        assert deserialized.alt_text == block.alt_text
        assert deserialized.caption == block.caption
        assert deserialized.width == block.width
        assert deserialized.height == block.height

    def test_video_block(self):
        """Test VideoBlock creation and properties."""
        block = VideoBlock(
            url="https://example.com/video.mp4",
            title="Example Video",
            description="A video example",
            thumbnail_url="https://example.com/thumbnail.jpg",
            duration=120,
            provider=VideoProvider.YOUTUBE,
        )
        assert block.url == "https://example.com/video.mp4"
        assert block.title == "Example Video"
        assert block.description == "A video example"
        assert block.thumbnail_url == "https://example.com/thumbnail.jpg"
        assert block.duration == 120
        assert block.provider == VideoProvider.YOUTUBE
        assert block.kind == "video"

        # Test with string provider
        block = VideoBlock(
            url="https://example.com/video.mp4",
            title="Example Video",
            provider="vimeo",
        )
        assert block.provider == VideoProvider.VIMEO

        # Test serialization/deserialization
        json_str = serialize_to_json(block)
        deserialized = deserialize_from_json(json_str, target_type=VideoBlock)
        assert deserialized.url == block.url
        assert deserialized.title == block.title
        assert deserialized.provider == block.provider

    def test_audio_block(self):
        """Test AudioBlock creation and properties."""
        block = AudioBlock(
            url="https://example.com/audio.mp3",
            title="Example Audio",
            artist="Example Artist",
            duration=180,
            format=AudioFormat.MP3,
        )
        assert block.url == "https://example.com/audio.mp3"
        assert block.title == "Example Audio"
        assert block.artist == "Example Artist"
        assert block.duration == 180
        assert block.format == AudioFormat.MP3
        assert block.kind == "audio"

        # Test with string format
        block = AudioBlock(
            url="https://example.com/audio.ogg",
            title="Example Audio",
            format="ogg",
        )
        assert block.format == AudioFormat.OGG

        # Test serialization/deserialization
        json_str = serialize_to_json(block)
        deserialized = deserialize_from_json(json_str, target_type=AudioBlock)
        assert deserialized.url == block.url
        assert deserialized.title == block.title
        assert deserialized.format == block.format

    def test_download_block(self):
        """Test DownloadBlock creation and properties."""
        block = DownloadBlock(
            url="https://example.com/file.pdf",
            filename="example.pdf",
            title="Example PDF",
            size=1024,
            mime_type=MimeType.APPLICATION_PDF,
        )
        assert block.url == "https://example.com/file.pdf"
        assert block.filename == "example.pdf"
        assert block.title == "Example PDF"
        assert block.size == 1024
        assert block.mime_type == MimeType.APPLICATION_PDF
        assert block.kind == "download"

        # Test with string mime_type
        block = DownloadBlock(
            url="https://example.com/file.zip",
            filename="example.zip",
            mime_type="application/zip",
        )
        assert block.mime_type == MimeType.APPLICATION_ZIP

        # Test serialization/deserialization
        json_str = serialize_to_json(block)
        deserialized = deserialize_from_json(json_str, target_type=DownloadBlock)
        assert deserialized.url == block.url
        assert deserialized.filename == block.filename
        assert deserialized.mime_type == block.mime_type

    def test_glossary_block(self):
        """Test GlossaryBlock creation and properties."""
        terms = [
            {"term": "Python", "definition": "A programming language"},
            {"term": "JSON", "definition": "JavaScript Object Notation"},
        ]
        block = GlossaryBlock(
            terms=terms,
            title="Programming Terms",
        )
        assert block.terms == terms
        assert block.title == "Programming Terms"
        assert block.kind == "glossary"
        assert block.get_term("Python") == "A programming language"
        assert block.get_term("JSON") == "JavaScript Object Notation"
        assert block.get_term("Not Found") is None
        assert set(block.get_terms()) == {"Python", "JSON"}

        # Test serialization/deserialization
        json_str = serialize_to_json(block)
        deserialized = deserialize_from_json(json_str, target_type=GlossaryBlock)
        assert deserialized.terms == block.terms
        assert deserialized.title == block.title

    def test_quote_block(self):
        """Test QuoteBlock creation and properties."""
        block = QuoteBlock(
            text="To be or not to be, that is the question.",
            source="William Shakespeare",
            citation="Hamlet, Act 3, Scene 1",
        )
        assert block.text == "To be or not to be, that is the question."
        assert block.source == "William Shakespeare"
        assert block.citation == "Hamlet, Act 3, Scene 1"
        assert block.kind == "quote"

        # Test serialization/deserialization
        json_str = serialize_to_json(block)
        deserialized = deserialize_from_json(json_str, target_type=QuoteBlock)
        assert deserialized.text == block.text
        assert deserialized.source == block.source
        assert deserialized.citation == block.citation

    def test_supplement_block(self):
        """Test SupplementBlock creation and properties."""
        links = [
            {"url": "https://example.com/1", "title": "Link 1"},
            {"url": "https://example.com/2", "title": "Link 2"},
        ]
        block = SupplementBlock(
            title="Additional Resources",
            content="Here are some additional resources.",
            links=links,
            tags=["resources", "links"],
        )
        assert block.title == "Additional Resources"
        assert block.content == "Here are some additional resources."
        assert block.links == links
        assert block.tags == ["resources", "links"]
        assert block.kind == "supplement"

        # Test serialization/deserialization
        json_str = serialize_to_json(block)
        deserialized = deserialize_from_json(json_str, target_type=SupplementBlock)
        assert deserialized.title == block.title
        assert deserialized.content == block.content
        assert deserialized.links == block.links
        assert deserialized.tags == block.tags

    def test_block_with_custom_id_and_meta(self):
        """Test creating a block with a custom ID and metadata."""
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

        assert block.id == block_id
        assert block.meta.created_at == created_at
        assert block.meta.updated_at == updated_at
        assert block.meta.is_favorite is True
        assert block.meta.tags == ["test", "example"]
        assert block.meta.extra == {"author": "Test Author"}

        # Test serialization/deserialization
        json_str = serialize_to_json(block)
        deserialized = deserialize_from_json(json_str, target_type=TextBlock)
        assert deserialized.id == block.id
        assert deserialized.meta.created_at == block.meta.created_at
        assert deserialized.meta.updated_at == block.meta.updated_at
        assert deserialized.meta.is_favorite == block.meta.is_favorite
        assert deserialized.meta.tags == block.meta.tags
        assert deserialized.meta.extra == block.meta.extra
