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
    #print(probs)
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
    if string=="":
        return
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
    #print(data)
    #print("location", list(location.values()))
    
    for i in range(length):
        
        left  = list(location.values())[i][0]
        right = list(location.values())[i][1]
        #print("iteration ",i, "left", left, "right", right, "data", data, "delta",right-left) 
        
        if left<data and right >data:
            #print("______returned list(location)[i]_____ ",list(location)[i])
            return list(location)[i]
        
            
def separator(string, count=8):#адаптивно менять count
    dataset = {}
    sector=""
    iter=0
    
    for i in range(len(string)):
        sector+=str(string[i])
        if i%count==0 and i!=0:
            dataset[iter]=sector
            iter+=1
            sector=""
        if i == len(string)-1:#ксли много не хватает - дополнять
            dataset[iter]=sector#+"1"*int((count-len(sector)-2)/1)
            sector=""
    return dataset        

    
def decompression(archive):
    #print("archive ",archive)
    probs = archive["p"]
    data = o_format(archive["c"])
    #print("probs ",probs)
   
   
    left = 0
    right = 1
    
    decompressed = ""
    alpha = ""
    while alpha!="!":
        location = get_location(probs, left, right)
       
        alpha = location_to_alpha(location, data)
        #print("alpha ",  alpha)
        if alpha==None:
            break
        if alpha=="!":
             break
        decompressed+= alpha
        left = location[str(alpha)][0]
        right = location[str(alpha)][1]
        #print(left, right)
        
    return decompressed
    
def unperiod(numb):
    num=numb
    num=str(num)
    num=num.replace("0.","")
    counter=0
    not_per=""
    for i in range(len(num)-1):
        if num[i+1]==num[i]:
            counter+=1
            if counter>=10:
                return f"{not_per}`{num[i]}"
        else:
            counter=0
            not_per = num[i]
    drob =1/numb
    return str(drob).replace(".0","")

def make_pure_prob(compressed):
        pure_prob=""
        for i in compressed['p']: 
            if str(i).isdigit():
                pure_prob+="%"+i+unperiod(compressed['p'][i])
            else:     
                pure_prob+=i+unperiod(compressed['p'][i])
        return pure_prob

def uncode_pure(path1, path2):
    pure_data= load(path1)
    compressed=[]
    pure_data = pure_data.split(sep=",")
    for data in pure_data:
        if data!="":
            compressed.append(data)
    pure_prob = load(path2)
    
    
    full_data={}
    stops = pure_prob.count("!")
    i=0
    for q in range(stops):
        value=""
        simb=""
        probs={"p":""}
        prob={}
        stop=0
        while stop!=1:
            
            simb=pure_prob[i]
            #print("now letter is ", simb)
            
            if simb.isalpha() or simb in"! ',/+.=:;%":
                if simb=="%":
                    simb=pure_prob[i+1]
                    i+=1
                    #print("found a digit ", simb)
                if value!="":
                    prob[key]=adapt_from_pure(value) 
                    value=""
                    #print("current value is ", value)
                    if key=="!" :
                        stop=1
                key = simb
             
            else:
                value+= simb
                #print("value has been plused", value)  
                  
            if i==len(pure_prob)-1:
                stop=1
                prob[key]=adapt_from_pure(value)     
            i+=1
            
        #print(prob)
        probs["p"]=prob
        probs["c"]=compressed[q]
        full_data[str(q)]=probs  
    save(full_data, "recovered_from_pure")        
    return full_data
    

def adapt_from_pure(value):
    if value.count("`")==0:
        return 1/float(value)
    elif len(value)==2:
        if value[1]!="6":
            return float("0."+value[1]*16+str(int(int(int(value[1])/5)+int(value[1]))))
        return float("0.0"+value[1]*16+str(int(int(value[1])/5+int(value[1]))))
    else:
        if value[0]!="6":
            return float("0."+str(value[0])+value[2]*16+str(int(int(value[2])/5+int(value[2]))))
        return float("0.0"+str(value[0])+value[2]*16+str(int(int(value[2])/5+int(value[2]))))
            
def long_compression(string):
       

    dataset=separator(string)
    compressed={}
    pure_data=""
    pure_prob=""
    for i in dataset:
        compressed[i]=compression(dataset[i])
        #print(compressed[i])
        if compressed[i]==None:
            break
        pure_data+=str(compressed[i]['c'])+","
        pure_prob+=make_pure_prob(compressed[i])
        
    save(compressed, "full_info")  
    save(pure_data, "pure_data")
    save(pure_prob, "pure_prob")

def long_decompression(name):
    archive = load(f"{name}")
    
    res=""
    for i in range(len(archive)):
        if archive[f'{i}']==None:
            break
        res+=decompression(archive[f'{i}'])
    return res


def lil_validator(str1, str2, str3):
    if  str1==str2 and str2 ==str3:
        print("correct")
    elif str2==str3: 
        print("compression with error")
    elif str1==str2:
        print("decompression from pure failked")
    elif str1==str3:
        print("full info decomp failed")

if __name__=="__main__":#15 уникальных символов a`3 -вероятность a 0.33333 f3 - 1/3
    test = "TWFuIGlzIGRpc3Rpbmd1aXNoZWQsIG5vdCBvbmx5IGJ5IGhpcyByZWFzb24sIGJ1dCBieSB0aGlzIHNpbmd1bGFyIHBhc3Npb24gZnJvbSBvdGhlciBhbmltYWxzLCB3aGljaCBpcyBhIGx1c3Qgb2YgdGhlIG1pbmQsIHRoYXQgYnkgYSBwZXJzZXZlcmFuY2Ugb2YgZGVsaWdodCBpbiB0aGUgY29udGludWVkIGFuZCBpbmRlZmF0aWdhYmxlIGdlbmVyYXRpb24gb2Yga25vd2xlZGdlLCBleGNlZWRzIHRoZSBzaG9ydCB2ZWhlbWVuY2Ugb2YgYW55IGNhcm5hbCBwbGVhc3VyZS4="
    long_compression(test)
    uncode_pure("pure_data.json", "pure_prob.json")
    print(long_decompression("full_info.json"))
    print(long_decompression("recovered_from_pure.json"))
    lil_validator(test,long_decompression("full_info.json"),long_decompression("recovered_from_pure.json"))
  
   