from io import IOBase
import xml.etree.ElementTree as ET
from typing import Any, Type

from masterpiece.masterpiece import MasterPiece, classproperty
from masterpiece.format import Format


class XMLFormat(Format):
    """
    The `XMLFormat` class provides methods for serializing and deserializing classes
    and objects to and from XML format.

    Features:
    ---------
    - Serializes object attributes to an XML file or stream.
    - Deserializes object attributes from an XML file or stream.
    - Serializes public class attributes to an XML file or stream
    - Deserializes public class attributes from an XML file or stream

    Usage:
    ------
    To use the `XMLFormat`, create an instance by passing the target stream. Then,
    call the `serialize` or `deserialize` method with the appropriate object.

    Example:
    --------
    .. code-block:: python

        from masterpiece.core import XMLFormat, MasterPiece

        # Create an XMLFormat instance with a file stream
        with open("output.xml", "w") as f:
            xml_format = XMLFormat(f)
            xml_format.serialize(piece)  # piece is the object to serialize

        with open("output.xml", "r") as f:
            xml_format = XMLFormat(f)
            xml_format.deserialize(piece)  # piece is the object to deserialize
    """

    # @override
    def __init__(self, stream: IOBase) -> None:
        """Initialize the XMLFormat with a stream (file object).

        Args:
            stream (Any): The stream to write/read XML data.
        """
        super().__init__(stream)

    # @override
    def serialize(self, obj: MasterPiece) -> None:
        """Serialize the object to the given XML stream.

        Args:
            obj (Any): The object to serialize.
        """
        root = ET.Element(obj.__class__.__name__)
        for key, value in obj.to_dict().items():
            child = ET.SubElement(root, key)
            child.text = str(value)
        tree = ET.ElementTree(root)
        tree.write(self.stream, encoding="unicode", xml_declaration=True)

    # @override
    def deserialize(self, obj: MasterPiece) -> None:
        """Load attributes from the given XML stream into the object.

        Args:
            obj (Any): The object to deserialize into.
        """
        tree = ET.parse(self.stream)
        root = tree.getroot()
        attributes = {child.tag: child.text for child in root}
        obj.from_dict(attributes)

    # @override
    def save_configuration(self, clazz: Type[MasterPiece]) -> None:
        """Create class configuration file, if configuration is enabled and
        if the file does not exist yet. See --config startup argument.

        Args:
            clazz (Type[Piece]) class to be saved
        """
        root = ET.Element(clazz.__name__)
        for key, value in clazz.classattrs_to_dict().items():
            child = ET.SubElement(root, key)
            child.text = str(value)
        tree = ET.ElementTree(root)
        tree.write(self.stream, encoding="unicode", xml_declaration=True)

    # @override
    def load_configuration(self, clazz: Type[MasterPiece]) -> None:
        """Load class attributes from an XML file.

        Args:
            clazz (Type[Piece]) class to be configured
        """
        tree = ET.parse(self.stream)
        root = tree.getroot()
        attributes = {child.tag: child.text for child in root}
        clazz.classattrs_from_dict(attributes)

    @classproperty
    def file_extension(cls) -> str:
        return ".xml"
