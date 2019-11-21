var1='SV4797929538862' #mã bảo bh y tế
var2= '4cc3aa204e68c6b020416e68' #họ và tên
var3= '09/06/1998' #Ngày sinh
var4= '1' #giới tính 1:nam, 0:nữ
var5 = '2e2c205068c6b0e1bb9d6e67205068c6b0e1bb9b63204c6f6e6720422c205175e1baad6e20392c205468c3a06e68207068e1bb912048e1bb93204368c3ad204d696e685f3136313436323334' #địa chỉ
var6 = '79 - 036' #Mã đăng ký khám chữa bệnh
var7 = '01/01/2018' #sử dụng từ
var8 = '-' #sử dụng đến
var9 = '09/01/2018' #ngày cấp
var10 = '79007929538862' #Mã bảo hiểm xã hội (bỏ 4 số đầu)
var11 = '-'
var12 = '4'
var13 = '01/01/2023'#Thời hạn đạt mức 5 năm liên tục
var14 = '162dc7c174f66de3-7102'
var15 = '$\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'


print( bytes.fromhex(var2).decode('utf-8'))
print( bytes.fromhex(var5).decode('utf-8'))
print( bytes.fromhex(var14).decode('utf-8'))


