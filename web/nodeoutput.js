class NodeOutput {
    constructor(parent, id, name) {
        this.id = id;
        this.name = name;
        this.parent = parent;
        this.links = [];
        this.elements = {};
    }

    addLink(link) {
        this.links.push(link);
    }

    removeLink(link) {
        this.links.splice(this.links.indexOf(link));
    }

    drawNodeOutput(node, position, nb) {
        var xPos = position.x + (this.parent.width - (CONNECTOR_SPACING / 2));
        var yPos = position.y + (CONNECTOR_SPACING * (nb + 1));
        var output_socket = new Konva.Circle({
            x: xPos,
            y: yPos,
            radius: CONNECTOR_RADIUS,
            stroke: '#666',
            fill: '#ddd',
            strokeWidth: 2,
        });
        var output_name = new Konva.Text({
            x: xPos - CONNECTOR_RADIUS - 5,
            y: yPos - CONNECTOR_RADIUS,
            text: this.name,
            fontSize: 12,
            fontFamily: 'Calibri',
            fill: 'cyan',
        });
        output_name.move({"x": -output_name.getTextWidth(), "y": 0});
        var self = this;
        output_socket.addEventListener('click', () => self.onClick(), false);
        this.elements = {
            "socket": output_socket,
            "name": output_name
        };
        node.add(output_socket);
        node.add(output_name);
    }

    onClick() {
        linkManager.linkData(this);
    }


    updateCurve() {
        for (var i in this.links) {
            this.links[i].update();
        }
    }
}