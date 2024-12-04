from django.shortcuts import render
from django.http import HttpResponse,HttpRequest,JsonResponse
from collections import Counter
import json
from random import Random
import datetime,time
w_n = Random(str(datetime.datetime.fromtimestamp(time.time()).date()))
with open('./home/WORDS.txt','r') as file:
    # print(w_n.randint(0,3102)*5)
    file.seek(w_n.randint(0,3102)*6,0)
    todays_word = file.readline().upper()

print(todays_word)
COLOURS = ('black','#656565','#2cf643','#c6ff1b')


# Create your views here.
def home(request : HttpRequest):
    words = request.COOKIES.get('words','')
    col = request.COOKIES.get('colour',','.join('black' for i in range(30)))
    win = request.COOKIES.get('win','0')
    col = col.split(',')
     
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            inputText = data.get('inputText','')
            if inputText:
                if len(inputText) == 5:
                    ma = word_match(inputText,todays_word)
                    for i in range(len(words),len(words)+5):
                        col[i] = COLOURS[ma[i-len(words)]]
                    
                    if check_win(ma):
                        win = '1'

                    words += inputText
        except json.JSONDecodeError:
            print("Invalid JSON")
            

            
        
    reponse = render(request,'page.html',{'lett':[[words[i+(j*5)] if i+(j*5) < len(words) else '' for i in range(5)] for j in range(6)],'col':col,'win':win})
    reponse.set_cookie('words',words,expires=datetime.datetime.fromtimestamp(time.time()+3600*24).date())
    reponse.set_cookie('colour',','.join(col),expires=datetime.datetime.fromtimestamp(time.time()+3600*24).date())
    reponse.set_cookie('win',win,expires=datetime.datetime.fromtimestamp(time.time()+3600*24).date())
    return reponse

def word_match(s1,s2):
    colour = [1,1,1,1,1]
    s2_c = Counter(s2)
    for i in range(5):
        if s1[i] == s2[i]:
            colour[i] = 2
            s2_c[s1[i]] -= 1
            if s2_c[s1[i]] == 0:
                s2_c.pop(s1[i])
    for i in range(5):
        if s1[i] != s2[i]:
            if s1[i] in s2_c:
                colour[i] = 3
                s2_c[s1[i]] -= 1
                if s2_c[s1[i]] == 0:
                    s2_c.pop(s1[i])
    
    return colour

def check_win(ma):
    for i in ma:
        if i != 2:
            return False
    
    return True