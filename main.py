#-*- coding: UTF-8 -*-
import pickle
import os
import numpy as np
from SVD_search import svd
from Bsets_search import bsets
from Kernel_perceptron import *


class Acount(object):
    def __init__(self):
        '''
        !!!!!每次用户登录以后要初始化的东西
        还需要传进来一个用户id之类的参数，根据这个读取用户数据
        因为我本地测试下，就没加
        '''
        # 如果用户刚注册  self.M = []
        # 如果用户数据已经存在 self.M = load(保存的用户信息数据库)
        print 'londing personal data'
        self.M = []
        self.target = []
        self.final_id = []
        self.k = None
        print 'loading ingredient_food_matrix_normalized matrix'
        path=os.path.abspath('ingredient_food_matrix_normalized.npy')
        print 'loading finished'
        self.data = np.load(path) 

    def input_ingre(self,str_ingredient):
        '''
        input string_ingre           a string passing from webpage 
        
        Format: using space to split ones and \'-\' to combine the multi-word-ingredient)
        '''

        ingredient_names=pickle.load(open("ingredients.p"))
        recipe_names=pickle.load(open("recipes.p"))
        
        ingredients_all = [i[28:] for i in ingredient_names]
        recipes_all = [n.split('/')[-1] for n in recipe_names]
    
        length_ingredients=len(ingredients_all)
        x_vector=[0]*length_ingredients

        ingredients_usr=str_ingredient.split(' ')
        numbers_ingredient=len(ingredients_usr)

        for i in range(numbers_ingredient):
            count=0
            l1=len(ingredients_usr[i].split('-'))
            for j in range(length_ingredients):
                l2=len(ingredients_all[j].split('-'))
                if ingredients_usr[i].split('-')[:l1]==ingredients_all[j].split('-')[:(l2)]:
                    count+=1
                    #print j,ingredients_all[j]
                    x_vector[j]=1
                    break
            if count==0:
                print('The ingredient [' +ingredients_usr[i] +'] does not exist in database')   
                  
        #print x_vector
        return x_vector


    def input_receipe(self,str_receipe):
        '''
        input string_ingre           a string passing from webpage 
        '''

        path=os.path.abspath('ingredient_food_matrix_binary.npy')
        a=np.load(path) 

        ingredient_names=pickle.load(open("ingredients.p"))
        recipe_names=pickle.load(open("recipes.p"))
        
        ingredients_all = [i[28:] for i in ingredient_names]
        recipes_all = [n.split('/')[-1] for n in recipe_names]
    
        length_ingredients=len(ingredients_all)
        x_vector=[0]*length_ingredients

        recipes_usr1=str_receipe.split('-')
        count=0
        for i in range(len(recipes_all)):
            l=len(recipes_all[i].split('-'))
            if recipes_usr1[:len(recipes_usr1)]==recipes_all[i].split('-')[:(l)]:
                x_vector=a[i]
                count+=1
                break
        print repr(recipes_usr1)
        if count==0: 
            print('The recipe [' + repr(recipes_usr1) + '] does not exist in database')

        #print x_vector
        return x_vector   



    def similar_receipe_for_ingre(self, x):
        '''
        input x      input ingredient list (1 for appearance and 0 else)
        output       a list of similar receipe id
        '''

        r1=svd(x,20)
        r2=bsets(x,20)
        if r1[0]!=r2[0]:
            recipe_final=r2[0:10]+r1[0:10]
        else: recipe_final=r2[1:11]+r1[1:11]
        
        #print recipe_final
        return recipe_final



    def similar_receipe_for_receipe(self, x):
        '''
        input x      ingredient list for an input recipe
        output       a list of similar receipe id
        '''
        r1=svd(x,11)
        r2=bsets(x,11)
        recipe_final=r2[1:11]+r1[1:11]
        #print recipe_final
        return recipe_final




############################################
    def recommend_ingredient(self,str):
        '''
        input str       ingredient list represented by string from user
        output recommand_id     final recommanded receipe: ten receipe id
        '''
        x = self.input_ingre(str)
        filtered_recipe = self.similar_receipe_for_ingre(x)

        self.k = Kernel_perceptron(self.M, self.data)
        self.final_id, self.target = self.k.predict(filtered_recipe)

        # 根据final_id 找到那10个receipe的名字 然后显示出来
        return self.final_id


    def recommend_recipe(self,str):
        '''
        input str       ingredient list represented by string from user
        output recommand_id     final recommanded receipe: ten receipe id
        '''
        x = self.input_receipe(str)
        filtered_recipe = self.similar_receipe_for_receipe(x)

        self.k = Kernel_perceptron(self.M, self.data)
        self.final_id, self.target = self.k.predict(filtered_recipe)


        # 根据final_id 找到那10个receipe的名字 然后显示出来
        return self.final_id


    def evaluate(self,feedback,num):
        '''
        input feedback      1 or -1 (depend on user's like or not)
              num           the number of 10 receipe
                            e.g num=2 we will know it is feedback to this receipe -> self.final_id[2]
        '''
        target = self.target[num]   # our prediction (1/-1)
        if target != feedback:
            receipe_id = self.final_id[num]
            mistake = np.append(self.data[receipe_id], feedback)
            mistake = mistake.reshape((1, mistake.shape[0]))
            if self.M == []:
                self.M = mistake
            else:
                self.M = np.concatenate((self.M, mistake), axis=0)


            # ！！！！
            # 每次更新 self.M 以后 都需要同时更新用户账号记录里该用户的M





if __name__ == '__main__':
    acount = Acount()
    '''
    #假设用户输入以下ingredient list
    ingre_str = 'pepper sweet-pepper onion garlic'
    out = acount.recommend_ingredient(ingre_str)
    print 'final 10:', out
    print 'predict:',acount.target
    #假设用户对10个结果中的第一个点了个like，对第三个点了like
    acount.evaluate(1,0)
    print acount.M.shape
    acount.evaluate(1,2)
    print acount.M.shape
    '''

    #假设用户输入以下receipe  
    receipe_str = 'black-eyed-peas-dip-113551' 
    out = acount.recommend_recipe(receipe_str)
    print 'final 10:', out
    print 'predict:',acount.target
    #假设用户对10个结果中的第一个点了个dislike，对第三个点了like
    acount.evaluate(-1,0)
    #print acount.M.shape
    acount.evaluate(1,2)
    #print acount.M.shape
    
 





