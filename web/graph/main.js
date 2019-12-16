const coords = [{ x: 100, y: 200, radius: 10 }, { x: 250, y: 230, radius: 50 }, { x: 350, y: 120, radius: 50 }, { x: 500, y: 200, radius: 50 }]
const rects = [
    new Konva.Rect({
        x: 100,
        y: 200,
        width: 100,
        height: 300,
        fill: '#555',
        stroke: "black",
        strokeWidth: 2,
        draggable: true
    }),
    new Konva.Rect({
        x: 200,
        y: 200,
        width: 100,
        height: 300,
        fill: '#555',
        stroke: "black",
        strokeWidth: 2,
        draggable: true
    }),
    new Konva.Rect({
        x: 500,
        y: 200,
        width: 100,
        height: 300,
        fill: '#555',
        stroke: "black",
        strokeWidth: 2,
        draggable: true
    }),
    new Konva.Rect({
        x: 700,
        y: 200,
        width: 100,
        height: 300,
        fill: '#555',
        stroke: "black",
        strokeWidth: 2,
        draggable: true
    })
]
const extraSpace = 18

var graph, path;

var width = window.innerWidth;
var height = window.innerHeight;

function main() {
    // Create app
    var stage = new Konva.Stage({
        container: 'container',
        width: width,
        height: height,
    });
    var layer = new Konva.Layer();
    var lineLayer = new Konva.Layer();
    for (var rect in rects) {
        layer.add(rects[rect]);
        rects[rect].on('dragmove', function () {
            lineLayer.removeChildren();
            lineLayer.clear();
            graph = buildGraph(rects)
            drawGraph(lineLayer, graph)
            var start = rectToPoints(rects[0]);
            var end = rectToPoints(rects[3]);
            path = shortestPath(rects, graph, {x:start[0].x, y: start[0].y}, {x: end[0].x, y: end[0].y})
            path = [{x: rects[0].x(), y: rects[0].y()}].concat(path.concat({x: rects[3].x(), y: rects[3].y()}));
            drawPath(lineLayer, path)
            layer.draw();
            lineLayer.draw();
        });
    }
    stage.add(layer);
    stage.add(lineLayer);
}

main()