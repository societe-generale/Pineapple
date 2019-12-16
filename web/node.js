var NODE_BASE_HEIGHT = 60;
var FLOW_SOCKET_SIZE = 10;

class Node {
    constructor(id, module, name, inputs, outputs, flows) {
        this.id = id;
        this.module = module;
        this.name = name;
        this.inputs = [];
        for (var input in inputs) {
            var input_details = inputs[input];
            this.inputs.push(new NodeInput(this, input_details["id"], input_details["name"]));
        }
        this.outputs = [];
        for (var output in outputs) {
            var output_details = outputs[output];
            this.outputs.push(new NodeOutput(this, output_details["id"], output_details["name"]));
        }
        this.flow_in = new FlowIn(this);
        this.flow_out = new FlowOut(this);
        this.height = this.getNodeHeight();
        this.width = this.getNodeWidth();
        this.elements = {};
        this.drawNode();
    }

    getInput(input_name) {
        for (var input in this.inputs) {
            if (this.inputs[input].name == input_name) {
                return this.inputs[input];
            }
        }
        return null;
    }

    getNodeHeight() {
        return Math.max(
            this.inputs.length * (CONNECTOR_RADIUS + CONNECTOR_SPACING) + NODE_BASE_HEIGHT,
            this.outputs.length * (CONNECTOR_RADIUS + CONNECTOR_SPACING) + NODE_BASE_HEIGHT
        );
    }

    getNodeWidth() {
        var maxInputSizeName = 0;
        for (var i in this.inputs) {
            var sizeName = this.inputs[i].name.length;
            if (sizeName > maxInputSizeName) {
                maxInputSizeName = sizeName;
            }
        }
        var maxOutputSizeName = 0;
        for (var i in this.outputs) {
            var sizeName = this.outputs[i].name.length;
            if (sizeName > maxOutputSizeName) {
                maxOutputSizeName = sizeName;
            }
        }

        return Math.max(
            NODE_SPACING + (maxInputSizeName + maxOutputSizeName) * 10,
            this.module.length * 10,
            this.name.length * 20
        );
    }

    move(position) {
        this.elements["group"].move(position);
    }

    setPosition(position) {
        this.elements["group"].setPosition(position);
    }

    getPosition(position) {
        return this.elements["group"].getPosition();
    }

    drawNode() {
        var node = new Konva.Group({
            x: 0,
            y: 0,
            draggable: true
        });
        this.elements["group"] = node;
        var self = this;
        node.on('dragmove', function () {
            self.update();
        });

        this.drawRect(node);
        this.drawTitle(node);
        for (var i in this.inputs) {
            var node_input_position = {
                "x": this.getPosition().x,
                "y": this.getPosition().y + NODE_BASE_HEIGHT
            }
            this.inputs[i].drawNodeInput(node, node_input_position, parseInt(i));
        }  
        for (var i in this.outputs) {
            var node_output_position = {
                "x": this.getPosition().x,
                "y": this.getPosition().y + NODE_BASE_HEIGHT
            }
            this.outputs[i].drawNodeOutput(node, node_output_position, parseInt(i));
        }

        nodeLayer.add(node);
        return node;
    }

    update() {
        self = this;
        for (var input of self.inputs) {
            input.updateCurve();
        }
        for (var output of self.outputs) {
            output.updateCurve();
        }
        self.flow_in.updateCurve();
        self.flow_out.updateCurve();
        nodeLayer.draw();
        linkLayer.draw();
    }

    drawTitle(node) {
        var scale = 1;
        var title_rect = new Konva.Rect({
            x: this.getPosition().x,
            y: this.getPosition().y,
            width: this.width / 2,
            height: 20,
            scale: {
                x: scale,
                y: scale
            },
            fill: 'grey',
            stroke: "black",
            strokeWidth: 2,
            startScale: scale
        });
        var module_text = new Konva.Text({
            x: this.getPosition().x + 4,
            y: this.getPosition().y + 4,
            text: this.module,
            fontSize: 12,
            fontFamily: 'Calibri',
            fill: 'white',
        });
        var node_name_text = new Konva.Text({
            x: this.getPosition().x + 4,
            y: this.getPosition().y + NODE_BASE_HEIGHT - 30,
            text: this.name,
            fontSize: 16,
            fontFamily: 'Calibri',
            fill: 'white',
        });
        node.add(title_rect);
        node.add(module_text);
        node.add(node_name_text);
    }

    drawRect(node) {
        var scale = 1;
        var rect = new Konva.Rect({
            x: this.getPosition().x,
            y: this.getPosition().y,
            width: this.width,
            height: this.height,
            scale: {
                x: scale,
                y: scale
            },
            fill: '#555',
            stroke: "black",
            strokeWidth: 2,
            shadowColor: 'black',
            shadowBlur: 10,
            shadowOffset: {
                x: 5,
                y: 5
            },
            shadowOpacity: 0.6,
            startScale: scale
        });

        // add hover styling
        rect.on('mouseover', () => function () {
            document.body.style.cursor = 'pointer';
            this.setStrokeWidth(4);
            nodeLayer.draw();
        });
        rect.on('mouseout', function () {
            document.body.style.cursor = 'default';
            this.setStrokeWidth(2);
            nodeLayer.draw();

        });
        node.add(rect);
        this.elements["rect"] = rect;

        this.flow_in.drawFlow(node);
        this.flow_out.drawFlow(node);
    }
}