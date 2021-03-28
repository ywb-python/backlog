#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/27 20:46
# @Author  : ywb
# @Site    : form表单
# @File    : forms.py
# @Software: PyCharm


from django import forms
from lists.models import Item


EMPTY_ITEM_ERROR = "You can't have an empty list item"


class ItemForm(forms.models.ModelForm):
    class Meta:
        model = Item
        fields = ('text', )
        widgets = {
            'text': forms.fields.TextInput(
                attrs={
                    'placeholder': "Enter a to-do item",
                    'class': 'form-control input-lg',
                }
            ),
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }

    def save(self, for_list):
        """
        待办事项的保存
        :param for_list: 待办事项隶属的清单
        """
        # instance:instance属性是将要修改或者创建的数据库对象
        self.instance.list = for_list
        return super().save()
