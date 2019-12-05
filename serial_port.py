import serial
import threading
from translate import Translator
#translator= Translator(from_lang='vi', to_lang='en')
portname = "COM51"
baudrate = 115200
ser = serial.Serial(portname,baudrate,timeout=2)

def translate_this(content, from_lang, to_lang):
    translator = Translator(from_lang=from_lang, to_lang=to_lang)
    out = translator.translate(content)
    print(out)
def handle_data(data):
    print(data)
    if (data != "" and "translate@" in data):
        a = data.split('@')
        translator = Translator(from_lang=a[2].rstrip(), to_lang=a[3].rstrip())
        out = translator.translate(a[1])
        print(out)
        ser.write((str(out) + '#').encode('utf-8'))

def read_from_port(_serial):
    while True:
       reading = ser.readline().decode("utf-8")
       handle_data(reading)

#port_thread = threading.Thread(target=read_from_port,args=(ser,))
#port_thread.start()
translate_this("Hello","en","vi")