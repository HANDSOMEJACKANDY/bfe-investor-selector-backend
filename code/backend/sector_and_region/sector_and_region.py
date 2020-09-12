from anytree import Node, RenderTree

class TreeNavigator:
    def __init__(self, file_name):
        with open(file_name) as f:
            # create tree
            self.name2node = {}
            root = Node("root")
            self.name2node["root"] = root
            with open(file_name, "r") as f:
                lines = f.readlines()
                for line in lines:
                    if line[0] not in ("\t", "\n"):
                        line = line.replace("\t", "")
                        key = line.replace("\n", "")
                        parent_node = Node(key.strip().lower(), parent=root)
                        self.name2node[key.strip().lower()] = parent_node
                    elif line[0] == "\t":
                        line = line.replace("\t", "")
                        line = line.replace("\n", "")
                        items = line.split(", ")
                        for i in items:
                            child_node = Node(i.strip().lower(), parent=parent_node)
                            self.name2node[i.strip().lower()] = child_node
                    else:
                        pass

    def find_node(self, node_name):
        try:
            return [node.name for node in self.name2node[node_name.lower()].iter_path_reverse() if node.name != "root"]
        except:
            raise ValueError("Unknown node name!")

    def has_node(self, node_name):
        return node_name.lower() in self.name2node

    def __str__(self):
        return "\n".join(list(self.name2node.keys())[1:])