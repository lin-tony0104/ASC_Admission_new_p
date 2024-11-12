說明在 https://hackmd.io/KQdtLfUNTsy2OhmxYbzGjg
* 當 size<c 時 : 准入
* 當 size>=c 時:做以下判斷
    * (S1)當輸入obj比驅逐obj(size大且freq小) : 不准入
    * (S2)當輸入obj比驅逐obj(size小且freq大) : 准入
    * (S3)其餘 : 照原始准入條件(size小於c值准入、size大於c值，根據機率准入)


ASC-Admission命中率:x  
其餘設定與ASC-Admission一樣下
- window大小設為 cache_size*5  時，命中率為:x
- window大小設為 cache_size*10  時，命中率為:x
- window大小設為 cache_size*15  時，命中率為:x
- window大小設為 cache_size*20  時，命中率為:x
- window大小設為 cache_size*30  時，命中率為:x

