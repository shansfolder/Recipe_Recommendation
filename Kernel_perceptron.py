import numpy as np 

def bubbleSort(A,B):
    '''
    sort the instances with their distances to the hyperplane
    I am using a modified quick sort algorithm for our problem

    such that the sequence of receipe id are also changed according to the predition.
    '''
    last_i = len(A)-1
    for i in xrange(last_i):        # outer loop
        in_sort = True
        for j in xrange(last_i-i):  # inner loop(last i elements are already biggest)
            if A[j] > A[j+1]:
                A[j],A[j+1] = A[j+1],A[j]
                B[j],B[j+1] = B[j+1],B[j]
                in_sort = False
        if in_sort:
            # print 'already sorted'
            break
        # print 'sequence after one pass through: ', A


def quick_sort(dist, target, start, end):
    '''
    sort the instances with their distances to the hyperplane
    I am using a modified quick sort algorithm for our problem

    such that the sequence of receipe id are also changed according to the predition.
    '''
    if start < end:
        mid = partition(dist, target, start, end)
        quick_sort(dist, target, start, mid-1)
        quick_sort(dist, target, mid+1, end)


def partition(dist, target, start, end):
    '''
    Partition the array into two parts
    All of one part is smaller than the other part.

    dist            the array to be sorted
    target          sorted wrt. the sequence of dist 
    start, end      index of the start/end of array'''

    # select a point, e.g. last element in array
    point = dist[end]
    left_i = start
    # move all elements smaller than "point" to the left
    for i in xrange(start, (end+1)):
        if dist[i] <= point:
            dist[i], dist[left_i] = dist[left_i], dist[i]
            target[i], target[left_i] = target[left_i], target[i]
            left_i += 1
    # return the index of left part
    left_end = left_i-1
    return left_end





class Kernel_perceptron(object):
    def __init__(self, M, data):
        self.M = M    
        self.data = data     

    def predict(self, receipe_id):
        '''
        input receipe_id     a list of id to be evaluated
        output final_id      a list of id that user likes most
               target        prediction of these receipes
        '''
        predict_value = [0 for i in xrange(len(receipe_id))]
        for i,id in enumerate(receipe_id):
            tmp = 0.
            x_star = self.data[id]
            for mistake in self.M:
                x = mistake[:-1]
                y = mistake[-1]
                tmp += y * self.kernel(x,x_star)
            predict_value[i] = tmp
        
        bubbleSort(predict_value, receipe_id)
        # 8 most possible like to ensure exploitation
        # and 2 possible dislike to ensure exploration
        final_id = receipe_id[:2] + receipe_id[12:] 
        target = list (np.sign(predict_value[:2]+predict_value[12:]))
        final_id.reverse()
        target.reverse()
        for i in xrange(10):
            if target[i] == 0:
                target[i] = -1

        return final_id, target
    
    def kernel(self, a, b):
        coef = 1000.
        kernel = ( np.dot(a,b.T)+coef ) **2
        #print kernel
        return kernel


