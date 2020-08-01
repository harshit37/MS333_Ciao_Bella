plate = list(input())

def jugaad(plate):
    if(plate[0]=="q"):
        plate = plate[1:]
    length_plt = len(plate)
   # print(district)
    for i in range(2):
        if(plate[i]=="2"):
            plate[i] = "Z"
        elif(plate[i]=="6"):
            plate[i] = "G"
        elif(plate[i]=="1"):
            plate[i] = "J"
        elif(plate[i]=="€"):
            plate[i] = "E"
        elif(plate[i]=="¥"):
            plate[i] = "V"
    if(plate[2]=='S'):
        plate[2] = '5'
    elif(plate[2]=='O'):
        plate[2] = '0'
    elif(plate[2]=='B' or plate[2]=='R'):
        plate[2] = "8"
       # print(district[2])
    if(plate[3]=='S'):
        plate[3] = '5'
    elif(plate[3]=="O"):
        plate[3] = 0
    elif(plate[3]=='B' or plate[3]=='R'):
        plate[3] = '8'  
    for i in range(length_plt-8):
        if(plate[i+4]=="2"):
            plate[i+4] = "Z"
        elif(plate[i+4]=="6"):
            plate[i+4] = "G"
        elif(plate[i+4]=="1"):
            plate[i+4] = "J"
        elif(plate[i+4]=="€"):
            plate[i+4] = "E"
        elif(plate[i+4]=="¥"):
            plate[i+4] = "V"
    for i in range(4):
        if(plate[length_plt-4+i]=='S'):
            plate[length_plt-4+i] = '5'
        elif(plate[length_plt-4+i]=='O'):
            plate[length_plt-4+i] = '0'
        elif(plate[length_plt-4+i]=='B' or plate[length_plt-4+i]=='R'):
            plate[length_plt-4+i] = "8"
    return plate

print(*jugaad(plate), sep="")
