function drawGraph(stage, graph) {
    Object.entries(graph).forEach(([src, dst]) => {
        dst.forEach(d => {
            const x = parseInt(src.split(' ')[0])
            const y = parseInt(src.split(' ')[1])
            var line = new Konva.Line({
                x: 0,
                y: 0,
                points: [x, y, d.x, d.y],
                stroke: 'red',
                tension: 1
            });
            stage.add(line);
        })
    })
}

function drawPath(stage, path) {
    if (path) {
        var line = new Konva.Line({
            x: 0,
            y: 0,
            points: [path[0].x, path[0].y],
            stroke: 'cyan',
            tension: 0
        });
        for (let k = 1; k < path.length; k++) {
            line.points(line.points().concat([path[k].x, path[k].y]))
        }
        stage.add(line)
    }
}