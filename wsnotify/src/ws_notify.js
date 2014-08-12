#!/usr/bin/evn node
// config
var authpassword_receiver = "12345678";
var authpassword_sender = "abcdefgh";
var logfilepath = "/home/dictoss/log/wsnotice.log";
var output_console = 1;

var fs = require('fs');
var ws = require("websocket.io");
var listen_port = 8888;


var clientlist = new Array();

function write_log(s) {
    nowdt = new Date();
    fs.appendFile(logfilepath, nowdt + ": " + s);
    fs.appendFile(logfilepath, "\n");

    if(0 < output_console){
        console.log(nowdt + ": " + s);
    }
}

function WsClient(socket) {
    this.socket = socket;
    this.type = "";
    this.is_auth = 0;
    this.number = 0;
}


var server = ws.listen(listen_port, function () {
    write_log("ws start");
}
);


server.on("connection", function(socket) {
    write_log("socket connect :" + socket.socket._handle.fd);

    var c = new WsClient(socket);
    c.number = socket.socket._handle.fd

    clientlist[socket.socket._handle.fd] = c;

    socket.on("disconnect",  function(reason) {
        write_log("client connection disconnect(success: " + reason + ")");
	delete clientlist[c.number];
        socket.close();
    });

    socket.on("error",  function(reason) {
        write_log("client connection disconnect(error: " + reason + ")");
        delete clientlist[c.number];
        socket.close();
    });

    socket.on("message",  function(msg) {
        write_log("message " + msg);

        var convjson;

        try{
            convjson = JSON.parse(msg);

            clfunc = convjson.func;
            write_log("funcname :" + clfunc);
        }
        catch(e){
            write_log("not parse funcname. try disconnect.")
            delete clientlist[socket.socket._handle.fd];
            socket.close();
            return;
        }

        if("auth" === clfunc){
	    write_log("IN auth ()");

            try{
                token = convjson.param.token;

                if (authpassword_receiver === token){
                    c.is_auth = 1;
                    c.type = "receiver";
                    
                    write_log("receiver auth success.");
                    authresponse = {"func": "auth",
                                    "statuscode": "200",
                                    "message": "success",
                                    "result": {"type": "receiver"}};
                    authres_msg = JSON.stringify(authresponse);
                    socket.send(authres_msg);
		}
                else if(authpassword_sender === token){
                    c.is_auth = 1;
                    c.type = "sender";
                    
                    write_log("sender auth success.");			
                    authresponse = {"func": "auth",
                                    "statuscode": "200",
                                    "message": "success",
                                    "result": {"type": "sender"}};
                    authres_msg = JSON.stringify(authresponse);
                    socket.send(authres_msg);
                }
                else{
                    throw "client auth failed.";
                }
            }
            catch(e){
                write_log("EXCEPT: client auth failed. (" + e + ")");
                delete clientlist[socket.socket._handle.fd];
                socket.close();
            }
        }
        else if("broadcast_msg" === clfunc){
            write_log("IN broadcast_msg()");

            if("sender" === clientlist[socket.socket._handle.fd].type){
                write_log("sender is " + socket.socket._handle.fd + ".")

                tmpmsg = {"func": "broadcast_msg",
                          "statuscode": "200",
                          "message": "success",
                          "result": convjson.param};
                relaymsg = JSON.stringify(tmpmsg);

                if(0 < clientlist[socket.socket._handle.fd].is_auth){
                    for(var i in clientlist){
                        write_log("try relay : " + i);

                        try{
                            if(0 < clientlist[i].is_auth){
                                if(clientlist[i].type === "receiver"){
                                    clientlist[i].socket.send(relaymsg);
                                    write_log("send success.")
                                }
                                else{
                                    write_log("this sender. not send.");
                                }
                            }
                            else{
                                write_log("not auth client.");
                            }
                        }
                        catch(e){
                            write_log("fail send(). (" + e + ")");
                        }
                    }
                }
            }
            else{
                write_log("sender is not auth. not relay. try disconnect.")
                socket.close();
            }
        }
        else{
            write_log("unknown func. try disconnect.");
            socket.close();
        }
    });
});
