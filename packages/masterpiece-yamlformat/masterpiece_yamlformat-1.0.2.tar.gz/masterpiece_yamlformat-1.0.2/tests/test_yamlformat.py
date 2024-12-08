"""Author Juha Meskanen
Date: 2024-10-26
"""

import yaml
import unittest
from io import StringIO

from masterpiece import MasterPiece, Composite
from masterpiece_yamlformat import YamlFormat


class TestYamlFormat(unittest.TestCase):

    def setUp(self) -> None:
        """Set up a hierarchical structure for testing."""
        self.parent = Composite("parent")
        self.child = MasterPiece("child")
        self.parent.add(self.child)

    def test_serialize(self) -> None:
        """Test serialization of the hierarchical object to yaml."""
        # Create a StringIO object to simulate a file
        stream = StringIO()
        yaml_format = YamlFormat(stream)

        # Serialize the parent object
        yaml_format.serialize(self.parent)

        # Verify the yaml output
        expected_output = yaml.dump(
            self.parent.to_dict(), default_flow_style=False, indent=4
        )
        self.assertEqual(stream.getvalue(), expected_output)

    def test_deserialize(self) -> None:
        """Test deserialization of yaml back to the hierarchical object."""
        # Create a StringIO object to simulate a file
        stream = StringIO()

        # Serialize the parent object to yaml first
        yaml_format = YamlFormat(stream)
        yaml_format.serialize(self.parent)

        # Prepare a new Composite object for deserialization
        new_parent = Composite("")

        # Seek to the beginning of the stream for reading
        stream.seek(0)

        # Deserialize the yaml back to the new parent object
        yaml_format = YamlFormat(stream)
        yaml_format.deserialize(new_parent)

        # Verify that the new_parent object has the same attributes
        self.assertEqual(new_parent.name, self.parent.name)
        self.assertEqual(len(new_parent.children), len(self.parent.children))
        self.assertEqual(new_parent.children[0].name, self.child.name)


if __name__ == "__main__":
    unittest.main()
