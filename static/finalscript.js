function loadDoc(url,func){
    let xhttp=new XMLHttpRequest();
    xhttp.onload=function(){
        if (xhttp.status !=200){
            console.log("error")
        }else{
            func(xhttp.response);
        }
    }
    xhttp.open("GET", url);
    xhttp.send();
}
function login(){
    let email=document.getElementById("email");
    let password=document.getElementById("password");
    if (email.value ==""|| password.value==""){
        alert("Email and Password are both required");
        return;
    }
    let url="/twitterLogin?email="+email.value+"&password="+password.value;
    loadDoc(url, twitterLogin_response);
}
function twitterLogin_response(response){
    let data=JSON.parse(response);
    let results=data["result"];
    if (results!="OK"){
        alert(results);
    }else{
        window.location.replace("editprofile.html")
    }
}
function signup(){
    let username=document.getElementById("username");
    let email=document.getElementById("email");
    let password=document.getElementById("password");
    if (username.value==""||email.value==""||password.value==""){
        alert("Username, Email, and Password are required");
        return;
    }
    let url="/twitterSignup?username="+username.value+"&email="+email.value+"&password="+password.value;
    loadDoc(url,twitterSignup_response);
}
function twitterSignup_response(response){
    let data=JSON.parse(response);
    let results=data["result"];
    if(results!="OK"){
        alert(results);
    }else{
        window.location.replace("editprofile.html")
    }
}
function upload_post(){
    let xhttp=new XMLHttpRequest();
    xhttp.onload=function(){
        if(xhttp.status!=200){
            console.log("Error");
        }else{
            upload_post_response(xhttp.response);
        }
    }
    xhttp.open("POST","/uploadpost",true);

    var formData=new FormData();
    formData.append("title",document.getElementById("title").value);
    formData.append("text", document.getElementById("text").value);
    xhttp.send(formData);
}
function upload_post_response(response){
    location.reload();
}
function removepost(uniqueID){
    let url="/deletepost?uniqueID="+uniqueID;
    loadDoc(url, removepost_response);
}
function removepost_response(response){
    let data=JSON.parse(response);
    let results=data["result"];
    if(results!="OK"){
        alert(results);
    }else{
        location.reload();
    }
}
function change_picture(){
    let xhttp=new XMLHttpRequest();
    xhttp.onload=function(){
        if (xhttp.status != 200){
            console.log("Error");
        }else{
            upload_picture_response(xhttp.response);
        }
    }
    xhttp.open("POST", "/changepicture", true);

    var formData = new FormData();
    formData.append("file", document.getElementById("file").files[0]);
    xhttp.send(formData);
}
function upload_picture_response(response){
    location.reload();
}
function upload_post(){
    let xhttp=new XMLHttpRequest();
    xhttp.onload=function(){
        if (xhttp.status !=200){
            console.log("Error");
        }else{
            upload_post_response(xhttp.response);
        }
    }
    xhttp.open("POST","/uploadpost", true)

    var formData=new FormData();
    formData.append("text", document.getElementById("text").value);
    xhttp.send(formData);
}
function upload_post_response(response){
    location.reload();
}
function editposts(){
    loadDoc("/editlistposts", editposts_response);
}
function editposts_response(response){
    let data=JSON.parse(response);
    let items=data["results"];
    let divResults=document.getElementById("divResults");
    let temp="";
    for (let i=0; i<items.length; i++){
        temp+="<div class=\"post_container\">";
        temp+="<button onclick=\"removepost('"+items[i]["uniqueID"]+"');\" style=\"font-size: 20px ;\">&#128465</button>";
        temp+="<br>"+items[i]["text"];
        temp+="<div style=\"font-size:12px;\">"+items[i]["time"]+"</div>";
        temp+="</div>";
        }
        divResults.innerHTML=temp;
}

function posts(){
    loadDoc("/listposts", listposts_response);
}
function listposts_response(response){
    let data=JSON.parse(response);
    let items=data["results"];
    let divResults=document.getElementById("divResults");
    let temp="";
    for (let i=0; i<items.length; i++){
        temp+="<div class=\"post_container\">";
        temp+="<img src=\""+items[i]["pic"]+"\" style= \"width:25px; border-radius:100px;\">";
        temp+="<strong>    <a href=\"/profile/"+items[i]["username"]+"\">@"+items[i]["username"]+"</a></strong>";
        temp+="<br>"+items[i]["text"];
        temp+="<div style=\"font-size:12px;\">"+items[i]["time"]+"</div>";
        temp+="<a href=\"/reply/"+items[i]["uniqueID"]+"\">reply</a>";
        temp+="</div>";
    }
    divResults.innerHTML=temp;
}

function profileposts(username){
    url="/profileposts?username="+username;
    loadDoc(url, profileposts_response);
}
function profileposts_response(response){
    let data =JSON.parse(response);
    let items=data["results"];
    let divResults=document.getElementById("divResults");
    let temp="";
    for (let i=0; i<items.length;i++){
        temp+="<div class=\"post_container\">";
        temp+="<strong>@"+items[i]['username']+"</strong>";
        temp+="<br>"+items[i]["text"];
        temp+="<div style=\"font-size:12px;\">"+items[i]["time"]+"</div>";
        temp+="<a href=\"/reply/"+items[i]["uniqueID"]+"\">reply</a>";
        temp+="</div>";
    }
    divResults.innerHTML=temp;
}
function replypost(uniqueID){
    url="/post?uniqueID="+uniqueID;
    loadDoc(url, replypost_response);
}
function replypost_response(response){
    let data=JSON.parse(response);
    let item=data["results"];
    let post=document.getElementById("post");
    let temp="";
    for (let i=0; i<item.length;i++){
        temp+="<div class=\"post_container\">";
        temp+="<strong>@"+item[i]['username']+"</strong>";
        temp+="<br>"+item[i]["text"];
        temp+="<div style=\"font-size:12px;\">"+item[i]["time"]+"</div>";
        temp+="</div>";
    }
    post.innerHTML=temp;
}
function upload_reply(uniqueID){
    let xhttp=new XMLHttpRequest();
    xhttp.onload=function(){
        if (xhttp.status !=200){
            console.log("Error");
        }else{
            upload_reply_response(xhttp.response);
        }
    }
    xhttp.open("POST","/uploadreply", true)

    var formData=new FormData();
    formData.append("text", document.getElementById("text").value);
    formData.append("uniqueID",uniqueID);
    xhttp.send(formData);
}
function upload_reply_response(response){
    location.reload();
}
function postsreplies(uniqueID){
    url="/postreplies?uniqueID="+uniqueID;
    loadDoc(url, postsreplies_response);
}
function postsreplies_response(response){
    let data=JSON.parse(response);
    let items=data["results"];
    let divResults=document.getElementById("divResults");
    let temp="";
    for (let i=0; i<items.length; i++){
        temp+="<div class=\"post_container\">";
        temp+="<strong>@"+items[i]['username']+"</strong>";
        temp+="<br>"+items[i]["text"];
        temp+="<div style=\"font-size:12px;\">"+items[i]["time"]+"</div>";
        temp+="</div>";
    }
    divResults.innerHTML=temp
}


console.log("script loaded");