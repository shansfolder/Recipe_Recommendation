
def bsets(x_vector,num):
    
    import os
    import numpy as np
    
    path=os.path.abspath('ingredient_food_matrix_binary.npy')
    a=np.load(path)
    c=2
    N=1
    class recipe:
        s=0.0
        ind=0
        def __init__(self,score,index):
            self.s=score
            self.ind=index
    num_row,num_column=a.shape
    m=[0]*num_column
    for i in range(num_row):
        m=m+a[i,:]
    
    m=m/num_row
    alpha=c*m
    beta=c*(1-m)
    alpha_t=alpha+x_vector
    beta_t=beta+N-x_vector
    cons=0.0
    for i in range(num_column):
        cons=cons+(np.log(alpha[i]+beta[i])-np.log(alpha[i]+beta[i]+N)+np.log(beta_t[i])-np.log(beta[i]))
    
    q=np.log(alpha_t)-np.log(alpha)-np.log(beta_t)+np.log(beta)
    temp=cons+np.dot(a,q)
    
    temp1=[0]*num_row
    for i in range(num_row):
        temp1[i]=recipe(np.exp(temp[i]),i)    
    
    score=sorted(temp1,key=lambda x:x.s,reverse=True)
    
    num_recipe=[0]*int(num)
    for i in range(int(num)):
        num_recipe[i]=score[i].ind
        #print score[i].s
    
    #print num_recipe
    return num_recipe
