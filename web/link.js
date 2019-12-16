var canvas = document.getElementById("container");

class Link {
    constructor(connector) {
        this.from = null;
        this.to = null;
        this.start = null;
        this.end = null;
        this.connect(connector);
        this.mousemovelistener = (event) => this.mouseMoveHandler(event);
        canvas.addEventListener('mousemove', this.mousemovelistener);
        this.line = new Konva.Line({
            x: 0,
            y: 0,
            points: [0, 0],
            stroke: 'red',
            tension: 10
        });
        this.line.off("click");
        linkLayer.add(this.line);
        if (connector instanceof FlowIn || connector instanceof FlowOut) {
            this.line.stroke("cyan");
        }
    }

    connect(connector) {
        if (this.start == null) {
            this.start = connector;
        }
        else {
            this.end = connector;
            canvas.removeEventListener("mousemove", this.mousemovelistener);
        }
        if (connector instanceof NodeInput || connector instanceof FlowIn) {
            if (this.from == null) {
                this.from = connector;
                return true;
            }
            else {
                console.error(`Link ${this} already has an Input`);
            }
        }
        else if (connector instanceof NodeOutput || connector instanceof FlowOut) {
            if (this.to == null) {
                this.to = connector;
                return true;
            }
            else {
                console.error(`Link ${this} already has an Output`);
            }
        }
        else {
            console.error("Wrong connector type", connector);
        }
        return false;
    }

    getStartConnector() {
        if (this.from != null) {
            return this.from;
        }
        else {
            return this.to;
        }
    }

    trash() {
        if (this.start) {
            this.start.removeLink(this);
        }
        if (this.end) {
            this.end.removeLink(this);
        }
        var context = linkLayer.getContext();
        //context.clear();
    }

    mouseMoveHandler(event) {
        if (this.from || this.to) {
            var xPos = event.clientX;
            var yPos = event.clientY;
            var startPos = this.start.elements["socket"].getAbsolutePosition();
            var endPos = {x: xPos, y: yPos};
            var self = this;
            //canvas.addEventListener('click', (event) => self.checkTarget(event, endPos));
            this.update(startPos=startPos, endPos=endPos);
        }
    }

    checkTarget(event, startPos) {
        var posX = event.clientX;
        var posY = event.clientY;
        this.update(startPos=startPos, {x:posX, y:posY});
    }

    // update link when a node is moved or being created
    update(startPos=null, endPos=null) {
        var refreshLayer = false;
        if (startPos || endPos) {
            refreshLayer = true;
        }
        if (startPos == null) {
            startPos = this.start.elements["socket"].getAbsolutePosition();
            if (this.start.elements["socket"] instanceof Konva.Rect) {
                startPos.x += this.start.elements["socket"].width() / 2;
                startPos.y += this.start.elements["socket"].height() / 2;
            }
        }
        if (endPos == null) {
            endPos = this.end.elements["socket"].getAbsolutePosition();
            if (this.end.elements["socket"] instanceof Konva.Rect) {
                endPos.x += this.end.elements["socket"].width() / 2;
                endPos.y += this.end.elements["socket"].height() / 2;
            }
        }

        //endPos.x -= 10; // Click event fix
        /*var rects = [];
        for (var node in scenario.nodes) {
            rects.push(scenario.nodes[node].elements["rect"]);
        }
        var graph = buildGraph(rects)
        var start = rectToPoints(this.start.parent.elements["rect"]);
        var end = rectToPoints(this.end.parent.elements["rect"]);
        var path = shortestPath(rects, graph, {x:start[0].x, y: start[0].y}, {x: end[0].x, y: end[0].y})
        path = [{x: rects[0].x(), y: rects[0].y()}].concat(path.concat({x: rects[3].x(), y: rects[3].y()}));
        console.log("==============> Path from", start, "to", end, "=", path);
        path = path.reduce(
            function(r, e) {
                r.push(e.x, e.y);
                return r;
            }, 
        []);
        console.log(path);
        this.line.points(path);*/
        this.line.points([
            (startPos.x - stage.x()) / stage.scaleX(),
            (startPos.y - stage.y()) / stage.scaleY(),
            (endPos.x - stage.x()) / stage.scaleX(),
            (endPos.y - stage.y()) / stage.scaleY()
        ]);
        if (refreshLayer) {
            linkLayer.draw();
        }
    }
}