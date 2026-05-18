import boto3
import uuid
from flask import Flask, request
from datetime import datetime
import os

AWSKEY = os.environ.get("AWSKEY")
AWSSECRET = os.environ.get("AWSSECRET")
defult='defultprofile.png'
PUBLIC_BUCKET='dv19500n-twitterpic'
STORAGE_URL='https://s3.amazonaws.com/'+PUBLIC_BUCKET+'/'

def get_public_bucket():
    s3=boto3.resource(service_name='s3',
                        region_name='us-east-1',
                        aws_access_key_id=AWSKEY,
                        aws_secret_access_key=AWSSECRET)
    bucket= s3.Bucket(PUBLIC_BUCKET)
    return bucket

def get_table(name):
    dbclient= boto3.resource(service_name='dynamodb',
                            region_name='us-east-1',
                            aws_access_key_id=AWSKEY,
                            aws_secret_access_key=AWSSECRET)
    return dbclient.Table(name)

def signup(username, email, password):
    defultpic_url=STORAGE_URL+defult
    table=get_table('TwitterUsers')
    item=table.get_item(Key={'email':email})
    if 'Item' not in item:
        user={
            'email':email,
            'username':username,
            'password':password,
            'picture':defultpic_url
        }
        table.put_item(Item=user)
        return True
    return False

def change_picture(email):
    bucket = get_public_bucket()
    file= request.files["file"]
    filename=file.filename
    ct='image/jpeg'
    if filename.endswith('.png'):
        ct='image/png'
    unique_filename=str(uuid.uuid4())+'_'+filename
    bucket.upload_fileobj(file, unique_filename, ExtraArgs={'ContentType':ct})
    url=STORAGE_URL+unique_filename
    table=get_table('TwitterUsers')
    table.update_item(
        Key={'email':email},
        UpdateExpression='set picture=:p',
        ExpressionAttributeValues={':p':url}
    )
    item=table.get_item(Key={'email':email})
    user=item['Item']
    current=user['picture']
    if url==current:
        return current

def upload_post(email, username):
    text=request.form.get("text","")
    time=str(datetime.now())
    ID=str(uuid.uuid4())
    post={
        'uniqueID': ID,
        'time':time,
        'text':text,
        'email':email,
        'username':username
        }
    table=get_table('twitterPost')
    table.put_item(Item=post)
    return{'result':'OK'}

def edit_list(email):
    table=get_table('twitterPost')
    results=[]
    for item in table.scan()['Items']:
        if item['email']==email:
            time=datetime.fromisoformat(item['time'])
            item['time']=time.strftime("%m/%d/%y %I:%M%p").lower()
            results.append(item)
    sorted_results=sorted(results,key=lambda x: x.get('time'), reverse=True)
    return sorted_results

def delete_post():
    ID=request.args.get('uniqueID','')
    table= get_table('twitterPost')
    table.delete_item(Key={'uniqueID':ID})
    return{'result':'OK'}

def list_posts(email):
    table=get_table('twitterPost')
    results=[]
    dic={}
    pictures=get_table('TwitterUsers')
    for item in table.scan()['Items']:
        if item['email'] != email:
            current=item['email']
            pics=pictures.get_item(Key={'email':current})
            pic=pics['Item']['picture']
            item['pic']=pic
            time=datetime.fromisoformat(item['time'])
            item['time']=time.strftime("%m/%d/%y %I:%M%p").lower()
            results.append(item)
    sorted_results=sorted(results, key=lambda x: x.get('time'), reverse=True)
    final=[]
    for item in sorted_results:
        current=item['email']
        if current not in dic:
            dic[current]=1
        if dic[current]<=10:
            final.append(item)
            dic[current]+=1
    return final

def profile_posts():
    table = get_table('twitterPost')
    username=request.args.get('username','')
    results=[]
    for item in table.scan()['Items']:
        if item["username"]==username:
            time=datetime.fromisoformat(item['time'])
            item['time']=time.strftime("%m/%d/%y %I:%M%p").lower()
            results.append(item)
    sorted_results=sorted(results, key=lambda x: x.get('time'), reverse=True)
    return sorted_results

def reply_post():
    table=get_table('twitterPost')
    uniqueID=request.args.get('uniqueID','')
    results=[]
    for item in table.scan()['Items']:
        if item['uniqueID']==uniqueID:
            time=datetime.fromisoformat(item['time'])
            item['time']=time.strftime("%m/%d/%y %I:%M%p").lower()
            results.append(item)
    sorted_results=sorted(results, key=lambda x: x.get('time'), reverse=True)
    return sorted_results

def upload_reply(email, username):
    text=request.form.get("text","")
    uniqueID=request.form.get("uniqueID","")
    time=str(datetime.now())
    reply={
        'replyID':uniqueID,
        'time':time,
        'text':text,
        'email':email,
        'username':username
        }
    table=get_table('twitterReplies')
    table.put_item(Item=reply)
    return {"result":"OK"}
def post_replies():
    table=get_table('twitterReplies')
    uniqueID=request.args.get('uniqueID','')
    results=[]
    for item in table.scan()['Items']:
        if item['replyID']==uniqueID:
            time=datetime.fromisoformat(item['time'])
            item['time']=time.strftime("%m/%d/%y %I:%M%p").lower()
            results.append(item)
    sorted_results=sorted(results, key=lambda x: x.get('time'), reverse=True)
    return sorted_results