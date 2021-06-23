


sink = []
node = []
links = []
ttl = 10
ttlLink = 3
var KeepAliveNode = new Map();
var KeepAliveLink = new Map();



function reset() {
    sink = []
    node = []
    links = []
}
// client code here
var socket = io.connect(':3000');

socket.on('connect', function (message) {
    console.log("Connected")
    reset()

});

function removeA(arr) {
    var what, a = arguments, L = a.length, ax;
    while (L > 1 && arr.length) {
        what = a[--L];
        while ((ax = arr.indexOf(what)) !== -1) {
            arr.splice(ax, 1);
        }
    }
    return arr;
}

socket.on('on', function (data) {
    console.log("ACCESO!!!!")
    console.log("Emit on ricecuta per il node", data)
    NodeMicOn.push(data)
    newNode = network.nodesHandler.body.nodes[data].options
    newNode.color = {
        border: '#FF9900',
        background: 'green',
        shape: "dot",
        highlight: {
            border: '#FF9900',
            shape: "dot",
            background: 'green'
        }
    }


    nodes.update(newNode)

});

socket.on('off', function (data) {
console.log("Emit off ricecuta per il node", data)
    removeA(NodeMicOn, data)
    nodes.get(data);
    newNode = network.nodesHandler.body.nodes[data].options
     newNode.color = {
        border: '#FF9900',
        background: '#FF9900',
        shape: "dot",

        highlight: {
            border: '#FF9900',
            background: '#FF9900',
            shape: "dot",
        }
    }


    nodes.update(newNode);

});


socket.on('Beacon', function (message) {
    console.log("Beacon  from" + message.Source)

    if (!sink.includes(message.Destination)) {
        addNode(message.Destination, "sink")
        console.log("sono il sink:", message.Destination)
        sink.push(message.Destination)
    }
    if (!node.includes(message.Source) && (message.Source != message.Destination)) {
        console.log("sono il nodo:", message.Source)
        addNode(message.Source, "node");
        KeepAliveNode.set(message.Source, ttl)
        node.push(message.Source)
    } else {
        KeepAliveNode.set(message.Source, ttl)

    }

    for ([key, value] of KeepAliveNode) {
        if (KeepAliveNode.get(key) == 0) {
            removeNode(key)
            removeA(node, key)
        }
        KeepAliveNode.set(key, value - 1)
    }






});


socket.on('Report', function (message) {
    Source = message.Source
    Payload = message.Payload.replace(/\s/g, '').split(',')
    console.log("Report  from" + Source + "Payload: " + Payload)

    if (Payload.length > 0) {
        for (i in Payload) {
            console.log(Source + "-" + Payload[i])
            if (!links.includes(Source + "-" + Payload[i]) && !links.includes(Payload[i] + "-" + Source)) {
                addEdge(Source, Payload[i])
                links.push(Source + "-" + Payload[i])
                KeepAliveLink.set(Source + "-" + Payload[i], ttlLink)
                //addNode(message.Type);
                //node.push(message.Type)
            } else {
                KeepAliveLink.set(Source + "-" + Payload[i], ttlLink)
            }
        }
    }

    for ([key, value] of KeepAliveLink) {
        if (KeepAliveLink.get(key) == 0) {
            removeEdge(key)
            removeA(links, key)
        }
        KeepAliveLink.set(key, value - 1)
    }

});



