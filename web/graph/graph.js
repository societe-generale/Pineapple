function lineIntersects(p0, p1, p2, p3) {
    var s1x = p1.x - p0.x
    var s1y = p1.y - p0.y
    var s2x = p3.x - p2.x
    var s2y = p3.y - p2.y

    var s = (-s1y * (p0.x - p2.x) + s1x * (p0.y - p2.y)) / (-s2x * s1y + s1x * s2y)
    var t = (s2x * (p0.y - p2.y) - s2y * (p0.x - p2.x)) / (-s2x * s1y + s1x * s2y)

    return s > 0 && s < 1 && t > 0 && t < 1
}

function linePolygonIntersection(src, dst, o) {
    var c = rectToPoints(o);
    for (var k = 0; k < c.length; k++) {
        if (lineIntersects(c[k], c[(k + 1) % c.length], src, dst)) {
            return true
        }
    }
    return false
}

function directPath(rects, src, dst) {
    return rects
        .filter(o => src !== o)
        .every(o => !linePolygonIntersection(src, dst, o))
}

var avoid_offset = 20;

function rectToPoints(dst) {
    var position = dst.getAbsolutePosition();
    var points = [
        { x: position.x - avoid_offset, y: position.y - avoid_offset },
        { x: position.x + dst.width() + avoid_offset, y: position.y - avoid_offset },
        { x: position.x + dst.width() + avoid_offset, y: position.y + dst.height() + avoid_offset },
        { x: position.x - avoid_offset, y: position.y + dst.height() + avoid_offset }
    ];
    //console.log("Rect to points", dst, "=", points);
    return points;
}

function buildGraph(rects) {
    // Add edge from each vertex to all visible vertex
    const allVertices = rects
        .map(rectToPoints)
        .reduce((a, b) => [...a, ...b])

    const graph = {}
    rects.forEach(src => {
        const srcPoly = rectToPoints(src);
        srcPoly.forEach(srcP => {
            allVertices
                .filter(c => c.x !== srcP.x || c.y !== srcP.y)
                .forEach(c => {
                    if (directPath(rects, srcP, c)) {
                        const key = `${srcP.x} ${srcP.y}`
                        if (graph[key] == null) {
                            graph[key] = []
                        }
                        graph[key].push(c)
                    }
                })
        })
    })
    return graph
}