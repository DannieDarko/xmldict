from typing import Self
from xml.sax.saxutils import escape
from xml.dom.minidom import parseString as parseXml

class XmlDict:
  class Node:
    def __init__(self, name: str):
      self._name=name
      self._attributes={}
      self._nodes={}
      self._text=''
      self._parent = None
      
    def add_node(self, name: str):
      node = XmlDict.Node(name)
      node.parent = self
      if name in self._nodes:
        if isinstance(self._nodes[name], XmlDict.Node):
          self._nodes[name]=[self._nodes[name]]
        self._nodes[name].append(node)
      else:
        self._nodes[name]=node
      return node
    
    @property
    def attributes(self):
      return self._attributes
    
    def get_attribute(self, name: str):
      return self._attributes.get(name, None)
    
    def set_attribute(self, name: str, value: str | int | None):
      self._attributes[name] = str(value) if value is not None else None
    
    def delete_attribute(self, name: str):
      if name in self._attributes:
        del self._attributes[name]

    @property
    def name(self):
      return self._name
    
    @property
    def text(self):
      return self._text
    
    @property
    def parent(self) -> Self | None:
      return self._parent
    
    @parent.setter
    def parent(self, parent: Self):
      self._parent = parent
    
    @property
    def children(self):
      return self._nodes
    
    @text.setter
    def text(self, text: str):
      if text is not None:
        self._text = str(text)
    
    def __str__(self):
      return self._text
    
    def __getattr__(self, name):
      return getattr(super(), name, self._nodes.get(name, None))
    
    def __len__(self):
      return len(self._nodes)
    
    def __getitem__(self, name: str):
      if not name:
        return None
      if name[0] == '@':
        return self._attributes.get(name[1:], None)
      return self._nodes.get(name, None)
    
    def to_dict(self):
      return {k: [nn.to_dict() for nn in n] if isinstance(n, list) else n.to_dict() for k, n in self._nodes.items()} if len(self._nodes)>0 else self._text
    
    def to_xml(self):
      return ''.join([f'<{k}{''.join([f' {k}="{escape(a).replace('"', '&quot;')}"' for k, a in nn.attributes.items() if a is not None])}>{nn.to_xml()}</{k}>' for k, n in self._nodes.items() for nn in (n if isinstance(n, list) else [n])]) if len(self._nodes)>0 else escape(self._text)
    
  def __init__(self, name: str):
    self._root_node = XmlDict.Node(name)
    
  def __getattr__(self, name: str):
    if name == self._root_node.name:
      return self._root_node
    return None
  
  def add_node(self, name: str):
    return self._root_node.add_node(name)
  
  def to_dict(self):
    return {self._root_node.name: self._root_node.to_dict()}
  
  def to_xml(self, xml_dec: bool = True):
    declaration='<?xml version="1.0" encoding="UTF-8"?>'
    return f'{declaration if xml_dec else ''}<{self._root_node.name}>{self._root_node.to_xml()}</{self._root_node.name}>'
  
  @property
  def root_node(self):
    return self._root_node
  
  @classmethod
  def from_dict(cls, dict_obj: dict) -> Self:
    xml_dict=None
    dict_stack=[]
    if len(dict_obj)>1:
      xml_dict=cls('root')
      dict_stack=[(key, 0, dict_obj[key]) for key in dict_obj]
    else:
      root_key=next(iter(dict_obj.keys()))
      xml_dict=cls(root_key)
      if type(dict_obj[root_key]) is dict:
        dict_stack=[(key, 0, dict_obj[root_key][key]) for key in dict_obj[root_key]]
      elif type(dict_obj[root_key]) is list:
        dict_stack=[(root_key, 0, o) for o in dict_obj[root_key]]
    cur_node=xml_dict.root_node
    cur_depth=0
    while len(dict_stack)>0:
      name, depth, cur_dict=dict_stack.pop(0)
      while depth<cur_depth:
        if cur_node.parent:
          cur_node=cur_node.parent
        cur_depth-=1
      cur_depth=depth
      if isinstance(cur_dict, dict):
        if not len(cur_dict):
          cur_node.add_node(name).text=None
        else:
          cur_node=cur_node.add_node(name)
          dict_stack=[(key, depth+1, cur_dict[key]) for key in cur_dict]+dict_stack
      elif isinstance(cur_dict, list):
        if not len(cur_dict):
          cur_node.add_node(name).text=None
        else:
          dict_stack=[(name, depth, o) for o in cur_dict]+dict_stack
      else:
        if cur_node is None:
          print('error', depth, name)
        else:
          cur_node.add_node(name).text=cur_dict
    return xml_dict
      
  @classmethod
  def from_xml(cls, xml_str: str) -> Self:
    xml_obj=parseXml(xml_str).documentElement
    xml_dict=cls(xml_obj.tagName)
    nodeStack=[(xml_dict.root_node, c) for c in xml_obj.childNodes]
    while len(nodeStack)>0:
      parent, node=nodeStack.pop(0)
      if node.nodeType == node.TEXT_NODE:
        if len(node.data.strip())>0:
          parent.text=node.data
      elif node.nodeType == node.ELEMENT_NODE:
        newParent=parent.add_node(node.tagName)
        if node.hasAttributes():
          for k, a in node.attributes.items():
            newParent.set_attribute(k, str(a))
        for childNode in node.childNodes:
          nodeStack.append((newParent, childNode))
    return xml_dict
  