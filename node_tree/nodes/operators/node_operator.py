
class NodeOperator:
    @property
    def node(self):    
        if self.tree:
            return self.tree.nodes.get(self.node_name)

    @property
    def labels(self):
        idx = self.node.labels_idx
        labels = self.node.labels

        active = labels[idx] if len(labels) else None

        return idx, labels, active
    
    @property
    def props(self):
        idx = self.node.properties_idx
        properties = self.node.properties

        active = properties[idx] if len(properties) else None

        return idx, properties, active