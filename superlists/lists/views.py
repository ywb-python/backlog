from django.shortcuts import redirect, render
from lists.models import Item, List
from django.core.exceptions import ValidationError
from django.utils.html import escape
from lists.forms import EMPTY_ITEM_ERROR


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
        error = escape(EMPTY_ITEM_ERROR)
        return render(request, 'home.html', {"error": error})
    return redirect(list_)


def view_list(request, list_id):
    """
    对应lists/1、lists/2等的视图函数。渲染待办事项列表页
    :param request:
    :param list_id: 待办事项列表id
    """
    list_ = List.objects.get(id=list_id)
    error = None
    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = escape(EMPTY_ITEM_ERROR)
    return render(request, 'list.html', {'list': list_, "error": error})

# Create your views here.
