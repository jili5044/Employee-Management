from django import forms
from django.core.exceptions import ValidationError
from app01 import models
from app01.utils.encrypt import md5
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class UserModelForm(forms.ModelForm):
    name = forms.CharField(min_length=3, label="姓名")

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "deposit", "create_time", "gender", "depart"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
            "age": forms.TextInput(attrs={"class": "form-control"}),
            "deposit": forms.TextInput(attrs={"class": "form-control"}),
            "create_time": forms.TextInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-control"}),
            "depart": forms.Select(attrs={"class": "form-control"}),
        }

    # # 用不了
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     for name, field in self.fields.items():
    #         field.widgets.attr = {"class": "form-control", "placeholder": field.label}


class NumberModelForm(forms.ModelForm):
    # 号码校验1
    # mobile = forms.CharField(
    #     label="Number",
    #     validators=[RegexValidator(r'^\d+$', 'Must be numbers')]
    # )

    class Meta:
        model = models.PrettyNum
        # fields = "__all__"
        fields = ["mobile", "price", "level", "status"]
        widgets = {
            "mobile": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.TextInput(attrs={"class": "form-control"}),
            "level": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }

    # 号码校验2
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        if len(txt_mobile) != 10 and len(txt_mobile) != 11:
            # 验证不通过
            raise ValidationError("length error")
        # 验证通过，返回号码
        return txt_mobile


class NumberEditModelForm(forms.ModelForm):
    # 号码校验1
    # mobile = forms.CharField(
    #     label="Number",
    #     validators=[RegexValidator(r'^\d+$', 'Must be numbers')]
    # )

    class Meta:
        model = models.PrettyNum
        # fields = "__all__"
        fields = ["mobile", "price", "level", "status"]
        widgets = {
            "mobile": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.TextInput(attrs={"class": "form-control"}),
            "level": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }

    # 号码校验2
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        # 判断号码是否重复
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("number already exists")
        # 验证通过，返回号码
        return txt_mobile


class AdminModelForm(forms.ModelForm):
    confirm_pwd = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = models.Admin
        # fields = "__all__"
        fields = ["username", "password", "confirm_pwd"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)

        exist = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exist:
            raise ValidationError("password already exist")
        return md5_pwd

    # 密码确认
    def clean_confirm_pwd(self):
        # 这里pwd已经加密了
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_pwd"))
        # 判断密码是否一致
        if pwd != confirm:
            raise ValidationError("Inconsistent password input")
        # 验证通过，返回密码
        return confirm


class AdminEditModelForm(forms.ModelForm):
    class Meta:
        model = models.Admin
        fields = ["username"]


class AdminPwdResetModelForm(forms.ModelForm):
    confirm_pwd = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    flag = 1

    class Meta:
        model = models.Admin
        fields = ["password", "confirm_pwd"]
        widgets = {
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)

        exist = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exist:
            self.flag = 0
            raise ValidationError("password already exist")
        self.flag = 1
        return md5_pwd

    # 密码确认
    def clean_confirm_pwd(self):
        # 这里pwd已经加密了
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_pwd"))
        if self.flag:
            # 判断密码是否一致
            if pwd != confirm:
                raise ValidationError("Inconsistent password input")
            # 验证通过，返回密码
            return confirm


class LoginForm(forms.Form):
    username = forms.CharField(
        label="username",
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'floatingInput', 'placeholder': 'a'}),
        required=True,
    )
    password = forms.CharField(
        label="password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'floatingPassword', 'placeholder': 'aaa'}),
        required=True,
    )
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(
            # 设置为英语
            api_params={'hl': 'en'}
        )
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        # fields = ["username", "password", "confirm_pwd"]
        exclude = ["order_id", "customer"]
        widgets = {
            "order_id": forms.TextInput(attrs={"class": "form-control"}),
            "product": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "customer": forms.Select(attrs={"class": "form-control"}),
        }
