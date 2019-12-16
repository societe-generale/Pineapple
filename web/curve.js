var canvas = document.getElementById("container");
var listAnchors = [];

var anchorSelected = false;

function drawDynamicCurve(event) {
    var xPos = event.clientX;
    var yPos = event.clientY;
    
    var startPos = event.target.startAnchorPos;
    var endPos = {x: xPos, y: yPos};
    drawCurves(startPos = startPos, endPos = endPos);
}

function createDynamicCurve() {
    console.log("createDynamicCurve function");
    if (anchorSelected == false) {
        anchorSelected = true;
        this.on('mouseout', function () {
            canvas.startAnchorPos = this.getAbsolutePosition();
            canvas.addEventListener('mousemove', drawDynamicCurve);
            canvas.addEventListener('click', event => {
                canvas.removeEventListener('mousemove', drawDynamicCurve);
                var posX = event.clientX;
                var posY = event.clientY;
                for (var i in listAnchors) {
                    var posAnchor = listAnchors[i].getAbsolutePosition();
                    var radius = listAnchors[i].attrs.radius
                    var isAnchor = false;
                    if ((posAnchor.x - radius <= posX) && (posX <= posAnchor.x + radius) && (posAnchor.y - radius <= posY) && (posY <= posAnchor.y + radius)) {
                        isAnchor = true; 
                    }
                }
                if (!isAnchor) {
                    var context = curveLayer.getContext();
                    context.clear();
                }
            });
        });
    }
    else {
        canvas.addEventListener('click', event => {
            canvas.removeEventListener('mousemove', drawDynamicCurve);
        });
    }
}

function drawCurves(startPos = null, endPos = null) {
    var context = curveLayer.getContext();

    context.clear();

    // draw quad
    context.beginPath();
    if (startPos == null) {
        startPos = quad.start.getAbsolutePosition();
    }
    if (endPos == null) {
        endPos = quad.end.getAbsolutePosition();
    }
    context.moveTo(startPos.x, startPos.y);
    context.quadraticCurveTo(quad.control.attrs.x, quad.control.attrs.y, endPos.x, endPos.y);
    context.setAttr('strokeStyle', 'red');
    context.setAttr('lineWidth', 4);
    context.stroke();
}

function updateDottedLines() {
    var q = quad;

    var quadLine = lineLayer.get('#quadLine')[0];
    var startPos = quad.start.getAbsolutePosition();
    var endPos = quad.end.getAbsolutePosition();

    quadLine.setPoints([startPos.x, startPos.y, q.control.attrs.x, q.control.attrs.y, endPos.x, endPos.y]);

    lineLayer.draw();
}