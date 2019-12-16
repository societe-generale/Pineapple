class NodeInput {
    constructor(parent, id, name) {
        this.id = id;
        this.name = name;
        this.parent = parent;
        this.link = null;
        this.elements = {};
    }

    addLink(link) {
        this.link = link;
    }

    removeLink() {
        this.link = null;
    }

    drawNodeInput(node, position, nb) {
        var xPos = position.x + CONNECTOR_SPACING / 2;
        var yPos = position.y + (CONNECTOR_SPACING * (nb + 1));
        var input_socket = new Konva.Circle({
            x: xPos,
            y: yPos,
            radius: CONNECTOR_RADIUS,
            stroke: '#666',
            fill: '#ddd',
            strokeWidth: 2,
        });
        var input_name = new Konva.Text({
            x: xPos + CONNECTOR_RADIUS + 5,
            y: yPos - CONNECTOR_RADIUS,
            text: this.name,
            fontSize: 12,
            fontFamily: 'Calibri',
            fill: 'cyan',
        });
        var self = this;
        input_socket.addEventListener('click', () => self.onClick(), false);
        this.elements = {
            "socket": input_socket,
            "name": input_name
        };
        node.add(input_socket);
        node.add(input_name);
    }

    onClick() {
        linkManager.linkData(this);
    }

    updateCurve() {
        if (this.link != null) {
            this.link.update();
        }
    }
}