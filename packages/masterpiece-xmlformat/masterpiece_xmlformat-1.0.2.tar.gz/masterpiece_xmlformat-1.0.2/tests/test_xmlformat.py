import unittest
import io
from xml.etree.ElementTree import ElementTree
from unittest.mock import MagicMock
from masterpiece.masterpiece import MasterPiece
from masterpiece_xmlformat.xmlformat import XMLFormat


class TestXMLFormat(unittest.TestCase):

    def setUp(self):
        # Mock a MasterPiece instance for testing
        self.piece = MasterPiece()
        self.piece.to_dict = MagicMock(
            return_value={"attribute1": "value1", "attribute2": "value2"}
        )
        self.piece.from_dict = MagicMock()

        # Mock a class for configuration testing and set a class name
        self.MockClass = MagicMock(spec=MasterPiece)
        self.MockClass.__name__ = "MockClass"
        self.MockClass.classattrs_to_dict = MagicMock(
            return_value={"config1": "config_value1"}
        )
        self.MockClass.classattrs_from_dict = MagicMock()

        # Set up an in-memory stream for XMLFormat
        self.stream = io.StringIO()
        self.xml_format = XMLFormat(self.stream)

    def test_serialize(self):
        """Test serializing an object to XML."""
        self.xml_format.serialize(self.piece)

        # Retrieve XML content and parse to check structure
        self.stream.seek(0)
        root = ElementTree(file=self.stream).getroot()

        self.assertEqual(
            root.tag, "MasterPiece"
        )  # Root element should match class name
        self.assertEqual(root.find("attribute1").text, "value1")
        self.assertEqual(root.find("attribute2").text, "value2")
        self.piece.to_dict.assert_called_once()  # Ensure to_dict was called

    def test_deserialize(self):
        """Test deserializing XML into an object."""
        # Write mock XML content into the stream
        self.stream.write(
            """<?xml version="1.0"?>
        <MasterPiece>
            <attribute1>value1</attribute1>
            <attribute2>value2</attribute2>
        </MasterPiece>"""
        )
        self.stream.seek(0)

        self.xml_format.deserialize(self.piece)

        # Verify from_dict was called with correct data
        self.piece.from_dict.assert_called_once_with(
            {"attribute1": "value1", "attribute2": "value2"}
        )

    def test_save_configuration(self):
        """Test saving class configuration to XML."""
        self.xml_format.save_configuration(self.MockClass)

        # Check XML structure for saved configuration
        self.stream.seek(0)
        root = ElementTree(file=self.stream).getroot()

        self.assertEqual(root.tag, "MockClass")  # Root element should match class name
        self.assertEqual(root.find("config1").text, "config_value1")
        self.MockClass.classattrs_to_dict.assert_called_once()  # Ensure classattrs_to_dict was called

    def test_load_configuration(self):
        """Test loading class configuration from XML."""
        # Write mock XML configuration into the stream
        self.stream.write(
            """<?xml version="1.0"?>
        <MockClass>
            <config1>config_value1</config1>
        </MockClass>"""
        )
        self.stream.seek(0)

        self.xml_format.load_configuration(self.MockClass)

        # Verify classattrs_from_dict was called with correct data
        self.MockClass.classattrs_from_dict.assert_called_once_with(
            {"config1": "config_value1"}
        )

    def test_file_extension(self):
        """Test file_extension class property."""
        self.assertEqual(XMLFormat.file_extension, ".xml")


if __name__ == "__main__":
    unittest.main()
