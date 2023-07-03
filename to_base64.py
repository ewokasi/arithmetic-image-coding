import base64
import alg_source

def to_64(path):
    with open(path, "rb") as image_file:
        encoded_string = str(base64.b64encode(image_file.read()))
        #print (encoded_string)
        return encoded_string
    

if  __name__=="__main__":
    test = to_64("test.png")
    alg_source.long_compression(test)
    full = alg_source.long_decompression("full_info.json")
    alg_source.uncode_pure("pure_data.json", "pure_prob.json")
    res = alg_source.long_decompression("recovered_from_pure.json")
    print (test,"\n\n",res)
    png_recovered =base64.b64decode(test)
    f = open("temp.png", "w")
    f.write(png_recovered)
    f.close()