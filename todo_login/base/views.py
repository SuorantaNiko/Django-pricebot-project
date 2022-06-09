from dataclasses import field, fields
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task


from bs4 import BeautifulSoup
import requests, re, json
from datetime import datetime



# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)

        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)

        context['search_input'] = search_input
        return context



class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title','price','wishPrice','complete']
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    
    def search_product(request):
        update_product()

        HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
        try:
            url = request.POST.get('url_name')
            
            now = datetime.now().strftime('%Y-%m-%d %Hh%Mm')
            
            page = requests.get(url, headers=HEADERS)

            Soup = BeautifulSoup(page.content, features="lxml")
            soup = BeautifulSoup(page.content, 'html.parser')
            
            title = soup.find(id='productTitle').get_text().strip()

            Img = Soup.find(id='imgTagWrapperId')
            Img = Img.img.get('data-a-dynamic-image')
            imgs_json = json.loads(Img)
            Img = list(imgs_json.keys())[0]


            Price = soup.find(id='corePrice_desktop').text
            Price = re.sub('\n', '', Price).strip()
            prices = 0
            prices = float(Price[Price.index('$')+1:Price.find('$', Price.find('$')+1)])
            
            
            
            """Price = soup.find(id='corePrice_desktop').text
            Price = re.sub('\n', '', Price).strip()
            prices =    {'default' : 0,
                        'discount' : 0,
                        'save' : 0}
            prices['default'] = float(Price[Price.index('$')+1:Price.find('$', Price.find('$')+1)])
            
            
            try:
                Price = Price[Price.find('$', Price.find('$')+1)+1:]
                print(Price)
                prices['discount'] = float(Price[Price.index('$')+1:Price.find('$', Price.find('$')+1)])
                Price = Price[Price.find('$', Price.find('$')+1)+1:]
                print(Price)
                prices['save'] = float(Price[Price.index('$')+1:Price.find('$', Price.find('$')+1)])
            except:
                prices['discount'] = 0
                prices['save'] = 0"""

            

            try:
                soup.select('#availability .a-color-state')[0].get_text().strip()
                stock = 'Out of Stock'
            except:
                try:
                    soup.select('#availability .a-color-price')[0].get_text().strip()
                    stock = 'Out of Stock'
                except:
                    stock = 'Available'


            product =   {'date': now.replace('h',':').replace('m',''),
                        'jpg' : Img,
                        'url': url,
                        'title': title,
                        'price': prices,
                        'stock': stock}


            if request.method == 'POST':
                try:
                    # makes new product or if product already exists -> update price.
                    Task.objects.update_or_create(
                        #kwargs= product,              
                        user = request.user,
                        title = title,
                        product = url,
                        defaults= {'price': prices},
                        )
                    
                    
                    return redirect('tasks')
                    
                except: redirect('tasks')
        except: return redirect('tasks')
        
    """
    def search_product(request):

        url = request.POST.get('url_name')
        
        now = datetime.now().strftime('%Y-%m-%d %Hh%Mm')

        page = requests.get(url, headers=HEADERS)

        Soup = BeautifulSoup(page.content, features="lxml")
        soup = BeautifulSoup(page.content, 'html.parser')
            
        title = soup.find(id='productTitle').get_text().strip()
        Img = Soup.find(id='imgTagWrapperId').get_text().strip()
        Price = soup.find(id='corePrice_desktop').text
        Price = re.sub('\n', '', Price).strip()
        prices =    {'default' : 0,
                        'discount' : 0,
                        'save' : 0}
        prices['default'] = float(Price[Price.index('$')+1:Price.find('$', Price.find('$')+1)])
            
            
        try:
            Price = Price[Price.find('$', Price.find('$')+1)+1:]
            print(Price)
            prices['discount'] = float(Price[Price.index('$')+1:Price.find('$', Price.find('$')+1)])
            Price = Price[Price.find('$', Price.find('$')+1)+1:]
            print(Price)
            prices['save'] = float(Price[Price.index('$')+1:Price.find('$', Price.find('$')+1)])
        except:
            prices['discount'] = 0
            prices['save'] = 0

            
        try: 
            all_imgs = soup.find_all('img')
                
            for i in all_imgs:
                if i['alt'] == title:
                    print('FOUND!')
                    Img = i
                    break

            Img = str(Img)
            Img = Img[Img.index('{')+2:Img.index('"')]
        except:
            Img = ''

        try:
            soup.select('#availability .a-color-state')[0].get_text().strip()
            stock = 'Out of Stock'
        except:
            try:
                soup.select('#availability .a-color-price')[0].get_text().strip()
                stock = 'Out of Stock'
            except:
                stock = 'Available'


        product =   {'date': now.replace('h',':').replace('m',''),
                    'jpg' : Img,
                    #'url': url,
                    'title': title,
                        
                    'price': prices,
                    'stock': stock}
        
        if request.method == 'POST':
            try:
                
                model = Task
                model.objects.create(
                   user = request.user,
                   title = title,
                   price = prices,
                )
                return redirect('tasks')
                  
            except: ValueError
            
"""


def update_product():
    
    
    HEADERS = ({'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'})
    
    url_list = list(Task.objects.values_list('product'))
    num = 0
    while num < len(url_list):
        
        for url in url_list[num]:
            print(url)
            num +=1
            
            now = datetime.now().strftime('%Y-%m-%d %Hh%Mm')
                    
            page = requests.get(url, headers=HEADERS)

            Soup = BeautifulSoup(page.content, features="lxml")
            soup = BeautifulSoup(page.content, 'html.parser')
                    
            title = soup.find(id='productTitle').get_text().strip()

            Img = Soup.find(id='imgTagWrapperId')
            Img = Img.img.get('data-a-dynamic-image')
            imgs_json = json.loads(Img)
            Img = list(imgs_json.keys())[0]


            Price = soup.find(id='corePrice_desktop').text
            Price = re.sub('\n', '', Price).strip()
            prices = 0
            prices = float(Price[Price.index('$')+1:Price.find('$', Price.find('$')+1)])
                    
            try:
                soup.select('#availability .a-color-state')[0].get_text().strip()
                stock = 'Out of Stock'
            except:
                try:
                    soup.select('#availability .a-color-price')[0].get_text().strip()
                    stock = 'Out of Stock'
                except:
                    stock = 'Available'


            product =   {'date': now.replace('h',':').replace('m',''),
                        'jpg' : Img,
                        'url': url,
                        'title': title,
                        'price': prices,
                        'stock': stock}


                    
            try:
                # makes new product or if product already exists -> update price.
                Task.objects.update_or_create(
                    #kwargs= product,              
                    #user = user,
                    title = title,
                    product = url,
                    defaults= {'price': prices},
                        )
                            
                            
                #return redirect('tasks')
                            
            except: redirect('tasks')
        

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['wishPrice','complete']
    success_url = reverse_lazy('tasks')

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')



