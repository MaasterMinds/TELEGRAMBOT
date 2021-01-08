import telepot
import csv
from telepot.loop import MessageLoop
from datetime import date
import time
import RPi.GPIO as gpio

bot = telepot.Bot("PASTE BOT  API TOKEN HERE")
print (bot.getMe())
newUpdateId=0
update_id=0
chatID=0
tv = 11
hall_Light = 13
room_Light1 = 15
gpio.setmode(gpio.BOARD)
gpio.setwarnnings(False)
gpio.setup(tv,gpio.OUT)
gpio.setup(Hall_Light,gpio.OUT)
gpio.setup(Room_Light1,gpio.OUT)
gpio.output(tv,False)
gpio.output(hall_Light,False)
gpio.output(room_Light1,False)


# Added by tony
def date():
    from datetime import date
    global dt_string
    now = date.today()
    dt_string = now.strftime("%d/%m/%Y")
    #print("date =", dt_string)
    return dt_string

date()


def subtotal(a,b):
    filename = r"FILE.csv"
    with open(filename,"r") as datafile:
        global hours,costs,units,ohours,ounits,ocosts
        hours,units,costs,ohours,ounits,ocosts=[],[],[],[],[],[]
        reader = csv.reader(datafile)
        next(reader)
        #next(reader)
        title = next(reader)
        #print(title[0])
        for row in reader:
            #print(row[0])
            if row[0]== a and row[2] == b :
                hour=float(row[3])
                hours.append(hour)
                unit=float(row[4])
                units.append(unit)
                cost=float(row[5])
                costs.append(cost)

            if row[0]== a and b == "over all" :
                ohour=float(row[3])
                ohours.append(ohour)
                ounit=float(row[4])
                ounits.append(ounit)
                ocost=float(row[5])
                ocosts.append(ocost)
        ohours=sum(ohours)
        ounits=sum(ounits)
        ocosts=sum(ocosts)
        hours=sum(hours)
        units=sum(units)
        costs=sum(costs)
        #print(hours,units,costs)
        #print(ohours,ounits,ocosts)



def summer(value , zero):
    filename = r"FILE.csvyo.csv"
    value = int(value)
    sumer =int(zero)
    with open(filename, 'r')as file:
        reader = csv.reader(file)
        next(reader)
        next(reader)
        for line in reader:
            a = float(line[value])
            sumer = sumer + a
##           print(line[value])
##        print("sum is : ",sumer)
    return sumer




global dict
dict ={ 'dev1': 'TV', 'dev1watts': '30',
        'dev2': 'HL', 'dev2watts': '40',
        'dev3': 'RM1L', 'dev3watts': '60'}


#
# def newfile():
#     global fields
#     fields = ['devices', 'wattage','date', 'time', 'units', 'cost']
#
#     filename = r"FILE.csvyo.csv"
#     with open(filename, 'a') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames = fields)
#         writer.writeheader()



def writer(x , y, z ,w):
    units = z
    rate= w
    device = x
    watts = y
    global mydict
    mydict =[{'devices':device, 'wattage':watts,'date': dt_string, 'time':str(hours), 'units':str(units), 'cost':str(rate)}]

    filename = r"FILE.csvyo.csv"
    fields = ['devices', 'wattage','date', 'time', 'units', 'cost']

    with open(filename, 'a' , newline="\n") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fields)
        writer.writerows(mydict)


# Till here


def readFile():
    path=r"user_data.csv"
    with open(path)as dataFile:
        csv_f=csv.DictReader(dataFile)
        usrData={}
        for row in csv_f:
            usrData[row['usrId']]=row['Name']
    return usrData

class checkUser:
#     valid_usr=readFile()
#     print(valid_usr)
    def users(self,user):
        valid_usr=readFile()
        print(valid_usr)
        if str(user) in valid_usr:
            return valid_usr[str(user)]
        else:
            return False

