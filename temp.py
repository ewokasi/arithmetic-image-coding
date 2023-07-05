import json

# with open("pure_prob.json") as file:
#     data = json.loads(file.read())

# dataset ={}
# uniq = set(data)
# for i in uniq:
#     dataset[i]= data.count(i)
# print(sorted(dataset.items(), key = lambda x:x[1]))

if __name__=="__main__":

    with open("full_info.json") as file:
        full_info = str(json.loads(file.read()))
    with open("recovered_from_pure.json") as file:
        recovered = str(json.loads(file.read()))
        

    for i in range(len(full_info)):
        if recovered[i]!=full_info[i]:
            print("error on",i )