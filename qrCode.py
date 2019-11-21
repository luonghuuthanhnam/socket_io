# Nhớ pip install pyzbar
# Nhớ pip install qrcode[pil]
import numpy
import cv2
import pyzbar.pyzbar as pyzbar
import qrcode

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN

def RecognizeQR(cvFrame):
    decodedObjects = pyzbar.decode(cvFrame)
    output = 'null'
    for obj in decodedObjects:
        print("Data", obj.data)
        output = str(obj.data)
    return str(output)

BHYT_Code, name, date_of_bird, gender, address, KCB_code, start_using_date, giving_date, BHXH_code, valid_date, _5years_member = "","","","","","","","","","",""
def Split_data(data_qr):
    data_split = data_qr.split('|')
    global BHYT_Code, name, date_of_bird, gender, address, KCB_code, start_using_date, giving_date, BHXH_code, valid_date, _5years_member
    BHYT_Code = data_split[0]
    name = bytes.fromhex(data_split[1]).decode('utf-8')
    date_of_bird = data_split[2]
    if data_split[3]=="1":
        gender = "Nam"
    else:
        gender = "Nữ"
    address = bytes.fromhex(data_split[4]).decode('utf-8')
    KCB_code = data_split[5]
    start_using_date = data_split[6]
    valid_date = data_split[7]
    giving_date = data_split[8]
    BHXH_code = (data_split[9])[4:]
    _5years_member = data_split[12]
    print("Mã BHYT: {}\n".format(BHYT_Code),
          "Tên: {}\n".format(name),
          "Ngày sinh: {}\n".format(date_of_bird),
          "Giới tính: {}\n".format(gender),
          "Địa chỉ: {}\n".format(address),
          "Nơi đk khám chữa bệnh: {}\n".format(KCB_code),
          "Ngày bắt đầu sử dụng: {}\n".format(start_using_date),
          "Ngày hết hạn: {}\n".format(valid_date),
          "Ngày cấp thẻ: {}\n".format(giving_date),
          "Mã BHXH: {}".format(BHXH_code),
          "Ngày đủ 5 năm liên tục: {}\n".format(_5years_member))




def TurnOnCamera():
    while(1):
        ret, frame = cap.read()
        _qr_content = str(RecognizeQR(frame))
        if _qr_content!= "null":
            print(_qr_content[2:])
            #print(type(_qr_content))
            Split_data(_qr_content[2:])
        cv2.putText(frame, _qr_content, (50, 50), font, 2, (255, 0, 0), 3)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def makeQR(content, isReturnCVimage):
    img = qrcode.make(content)
    img = img.convert('RGB')
    open_cv_image = numpy.array(img)
    if(isReturnCVimage==0 or isReturnCVimage=="no"):
        return img
    else:
        return open_cv_image

def TestMakeQR(content):
    image = makeQR(content,1)
    cv2.imshow("qr",image)
    cv2.waitKey()

#TestMakeQR("Hello Nam")
TurnOnCamera()