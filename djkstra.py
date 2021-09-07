'''
This project is the implementation of Djkstra algorithm, to find the best path given certain conditions.
'''
class minHeap:
    def __init__(self):
        '''
        Initialises the main array and set counter to count how many vertexes there are
        
        @precondition: None
        @postcondition: None
        @return: None
        '''
        self.array=[(0,0)]
        self.count=0

    def is_empty(self):
        '''
        Checks if the MinHeap array is empty
        
        @precondition: None
        @postcondition: None
        @return: True/False
        '''
        if self.count==0:
            return True
        else:
            return False
        
    def swap(self,x,y,vertices):
        '''
        Swaps contents of MinHeap array and vertices between 2 vertexes
        
        @param -> x: targeted index 1
        @param -> y: targeted index 2
        @param -> vertices: passed on list vertices
        @precondition: None
        @postcondition: None
        @return: None
        '''
        a,b=self.array[x]
        c,d=self.array[y]
        vertices[b],vertices[d]=vertices[d],vertices[b]
        self.array[x],self.array[y]=self.array[y],self.array[x]
        
    def rise(self,i,vertices):
        '''
        Checks if node is smaller then child and swaps

        @param -> i: targeted index
        @param -> vertices: passed on list vertices
        @precondition: None
        @postcondition: None
        @return: None
        '''
        while (i//2 > 0):
            if(self.array[i] < self.array[i//2]):
                self.swap(i,(i//2),vertices)
            i=i//2

    def insert(self,key,value,vertices):
        '''
        Inserts new item into the heap and initialise vertices[vertex]to the count+1

        @param -> key: distance to vertex being passed
        @param -> value: vertex being passed
        @param -> vertices: passed on list vertices
        @precondition: None
        @postcondition: None
        @return: None
        '''
        item=(key,value)
        self.array.append(item)
        vertices[value]=self.count+1
        self.count=self.count+1
        self.rise(self.count,vertices)

    def sink(self,i,vertices):
        '''
        Re-sorts the heap once an item had been removed

        @param -> i: index being passed
        @param -> vertices: passed on list vertices
        @precondition: None
        @postcondition: None
        @return: None
        '''
        while (i*2) <= self.count:
            small_child=self.min_child(i)
            if self.array[i]> self.array[small_child] :
                self.swap(i,small_child,vertices)
            i=small_child

    def min_child(self,i):
        '''
        Finds smallest child in the heap

        @param -> i: index being passed
        @precondition: None
        @postcondition: None
        @return: the index of the smallest vertex 
        '''
        if ((i*2+1)>self.count):
            return i*2
        else:
            if self.array[i*2]<self.array[i*2+1]:
                return i*2
            else:
                return i*2+1

    def delMin(self,vertices):
        '''
        Removes smallest from the heap and initialises the vertices at that vertex to -1

        @param -> vertices: passed on list vertices
        @precondition: None
        @postcondition: None
        @return: the value of the removed vertex
        '''
        self.swap(1, self.count,vertices)
        x,y = self.array[self.count]
        vertices[y]=-1
        self.array.pop(self.count)
        self.count -= 1
        self.sink(1,vertices)
        return (x,y)

    def length(self):
        '''
        Finds current length of minheap
        
        @precondition: None
        @postcondition: None
        @return: the length of array
        '''
        return self.count
    
def readfile(filename):
    '''
    Reads File and splits contents

    @param -> filename: name of file to be read
    @precondition: None
    @postcondition: None
    @return: the contents of file in list form
    '''
    file = open(filename,"r")
    contents=file.read().splitlines()
    for i in range (len(contents)):
        contents[i]=contents[i].split()
    return contents

def adjacency_list(filename):
    '''
    Creates adjacency List from the file given

    @param -> filename: name of file to be read
    @precondition: None
    @postcondition: None
    @return: the adjacency list and the last vertex
    @complexity:O(N) where N is length of list
    '''
    data=readfile(filename)

    #finds the last vertex in the file
    max=0
    for i in range(len (data)):
        if int(data[i][1])>max:
            max=int(data[i][1])  
    List=[[] for i in range (max+1)]

    #appends the vertexes and its distance between the two to each possible start to end
    for i in range (len(data)):
        List[int(data[i][0])].append([int(data[i][1]),int(data[i][2])])
        List[int(data[i][1])].append([int(data[i][0]),int(data[i][2])])
        
    return List,max

def djikstra_algo(source):
    '''
    Finds minimal distance from source to every vertex

    @param -> source: The starting vertex
    @precondition: None
    @postcondition: None
    @return: finalized and previous list
    @timecomplexity: O (E log(V))
    '''
    my_list,max = adjacency_list('edges.txt')
    vertices= [-2 for i in range (max+1)]
    previous= [0 for i in range (max+1)]
    finalized=[]
    discovered=minHeap()

    #intialising first vertex with distance of zero
    discovered.insert(0,source,vertices)

    #while there are new paths found
    while discovered.is_empty()==False:

        #initializing main vertex
        distance,vertex=discovered.array[1]

        #for every other vertex the main vertex is connected to
        for i in range (len(my_list[vertex])):

            #if not vertex not discovered
            if vertices[my_list[vertex][i][0]]== -2:
                discovered.insert(distance+my_list[vertex][i][1],my_list[vertex][i][0],vertices)
                previous[my_list[vertex][i][0]]=vertex

            #if vertex is discovered
            elif vertices[my_list[vertex][i][0]]>= 0:
                x,y=discovered.array[vertices[my_list[vertex][i][0]]]
                if x > distance+my_list[vertex][i][1]:
                    discovered.array[vertices[my_list[vertex][i][0]]]= (distance+my_list[vertex][i][1],y)
                    previous[my_list[vertex][i][0]]=vertex

        #store the minimal vertices value into finalized
        minimal=discovered.delMin(vertices)
        finalized.append(minimal)
        
    return finalized,previous

def printing(source,target,previous,finalized):
    '''
    Prints the path from source to target

    @param -> source: The starting vertex
    @param -> target: The end vertex
    @param -> previous: The List that contains all the previous edges of all of the edges
    @param -> finalized: The list that contains the shortest distance to all other vertexes
    @precondition: None
    @postcondition: None
    @return: string that is going to be printed for task1
    '''
     #Read from customers.txt
    c_list=readfile('customers.txt')

     
    #Making C_List contain only values without customers
    for i in range (len(c_list)):
        c_list[i]=int(c_list[i][0])
        
    #Check if Source and Target is the same and is a customer
    if source==target:
        if source in c_list:
            return str(source)+' (C)'
        else:
            return str(source)

    #printing of discovered
    if target in c_list:
        string=str(target)+' (C)'
    else:
        string=str(target)
    current=previous[target]
    while current!= source:
        for i in range (len(finalized)):
            x,y=finalized[i]
            if y==current:
                if current in c_list:
                    string=str(y)+' (C)'+' --> '+string 
                else:
                    string=str(y)+' --> '+string
        current=previous[current]
    if source in c_list:
        string= str(source) +' (C)'+' --> '+ string
    else:
        string= str(source)+' --> '+ string
    return string

def dis(finalized,target):
    '''
    Find distance from source to targeted vertex
    
    @param -> finalized: The list that contains the shortest distance to all other vertexes
    @param -> target: The end vertex
    @precondition: None
    @postcondition: None
    @return: distance between source and target from finalized list
    '''
    for i in range (len(finalized)):
           x,y=finalized[i]
           if y==target:
               distance=x
               return distance
            
def customer(source,target,finalized,previous,finalized2,previous2):
    '''
    Gets customer list and searches the minimum distance that goes through at least one customer from source to target

    @param -> source: The starting vertex
    @param -> target: The end vertex
    @param -> previous: The List that contains all the previous edges of all of the edges of source
    @param -> finalized: The list that contains the shortest distance to all other vertexes of source
    @param -> previous2: The List that contains all the previous edges of all of the edges of target
    @param -> finalized2: The list that contains the shortest distance to all other vertexes of target
    @precondition: None
    @postcondition: None
    @return: minimum distance and string that is going to be printed for task2
    @timecomplexity: O (E log(V))
    '''
    #Read from customers.txt
    c_list=readfile('customers.txt')

    #Making C_List contain only values without customers
    for i in range (len(c_list)):
        c_list[i]=int(c_list[i][0])

    
    #initialising min and minc to the first item in C_list
    min=dis(finalized,c_list[0])+dis(finalized2,c_list[0])
    minc=c_list[0]
    #Discovering shortest distance between 2 points and a customer
    for i in range (1,len(c_list)-1):
        disc1=dis(finalized,c_list[i])
        disc2=dis(finalized2,c_list[i])

        #make sure that none existant connectionas are not included
        if disc1!=None:
            if disc2!=None:
                if disc1+disc2 < min:
                    min= disc1+disc2
                    minc=c_list[i]
    
    #Check if Source and Target is the same and is a customer
    if source==target:
        if source in c_list:
            return 0,str(source)+' (C)'
        
    #Creation of string1 from Source to before C

    #if source is a c return source directly
    if source==previous[minc]:
        if source in c_list:
            string1=str(source)+' (C)'
    elif source== minc:
            string1=''

    else:
        if previous[minc] in c_list:
            string1=str(previous[minc])+' (C)'
        else:
            string1=str(previous[minc])
        current=previous[previous[minc]]
        while current!= source:
            for i in range (len(finalized)):
                x,y=finalized[i]
                if y==current:
                    if current in c_list:
                        string1=str(y)+' (C)'+' --> '+string1 
                    else:
                        string1=str(y)+' --> '+string1
            current=previous[current]
        string1= str(source) +' --> '+ string1 + ' --> '

    #Creation of string2 from C to Target

    #if target is  minc then return target directly
    if minc==target:
        if target in c_list:
            return min,string1+str(target)+' (C)'
    else:
        string2=str(minc)+' (C)'
        current=previous2[minc]
        while current!= target:
            for i in range (len(finalized2)):
                x,y=finalized2[i]
                if y==current:
                    if current in c_list:
                        string2=string2+' --> '+str(y)+' (C)'
                    else:
                        string2=string2+' --> '+str(y)
            current=previous2[current]
        string2=string2+' --> '+ str(target)

        return min,string1+string2
       
if __name__ == "__main__":
    source=int(input("Enter source:"))
    target=int(input("Enter target:"))
    print()
    finalized,previous=djikstra_algo(source)
    distance=dis(finalized,target)
    print('Shortest Path and Distance: ')
    print(printing(source,target,previous,finalized))
    print ('Total route distance:',distance)
    finalized2,previous2=djikstra_algo(target)
    print()
    print('Minimum Detour Path and Distance: ')
    distance,path=customer(source,target,finalized,previous,finalized2,previous2)
    print(path)
    print('Total route distance:',distance)
    
    
