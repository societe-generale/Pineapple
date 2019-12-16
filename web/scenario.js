class Scenario {
    constructor () {
        this.nodes = [];
    }

    addNode(node) {
        this.nodes.push(node);
    }
    removeNode(node) {
        this.nodes.splice(this.nodes.indexOf(node), 1);
    }

    findNodeById(node_id) {
        for (var i = 0; i < this.nodes.length; i++) {
            if (this.nodes[i].id == node_id) {
                return this.nodes[i];
            }
        }
        return null;
    }

    findInputById(input_id) {
        for (var i = 0; i < this.nodes.length; i++) {
            for (var input in this.nodes[i].inputs) {
                if (this.nodes[i].inputs[input].id == input_id) {
                    return this.nodes[i].inputs[input];
                }
            }
        }
        return null;
    }

    findOutputById(output_id) {
        for (var i = 0; i < this.nodes.length; i++) {
            for (var output in this.nodes[i].outputs) {
                if (this.nodes[i].outputs[output].id == output_id) {
                    return this.nodes[i].outputs[output];
                }
            }
        }
        return null;
    }
}

scenario = new Scenario();