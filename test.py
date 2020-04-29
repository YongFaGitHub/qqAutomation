import json

data= json.loads('{"19793": {"count": [{"add": 2,"budget": 0,"countid": 111888,"left": 2,"modid": "platform","name": "卡片“破解鬼手之谜”","rekey": "conf","used": 0,"user": "1071343549"}]}}')
for key, value in data.items():
    # print(key, value)
    for key, value in value.items():
        print(key, value)
# for num in range(19793,19874):
#     count=str(num)
#     print(count)
#     print("卡牌：",data[str(num)])
  
# print (data[str(19793)])



# data = json.dumps(data)

# print (data)

