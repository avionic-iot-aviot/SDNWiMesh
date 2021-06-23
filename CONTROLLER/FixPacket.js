var pkt = require('./packet.js');


exports.ParsePacket = function (msg) {
    var buff = Buffer.from(msg)
    var NetId = buff.toString('ascii', 0, 2).replace(/-/g, "")
    var Length = buff.toString('ascii', 2, 6).replace(/-/g, "")
    var Destination = buff.toString('ascii', 6, 22).replace(/-/g, "")
    var Source = buff.toString('ascii', 22, 37).replace(/-/g, "")
    var Type = buff.toString('ascii', 37, 38).replace(/-/g, "")
    var TTL = buff.toString('ascii', 38, 42).replace(/-/g, "")
    var NextHop = buff.toString('ascii', 42, 56).replace(/-/g, "")
	
    var Payload = buff.toString('ascii', 56)
	
	
    var packet = new pkt(NetId, Length, Destination, Source, Type, TTL, NextHop, Payload)

    return packet

}


exports.leftFillNum = function (num, targetLength) {
    return num.toString().padStart(targetLength, '-');
}

