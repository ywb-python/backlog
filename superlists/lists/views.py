from django.shortcuts import redirect, render
from lists.models import Item, List
from django.core.exceptions import ValidationError
from django.utils.html import escape
from lists.forms import EMPTY_ITEM_ERROR, ItemForm


def home_page(request):
    """
    对应'/'的视图函数,渲染首页
    """
    return render(request, 'home.html', {'form': ItemForm()})


def new_list(request):
    """
    用于新的用户新提交待办事项之后的页面重定向
    """
    form = ItemForm(data=request.POST)
    # form.is_valid():判断表单提交是否成功
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form})


def view_list(request, list_id):
    """
    对应lists/1、lists/2等的视图函数。渲染待办事项列表页
    :param request:
    :param list_id: 待办事项列表id
    """
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            form.save(for_list=list_)
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, "form": form})

# Create your views here.
