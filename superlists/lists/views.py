from django.shortcuts import redirect, render
from lists.models import Item, List
from django.core.exceptions import ValidationError
from django.utils.html import escape


def home_page(request):
    """
    对应'/'的视图函数,渲染首页
    """
    return render(request, 'home.html')


def new_list(request):
    """
    用于新的用户新提交待办事项之后的页面重定向
    """
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = escape("You can't have an empty list item")
        return render(request, 'home.html', {"error": error})
    return redirect(f'/lists/{list_.id}/')


def add_item(request, list_id):
    """
    用于原有的用户新提交待办事项之后的页面重定向
    :param request:
    :param list_id: 待办事项列表id
    """
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')


def view_list(request, list_id):
    """
    对应lists/1、lists/2等的视图函数。渲染待办事项列表页
    :param request:
    :param list_id: 待办事项列表id
    """
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_})

# Create your views here.
