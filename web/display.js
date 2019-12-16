var width = window.innerWidth;
var height = window.innerHeight;

// globals
var linkLayer, nodeLayer;


var stage = new Konva.Stage({
    container: 'container',
    width: width,
    height: height,
    draggable: true
});

var scaleBy = 1.1;
stage.on('wheel', e => {
    e.evt.preventDefault();
    var oldScale = stage.scaleX();

    var mousePointTo = {
        x: stage.getPointerPosition().x / oldScale - stage.x() / oldScale,
        y: stage.getPointerPosition().y / oldScale - stage.y() / oldScale
    };

    var newScale =
        e.evt.deltaY < 0 ? oldScale * scaleBy : oldScale / scaleBy;
    stage.scale({ x: newScale, y: newScale });

    var newPos = {
        x:
            -(mousePointTo.x - stage.getPointerPosition().x / newScale) *
            newScale,
        y:
            -(mousePointTo.y - stage.getPointerPosition().y / newScale) *
            newScale
    };
    stage.position(newPos);
    stage.batchDraw();
});

nodeLayer = new Konva.Layer();
linkLayer = new Konva.Layer();
linkLayer.off("click");
linkLayer.off("wheel");

var sc = new ServerCommunication("localhost", 5678);

var linex = 0;
var liney = 0;
var keepheight = 0;
var connecting_actions = [];

sc.ws_onopen = function () {
    sc.r_getAllNodes().then(function (data) {
        data.forEach(function (node) {
            console.log("Getting informations on Node", node)
            sc.r_getNode(node).then(function (node_details) {
                console.log("  Informations about Node", node, "=>", node_details);
                var new_node = new Node(
                    node_details["id"],
                    node_details["module"],
                    node_details["name"],
                    node_details["inputs"],
                    node_details["outputs"],
                    node_details["flows"]
                )
                connecting_actions.push(function () {
                    for (var input in node_details["inputs"]) {
                        var connect_output = scenario.findOutputById(node_details["inputs"][input].connected_output);
                        if (connect_output) {
                            linkManager.linkData(connect_output);
                            linkManager.linkData(new_node.getInput(input));
                        }
                    }
                    for (var flow in node_details["flows"]) {
                        var other_node = scenario.findNodeById(node_details["flows"][flow].node);
                        if (other_node) {
                            linkManager.linkFlow(new_node.flow_out);
                            linkManager.linkFlow(other_node.flow_in);
                        }
                    }
                })
                new_node.setPosition({ x: linex, y: liney });
                linex += new_node.getNodeWidth();
                if (new_node.getNodeHeight() > keepheight) {
                    keepheight = new_node.getNodeHeight();
                }
                if (linex > width) {
                    linex = 0;
                    liney += keepheight;
                }

                scenario.addNode(new_node);
                stage.add(nodeLayer);
                stage.add(linkLayer);
            })
        });
    });
}

function initialize_everything() {
    for (var i in connecting_actions) {
        connecting_actions[i]();
    }
    for (var node in scenario.nodes) {
        scenario.nodes[node].update();
    }
}