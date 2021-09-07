#Bernard Librano 28117158
'''
Perform lzss decoding on the given generated bit string to get message back
'''
import sys
def lzssdecode(string,d,b):
    ret_val=""
    index= 0
    while index < len(string):
        if string[index] == "1":
            ret_val += str(chr(int(string[index+1:index+9],2)))
            index += 8
        else:
            value1,size = elias_decode(string[index:])
            index += size
            value2, size = elias_decode(string[index:])
            back = ret_val[-int(value1):]
            diff = int(value2)-int(value1)
            exceed = ret_val[:diff]
            ret_val+=back+exceed
            index += size
            index -=1
        index += 1
    return (ret_val)


def elias_decode(string):
    index = 0
    temp = string[index]
    readlen = 1 + int(temp, 2)
    count=1
    while temp[0] != "1":
        temp = "1" + temp[1:]
        index = index + readlen
        readlen = 1 + int(temp, 2)
        count += readlen
        temp = string[index:index+readlen]
    return(str(int(temp,2)),count)

def runfile():
  filename = sys.argv[1]
  d= sys.argv[2]
  b= sys.argv[3]
  string_file = open(filename, "r")
  string = string_file.read()
  string_file.close()
  file = open("output_lzss_decoder.txt", "w")
  task = lzssdecode(string,int(d),int(b))
  file.write(task)
  file.close()

#runfile()
#print(elias_decode("000100"))
