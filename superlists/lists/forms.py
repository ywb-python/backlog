#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/3 21:07
# @Author  : ywb
# @Site    : 
# @File    : forms.py
# @Software: PyCharm


from django import forms
from lists.models import Item


EMPTY_ITEM_ERROR = "You can't have an empty list item"


class ItemForm(forms.models.ModelForm):

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg',
                'name': 'item_text',
                'id': 'id_new_item'
            }),
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()