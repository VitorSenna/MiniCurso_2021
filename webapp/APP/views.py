import time
from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import chrome
from collections import namedtuple
from time import sleep

# Create your views here.

options = Options()
options.add_argument('window-size=1280,720')
#options.add_argument('--headless')

def index(request):

    filtro = request.GET.get('filtro')

    tweet_texto = []
    tweet_resposta = []
    tweet_qtdlikes = []
    publicacao = []

    Tweet_Touple = namedtuple('tweet', ['texto', 'resposta', 'likes'])
    tweet = []

    if 'filtro' in request.GET:
        navegador = webdriver.Chrome()
        navegador.get('https://twitter.com/explore')

        sleep(4)

        search_box = navegador.find_element_by_xpath('//input[@data-testid="SearchBox_Search_Input"]')
        search_box.send_keys(filtro)
        search_box.send_keys(Keys.ENTER)

        sleep(6)

        navegador.execute_script('window.scrollTo(0, 5000);')

        publicacao = navegador.find_elements_by_xpath('//article[@data-testid="tweet"]')
        
        j = 0
        for i in publicacao:
            tweet_texto.append(i.find_element_by_xpath('.//div[2]/div[2]/div[2]/div[1]').text)
            

            if i.find_element_by_xpath('.//div[2]/div[2]/div[2]/div[2]').text:
                tweet_resposta.append(i.find_element_by_xpath('.//div[2]/div[2]/div[2]/div[2]').text)
            else:
                tweet_resposta.append('None')
                
            if i.find_element_by_xpath('.//div[@data-testid="like"]').text:
                tweet_qtdlikes.append(i.find_element_by_xpath('.//div[@data-testid="like"]').text)
            else:
                tweet_qtdlikes.append('0')

            tweet.append(Tweet_Touple(tweet_texto[j], tweet_resposta[j], tweet_qtdlikes[j]))
            j = j + 1



    return render(request, 'paginas/index.html', {'tweet': tweet})
