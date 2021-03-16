from django.test import TestCase


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        """
        测试网站根路径("/")能否被正确解析，映射到对应的视图函数上
        """
        # assertTemplateUsed():检查响应是使用哪个模板进行渲染的
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

# Create your tests here.
