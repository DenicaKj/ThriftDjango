from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django.contrib.auth.forms import AuthenticationForm
from Thrift.models import CustomUser, ImageProd, Product, Color


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control m-2"
            field.field.widget.attrs["style"] = "background-color:#79b9a8"
            field.label_tag(attrs={'style': 'display: inline-block;text-align: right;width: 50%;'})
    class Meta:
        model = CustomUser
        fields = ("username","first_name","last_name", "email", "password1", "password2","image",)

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            return user



class StyledAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control m-2"
            field.field.widget.attrs["style"] = "background-color:#79b9a8"
            field.label_tag(attrs={'style': 'display: inline-block;text-align: right;width: 50%;'})

class ImageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control m-2"
            field.field.widget.attrs["style"] = "background-color:#79b9a8"
            field.label_tag(attrs={'style': 'display: inline-block;text-align: right;width: 50%;'})
    class Meta:
        model = ImageProd
        fields = ('image',)

class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control m-2"
            field.field.widget.attrs["style"] = "background-color:#79b9a8"
            field.label_tag(attrs={'style': 'display: inline-block;text-align: right;width: 50%;'})
    class Meta:
        model = Product
        fields = [ 'price', 'condition', 'size', 'description', 'shop', 'type', 'colors', 'gender']

class ProductFormEdit(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control m-2"
            field.field.widget.attrs["style"] = "background-color:#79b9a8"
            field.label_tag(attrs={'style': 'display: inline-block;text-align: right;width: 50%;'})
    class Meta:
        model = Product
        fields = [ 'price', 'condition', 'size', 'description', 'shop', 'type', 'colors', 'gender']

ImageFormSet = inlineformset_factory(Product, ImageProd, form=ImageForm, extra=1)
#ColorFormSet = inlineformset_factory(Product,Color,fields=('image',), extra=1)