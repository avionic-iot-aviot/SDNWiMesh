
const { Console } = require('console');
const dgram = require('dgram');
const server = dgram.createSocket('udp4');
const app = require('express')();
const http = require('http').Server(app);
const io = require('socket.io')(http);
var path = require('path');
var serveStatic = require('serve-static')
app.use(serveStatic('./'))


var IpSink= "10.11.0.190"
var PortSink=4100
var MyIp="10.11.0.4"
var LenNetId = 2
var LenLength = 4
var LenDestination = 15
var LenSource = 15
var LenType = 2
var LenTTL = 3
var LenNextHop = 15
const fs = require('fs');







var pktTool = require('./FixPacket.js');
var pkt = require( './packet.js');




app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

//-1--46----192.168.3.1----192.168.3.2-2100----192.168.3.1
io.on('connection', (socket) => {
    console.log('a user connected');
    nodes = []

    socket.on('MicOn', (data) => {
        console.log('Microphone activated on node: ' + data);
        socket.broadcast.emit('on', data);
        //     -1--45--192.168.1.131--192.168.1.189-3100--192.168.1.1892
       //    var packet = new pkt(NetId, Length, Destination, Source, Type, TTL, NextHop, Payload)
       var buffLen='1'+IpSink+ MyIp+"3"+"100"+IpSink+data
    
        //var AudioPacket = new pkt(pktTool.leftFillNum('1', LenNetId), pktTool.leftFillNum(buffLen.length,LenLength), pktTool.leftFillNum(data,LenDestination),pktTool.leftFillNum(MyIp,LenSource),pktTool.leftFillNum('3',LenType),pktTool.leftFillNum('100',LenTTL),pktTool.leftFillNum(IpSink,LenNextHop),"ON")
        var AudioPacket = Buffer.from(pktTool.leftFillNum('1', LenNetId) + pktTool.leftFillNum(buffLen.length,LenLength)+pktTool.leftFillNum(data,LenDestination)+pktTool.leftFillNum(MyIp,LenSource)+pktTool.leftFillNum('3',LenType)+pktTool.leftFillNum('100',LenTTL)+pktTool.leftFillNum(IpSink,LenNextHop)+"ON")
    
        console.log("Packet to send: ", AudioPacket.toString())

        server.send(AudioPacket.toString(),PortSink,IpSink,function(err, bytes) {
            if (err) throw err;
            console.log('UDP message sent to ' + IpSink +':'+ PortSink);
           // server.close();
          });

    });








    
    socket.on('MicOff', (data) => {
        socket.broadcast.emit('off', data);
        console.log('Microphone deactivated on node: ' + data);
        var buffLen='1'+IpSink+ MyIp+"3"+"100"+IpSink+data
    
        //var AudioPacket = new pkt(pktTool.leftFillNum('1', LenNetId), pktTool.leftFillNum(buffLen.length,LenLength), pktTool.leftFillNum(data,LenDestination),pktTool.leftFillNum(MyIp,LenSource),pktTool.leftFillNum('3',LenType),pktTool.leftFillNum('100',LenTTL),pktTool.leftFillNum(IpSink,LenNextHop),"ON")
        var AudioPacket = Buffer.from(pktTool.leftFillNum('1', LenNetId) + pktTool.leftFillNum(buffLen.length,LenLength)+pktTool.leftFillNum(data,LenDestination)+pktTool.leftFillNum(MyIp,LenSource)+pktTool.leftFillNum('3',LenType)+pktTool.leftFillNum('100',LenTTL)+pktTool.leftFillNum(IpSink,LenNextHop)+"OFF")
    
        console.log("Packet to send: ", AudioPacket.toString())

        server.send(AudioPacket.toString(),PortSink,IpSink,function(err, bytes) {
            if (err) throw err;
            console.log('UDP message sent to ' + IpSink +':'+ PortSink);
           // server.close();
          });

    });


});

http.listen(3000, () => {
    console.log('listening on *:3000');
});


server.on('error', (err) => {
    console.log(`server error:\n${err.stack}`);
    server.close();
});

server.on('message', (msg, rinfo) => {
    //console.log(`server got: ${msg} from ${rinfo.address}:${rinfo.port}`);
    PacketRcv = pktTool.ParsePacket(msg)

    switch (PacketRcv.Type) {
        case "0":
            console.log("Beacon");
            io.emit('Beacon', PacketRcv);
            break;
        case "1":
            console.log("Report");
            io.emit('Report', PacketRcv);
            break;
        case "2":
            console.log("Data");
            data=PacketRcv.Payload.replace("[","").replace("]","").split(",");
            console.log(data)
            for(i=0; i<= data.length-1; i++){
                //console.log(data[i])
                fs.appendFileSync('message.txt', "\n");
                fs.appendFileSync('message.txt', data[i])
                

            }
         
  
        
            

          




            break;
        default:
            console.log("Packet not recognized");
    }

    /* console.log(NetId.replace(/-/g, ""))
     console.log(Length.replace(/-/g, ""))
     console.log(Destination.replace(/-/g, ""))
     console.log(Source.replace(/-/g, ""))
     console.log(Type.replace(/-/g, ""))
     console.log(TTL.replace(/-/g, ""))
     console.log(NextHop.replace(/-/g, ""))
     console.log(Payload.replace(/-/g, ""))
 */



});








server.on('listening', () => {
    const address = server.address();
    console.log(`server listening ${address.address}:${address.port}`);

});


server.bind(5000);
