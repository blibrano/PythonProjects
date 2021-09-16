class minHeap:
    def __init__(self):
        self.array=[(0,0)]
        self.count=0

    def is_empty(self):
        if self.count==0:
            return True
        else:
            return False
        
    def swap(self,x,y,vertices):
        a,b=self.array[x]
        c,d=self.array[y]
        vertices[b],vertices[d]=vertices[d],vertices[b]
        self.array[x],self.array[y]=self.array[y],self.array[x]
        
    def rise(self,i,vertices):
        while (i//2 > 0):
            if(self.array[i] < self.array[i//2]):
                self.swap(i,(i//2),vertices)
            i=i//2

    def insert(self,key,value,vertices):
        item=(key,value)
        vertices[value]=self.count+1
        self.array.append(item)
        self.count=self.count+1
        self.rise(self.count,vertices)

    def sink(self,i,vertices):
        while (i*2) <= self.count:
            small_child=self.min_child(i)
            if self.array[i]> self.array[small_child] :
                self.swap(i,small_child,vertices)
            i=small_child

    def min_child(self,i):
        if ((i*2+1)>self.count):
            return i*2
        else:
            if self.array[i*2]<self.array[i*2+1]:
                return i*2
            else:
                return i*2+1

    def delMin(self,vertices):
        self.swap(1, self.count,vertices)
        x,y = self.array[self.count]
        vertices[y]=-1
        self.array.pop(self.count)
        self.count -= 1
        self.sink(1,vertices)
        return x,y

    def length(self):
        return self.count
        
if __name__ == "__main__":
    my_list = [[10,1],[9,3],[8,7],[7,5],[6,6],[5,2],[4,8],[3,9],[2,4],[1,10]]
    vertices= [-2 for i in range (11)]
    New=minHeap()
    New.insert(0,0,vertices)
    for i in range (len(my_list)):
        New.insert(my_list[i][0],my_list[i][1],vertices)
        #print(vertices)
    print (New.array)
    print(vertices)
    New.delMin(vertices)
    print (New.array)
    print(vertices)
   
    
    

