#BERNARD LIBRANO 28117158
import sys

'''
This project is the implementation of the suffix tree with the ukkonen's algorithm, that allows
the construction of the suffix tree be done in O(N) time. The resulting suffix tree is then used
for BWT transformation.
'''

class Node:
    index = -1  # if rule 2 then increase this index (used of rule 1 as a global counter)
    # starts with -1 because first index 0

    def __init__(self, newparent=None, start=None):
        self.children = [0 for x in range(256)]
        self.parent = newparent

        # application of trick 2 where we store indexes instead of characters
        self.start = start
        self.end = None

        #stores the suffix link
        self.suffixlink = None

    # if is not leaf node meaning, in between 2 other nodes then i return its current end
    # else i return the global counter
    def get_end(self):
        if self.end is None:
            return Node.index
        else:
            return self.end

    def get_start(self):
        return self.start

    def set_start(self, newstart):
        self.start = newstart

    def set_end(self, newend):
        self.end = newend

    def update_end(self):
        Node.index += 1

    def get_children(self):
        return self.children

    def set_children(self, index, newnode):
        self.children[index] = newnode

    def set_parent(self, newparent):
        self.parent = newparent

    def get_parent(self):
        return self.parent

    def set_suffixlink(self, newlink):
        self.suffixlink = newlink

    def get_suffixlink(self):
        return self.suffixlink

def Ukkonen(filename):
    string = readfile(filename)
    string += "$"

    root=Node()
    i=0
    j=0
    while i < len(string):

        #Rule 2
        #intialisation of previous node and previous offset
        previous_node = None

        #dis tracks how much path traveled
        prev_dis=0

        while j < i:
            #gets the length from i to j
            act_length = i - j + 1

            #make the character at j the current node
            current_node = root.get_children()[ord(string[j])]

            #skip counts and get the active node, dis is used to track how many characters the active length skips
            if previous_node is not None and previous_node.get_suffixlink() is not None:
                current_node, offset, dis = search_active(previous_node.get_suffixlink(), act_length - dis, string,j + dis,dis)  # a recursion function that finds the active_node
            else:
                current_node, offset, dis = search_active(current_node,act_length,string,j) #a recursion function that finds the active_node

            #if character pattern existed before then breaks
            if string[current_node.get_start() + offset] == string[i]:
                break
            else:
                #adds new node in between and another link
                split(current_node,offset+current_node.get_start()-1,i,string)

                #stores the suffix link from previous node to the current node
                if previous_node is not None:
                    previous_node.set_suffixlink(current_node)
                    prev_dis = dis

            j = j + 1

        # if character never existed then create new node and applies rule 3 and trick 3 where if no need character do nothing
        if root.get_children()[ord(string[i])] == 0:
            newNode=Node(root,i)
            root.set_children(ord(string[i]),newNode)
            j = j + 1

        i= i + 1

        #rule 1 by applying trick 4 with the use of global variables
        root.update_end()

    return (bwt(root,string))

#Splits a Node into 3 different nodes
def split(current_root,start,pos_i,string):

    #check if the node is not the end letter
    if start != current_root.get_end():
        cur_start=current_root.get_start()
        cur_parent = current_root.get_parent()

        #create he new node that exists between the parent and the child node
        newNode = Node(cur_parent,cur_start)
        newNode.set_end(start)

        #change the parent's child to the newly created node
        cur_parent.set_children(ord(string[cur_start]), newNode)

        #set new starting value and parent of the current_node
        current_root.set_start(start+1)
        current_root.set_parent(newNode)

        #update the children of the new node
        newNode.set_children(ord(string[start + 1]), current_root)
    else:
        #the current root would be the node
        newNode=current_root

    #and the ext node will be linked to the newly created node
    ext_Node=Node(newNode,pos_i)
    newNode.set_children(ord(string[pos_i]),ext_Node)

#essentialy trick 1 where we jump nodes instead of every character to search for the active node
def search_active(node,length,string,j,dis=0):

    # Calculate the node length
    node_length= node.get_end() - node.get_start() + 1

    #Base Case when character is in node:
    if length <= node_length :
        return node, length - 1, dis
    else:
        #condition where next child does not exist
        if node.get_children()[ord(string[j+node_length])] == 0:
            return node, length -1,dis
        else:
            #condition where next child exists
            return search_active(node.get_children()[ord(string[j+node_length])], length - node_length,string,j + node_length,dis + node_length)

def bwt(newnode,inp):

    #usage of list as list is immutable
    suffixends=[]

    #count amount of skips done to reach leaf
    skip = 0

    #initialise the node
    node = newnode

    #run the function to find the bwt
    bwt_aux(node,skip,suffixends,inp)

    #convert list to string
    suffix_string=""
    for i in range (len(suffixends)):
        suffix_string+=suffixends[i]

    return suffix_string

def bwt_aux(node,skip,array,inp):
    #loops through every possible child
    for i in range(256):
        #initialises node to the child at that position
        new_node = node.get_children()[i]

        #ignores if none else searches for leaf
        if new_node != 0:

            #if is leaf condition
            if new_node.get_end() == len(inp)-1 :
                array.append(inp[new_node.get_start() - skip - 1])
            else:
                #else search deeper through recursion
                bwt_aux(new_node,skip+(new_node.get_end()-new_node.get_start()+1),array,inp)

def readfile(filename):
    #reads file contents and reverses it
    file = open(filename, "r")
    contents = file.read()
    return contents

def runfile():
    filename = sys.argv[1]
    file = open("output_bwt.txt","w")
    task = Ukkonen(filename)
    file.write(task)
    file.close()

runfile()
