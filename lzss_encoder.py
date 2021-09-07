#Bernard Librano 28117158
'''
Perform lzss encoding given a string and to bit form.
'''
import sys
def z_box(new_string):

    # initialise z-array to the size of string
    array = [0] * len(new_string)

    # set Z1 to its value which is the length of string or 0
    array[0] = 0

    # initialise L and R
    l = 0
    r = 0

    # loop skips zero as we start from Z2
    for i in range(1, len(new_string)):

        # Case 1 if character found outside Z-box
        if i > r:
            count = 0

            # checks how many character match from the matched character
            while i + count < len(new_string) and new_string[count] == new_string[i + count]:
                # increment count
                count += 1

            # set new Z-value in Z[i]
            array[i] = count

            # update box boundary if there is a pattern
            if count > 0:
                l = i
                r = i + count - 1

        # if i <= r ( character inside Z-box)
        else:

            # prefix index paired
            index_prefix = i - l

            # remaining length of the box
            remain = r - i + 1

            # case 2a
            # if z within box
            if array[index_prefix] < remain:
                array[i] = array[index_prefix]

            # case 2b
            # if value is exactly the box then find new box
            elif array[index_prefix] == remain:
                new_r = r + 1
                while new_r < len(new_string) and new_string[new_r] == new_string[new_r - i]:
                    new_r += 1
                array[i] = new_r - i
                l = i
                r = new_r - 1


            else:
                # case 2c
                array[i] = remain
    return array

def elias(N):

    #N is a numbered string input
    #get the binary value of the number string
    bin_val = str(bin(N)[2:])

    #attach the current binary value to string
    string= bin_val

    while (len(bin_val)!=1):
        new_N = len(bin_val) - 1
        bin_val = str(bin(new_N)[2:])
        bin_val = "0"+bin_val[1:]
        string = str(bin_val) + string
    return string

def lzss(string,d,b):
    array=[]
    d_pointer=0
    b_pointer=b-1
    while b_pointer-(b - 1) < len(string):
        next_char = b_pointer - (b - 1)
        dict= d_pointer - (d - 1)
        temp_d = d
        if dict < 0:
            temp_d = d+dict
            dict = 0
        z= z_box(string[next_char:b_pointer+1]+"$"+string[dict:d_pointer]+string[next_char:b_pointer+1])
        z=z[b+1:len(z)-(b)]
        print(z)
        longest=1
        index = -1
        for i in range (len(z)):
            if z[i] >= longest:
                longest =z[i]
                index = i  #aaca$aacaaca
        if (longest < 3):
            longest = 1 #abc|ab ... (1,a),(1,b) ...
            array.append(["1",string[next_char:next_char+longest]])
        else:
            array.append(["0",temp_d-1-index,longest])
            print(temp_d,index,d_pointer)
        d_pointer += longest - 1 + 1
        b_pointer += longest
    return array

def encode(string,d,b):
    array = lzss(string,d,b)
    out=""
    for i in range(len(array)):
        if array[i][0] == "1":
            char_out=str(bin(ord(array[i][1]))[2:])
            char_out = "0"*(8-len(char_out)) + char_out
            out = out + "1" + char_out
        elif array[i][0]=="0":
            out = out + elias(array[i][1]) + elias(array[i][2])
    return out

def runfile():
  filename = sys.argv[1]
  d= sys.argv[2]
  b= sys.argv[3]
  string_file = open(filename, "r")
  string = string_file.read()
  string_file.close()
  file = open("output_lzss_encoder.txt", "w")
  task = encode(string,int(d),int(b))
  file.write(task)
  file.close()

#runfile()
print(lzss("aaaaaaaaaaaa",6,4))