# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.auth.models import User
from models import *
import os
import uuid
import pickle
from main import *
import numpy as np

# SOLite3 


def index(request):
    return render_to_response('index.html', locals())


def ingredient(request):
    all_ingredients = Ingredient.objects.all()
    return render_to_response('ingredient.html', locals())

def recipe(request):
    all_recipes = Recipe.objects.all()
    return render_to_response('recipe.html', locals())


def recommend_ingredient(request):

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")

    ingredients = request.REQUEST.get('ingredients', '')
    ingredients = ingredients[:-1]

    #=====================================================
    user = request.user
    ua = User_account.objects.get(user=user)
    acount = Acount()
    M_path = ua.M_path
    if M_path == '[]':
        acount.M = []
    else:
        acount.M = np.load(M_path)
    ingre_str = ingredients     #'pepper sweet-pepper onion garlic'
    out = acount.recommend_ingredient(ingre_str)
    print 'final 10:', out
    print 'predict:',acount.target
    ua.final_id = str(out)
    ua.target = str(acount.target)
    ua.save()
    #=====================================================

    recipes = ['a' for i in xrange(10)]
    for i, out_id in enumerate(out):
        recipes[i] = Recipe.objects.all()[out_id]
        #recipes[i] = Recipe.objects.get(id=out_id)

    res = []
    for r in recipes:
        e = r.evaluate(request.user)
        res.append((r, e))
    return render_to_response('recommend.html', locals())


def recommend_recipe(request):

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")

    recipe = request.REQUEST.get('recipe', '')
    #recipe = recipe.replace(" ", "-")

    #=====================================================
    user = request.user
    ua = User_account.objects.get(user=user)
    acount = Acount()
    M_path = ua.M_path
    if M_path == '[]':
        acount.M = []
    else:
        acount.M = np.load(M_path)
    receipe_str = recipe      #'black-eyed-peas-dip'
    out = acount.recommend_recipe(receipe_str)
    print 'final 10:', out
    print 'predict:',acount.target
    ua.final_id = str(out)
    ua.target = str(acount.target)
    ua.save()
    #=====================================================
    recipes = ['a' for i in xrange(10)]
    for i, out_id in enumerate(out):
        recipes[i] = Recipe.objects.all()[out_id]
        #print recipes[i].name
           
    res = []
    for r in recipes:
        e = r.evaluate(request.user)
        res.append((r, e))
    return render_to_response('recommend.html', locals())


def evaluate(request):

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")

    user = request.user
    recipe_id = request.REQUEST.get('recipe_id', '')
    evaluate = request.REQUEST.get('evaluate', '')
    sn = request.REQUEST.get('sn', '')
    sn = int(sn)
    recipe = Recipe.objects.get(id=recipe_id)
    e = Evaluate()
    e.user = user
    e.recipe = recipe
    e.evaluate = evaluate
    e.save()
    #=================================================
    user = request.user
    ua = User_account.objects.get(user=user)
    acount = Acount()
    M_path = ua.M_path
    if M_path == '[]':
        acount.M = []
    else:
        acount.M = np.load(M_path)
    acount.final_id = eval(ua.final_id)
    acount.target = eval(ua.target)
    if evaluate == "Like":
        acount.evaluate(1,sn)
    else:
        acount.evaluate(-1,sn)
    M_path = "data/" + user.username
    if acount.M != []:
        np.save(M_path, acount.M)
        ua.M_path = M_path + ".npy"
    else:
        ua.M_path = "[]" 
    ua.save()

    #=================================================

    return HttpResponse("I %s it" % evaluate)


def load_data(request):
    Ingredient.objects.all().delete()
    Recipe.objects.all().delete()

    ingredient_names = pickle.load(open("ingredients.p"))
    recipe_names = pickle.load(open("recipes.p"))
    ingredients_all_name = [i[28:] for i in ingredient_names]
    recipes_all_name = [n.split('/')[-1] for n in recipe_names]

    print len(ingredients_all_name) , len(recipes_all_name)

    for name in ingredients_all_name:
        ingredient = Ingredient()
        ingredient.name = name
        ingredient.save()

    for i in xrange(len(recipes_all_name)):
        recipe = Recipe()
        recipe.name =  recipes_all_name[i]
        recipe.link = recipe_names[i]
        recipe.save()

    return HttpResponse("OK!")



#====================auth system=========================================
def reg_page(request):
    return render_to_response('reg.html', locals())

def reg(request):
    username = request.REQUEST.get('username', '')
    password1 = request.REQUEST.get('password1', '')
    password2 = request.REQUEST.get('password2', '')
    if password1 != password2:
        return HttpResponse("<script>alert('Two passwords are not the same, Please try again.');top.location='/'</script>")
    if User.objects.filter(username = username):
        return HttpResponse("<script>alert('The user is already exist, Please try other username.');top.location='/'</script>")
    u = User()
    u.username = username
    u.set_password(password1)
    u.save()

    ua = User_account()
    ua.user = u
    ua.M_path = "[]"
    ua.save()

    return HttpResponse("<script>alert('Successful registration!');top.location='/'</script>")

def login_page(request):
    return render_to_response('login.html', locals())

def login(request):
    username = request.REQUEST.get('username', '')
    password = request.REQUEST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
    else:
        return HttpResponse("<script>alert('The password is incorrect');top.location='/'</script>")
    return HttpResponseRedirect("/")

def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
    return HttpResponseRedirect("/")
#======================================================================
