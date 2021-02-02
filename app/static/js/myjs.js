function getDateTime() {
  var today = new Date();
    // var date = today.getDate()+'/'+(today.getMonth()+1)+'/'+today.getFullYear();
    var h = today.getHours()
    var m = today.getMinutes()
    var s = today.getSeconds()
    if (h < 10) h = '0' + h
    if (m < 10) m = '0' + m
    if (s < 10) s = '0' + s
    var time = h + ":" + m + ":" + s;
    var dt = time;
  return dt;
}

$(document).ready(function(){
    var socket = io();
    // jquery 
    $('#multiBox').hide()
    $('#logoutBtn').hide()
    $('#sayhi').hide()
    $('#registerBtn').on('click', () => {
      $('#username').show(1000)
      $('#username').val($('textBtn').val())
      socket.emit('client-send-username-register', $('#textBtn').val());
    });

    socket.on('server-send-failed-register', (msg) => {
      alert("Tên không được là khoảng trắng hoặc đã có người sử dụng tên này.")   
    });

    $('#logoutBtn').on('click', ()=>{
      $('#loginForm').show(1000)    
      $('#logoutBtn').hide(1000) 
      $('#multiBox').hide(1000)
      $('#sayhi').hide(1000)     
      $('#username').hide()
      $('#username').val('')
       
      socket.emit('client-logout', $('#textBtn').val())
    });

    $('#my-message-1').keypress(function(e){
      if(e.keyCode==13)
      $('#send-btn-1').click();
    });
    
    $('#my-message-2').keypress(function(e){
      if(e.keyCode==13)
      $('#send-btn-2').click();
    });

    $('#textBtn').keypress(function(e){
      if(e.keyCode==13)
      $('#registerBtn').click();
    });

    // socketio
    
    socket.on('disconnect', function() {
      socket.emit('client-send-disconnect', $('#textBtn').val());
    });
    socket.on('connect', function() {
      socket.emit('connected', socket.id);
    });
    
    socket.on('server-send-successful-register', (msg) =>{
      $("#multi-messages").scrollTop($("#multi-messages").height());
      $('#multiBox').show(1000)    
      $('#loginForm').hide(1000)
      $('#logoutBtn').show(1000)    
      $('#sayhi').show(1000) 
      $('#username').append($('#textBtn').val())   
      $("#multi-messages").html("")
      socket.emit('client-send-message-successful-register', $('#textBtn').val())
    });

    socket.on('server-send-message-successfull-register', (username) => {
      console.log("server-send-message-successfull-register " + username)
      $("#multi-messages").append('<div class="row"><p class="box3">' + '<span id="username">' + username + '</span>' + '<span id="joinRoom">' + " vừa tham gia phòng." + '</span>' + '<div class="dateTime">' + getDateTime() + '</div>' + '</p>' +'</div>')
    });

    $('#send-btn-2').on('click', ()=>{
      var data = {};
      data['username'] = $('#textBtn').val()
      data['msg'] = $('#my-message-2').val() 
      socket.emit('client-send-multiple-messages', data)
      $('#my-message-2').val('')
    });

    socket.on('server-send-multiple-messages', (data) => {
      $('#multi-messages').append('<div class="row"><p class="box3">' + '<span id="username">' + data['username'] + '</span>'  + ': ' + data['msg'] + '<div class="dateTime">' + getDateTime() + '</div>' + '</p>' +'</div>')
      $("#multi-messages").scrollTop($("#multi-messages").height());
      console.log(data)
    }); 
    
    $('#send-btn-1').on('click', ()=>{
      socket.emit('client-send-single-messages', $('#my-message-1').val())
      var msg = $('#my-message-1').val()
      $('#single-messages').append('<div class="row"><div class="col-sm-6"><p class="float-start box1"></p></div><div class="col-sm-6"><p class="float-end box2">' + msg + '</p></div></div>')
      $('#single-messages').append('<div class="row"><div class="col-sm-6"><p class="float-start box1"></p></div><div class="col-sm-6"><p class="float-end dateTime">' + getDateTime() + '</p></div></div>')
      $('#my-message-1').val('')
    });
    
    socket.on('server-send-single-messages', (msg) => {
      if (msg['flag_image'] === "false"){
        $('#single-messages').append('<div class="row"><div class="col-sm-6"><p class="float-start box1">' + msg['server_msg'] + '</p></div><div class="col-sm-6"><p class="float-end box2"></div></div>')
      }
      else{
        var tmp = '<a target="_blank" href="' + msg['server_msg'] + '"><img alt="lol" src="' + msg['server_msg'] + '"width=350"></a>'
        $('#single-messages').append('<div class="row"><div class="col-sm-6"><p class="float-start box1">' + tmp + '</p></div><div class="col-sm-6"><p class="float-end box2"></div></div>')
        console.log(msg['flag_image'])
      }
      $('#single-messages').append('<div class="row"><div class="col-sm-6"><p class="float-start box1 dateTime">' + getDateTime() + '</p></div><div class="col-sm-6"><p class="float-end box2"></div></div>')
      $("#single-messages").scrollTop($("#single-messages").height());
      console.log(msg['client_msg'] + " " + msg['server_msg'])
    });

    socket.on('server-send-logout', (username) => {
      $("#multi-messages").append('<div class="row"><p class="box3">' + '<span id="username">' + username + '</span>' + '<span id="leftRoom">' + " vừa rời phòng." + '</span>' + '<div class="dateTime">' + getDateTime() + '</div>' + '</p>' +'</div>')  
      $('#username').html('')
    });

    socket.on('server-send-disconnect', (data) => {
      $("#multi-messages").append('<div class="row"><p class="box3">' + '<span id="username">' + data['username'] + '</span>' + '<span id="leftRoom">' + data['msg'] + '</span>' + '<div class="dateTime">' + getDateTime() + '</div>' + '</p>' +'</div>')
    });

  });