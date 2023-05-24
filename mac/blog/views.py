from django.shortcuts import render
from django.http import HttpResponse
from .models import Blogpost
# Create your views here.
def index(requst):
    myposts =  Blogpost.objects.all()
    print(myposts)
    return render(requst, 'blog/index.html', {'myposts' : myposts})

def blogpost(requst,id):
    # Fetch the product using the id
    blogpost = Blogpost.objects.filter(post_id = id)[0]
    return render(requst, 'blog/blogpost.html', {'blogpost': blogpost})