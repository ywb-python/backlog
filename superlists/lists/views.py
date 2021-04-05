from django.shortcuts import redirect, render
from lists.models import Item, List
from django.core.exceptions import ValidationError
from django.utils.html import escape
from lists.forms import EMPTY_ITEM_ERROR, ExistingListItemForm, ItemForm
from django.contrib.auth import get_user_model


User = get_user_model()


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
        list_ = List()
        if request.user.is_authenticated:
            list_.owner = request.user
        list_.save()
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
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, "form": form})


def my_lists(request, email):
    """
    my_lists对应的视图函数，用户展示当前用户的待办事项清单
    :param request:
    :param email: 当前用户邮箱
    """
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner': owner})
# Create your views here.
