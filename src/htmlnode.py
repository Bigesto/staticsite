

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def __eq__(self, value):
        if isinstance(value, HTMLNode):
            return (self.tag == value.tag and 
                    self.value == value.value and 
                    self.children == value.children and
                    self.props == value.props)
        return False

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        text = ""
        for key, value in self.props.items():
            text += " " + key + "=" + f'"{value}"'
        return text
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if not self.value:
            raise ValueError("Value is mandatory.")
        if not self.tag or len(self.tag) == 0:
            return f'{self.value}'
        if self.props:
            props_str = self.props_to_html()
            return f'<{self.tag}{props_str}>{self.value}</{self.tag}>'
        return f"<{self.tag}>{self.value}</{self.tag}>"
    
    def __eq__(self, value):
        if isinstance(value, LeafNode):
            return (self.tag == value.tag and 
                    self.value == value.value and
                    self.props == value.props)
        return False

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("Tag is mandatory.")
        if not self.children or len(self.children) == 0:
            raise ValueError("Kevin!")
        children = []
        for child in self.children:
            children.append(child.to_html())
        joined_children = "".join(children)
        
        if self.props:
            props_str = self.props_to_html()
            return f"<{self.tag}{props_str}>{joined_children}</{self.tag}>"

        return f"<{self.tag}>{joined_children}</{self.tag}>"