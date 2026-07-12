# XmlDict-light - Lightweight XML Library

**Description:**
`XmlDict` is a lightweight Python library for working with XML data, designed to be dependency-free and utilizing only standard Python libraries (specifically `xml.sax.saxutils` and `xml.dom.minidom`). It provides basic XML node manipulation, attribute handling, and conversion between XML and dictionary representations. It's a simplified version of a full-fledged XML parser, focusing on core conversion tasks.

**Key Features:**

*   **Node-Based Structure:** Represents XML data as a tree of nodes.
*   **Attribute Handling:** Allows setting, getting, and deleting node attributes.
*   **Text Content:** Supports storing text content within nodes.
*   **Conversion to Dictionary:** Provides methods for converting XML data into a Python dictionary and vice versa.
*   **Dependency-Free:**  Does not require any external libraries beyond Python's standard library.

**Usage examples**
```
from xmldict_light import XmlDict

# create xml from dict
xml_dict = XmlDict.from_dict({"root": {"one": 1, "two": 2}})
xml_dict.three = 3
print(xml_dict.to_xml())

# create dict from xml
xml_dict = XmlDict.from_xml("<root><one>1</one><two>2</two></root>")
xml_dict.three = 3
print(xml_dict.to_dict())
```

**Classes and Methods:**
*   **`XmlDict`**:
    *   The main class for representing and manipulating XML data.
    *   `__init__(self, name: str)`: Initializes the root node of the XML document.
    *   `add_node(self, name: str) -> Node`: Adds a new node as a child of the root node.
    *   `to_dict(self) -> dict`: Converts the entire XML structure to a dictionary.
    *   `to_xml(self, xml_dec: bool = True) -> str`: Converts the entire XML structure to an XML string.
    *   `root_node(self) -> Node`: Returns the root node of the XML document.
    *   `from_dict(cls, dict_obj: dict) -> Self`: Creates an `XmlDict` object from a Python dictionary.
    *   `from_xml(cls, xml_str: str) -> Self`: Creates an `XmlDict` object from an XML string.
*   **`XmlDict.Node`**:
    *   Represents an individual XML node in the tree structure.
    *   `__init__(self, name: str)`: Initializes a new node with the given tag name.
    *   `add_node(self, name: str) -> Node`: Adds a child node to the current node.
    *   `attributes(self) -> list[str | int | None]`: Returns a list of attributes associated with the node.
    *   `get_attribute(self, name: str) -> str | int | None`: Retrieves a specific attribute value.
    *   `set_attribute(self, name: str, value: str | int | None)`: Sets the value of an attribute.
    *   `delete_attribute(self, name: str)`: Removes an attribute from the node.
    *   `name(self) -> str`: Returns the tag name of the node.
    *   `text(self) -> str`: Returns the text content of the node.
    *   `parent(self) -> Self | None`: Returns the parent node of the current node.
    *   `children(self) -> list[Self]`: Returns a list of child nodes.
    *   `to_dict(self) -> dict`: Converts the node and its children to a dictionary representation.
    *   `to_xml(self, xml_dec: bool = True) -> str`: Converts the node and its children to an XML string representation.
