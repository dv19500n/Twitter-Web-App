from flask import Flask, redirect, render_template, session, request, make_response
from flask_session import Session
import final
app = Flask(__name__)
app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]='filesystem'
Session(app)
#FINAL code
@app.route('/twittersignup.html')
def signup_html():
    if twitterlogged_in():
        return redirect('/editprofile.html')
    return render_template('/twittersignup.html')

@app.route('/twitterlogin.html')
def log_in_html():
    if twitterlogged_in():
        return redirect('/editprofile.html')
    return render_template('/twitterlogin.html')

@app.route('/changepicture.html')
def change_pic_html():
    if twitterlogged_in():
        username=session['username']
        image=session['picture']
        return render_template('/changepicture.html', username=username, image=image)
    return redirect('/static/Final.html')

@app.route('/editprofile.html')
def edit_profile():
    if twitterlogged_in():
        username=session['username']
        image=session['picture']
        return render_template('/editprofile.html', username=username, image=image)
    return redirect('/static/Final.html')

@app.route('/twitterLogout.html')
def twitter_logout_html():
    session.pop('email',None)
    session.pop('username',None)
    session.pop('picture', None)
    return redirect("/static/Final.html")

@app.route('/feed.html')
def feed_html():
    if twitterlogged_in():
        username=session['username']
        image=session['picture']
        return render_template('/feed.html', username= username, image=image)
    return redirect('/static/Final.html')

@app.route('/twitterLogin')
def twitter_login():
    email=request.args.get('email','')
    password=request.args.get('password','')
    if email=='' or password=='':
        return{'result':'Password and Email are both required'}
    table=final.get_table('TwitterUsers')
    item=table.get_item(Key={'email':email})
    if 'Item' not in item:
        return{'result':'Email not found'}
    user=item['Item']
    if password!=user['password']:
        return{'result':'Password is incorrect'}
    # session['user']=user
    session['username']=user['username']
    session['email']=user['email']
    session['password']=user['password']
    session['picture']=user['picture']
    return {'result':'OK'}

def twitterlogged_in():
    if not session.get('email'):
        return False
    return True

@app.route('/twitterSignup')
def twitter_signup():
    username=request.args.get('username','')
    email=request.args.get('email','')
    password=request.args.get('password','')
    if email=='' or password=='' or username=='':
        return{'result':'Username, Email, and Password are required'}
    if '@' not in email or '.' not in email:
        return{'result':'\"@\" and \".\" must be in the email'}
    signedup=final.signup(username, email, password)
    if signedup:
        table=final.get_table('TwitterUsers')
        item=table.get_item(Key={'email':email})
        user=item['Item']
        session['email']=user['email']
        session['username']=user['username']
        session['password']=user['password']
        session['picture']=user['picture']
        return {'result':'OK'}
    return{'result':'Email is already in use'}

@app.route('/changepicture', methods=['POST'])
def changepicture():
    email=session['email']
    current=final.change_picture(email)
    session['picture']=current
    return{'result':'OK'}

@app.route('/uploadpost', methods=['POST'])
def uploadpost():
    email=session['email']
    username=session['username']
    return final.upload_post(email, username)

@app.route('/editlistposts')
def editlistpost():
    email=session['email']
    posts=final.edit_list(email)
    return{'results':posts}

@app.route('/deletepost')
def removepost():
    return final.delete_post()

@app.route('/listposts')
def listposts():
    email=session['email']
    posts=final.list_posts(email)
    return {'results':posts}

@app.route('/profile/<username>')
def profile(username):
    table=final.get_table('TwitterUsers')
    image=""
    for item in table.scan()['Items']:
        if item['username']==username:
            image=item['picture']
    return render_template("profile.html", username=username, image=image)

@app.route('/profileposts')
def profileposts():
    results=final.profile_posts()
    return{'results':results}

@app.route('/reply/<uniqueID>')
def reply(uniqueID):
    table=final.get_table('twitterPost')
    username=""
    for item in table.scan()['Items']:
        if item['uniqueID']==uniqueID:
            username=item['username']
    return render_template("reply.html", username=username, uniqueID=uniqueID)

@app.route('/post')
def replypost():
    results=final.reply_post()
    return {'results':results}

@app.route('/uploadreply', methods=['POST'])
def uploadreply():
    email=session['email']
    username=session['username']
    return final.upload_reply(email, username)

@app.route('/postreplies')
def postreplies():
    results=final.post_replies()
    return {'results':results}

