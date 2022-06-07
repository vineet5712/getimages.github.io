from unicodedata import name
from django.shortcuts import render
from google_images_download import google_images_download
import sys

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Members
from django.urls import reverse
import sys
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import requests  # pip install requests #to sent GET requests
# pip install bs4 #to parse html(getting data out from html, xml or other markup languages)
from bs4 import BeautifulSoup
# from django.template import template


# creating object


def ApiData():
    orig_stdout = sys.stdout


    f = open('URLS.txt', 'w')
    sys.stdout = f

    response = google_images_download.googleimagesdownload()

    arguments = {"keywords": 'stackoverflow',
             "limit": 3,
             "print_urls": True,
             "size": ">2MP",
             }
    paths = response.download(arguments)

    sys.stdout = orig_stdout
    f.close()

    with open('URLS.txt') as f:
     content = f.readlines()
    f.close()

    urls = []
    for j in range(len(content)):
        if content[j][:9] == 'Completed':
         urls.append(content[j-1][11:-1])
    print(urls)


@csrf_exempt
def addApiData(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        name = data['name']
        Google_Image = \
            'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

# The User-Agent request header contains a characteristic string
# that allows the network protocol peers to identify the application type,
# operating system, and software version of the requesting software user agent.
# needed for google search
        u_agnt = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
        }  # write: 'my user agent' in browser to get your browser user agent details

        Image_Folder = 'E:/spvaig/Image_Folder'

        if not os.path.exists('E:/spvaig/Image_Folder'):
            os.mkdir('E:/spvaig/Image_Folder')

        data = data['name']
        # data = data.replace(" ", "+")
        num_images = 5

        # print('Searching Images....')

        search_url = Google_Image + 'q=' + data  # 'q=' because its a query

# request url, without u_agnt the permission gets denied
        response = requests.get(search_url, headers=u_agnt)
        html = response.text  # To get actual result i.e. to read the html data in text mode

# find all img where class='rg_i Q4LuWd'
# html.parser is used to parse/extract features from HTML files
        b_soup = BeautifulSoup(html, 'html.parser')
        results = b_soup.findAll('img', {'class': 'rg_i Q4LuWd'})

# extract the links of requested number of images with 'data-src' attribute and appended those links to a list 'imagelinks'
# allow to continue the loop in case query fails for non-data-src attributes
        count = 0
        imagelinks = []
        for res in results:
            try:
                link = res['data-src']
                imagelinks.append(link)
                count = count + 1
                if (count >= num_images):
                    break

            except KeyError:
                continue

            # print(f'Found {len(imagelinks)} images')
            # print('Start downloading...')

            for i, imagelink in enumerate(imagelinks):
                # # open each image link and save the file
                response = requests.get(imagelink)

                imagename = Image_Folder + '/' + data + str(i+1) + '.jpg'

                with open(imagename, 'wb') as file:
                    file.write(response.content)
            # return HttpResponseRedirect(imagelinks)

            #  print('Download Completed!')
                value = {
                      "img_url": imagelink,
                    
    }
            return HttpResponse(json.dumps(value))



def index(request):
    return render(request, 'myfirst.html')
#      template = loader.get_template('myfirst.html')
#   return HttpResponse(template.render())


def showData(request):
    mymembers = Members.objects.all().values()
    print(mymembers)
    template = loader.get_template('index.html')
    context = {
        'mymembers': mymembers,
    }
    return HttpResponse(template.render(context, request))


def add(request):
    return render(request, 'add.html')


def addrecord(request):
    x = request.POST['first']
    y = request.POST['last']
    member = Members(firstname=x, lastname=y)
    member.save()
    print(member)

    return HttpResponseRedirect(reverse('showData'))
