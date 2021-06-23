

function Packet (NetId, Length, Destination, Source, Type, TTL, NextHop, Payload) {
        this.NetId = NetId
        this.Length = Length
        this.Destination = Destination
        this.Source = Source
        this.Type = Type
        this.TTL = TTL
        this.NextHop = NextHop
        this.Payload = Payload
       
    }

    module.exports = Packet;

    /*this.PrintPacket = function PrintPacket() {
        return "NetId: " + this.NetId + " Length: " + this.Length + " Destination: " + this.Destination + " Source: " + this.Source + " Type: " + this.Type + " TTL: " + this.TTL + " NextHop: " + this.NextHop + " Payload: " + this.Payload;
    }*/

