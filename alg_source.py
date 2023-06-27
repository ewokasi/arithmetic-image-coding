import json
from decimal import Decimal
def get_probs(string):
    #print(string)
    string=str(string)
    if string=="" or string ==None:
        print("The input string is None or empty")
        return 0
    
    string= string+"!"
    alphabet = string
    length = len(string)
    probs = {}
    for alpha in alphabet:
        probs[alpha]= string.count(alpha)/length
    return probs


def get_location(probs, entering = 0, finish =1):
    location= {}
    previous = entering
    mults = finish-entering
    for alpha in probs:
        
        left = previous
        right = left+(probs[alpha]) * mults
        #print(right-left)
        previous=right
        location[alpha] = [left, right]
    return location
   


def select(start, end):
    #print(start, end)
    start = str(start)
    end = str(end)
    res = ""
    for i in range(2,len(start)):

        if start[i]==end[i]:
            res+=start[i]
        else:
            #print("sss",start[i])
            if int(end[i])-int (start[i])>=1:
                res+=str(int(start[i])+1)
                break
    #print(res)
    #print(start, end)
    return res


def compression(string):
    probs= get_probs(string)
    string+="!"
    #probs ={"a":0.6, "b":0.2,"c":0.1, "!":0.1}
    location = get_location(probs)
    left = 0
    right = 1

    for alpha in string:
        #print("iteration", alpha)
        left = location[alpha][0]
        right = location[alpha][1]
        location = get_location(probs, left, right)
        #print("calcs" ,location)
      
    compressed = select(left, right)
    #print("select" ,compressed)
    archive ={}
    archive['p']=probs
    archive['c']=compressed
    return archive

def save(archive, name):
    with open(f'{name}.json', 'w') as outfile:
        json.dump(archive, outfile)

def load(name):
    with open(f'{name}', 'r') as infile:
        return json.loads(infile.read())


def o_format(data):
    return float('0.'+str(data))


def location_to_alpha(location, data):
    length = len(location)
    #print("location", list(location.values()))
    
    for i in range(length):
     
        left  = list(location.values())[i][0]
        right = list(location.values())[i][1]
        #print("iteration ",i, "left", left, "right", right, "data", data, "delta",right-left) 
        
        if left<=data and right >=data:
    
            return list(location)[i]
        
            
def separator(string):
    dataset = {}
    sector=""
    iter=0
    for i in range(len(string)):
        sector+=str(string[i])
        if i%13==0 and i!=0:
            dataset[iter]=sector
            iter+=1
            sector=""
        if i == len(string)-1:
            dataset[iter]=sector
            sector=""
    return dataset        

    
def decompression(archive):
   
    probs = archive["p"]
    data = o_format(archive["c"])
   
    left = 0
    right = 1
    
    decompressed = ""
    alpha = ""
    while alpha!="!":
        location = get_location(probs, left, right)
        
        alpha = location_to_alpha(location, data)
        if alpha=="!":
            break
        decompressed+= alpha
        left = location[alpha][0]
        right = location[alpha][1]
        
    return decompressed
    

def long_compression(string):

    dataset=separator(string)
    compressed={}
    pure_data=""
    pure_prob=""
    for i in dataset:
        compressed[i]=compression(dataset[i])
        pure_data+=str(compressed[i]['c'])+","
        #Decimal("0.2").as_integer_ratio()
        pure_prob+=str(compressed[i]["p"])+"\n"
        pure_prob=pure_prob.replace("\"", "")
        pure_prob=pure_prob.replace("{", "")
        pure_prob=pure_prob.replace("}", "")
        pure_prob=pure_prob.replace("'", "")
        pure_prob=pure_prob.replace(":", "")
        pure_prob=pure_prob.replace(" ", "")
        pure_prob=pure_prob.replace("0.", "")
        pure_prob=pure_prob.replace(",", "")
    save(compressed, "full_info")  
    save(pure_data, "pure_data")
    save(pure_prob, "pure_prob")

def long_decompression(name):
    archive = load(f"{name}")
    
    res=""
    for i in range(len(archive)):
        res+=decompression(archive[f'{i}'])
    return res

if __name__=="__main__":#13 уникальных символов
    test = "hello world and everyone who wathes"
 
    long_compression(test)
    print(long_decompression("full_info.json"))
    
  
   