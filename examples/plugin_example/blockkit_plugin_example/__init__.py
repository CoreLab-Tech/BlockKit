"""Example plugin for blockkit that adds a CodeBlock type."""

from typing import Any, Dict, Optional

from corelab_blockkit.blocks.base import BaseBlock


class CodeBlock(BaseBlock):
    """A block containing code with syntax highlighting.

    Attributes:
        code: The code content
        language: The programming language for syntax highlighting
        line_numbers: Whether to display line numbers
    """

    KIND: str = "code"

    def __init__(
        self,
        *,
        code: str,
        language: str = "python",
        line_numbers: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a code block.

        Args:
            code: The code content
            language: The programming language for syntax highlighting
            line_numbers: Whether to display line numbers
            **kwargs: Additional arguments to pass to BaseBlock
        """
        payload = {
            "code": code,
            "language": language,
            "line_numbers": line_numbers,
        }
        super().__init__(kind=self.KIND, payload=payload, **kwargs)

    @property
    def code(self) -> str:
        """Get the code content.

        Returns:
            The code content
        """
        return self.payload.get("code", "")

    @property
    def language(self) -> str:
        """Get the programming language.

        Returns:
            The programming language
        """
        return self.payload.get("language", "python")

    @property
    def line_numbers(self) -> bool:
        """Get whether to display line numbers.

        Returns:
            Whether to display line numbers
        """
        return self.payload.get("line_numbers", True)