def verifyPass(chatID):
    Pass="Im_Master"
    bot.sendMessage(chatID,"enter password")
    input_pass=reciveMsg()
    message=input_pass['message']
    chat=message['chat']
    text=message['text']
    count=3

    while(text != Pass):
        bot.sendMessage(chatID,"wrong password try again {} chance left".format(count))
        input_pass=reciveMsg()
        message=input_pass['message']
        chat=message['chat']
        text=message['text']
        print(text)
        if count==0:
            bot.sendMessage(chatID,"Max attempt exceeds")
            return False
            break
        count-=1
    return True

def addUsr(chatID,name):
    path=r"user_data.csv"
    user=[{"usrId":chatID,'Name':str(name)}]
    key=['usrId','Name']
    with open(path,"a")as dataFile:
        writer=csv.DictWriter(dataFile,fieldnames=key)
        writer.writerows(user)
    bot.sendMessage(chatID,"yhee you have became my master now")
    return

def reciveMsg():
    global newUpdateId
    global update_id
    while(True):
        response = bot.getUpdates()
        for ele in response:
            response=ele
#         print(response)
        update_id=response['update_id']
        if update_id != newUpdateId:
            newUpdateId=update_id
#             print(update_id)

            return(response)
        else: continue

def controlGPIO(chatID,user):
    tmep_chatID=0
    bot.sendMessage (chatID,"{} I'm ready to recive command please proceed".format(user))
    bot.sendMessage (chatID," Use following command \n \
    ON_TV: ON T or OFF T\n \
    Hall_light:ON HL or OFF HL\n \
    Room_1_light: ON RM1L or OFF RM1L \n \
    Room_2_light: ON RM2L or OFF RM2L \n \
    End : exit ")
    while(1):
        msg=reciveMsg()
        message=msg['message']
        chat=message['chat']
        text=message['text']
        temp_chatID=(chat['id'])
        global hours
        global ta
        global tb
        global tc
        if chatID==temp_chatID:
            text=text.lower()
            if "exit" in text:
                bot.sendMessage (chat['id'], "ending... bye see-you {} ".format(user))
                return
            if "on" in text:
                if "on t" in text:
                    gpio.output(tv,True)
                    ta= time.perf_counter()
                    date()
                    bot.sendMessage (chat['id'], "{}, TV is turned ON".format(user))
                elif "on hl" in text:
                    gpio.output(hall_Light,True)
                    tb= time.perf_counter()
                    date()
                    bot.sendMessage (chat['id'], "{}, Hall lights turned ON".format(user))
                elif "on rm1l" in text:
                    gpio.output(room_Light1,True)
                    tc= time.perf_counter()
                    date()
                    bot.sendMessage (chat['id'], "{}, ROOM_1 lights turned ON".format(user))
                elif "on rm2l" in text:
                    bot.sendMessage (chat['id'], "{}, ROOM_2 lights turned ON".format(user))
            elif "off" in text:
                if "off t" in text:
                    gpio.output(tv,False)
                    t1= float(time.perf_counter() - ta)
                    hours= t1
                    unit1=((float(dict['dev1watts'])*t1)/1000)
                    rate1 = unit1 * 2.65
                    print(t1, unit1 ,rate1)
                    writer(dict['dev1'], dict['dev1watts'] ,unit1 ,rate1)
                    bot.sendMessage (chat['id'], "{}, TV is turned off".format(user))
                elif "off hl" in text:
                    gpio.output(hall_Light,False)
                    t2= float(time.perf_counter() - tb)
                    hours= t2
                    unit2=((int(dict['dev2watts'])*t2)/1000)
                    rate2 = unit2 * 2.65
                    print(t2, unit2 ,rate2)
                    writer(dict['dev2'], dict['dev2watts'],unit2 ,rate2)
                    bot.sendMessage (chat['id'], "{}, Hall lights turned off".format(user))
                elif "off rm1l" in text:
                    gpio.output(room_Light1,False)
                    t3= (time.perf_counter() - tc)
                    hours= t3
                    unit3=((float(dict['dev3watts'])*t3)/1000)
                    rate3= unit3 * 2.65
                    print(t3, unit3 ,rate3)
                    writer(dict['dev3'], dict['dev3watts'] ,unit3 ,rate3)
                    bot.sendMessage (chat['id'], "{}, ROOM_1 lights turned off".format(user))
                elif "off rm2l" in text:
                    bot.sendMessage (chat['id'], "{}, ROOM_2 lights turned off".format(user))
            elif "show usage" in text:
                print("use commands")
                response = ("use the following commands:\n \n 'TOTAL USAGE' = Gives total consumption by all devices till date\n \n 'TODAY USAGE' = Gives today's total consumption by all devices seperately \n \n 'DEVICE USAGE' = Gives seperate total consumption by all devices till date")
                response = response + "."
                bot.sendMessage(chatID, response)

            elif "total usage" in text:
                s1=summer(3,0)
                s2=summer(4,0)
                s3=summer(5,0)
                sumer = (" TOTAL CONSUMPTION OF ALL DEVICES: \n \n total time = {}hrs \n \n total energy = {}units \n \n total cost = {}rs".format(round(s1,2),round(s2,2),round(s3,2)))
                bot.sendMessage(chatID,sumer)
            elif "today usage" in text:
                date()
                subtotal("TV",dt_string)
                response1=("Today you used \n \n TV :- \n Time: {}hrs \n Energy: {}units \n Cost: {}rs".format(round(hours,2),round(units,2),round(costs,2)))
                date()
                subtotal("HL",dt_string)
                response2=("\n \n HALL LIGHT :- \n Time: {}hrs \n Energy: {}units \n Cost: {}rs".format(round(hours,2),round(units,2),round(costs,2)))
                date()
                subtotal("RM1L",dt_string)
                response3=("\n \n ROOM1 LIGHT :- \n Time: {}hrs \n Energy: {}units \n Cost: {}rs".format(round(hours,2),round(units,2),round(costs,2)))
                response = (response1 + response2 + response3 +".")
                bot.sendMessage(chatID, response)
            elif "device usage" in text:
                subtotal("TV","over all")
                response1=("TILL THIS DAY \n \n TV :- \n Time: {}hrs \n Energy: {}units \n Cost: {}rs".format(round(ohours,2),round(ounits,2),round(ocosts,2)))
                #print(response1)
                subtotal("HL","over all")
                response2=("\n \n HALL LIGHT :- \n Time: {}hrs \n Energy: {}units \n Cost: {}rs".format(round(ohours,2),round(ounits,2),round(ocosts,2)))
                subtotal("RM1L","over all")
                response3=("\n \n ROOM1 LIGHT :- \n Time: {}hrs \n Energy: {}units \n Cost: {}rs".format(round(ohours,2),round(ounits,2),round(ocosts,2)))
                #print(response3)
                response = (response1 + response2 + response3 +".")
                bot.sendMessage(chatID, response)

            else:
                bot.sendMessage (chat['id'], "{}, invalid command use below command: \n \
        ON_TV: ON T or OFF T\n \
        Hall_light:ON HL or OFF HL\n \
        Room_1_light: ON RM1L or OFF RM1L \n \
        Room_2_light: ON RM2L or OFF RM2L \n \
        End : exit ".format(user))

        else:
            bot.sendMessage (chat['id'], "I'm working for {} Now".format(user))



def start(msg):
#     print(msg.keys())
    message=msg['message']
    chat=message['chat']
    text=message['text']
    chatID=(chat['id'])
    name=(chat['first_name'])
    validate=checkUser()
    user=validate.users(chat['id'])
    print(user)
    if user:
        print("command form {}".format(user))
        bot.sendMessage (chat['id'], "Hi {} this is RPIGenie what can i do for you".format(user))
        controlGPIO(chatID,user)

    else:
        bot.sendMessage(chatID,"ooops you're not my master i can't take commands form you!")
        bot.sendMessage(chatID,"you can authenticate to become my master")
        Authentication=verifyPass(chatID)
        if Authentication:
            addUsr(chatID,name)
            return
if __name__ == '__main__':
    reciveMsg()
    while(1):
        msg=reciveMsg()
        start(msg)
