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

