# -*- coding: utf-8 -*-
"""
@Time ： 2024/4/22 上午11:26
@Auth ： lixingshuo
@File ：forms.py
@IDE ：PyCharm
@mail ： lixingshuo@gotion.com.cn
"""
from wtforms import Form, StringField, ValidationError
from wtforms.validators import length, equal_to

registered_email = ['aa@example.com', 'bb@example.com']


class RegisterForm(Form):
    username = StringField(validators=[length(min=3, max=16, message="请输入正确长度的用户名！")])
    password = StringField(validators=[length(min=6, max=16, message="请输入正确长度的密码！")])
    confirm_password = StringField(validators=[equal_to("password", message="两次密码不一致！")])

    def validate_email(self, field):
        email = field.data
        if email in registered_email:
            raise ValidationError("邮箱已经被注册！")
        return True

