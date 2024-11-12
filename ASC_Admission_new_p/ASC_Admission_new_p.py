from Deque import Deque
import numpy as np

class window_deque(Deque):
    def __init__(self, cache_size):
        super().__init__(cache_size)
        self.freq={}

    def pushFirst(self,obj):
        headEntry=self.head
        entry=self.entry(obj)
        if headEntry:
            headEntry.prev=entry
            entry.next=headEntry
        else:
            self.tail=entry
        self.head=entry
        self.used+=obj.size

        # update freq
        self.freq[obj.ID]=self.freq.get(obj.ID,0) + 1

    
    def popLast(self):
        entry=self.tail
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

        self.used-=entry.obj.size
        # update freq
        self.freq[entry.ID]-=1
        if self.freq[entry.ID]==0:
            del self.freq[entry.ID]


    def get_freq(self,Obj):
        return self.freq.get(Obj.ID,0)



class ASC_Admission_new_p:
    #改寫Deque 加上cache.size , cache.used
    class entry:
        def __init__(self,ID,size):
            self.ID=ID
            self.size=size
            self.admit_tag=False
            self.hit_tag=False


    def __init__(self,cache_size,c,delta):
        self.cache=Deque(cache_size)#用來記錄cache.size
        self.history=Deque(cache_size)
        

        self.window_size=10
        self.window=window_deque(cache_size*self.window_size)

        


        self.c=c
        self.delta=delta
        
        self.DEBUG_reqCount=0
        self.DEBUG_HitCount=0
        self.DEBUG_Admit=0
        self.DEBUG_noAdmit=0
        self.DEBUG_evictCount=0
        self.DEBUG_c_up=0
        self.DEBUG_c_down=0
        self.DEBUG_s1=0
        self.DEBUG_s2=0
        self.DEBUG_s3=0        
        self.DEBUG_g1=0
        self.DEBUG_g2=0
        self.DEBUG_g3=0
        self.DEBUG_g4=0


    def DEBUG(self):
        hit_rate=round(100*self.DEBUG_HitCount/self.DEBUG_reqCount,2)
        s="  cache-used:  "+str(self.cache.used)\
            +"  req_num:  "+str(self.DEBUG_reqCount)\
            +"  hit_num:  "+str(self.DEBUG_HitCount)\
            +"  hit_rate:  "+str(hit_rate)\
            +"  evictCount:  "+str(self.DEBUG_evictCount)\
            +"  Admit:  "+str(self.DEBUG_Admit)\
            +"  noAdmit:  "+str(self.DEBUG_noAdmit)\
            +"  c:  "+str(self.c)\
            +"  c_up:  "+str(self.DEBUG_c_up)\
            +"  c_down:  "+str(self.DEBUG_c_down)\
            +"  s1/s2/s3:  "+str(self.DEBUG_s1)+" / "+str(self.DEBUG_s2)+" / "+str(self.DEBUG_s3)\
            +"  g1/g2/g3/g4:  "+str(self.DEBUG_g1)+" / "+str(self.DEBUG_g2)+" / "+str(self.DEBUG_g3)+" / "+str(self.DEBUG_g4)\
            +"  window_size:  "+str(self.window_size)\
            +"  window_used:  "+str(round(self.window.used/self.window.size,2))
            # +"  window_used:  "+str(round(self.window.used/self.window.size,2))+" "+str(self.window.used)
            
        return s

# ===========================================================

    def update_window(self,obj):
        #清空間
        while(self.window.size < obj.size + self.window.used):
            self.window.popLast()
        #放入
        self.window.pushFirst(obj)
        

    def admit(self,O_i):
        self.DEBUG_Admit+=1
        O_i.admit_tag=True
        O_i.hit_tag=False
        cache=self.cache
        #清空間
        while(cache.size < O_i.size + cache.used):
            O_e=self.cache.popLast()
            self.evict(O_e)
        #放入cache
        cache.pushFirst(O_i)


    def not_admit(self,O_i):
        self.DEBUG_noAdmit+=1
        O_i.admit_tag=False
        O_i.hit_tag=False
        O_e=O_i
        self.evict(O_e)


    def evict(self,O_e):
        H=self.history
        # 調整c值
        if O_e.admit_tag==True:
            if O_e.hit_tag==False:
                # self.c=self.c-self.delta 若不做限制 c小於會全部准入
                self.c=max(self.c-self.delta , self.delta)
                self.DEBUG_c_down+=1
        else:
            if O_e.ID in H:
                self.c=self.c+self.delta
                self.DEBUG_c_up+=1       
        # 放入H
        if O_e.ID in H:
            del H[O_e.ID]
        while(H.size<O_e.size+H.used):#如果H滿了則清空間
            H.popLast()
        H[O_e.ID]=O_e        

# =================================================
    def request(self,ID,size):
        self.DEBUG_reqCount+=1
        cache=self.cache
        H=self.history
        O_i=cache[ID] if ID in cache else self.entry(ID,size)
        self.update_window(O_i)
        last_obj=cache.Last() if cache.Last()!=None else O_i #例外狀況

        # not hit
        if not (O_i.ID in cache):

            if O_i.size<self.c:
                self.admit(O_i)
            else:

                if self.window.get_freq(O_i)>self.window.get_freq(last_obj):
                    self.DEBUG_g1+=1
                else:
                    self.DEBUG_g2+=1

                if O_i.size<last_obj.size:
                    self.DEBUG_g3+=1
                else:
                    self.DEBUG_g4+=1


                # admit
                if self.window.get_freq(O_i)>self.window.get_freq(last_obj)  and  O_i.size<last_obj.size:
                    self.admit(O_i)
                    self.DEBUG_s1+=1
                # not admit
                elif self.window.get_freq(O_i)<self.window.get_freq(last_obj)  and  O_i.size>last_obj.size:
                    self.not_admit(O_i) 
                    self.DEBUG_s2+=1
                #原始
                else: 
                    p=np.exp(-O_i.size/self.c)
                    r=np.random.rand()
                    if p<=r:
                        self.not_admit(O_i)
                    else:
                        self.admit(O_i)
                    self.DEBUG_s3+=1
                
        else: #hit
            self.DEBUG_HitCount+=1
            O_i.hit_tag=True
            cache[O_i.ID]=O_i
            # if O_i.ID in H:
            #     del H[O_i.ID]
        # if O_i.ID in H:#會導致H O_e.ID in H永遠是false   改到
        #     del H[O_i.ID]


