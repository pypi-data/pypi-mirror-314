"""
Yaml serialization format

Author: Juha Meskanen
Date: 2024-10-26
"""

import yaml
from typing import Type
from typing_extensions import override  # for python 3.9 compatibility
from io import IOBase
from masterpiece import MasterPiece, classproperty, Format


class YamlFormat(Format):
    """
    The `YamlFormat` class provides methods for serializing and deserializing objects
    to and from YAML format.

    Features:
    ---------
    - Serializes object attributes to a YAML file or stream.
    - Deserializes object attributes from a YAML file or stream.

    Usage:
    ------
    To use the `YamlFormat`, create an instance by passing the target stream. Then,
    call the `serialize` or `deserialize` method with the appropriate object.

    Example:
    --------
    .. code-block:: python

        from masterpiece.core import YamlFormat, MasterPiece

        # create something to serialize
        piece = SomePiece()

        with open("output.yaml", "w") as f:
            yaml_format = YamlFormat(f)
            yaml_format.serialize(piece)

        with open("output.yaml", "r") as f:
            yaml_format = YamlFormat(f)
            yaml_format.deserialize(piece)
    """

    @override
    def __init__(self, stream: IOBase) -> None:
        """Initialize the YamlFormat with a stream (file object).

        Args:
            stream (Any): The stream to write/read YAML data.
        """
        super().__init__(stream)
        self.indent = 4
        self.default_flow_style = False

    @override
    def serialize(self, obj: MasterPiece) -> None:
        """Serialize the object to the given YAML stream.

        Args:
            obj (Any): The object to serialize.
        """
        yaml.dump(
            obj.to_dict(),
            self.stream,
            default_flow_style=self.default_flow_style,
            indent=self.indent,
        )

    @override
    def deserialize(self, obj: MasterPiece) -> None:
        """Load attributes from the given YAML stream into the object.

        Args:
            obj (Any): The object to deserialize into.
        """
        obj.from_dict(yaml.safe_load(self.stream))

    @override
    def save_configuration(self, clazz: Type[MasterPiece]) -> None:
        """Create class configuration file, if configuration is enabled and
        if the file does not exist yet. See --config startup argument.
        Args:
            clazz (Type[Piece]) class to be saved

        """
        yaml.dump(
            clazz.classattrs_to_dict(),
            self.stream,
            default_flow_style=self.default_flow_style,
            indent=self.indent,
        )

    @override
    def load_configuration(self, clazz: Type[MasterPiece]) -> None:
        """Load class attributes from a Yaml file.
        Args:
            clazz (Type[Piece]) class to be configured
        """
        clazz.classattrs_from_dict(yaml.safe_load(self.stream))

    @classproperty
    def file_extension(self) -> str:
        return ".yaml"
