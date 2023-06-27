import json

def get_probs(string):
    if string=="" or string ==None:
        print("The input string is None or empty")
        return 0
    string+="!"
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
    print(start, end)
    start = str(start)
    end = str(end)
    res = ""
    for i in range(2,len(start)):

        if start[i]==end[i]:
            res+=start[i]
        else:
            print("sss",start[i])
            if int(end[i])-int (start[i])>=1:
                res+=str(int(start[i])+1)
                break
    print(res)
    print(start, end)
    return res


def compression(string):
    probs= get_probs(string)
    string+="!"
    #probs ={"a":0.6, "b":0.2,"c":0.1, "!":0.1}
    location = get_location(probs)
    left = 0
    right = 1

    for alpha in string:
        print("iteration", alpha)
        left = location[alpha][0]
        right = location[alpha][1]
        location = get_location(probs, left, right)
        print("calcs" ,location)
      
    compressed = select(left, right)
    print("select" ,compressed)
    archive ={}
    archive['probs']=probs
    archive['compressed']=compressed
    save(archive, "test")

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
        print("iteration ",i, "left", left, "right", right, "data", data)
        if left<=data and right >=data:
            print("________________returned_________ ", list(location)[i])
            return list(location)[i]
        
            

    
def decompression(name):
    archive = load(f"{name}")
    probs = archive["probs"]
    data = o_format(archive["compressed"])
   
    left = 0
    right = 1
    location = get_location(probs, left, right)
    decompressed = ""
    alpha = location_to_alpha(location, data)
    while alpha!="!":
        decompressed+= alpha
        left = location[alpha][0]
        right = location[alpha][1]
        location = get_location(probs, left, right)
        
        alpha = location_to_alpha(location, data)
    return decompressed
    
if __name__=="__main__":
    test = "hello world everyone"
    print(get_probs(test))
    compression(test)
    print(decompression("test.json"))
    
  
   