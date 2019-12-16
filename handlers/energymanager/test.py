import datetime
import arrow
to = 0.0
for i in range(1,3):
    to = to + 1.1
print(int("05") + 1)
aaa = None
if aaa is None:
    print("aa")
if aaa == None:
    print("c")



a = round((1.9 + (1.2 - 1.0)), 2)
print(round(0.0, 2))
print(datetime.datetime.now())
now_time=datetime.datetime.now()
aa = "2019-12-11 00"
print(datetime.datetime.strptime(aa, "%Y-%m-%d %H"))
vv = datetime.datetime.strptime(aa, "%Y-%m-%d %H:%M:%S")
print(str(vv + datetime.timedelta(days=-1))[0:10])
print((vv+datetime.timedelta(hours=-1)).strftime("%Y-%m-%d %H:%M:%S")[0:1])
a = 1.23
b = 2.23
print(float(b)-float(a))
def subtract(float1, float2):
    float2
def strlastMonth(currentmonth):
    curr = currentmonth.split("-")
    str0 = curr[0]
    str1 = curr[1]
    if "0" in str1:
        str00 = str1[1]
    else:
        str00 = str1
    if str00 == "1":
        return str(int(str0)-1)+"-"+"12"
    else:
        las = int(str00) - 1
        if las < 10:
            la = "0" + str(las)
        else:
            la = str(las)
        return str0 + "-" + la
currentmonth = "2018-11"
aa = strlastMonth(currentmonth)
str = currentmonth.split("-")
str0 = str[0]
str1 = str[1]
arro = arrow.now()
currentmonth = datetime.datetime.now().month
currentmonth = arro.shift(months=0).format("YYYY-MM")
lastM = arro.shift(months=-1).format("YYYY-MM")
start = arrow.get('2015-01','YYYY-MM')

end = arrow.get('2015-12','YYYY-MM')
print(lastM)