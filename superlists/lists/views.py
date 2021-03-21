from django.shortcuts import render, redirect
from lists.models import Item, List


def home_page(request):
    """
    对应'/'的视图函数,渲染首页
    """
    return render(request, 'home.html')


def view_list(request, list_id):
    """
    对应lists/1、lists/2等的视图函数。渲染待办事项列表页
    :param list_id: 待办事项id
    """
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_})


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')


def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')

# Create your views here.
