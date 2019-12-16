class Flow {
    constructor(parent) {
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

    onClick() {
        linkManager.linkFlow(this);
    }

    updateCurve() {
        for (var i in this.links) {
            this.links[i].update();
        }
    }
}

class FlowIn extends Flow
{
    constructor(parent) {
        super(parent);
    }

    drawFlow(node) {
        var flow_socket = new Konva.Rect({
            x: this.parent.getPosition().x,
            y: this.parent.getPosition().y + NODE_BASE_HEIGHT - 10,
            width: FLOW_SOCKET_SIZE,
            height: FLOW_SOCKET_SIZE,
            fill: '#6c0277',
            stroke: "cyan",
            strokeWidth: 1,
            cornerRadius: 3
        });
        var self = this;
        flow_socket.addEventListener('click', () => self.onClick(), false);
        this.elements = {
            "socket": flow_socket,
        };
        node.add(flow_socket);
        flow_socket.moveToTop();
    }
}

class FlowOut extends Flow
{
    constructor(parent) {
        super(parent);
    }

    drawFlow(node) {
        var flow_socket = new Konva.Rect({
            x: this.parent.getPosition().x + this.parent.width - FLOW_SOCKET_SIZE,
            y: this.parent.getPosition().y + NODE_BASE_HEIGHT - 10,
            width: FLOW_SOCKET_SIZE,
            height: FLOW_SOCKET_SIZE,
            fill: '#6c0277',
            stroke: "cyan",
            strokeWidth: 1,
            cornerRadius: 3
        });
        var self = this;
        flow_socket.addEventListener('click', () => self.onClick(), false);
        this.elements = {
            "socket": flow_socket,
        };
        node.add(flow_socket);
        flow_socket.moveToTop();
    }
}