from django import forms
from django.core.exceptions import ValidationError
import re






class RegForm(forms.Form):
    company = forms.CharField(max_length=100,required=True,
                           error_messages={'required': '用户名不能为空'},
                           widget=forms.TextInput(
                                attrs={'id': 'username','placeholder': '用户名','name':'company'
                                       }))
    phone = forms.CharField(max_length=11,required=True,
                            error_messages={'required':'手机号不能为空'},
                            widget=forms.TextInput(
                                attrs={
                                    'id':'phone','placeholder':'手机号','name':'phone'
                                })
                            )

    name= forms.IntegerField(required=False,
                             widget=forms.TextInput(
                                 attrs={
                                     'id': 'name', 'placeholder': '联系人', 'name': 'name'
                                 })
                            )


    content_phone = forms.CharField(required=False,
                            widget=forms.TextInput(
                                attrs={
                                    'placeholder':'联系人电话',
                                    'name':'content_phone'
                                })
                            )
    address = forms.CharField(max_length=80, required=False,
                           widget=forms.TextInput(
                               attrs={
                                   'placeholder': '地址',
                                   'name':'address'
                               })
                           )

    email = forms.EmailField(required=False,
        widget=forms.EmailInput(
            attrs={'id': 'email', 'placeholder':'邮箱','name':'email'})

        )

    we_chat = forms.CharField(max_length=30, required=False,
                           widget=forms.TextInput(
                               attrs={
                                   'placeholder': '微信','name':'we_chat'
                               })
                           )
    qq = forms.CharField(max_length=20, required=False,
                              widget=forms.TextInput(
                                  attrs={
                                      'placeholder': 'QQ','name':'qq'
                                  })
                              )
    position = forms.CharField(max_length=30, required=False,
                              widget=forms.TextInput(
                                  attrs={
                                      'placeholder': '工作岗位','name':'position'
                                  })
                              )
    note = forms.CharField(required=False,
                                   widget=forms.Textarea(
                                   attrs={
                                       'placeholder': '备注','name':'note',
                                       'class':'textarea'
                                   })
                               )
    contact_list = forms.CharField(required=False,
                                   widget=forms.TextInput(
                                   attrs={
                                       'placeholder': '联系人','name':'contact_list'
                                   })
                               )


    def  __init__(self,*args,**kwargs):
        super(RegForm,self).__init__(*args,**kwargs)
        self.initial['choices'] = [1,]

    def clean_mobile(self):
        """
        验证手机是否合法
        """
        phone = self.cleaned_data['phone']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(phone):
            return phone
        else:
            raise forms.ValidationError("手机号码不合法", code="InvalidMobile")


class SmallRegForm(forms.Form):
    contact_name = forms.CharField(max_length=100, required=True,
                           error_messages={'required': '用户名不能为空'},
                           widget=forms.TextInput(
                               attrs={'id': 'contact_name', 'placeholder': '联系人姓名', 'name': 'contact_name'
                                      }))
    contact_type = forms.IntegerField(required=True,
                                      widget=forms.Select(
                                          choices=((1, '联系人'), (2, '开票地址'),(3,'送货地址'),(4,'其他地址')),
                                          attrs={
                                              'id': 'contact_type',
                                              'placeholder': '联系人类型',
                                              'class': 'select',
                                              'name': 'contact_type'
                                          })
                                      )
    contact_position = forms.CharField(max_length=30, required=False,
                              widget=forms.TextInput(
                                  attrs={
                                      'placeholder': '联系人工作岗位', 'name': 'contact_position'
                                  })
                              )
    contact_phone = forms.CharField(required=False,
                         widget=forms.TextInput(
                             attrs={
                                 'placeholder': '联系人电话', 'name': 'contact_phone'
                             })
                         )
    contact_email = forms.EmailField(required=False,
                             widget=forms.EmailInput(
                                 attrs={'id': 'email', 'placeholder': '联系人邮箱', 'name': 'contact_email'})

                             )
    contact_address = forms.CharField(max_length=80, required=False,
                              widget=forms.TextInput(
                                  attrs={
                                      'placeholder': '联系人地址',
                                      'name': 'contact_adress'
                                  })
                              )
    contact_we_chat = forms.CharField(max_length=30, required=False,
                              widget=forms.TextInput(
                                  attrs={
                                      'placeholder': '联系人微信', 'name': 'contact_we_chat'
                                  })
                              )
    contact_qq = forms.CharField(max_length=20, required=False,
                         widget=forms.TextInput(
                             attrs={
                                 'placeholder': '联系人QQ', 'name': 'contact_qq'
                             })
                         )

class LoginForm(forms.Form):
    uname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'uid', 'placeholder': '用户名','name':"username"}))
    pwd = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'pwd', 'placeholder': '密码','name':'password'}))