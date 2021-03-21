from django.http import HttpResponse


def home_page(request):
    """
    对应'/'的视图函数,渲染首页
    """
    return HttpResponse('<html><title>To-Do lists</title></html>')


# Create your views here.
