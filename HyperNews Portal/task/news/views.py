import json
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from django.conf import settings
import datetime
import random

news = json.load(open(settings.NEWS_JSON_PATH))
print('json loaded:', news)


class MainPageView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')


class NewsMainView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')
        print('NewsMainView, q:', q)
        if q:
            news_q = [new for new in news if new['title'].find(q) != -1]
            context = {'info': news_q}
        else:
            context = {'info': news}
        return render(request, 'news_list/news_list.html', context=context)


class NewsView(View):
    def get(self, request, uniq, *args, **kwargs):
        try:
            news_got = [k for k in news if k['link'] == int(uniq)]
            print(uniq, news_got)
            if len(news_got) > 0:
                return render(request, 'news/show_post.html', context=news_got[0])
            else:
                return HttpResponse("Coming soon")
        except:
            return HttpResponse("Coming soon")


def add_new_post(title, text):
    current_date = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    uniques_list = [int(obj['link']) for obj in news]
    new_unique = random.randint(1, 9999999)
    while True:
        if new_unique in uniques_list:
            new_unique = random.randint(1, 9999999)
        else:
            break

    new_post = {
        'created': current_date,
        'title': title,
        'text': text,
        'link': new_unique,
    }
    news.append(new_post)
    json.dump(news, open(settings.NEWS_JSON_PATH, 'w'))


class CreateNewsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'create_news/create.html')

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        text = request.POST.get('text')

        add_new_post(title, text)

        return redirect('/news/')
