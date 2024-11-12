class Deque:
    class entry:
        def __init__(self,obj):
            self.ID=obj.ID
            self.obj=obj 
            self.prev=None
            self.next=None
    def __init__(self,cache_size):
        self.htbl={}# ID,entry
        self.head=None
        self.tail=None
        self.size=cache_size#cache_size
        self.used=0#used cache size

    def pushFirst(self,obj):#LRU-insert
        headEntry=self.head
        entry=self.entry(obj)
        if headEntry:
            headEntry.prev=entry
            entry.next=headEntry
        else:
            self.tail=entry
        self.head=entry
        self.htbl[entry.ID]=entry
        self.used+=obj.size

    
    def pushLast(self,obj):
        tailEntry=self.tail
        entry=self.entry(obj)
        if tailEntry:
            tailEntry.next=entry
            entry.prev=tailEntry    
        else:
            self.head=entry
        self.tail=entry
        self.htbl[entry.ID]=entry
        self.used+=obj.size

    def popFirst(self):
        entry=self.head
        self._remove(entry.ID)
        return entry.obj
    
    def popLast(self):
        entry=self.tail
        self._remove(entry.ID)
        return entry.obj
    

    def Last(self):
        if self.tail==None:#避免None.obj錯誤
            return None
        else:
            return self.tail.obj
    
    def First(self):
        if self.head==None:#避免None.obj錯誤
            return None
        else:
            return self.head.obj


    def _remove(self,ID):
        assert(ID in self)
        entry=self.htbl[ID]
        prevEntry=entry.prev
        nextEntry=entry.next

        if prevEntry:
            prevEntry.next=nextEntry
        else:
            self.head=nextEntry
        
        if nextEntry:
            nextEntry.prev=prevEntry
        else:
            self.tail=prevEntry
        
        del self.htbl[ID]
        self.used-=entry.obj.size
        return entry.obj


    # obj in cache
    def __contains__(self,ID):
        return ID in self.htbl
    
    #obj=cache[ID]
    def __getitem__(self,ID):
        return self.htbl[ID].obj

    #cache[ID]=obj       set or update
    def __setitem__(self,ID,obj):
        if ID in self:
            self._remove(ID)
        self.pushFirst(obj)
    #del cache[ID]
    def __delitem__(self, ID):
        self._remove(ID)

    
#===========================
    def DEBUG_ShowQueue(self):#把queue中的所有元素逐個print出[prev , curr , next]
        curr=self.head
        que=[]
        result=["\nprev , curr , next "]
        while(curr):
            que.append(curr.ID)
            temp=[]
            temp.append(curr.prev.ID if curr.prev else curr.prev)
            temp.append(curr.ID)
            temp.append(curr.next.ID if curr.next else curr.next)
            result.append(temp)
            curr=curr.next
        for s in result:
            print(s)
        return que




class my_obj:
    def __init__(self,ID,size=0):
        self.ID=ID
        self.size=size
if __name__=="__main__":
    queue=Deque(20)
    req=[1,2,3,4,5,6]

    for i in req:
        queue.pushLast(my_obj(i,1))
    que=queue.DEBUG_ShowQueue()
    print("queue:",que)
    print("head: ",queue.head.ID)
    print("tail: ",queue.tail.ID)
    print("used: ",queue.used)

    print("===after pop===")
    queue.popFirst()
    queue.popFirst()
    queue.popLast()
    queue[5]=queue[5]
    queue[6]=my_obj(6)
    # queue[5]=my_obj(5)
    que=queue.DEBUG_ShowQueue()
    print("queue:",que)
    print("used: ",queue.used)

    print("head: ",queue.head.ID)
    print("tail: ",queue.tail.ID)
