
from ASC_Admission_new_p import ASC_Admission_new_p
from ASC_Admission import ASC_Admission



def run_ASC_Admission_new_p():
    c=20000
    delta=200

    cache_size=21990232555 #2.56GB  512GB*0.005 = 512 * 2^30 * 8 * 0.005
    # cache_size=43980465111 #5.12GB  512GB*0.01 = 512 * 2^30 * 8 * 0.01
    # cache_size=219902325555 #25.6GB 512GB*0.05 = 512 * 2^30 * 8 * 0.05
    # cache_size=439804651110 #51.2GB 512GB*0.1 = 512 * 2^30 * 8 * 0.1
    
    
    DEBUG_reqCount=0
    trace="D:/all_Trace/ASC-IP/raw_trace/wiki2018.tr"
    # cache_size=2748779069 # 512GB*0.005= 2.56GB 以Byte為單位
    policy=ASC_Admission_new_p(cache_size,c,delta)
    with open(trace,'r') as f:
        for line in f:
            temp=line.split()
            ID=int(temp[1])
            size=int(temp[2])
            if size>cache_size:
                print("object bigger then cache!  used-cache:",policy.cache.used,"  obj_size:  ",size)

            policy.request(ID,size)
            DEBUG_reqCount+=1


            if not DEBUG_reqCount%1000000:
                s="ASC_Admission_new_p "\
                    +"  cache_size: "+str(cache_size)\
                    +"  req_num:  "+str(DEBUG_reqCount)\
                    +policy.DEBUG()
                print(s)

            # print(policy.DEBUG_HitCount)
            #第560000000個req結束後，重置reqCount,HitCount    
            # if DEBUG_reqCount==560000000:
            #     policy.DEBUG_reqCount=0
            #     policy.DEBUG_HitCount=0           

def run_ASC_Admission():
    c=20000
    delta=200

    cache_size=21990232555 #2.56GB  512GB*0.005 = 512 * 2^30 * 8 * 0.005
    # cache_size=43980465111 #5.12GB  512GB*0.01 = 512 * 2^30 * 8 * 0.01
    # cache_size=219902325555 #25.6GB 512GB*0.05 = 512 * 2^30 * 8 * 0.05
    # cache_size=439804651110 #51.2GB 512GB*0.1 = 512 * 2^30 * 8 * 0.1
    
    
    DEBUG_reqCount=0
    trace="D:/all_Trace/ASC-IP/raw_trace/wiki2018.tr"
    # cache_size=2748779069 # 512GB*0.005= 2.56GB 以Byte為單位
    policy=ASC_Admission(cache_size,c,delta)
    with open(trace,'r') as f:
        for line in f:
            temp=line.split()
            ID=int(temp[1])
            size=int(temp[2])
            if size>cache_size:
                print("object bigger then cache!  used-cache:",policy.cache.used,"  obj_size:  ",size)

            policy.request(ID,size)
            DEBUG_reqCount+=1


            if not DEBUG_reqCount%1000000:
                s="ASC_Admission_new_p "\
                    +"  cache_size: "+str(cache_size)\
                    +"  req_num:  "+str(DEBUG_reqCount)\
                    +policy.DEBUG()
                print(s)

            # print(policy.DEBUG_HitCount)
            #第560000000個req結束後，重置reqCount,HitCount    
            # if DEBUG_reqCount==560000000:
            #     policy.DEBUG_reqCount=0
            #     policy.DEBUG_HitCount=0    


if __name__=="__main__":
    run_ASC_Admission()
    # run_ASC_Admission_new_p()