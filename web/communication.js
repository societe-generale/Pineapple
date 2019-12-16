function uuidv4() {
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
      (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    )
}

class ServerCommunication
{
    // WebSocket events
    ws_onclose() {}
    ws_onerror() {}
    ws_onmessage(event) { this.manageEvent(event); }
    ws_onopen() {}

    constructor(hostname, port) {
        this.hostname = hostname;
        this.port = port;
        this.buffer = {};
        this.ws = new WebSocket(`ws://${this.hostname}:${this.port}/`);
        this.ws.onclose = (...args) => this.ws_onclose(...args);
        this.ws.onerror = (...args) => this.ws_onerror(...args);
        this.ws.onmessage = (...args) => this.ws_onmessage(...args);
        this.ws.onopen = (...args) => this.ws_onopen(...args);
    }

    consume(id, timeout=-1) {
        return new Promise(
            resolve => this.buffer[id] = resolve,
            reject => { if (timeout > 0) { setTimeout(reject, timeout) } }
        );
    }

    send(data) {
        this.ws.send(JSON.stringify(data));
    }

    expect_response(dict, callback) {
        var rid = uuidv4()
        dict["rid"] = rid;
        this.send(dict);
        return this.consume(rid);
    }

    manageEvent(event) {
        var data = JSON.parse(event.data);
        if ("rid" in data && data["rid"] in this.buffer) {
            this.buffer[data.rid](data.data);
            delete this.buffer[data.rid];
        }
    }

    r_getAllNodes() {
        return this.expect_response({
            "type": "on_get_all_nodes"
        })
    }

    r_getAllModels() {
        return this.expect_response({
            "type": "on_get_all_models"
        })
    }

    r_getModel(node_name) {
        return this.expect_response({
            "type": "on_get_model",
            "node_name": node_name
        });
    }

    r_getNode(node_id) {
        return this.expect_response({
            "type": "on_get_node",
            "node_id": node_id
        })
    }

    r_exportScenario(gherkins = false) {
        return this.expect_response({
            "type": "on_export_scenario",
            "gherkins": gherkins
        })
    }

    s_createLink(fromId, toId) {
        this.send({
            "type": "on_link_connect",
            "input": fromId,
            "output": toId
        });
    }

    s_createNode(nodeType) {
        this.send({
            "type": "on_node_create",
            "nodetype": nodeType
        })
    }

    s_createFlow(fromId, toId) {
        this.send({
            "type": "on_flow_create",
            "node1": fromId,
            "node2": toid
        })
    }
}