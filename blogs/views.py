from django.shortcuts import render

# Create your views here.
from blogs.models import *
from django.http import JsonResponse
# from rest_framework.response import Response 

def blog(request):
    if request.method =="POST"  and request.is_ajax():
        print("Post")
        return JsonResponse({'status':"hello"})
    return render(request, 'blogs/blog.html',)
def lead_list(request):
    context = {
        "leads": Lead.objects.all()
    }
    return render(request, 'blogs/leads/leads.html', context)
def lead_detail(request, slug):
    context = {
        'leads':Lead.objects.get(slug=slug)
    }
    print(slug)
    return render(request, 'blogs/leads/detail.html', context)