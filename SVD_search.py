
def svd(x_vector,num):
    
    import numpy as np
    import os
    import scipy.sparse.linalg
    from scipy import linalg
    import pylab as pl
    
    def cos_similarity(vec1,vec2):
        dot_product=np.dot(vec1,vec2) 
        norm_vec1=linalg.norm(vec1)
        norm_vec2=linalg.norm(vec2)
        if norm_vec1*norm_vec2!=0:
            return(dot_product/(norm_vec1*norm_vec2))
        else: return 0
    
    class recipe:
        c=0.0
        ind=0
        def __init__(self,cosine_value,index):
            self.c=cosine_value
            self.ind=index
    
    path=os.path.abspath('ingredient_food_matrix_binary.npy')
    a=np.load(path)
    u,s,v=scipy.sparse.linalg.svds(a)

    S=linalg.diagsvd(s,len(u),len(v))
    S.resize(6,6)
    tar=np.dot(np.dot(x_vector,v.T),linalg.inv(S))
    #print(tar)

    cos=[0]*len(u)
    l=[0 for i in range(len(u))]

    for i in range(len(u)): 
        cos[i]=cos_similarity(tar,u[i,:])
        l[i]=recipe(cos[i],i)
  
        
    cos_sorted=sorted(l,key= lambda x:x.c,reverse=True)
    num_recipe=[0 for i in range(int(num)+1)]

    count=0
    while count<int(num)+1:
        num_recipe[count]=cos_sorted[count].ind
        #print cos_sorted[count].c
        count +=1
    
    #print num_recipe

    if __name__ =='__main__':
        ii=0
        pl.ylim=(-0.1,0.1)
        pl.xticks=(np.linspace(-0.1,0.1,100))
        while ii<int(num):
            r=np.random.randint(0,len(u))
            pl.plot(u[r,0],u[r,1],'ro')
            pl.plot(u[num_recipe[ii],0],u[num_recipe[ii],1],'g^')
            ii +=1

        pl.legend('RS',loc='upper left',numpoints=1)
        pl.annotate('input recipe', xy=(u[num_recipe[0],0],u[num_recipe[0],1])),
        pl.savefig('test.png')
        pl.show()
    
    return num_recipe    

     
  
