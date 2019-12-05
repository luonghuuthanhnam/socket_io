import asyncio
import json
from aiohttp import web
import socketio
from translate import Translator
qr_code = ""
users_data = json.load(open('userdata.json',encoding="utf8"))

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)

async def background_task():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        await sio.sleep(10)
        count += 1
        #await sio.emit('my_response', {'data': 'OpenLab Server is Alive'})

async def index(request):
    with open('app.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

@sio.event
async def my_event(sid, message):
    await sio.emit('my_response', {'data': message['data']}, room=sid)

@sio.event
async def my_broadcast_event(sid, message):
    await sio.emit('my_response', {'data': message['data']})

@sio.event
async def join(sid, message):
    sio.enter_room(sid, message['room'])
    await sio.emit('my_response', {'data': 'Entered room: ' + message['room']},
                   room=sid)

@sio.event
async def leave(sid, message):
    sio.leave_room(sid, message['room'])
    await sio.emit('my_response', {'data': 'Left room: ' + message['room']},
                   room=sid)

@sio.event
async def close_room(sid, message):
    await sio.emit('my_response',
                   {'data': 'Room ' + message['room'] + ' is closing.'},
                   room=message['room'])
    await sio.close_room(message['room'])

@sio.event
async def my_room_event(sid, message):
    await sio.emit('my_response', {'data': message['data'], 'client' : message['client']},
                   room=message['room'])

@sio.event
async def disconnect_request(sid):
    await sio.disconnect(sid)

@sio.event
async def connect(sid, environ):
    print("Client Connected")
    await sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)

@sio.event
def disconnect(sid):
    print('Client disconnected')

@sio.on('Android-Connect-Server')
async def android_connect(sid, message):
    if message=='ConnectRequire':
        await sio.emit('Server-Connect-Android','success')

@sio.on('Doctor-Connect-Server')
async def doctor_connect(sid, message):
    if message=='ConnectRequire':
        print("doctor connected")
        await sio.emit('Server-Connect-Doctor','success')

@sio.on('Tele-Connect-Server')
async def Tele_connect(sid, message):
    if message=='ConnectRequire':
        await sio.emit('Server-Connect-Tele','success')

@sio.on('Android-Login-Server')
async def android_login(sid, message):
    for x in users_data['UsersData']:
        if message['id'] == x['id']:
            print('correct id')
            if message['pass'] == x['pass']:
                print('correct pass')
                print('sendding user package')
                await sio.emit('Server-Send-AndroidPackage',x)

@sio.on('Tele-Login-Server')
async def tele_login(sid, message):
    for x in users_data['UsersData']:
        if message['id'] == x['id']:
            print('correct id')
            if message['pass'] == x['pass']:
                print('correct pass')
                print('sendding user package')
                await sio.emit('Server-Send-TelePackage',x)

@sio.on('Android-Send-QR')
async def Android_Send_QR(sid, message):
    print(message)
    if  qr_code == message['qr']:
        for x in users_data['UsersData']:
            if message['id'] == x['id']:
                print("send package via qr")
                await sio.emit('Server-Send-TelePackage',x)
        print("corect qr")

@sio.on('Tele-Send-QR')
async def Tele_Send_QR(sid, message):
    global qr_code
    qr_code = message
    print('tele send qr')

@sio.on('Speech-Translate')
async def Speech_Translate(sid, message):
    a = message.split('@')
    out = ""
    if a[0]=="tele":
        translator = Translator(from_lang=a[2].rstrip(), to_lang=a[3].rstrip())
        out = "tele@" + translator.translate(a[1])
    else:
        translator = Translator(from_lang=a[2].rstrip(), to_lang=a[3].rstrip())
        out = "doctor@" + translator.translate(a[1])
    print(out)
    await sio.emit('Server-Translated', out)


app.router.add_static('/static', 'static')
app.router.add_get('/', index)

if __name__ == '__main__':
    sio.start_background_task(background_task)
    web.run_app(app)
