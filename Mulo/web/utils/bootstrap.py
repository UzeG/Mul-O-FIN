from django import forms


class Bootstrap:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环找到所有的插件，添加了class="form-control"
        for name, field in self.fields.items():
            field.widget.attrs = {
                'class': 'form-control bg-secondary-subtle',
                'style': "border-radius: 15px;",
            }


class BootStrapModelForm(Bootstrap, forms.ModelForm):
    pass


class BootStrapForm(Bootstrap, forms.Form):
    pass


class SelectModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环找到所有的插件，添加了class="form-control"
        for name, field in self.fields.items():
            field.widget.attrs = {
                'class': 'form-control',
            }
