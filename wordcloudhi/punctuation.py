filename = "nofor.txt"
 
 
def remove_punc(data):
    punc = '''!()-[]{};:'"\,<>।/?@#$%^&*_~'''   # punctuations to be removed
    for i in data:  
        if i in punc:  
            data = data.replace(i, "") 
    return data
 
 
with open(filename,'r',encoding="utf-8") as f:
    data = f.read()
with open(filename,"w+",encoding="utf-8") as f:
    f.write(remove_punc(data))
