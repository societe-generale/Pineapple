
var width = window.innerWidth;
var height = window.innerHeight;

var tween = null;

function addConnector(layer, stage, rec1, rec2) {
    x1 = rec1.attrs.x + rec1.attrs.width
    y1 = (rec1.attrs.y + rec1.attrs.height) / 2
    x2 = rec2.attrs.x
    y2 = (rec2.attrs.y + rec2.attrs.height) / 2
    connector = new Konva.Line({
        points: [x1, y1, x2, y2],
        stroke: 'black',
        strokeWidth: 10,
        lineCap: 'round',
        lineJoin: 'round'
    });
    layer.add(connector);
}

function addRect(layer, stage, xPos, yPos) {
    var scale = 1;
    var rectangle = new Konva.Rect({
        x: xPos,
        y: yPos,
        width: 100,
        height: 70,
        scale: {
            x : scale,
            y : scale
          },
        fill: 'grey',
        stroke: "black",
        strokeWidth: 2,
        draggable: true,
        shadowColor: 'black',
        shadowBlur: 10,
        shadowOffset: {
            x : 5,
            y : 5
        },
        shadowOpacity: 0.6,
        startScale: scale
        });
    layer.add(rectangle);
    return rectangle;
}


var stage = new Konva.Stage({
  container: 'container',
  width: width,
  height: height
});

var layer = new Konva.Layer();
var dragLayer = new Konva.Layer();

rec1 = addRect(layer, stage, 150, 150);
rec2 = addRect(layer, stage, 350, 150);
addConnector(layer, stage, rec1, rec2)

stage.add(layer, dragLayer);

stage.on('dragstart', function(evt) {
  var shape = evt.target;
  // moving to another layer will improve dragging performance
  shape.moveTo(dragLayer);
  stage.draw();
  
  if (tween) {
    tween.pause();
  }
  shape.setAttrs({
    shadowOffset: {
      x: 15,
      y: 15
    },
    scale: {
      x: shape.getAttr('startScale') * 1.2,
      y: shape.getAttr('startScale') * 1.2
    }
  });
});

stage.on('dragend', function(evt) {
  var shape = evt.target;
  shape.moveTo(layer);
  stage.draw();
  shape.to({
    duration: 0.5,
    easing: Konva.Easings.ElasticEaseOut,
    scaleX: shape.getAttr('startScale'),
    scaleY: shape.getAttr('startScale'),
    shadowOffsetX: 5,
    shadowOffsetY: 5
  });
});


