import re
import xml.etree.ElementTree as ET


__all__ = [
    "DictWrapper",
    "simplify_object_dict",
    "xml_to_dict",
]


class ObjectDict(dict):
    """
    Extension of dict to allow accessing keys as attributes.
    """

    def __init__(self, initd=None):
        if initd is None:
            initd = {}
        dict.__init__(self, initd)

    def __getattr__(self, item):
        node = self.__getitem__(item)

        if isinstance(node, dict) and "value" in node and len(node) == 1:
            return node["value"]
        return node

    # if value is the only key in object, you can omit it
    def __setstate__(self, item):
        return False

    def __setattr__(self, item, value):
        self.__setitem__(item, value)

    def getvalue(self, item, value=None):
        """
        Old Python 2-compatible getter method for default value.
        """
        return self.get(item, {}).get("value", value)


class XML2Dict:
    def __init__(self):
        pass

    def _parse_node(self, node):
        node_tree = ObjectDict()
        # Save attrs and text, hope there will not be a child with same name
        if node.text:
            node_tree.value = node.text
        for key, val in node.attrib.items():
            key, val = self._namespace_split(key, ObjectDict({"value": val}))
            node_tree[key] = val
        # Save childrens
        for child in list(node):
            tag, tree = self._namespace_split(child.tag, self._parse_node(child))
            if tag not in node_tree:  # the first time, so store it in dict
                node_tree[tag] = tree
                continue
            old = node_tree[tag]
            if not isinstance(old, list):
                node_tree.pop(tag)
                node_tree[tag] = [old]  # multi times, so change old dict to a list
            node_tree[tag].append(tree)  # add the new one

        return node_tree

    def _namespace_split(self, tag, value):
        """
        Split the tag '{http://cs.sfsu.edu/csc867/myscheduler}patients'
        ns = http://cs.sfsu.edu/csc867/myscheduler
        name = patients
        """
        result = re.compile(r"\{(.*)\}(.*)").search(tag)
        if result:
            value.namespace, tag = result.groups()

        return (tag, value)

    def parse(self, filename):
        """
        Parse XML file to a dict.
        """
        file_ = open(filename, "r")
        return self.fromstring(file_.read())

    def fromstring(self, str_):
        """
        Parse a string
        """
        text = ET.fromstring(str_)
        root_tag, root_tree = self._namespace_split(text.tag, self._parse_node(text))
        return ObjectDict({root_tag: root_tree})


def remove_namespace(xml):
    """
    Strips the namespace from XML document contained in a string.
    Returns the stripped string.
    """
    regex = re.compile(' xmlns(:ns2)?="[^"]+"|(ns2:)|(xml:)')
    return regex.sub("", xml)


class DictWrapper:
    def __init__(self, xml, rootkey=None):
        self.original = xml
        self.response = None
        self._rootkey = rootkey
        self._mydict = XML2Dict().fromstring(remove_namespace(xml))
        self._response_dict = self._mydict.get(list(self._mydict.keys())[0], self._mydict)

    @property
    def parsed(self):
        if self._rootkey:
            return self._response_dict.get(self._rootkey)
        return self._response_dict


def simplify_object_dict(obj):
    """
    Упрощение структуры экземляра класса ObjectDict.
    """

    if isinstance(obj, list):
        return [simplify_object_dict(obj_child) for obj_child in obj]
    elif obj is None:
        return ""
    else:
        json_obj = {}
        if (len(obj) == 1) and ("value" in obj):
            return obj.value
        for key, val in obj.items():
            if isinstance(val, str):
                if (key == "value") and (not val.strip()):
                    continue
                json_obj[key] = val
            elif isinstance(val, dict) and (len(val) == 1) and ("value" in val):
                json_obj[key] = val["value"]
            else:
                json_obj[key] = simplify_object_dict(val)
    return json_obj


def xml_to_dict(xml: str, rootkey=None):
    return simplify_object_dict(DictWrapper(xml, rootkey=rootkey).parsed)
