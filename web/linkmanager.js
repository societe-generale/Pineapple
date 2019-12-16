class LinkManager {
    constructor() {
        this.link = null;
    }

    linkData (connector) {
        if (connector == null) {
            this.link = null;
        }
        else if (this.link == null) {
            this.link = new Link(connector);
            connector.addLink(this.link);
        }
        else {
            if (this.link.connect(connector)) {
                connector.addLink(this.link);
            }
            else {
                this.link.trash();
            }
            this.link = null;
        }
    }

    linkFlow (connector) {
        if (connector == null) {
            this.link = null;
        }
        else if (this.link == null) {
            this.link = new Link(connector);
            connector.addLink(this.link);
        }
        else {
            if (this.link.connect(connector)) {
                connector.addLink(this.link);
                this.link.update();
            }
            else {
                this.link.trash();
            }
            this.link = null;
        }
    }
}

linkManager = new LinkManager();