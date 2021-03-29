#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/27 20:46
# @Author  : ywb
# @Site    : form表单
# @File    : forms.py
# @Software: PyCharm


from django import forms
from lists.models import Item
from django.core.exceptions import ValidationError


EMPTY_ITEM_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "You're already got this in your list"

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


class ExistingListItemForm(ItemForm):

    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def Validate_unique(self):
        try:
            # validate_unique():Django在表单和模型验证时会用到该方法
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)