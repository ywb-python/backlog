from django.shortcuts import redirect, render
from lists.models import Item


def home_page(request):
    """
    对应'/'的视图函数,渲染首页
    """
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})


# Create your views here.
