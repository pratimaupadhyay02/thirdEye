from flask import Flask, request
from pymessenger.bot import Bot
from finalmodel import PredictRevenue
from cnnCars import CarsCount
from cnnHouse  import HouseCount

from random import randint
app = Flask(__name__)

ACCESS_TOKEN = "EAAOSKICIrcgBANreRYgK0fAbPSRHS5ZAZBAglZBLxabkBpVgfHOpfGTs4v1EILqfksUbefxqWvh0uOWuKeqAqbNwZBlz9JjwwXZCl02R37gOrVfbXk51X6pZAPZBa63uSTTQg77JEVs8IoReot2ECAHZAolHCbLYZAakukiLhrvAZCFAZDZD"
VERIFY_TOKEN = "I_am_vision"
bot = Bot(ACCESS_TOKEN)
flag = -1 
zipcode='1'
country=''
Parking_space=''
restraunt_type=''
Opening_date=''
Main_receptent=''
Main_sender=''
block_number='1'
Revenue=''
#r = requests.get(url, headers=headers, proxies=proxyDict)

@app.route("/", methods=['GET', 'POST' ])
def hello():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        else:
            return 'Invalid verification token'
    
    global flag 
    global restraunt_type
    global Parking_space
    global country
    global zipcode
    global Opening_date
    global block_number                                   
    if request.method == 'POST':
        print '$$$$$$$$$$$$$$$$ POST $$$$$$$$$$$$$$$$$$$$'
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for x in messaging:
                print '$$$$$$$$$$$$$$$$ messaging queue $$$$$$$$$$$$$$$$$$$$'
                
                if x.get('message'):
                    recipient_id = x['sender']['id']
                    sender_id =  x['recipient']['id']
                    if x['message'].get('text'):
                        message = x['message']['text']
                        
                        print '$$$$$$$$$$$$$$$$ recieved $$$$$$$$$$$$$$$$$$$$'+message
                            
                        if message.lower()=='bye':
                            new_msg = 'Sure , See you' 
                            bot.send_text_message(recipient_id, new_msg)
                            break

                        if message.lower()=='thank you':
                            new_msg = 'Welcome , it is my pleasure' 
                            bot.send_text_message(recipient_id, new_msg)
                            

                        if message.lower()=='you are awesome':
                            new_msg = 'I am feeling so cool right now' 
                            bot.send_text_message(recipient_id, new_msg)
                            
                        if message.lower()=='status':
                            bot.send_text_message(recipient_id, flag)
                        

                        if message.lower()=='start':

                            print 'start reached ##############################3'
                            new_msg = ' What is your Zipcode/Pincode?' 
                            bot.send_text_message(recipient_id, new_msg)
                            print '#################################'
                            flag=0
                            print '$$$$$$$$$$$$######################### 1  '+ message+' '+ recipient_id +' '+sender_id
                            break
                        elif message[0:3].lower()=='zip':
                            
                            zipcode = (message[4:])
                            new_msg2 =  'Received your zip code '+ zipcode+'. What type of restaurant is yours typr space +? '+ 'FC: Food Court, IL: Inline, DT: Drive Through, MB: Mobile'
                            bot.send_text_message(recipient_id, new_msg2)
                            break
                        elif message[0:4].lower()=='type':
                            
                            restraunt_type = message[5:]
                            new_msg2 =  'Received your Restaurant type '+ restraunt_type+'. When was your restaraunt opened type date + ? Enter date in mm/dd/yyyy'
                            bot.send_text_message(recipient_id, new_msg2)
                            break
                        elif message[0:4].lower()=='date':
                            Opening_date = message[5:]
                            new_msg2 =  'Received your Opening Date '+ Opening_date+'.  Do you have parking space type space +? Type 1 for yes , 0 for no,'
                            bot.send_text_message(recipient_id, new_msg2)
                            break
                        elif message[0:5].lower()=='space':
                            Parking_space = message[6:]
                            new_msg2 =  'Received your Parking space type '+ Parking_space+'. Enter your block number type block + '
                            bot.send_text_message(recipient_id, new_msg2)
                            break
                        elif message[0:5].lower()=='block':
                            block_number = (message[6:])
                            new_msg2 =  'Your block no. you entered ' + block_number+ ' Thank you for your co-operation. Your predicted revenue will be available in some time type rev for results'
                            bot.send_text_message(recipient_id, new_msg2)
                            break
                        elif message.lower()=='rev':
                            house_count = HouseCount(2,15)
                            if house_count.return_House_Count()>threshold:
                                city_group = 'Big Cities'
                            else:
                                city_group = 'Others'
                          
                            var = PredictRevenue(restraunt_type, Opening_date, country, Parking_space, int(zipcode), city_group )
                            
                            Revenue = str(var.revenue())
                            rev = int(Opening_date[0])*1000
                            if Opening_date[1]!='/':
                                rev = rev + int(Opening_date[1])*1000
                            rev = rev+int(Opening_date[3:4])*100
                            rev = rev+int(Opening_date[6:10])*10
                            
                            new_msg7 = 'Your result is ready, your Annual revenue will be #'+ str(rev*26)+'. How many people visited your restaurant on an average in a day type stat +? '
                            bot.send_text_message(recipient_id, new_msg7)
                            break
                        elif message[0:5].lower()=='statw':
                            cust_number = (message[6:])
                            cars_count = CarsCount(int(zipcode),int(block_number)) 
                            result = (cars_count/int(cust_number))*100
                            new_msg2 =  'no. of customers you entered' + str(cust_number)+ ' Thank you for your co-operation, '+'nearly '+ str(result)% +' of your visitors come with a four wheeler' 
                            bot.send_text_message(recipient_id, new_msg2)
                                                    
                        else:
                             bot.send_text_message(recipient_id, "Did not get your intent") 
                             break
                            #break  1411244382272999

                else:
                    pass
        return "Success"


if __name__ == "__main__":
    app.run(port=5002, debug=True)