from django.shortcuts import render


def home_page(request):
    """
    对应'/'的视图函数,渲染首页
    """
    return render(request, 'home.html')


# Create your views here.
