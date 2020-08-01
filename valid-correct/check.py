import location

def is_valid(number_plate):
    valid = False
    number_plate_size = len(number_plate)
    i = 2
    digit = 0
    city_code = ""
    state_code = number_plate[0:2]
    
    for y in location.state:
        if (state_code==y):
            valid = True

    if(valid):
        while(48<=ord(number_plate[i])<=57 and i<number_plate_size):
            digit+=1
            city_code += number_plate[i]
            i+=1
        if(digit>2 or (digit==1 and (not(state_code=="DL" or state_code=="GJ")))):
            return False
    else:
        return False
    
    if(digit==1):
        if(not(state_code=="DL" or state_code=="GJ")):
            return False
    else:
        if(not(location.state[state_code].count(int(city_code)))):
            return False
    
    while(65<=ord(number_plate[i])<=90):
        i+=1
    
    if(len(number_plate[i:number_plate_size])!=4):
        return False

    for alph in number_plate[i:number_plate_size]:
        if(not(48<=ord(alph)<=57)):
            return False
    
    return True, location.state_detect[state_code]
    

print(is_valid("GJ19A3696"))