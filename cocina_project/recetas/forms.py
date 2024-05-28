from django import forms
from .models import Recipe

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div

# Add your forms here

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title','description','ingredients','steps','preparation_time',
                    'image','category']
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.form_class = 'form-floating mb-3'
            self.helper.layout = Layout(
            Div(
                Field('title', css_class='form-control', wrapper_class='form-floating mb-3', placeholder='Recipe Title'),
                css_class='form-floating mb-3'
            ),
            Div(
                Field('description', css_class='form-control', wrapper_class='form-floating mb-3', placeholder='Description'),
                css_class='form-floating mb-3'
            ),
            Div(
                Field('ingredients', css_class='form-control', wrapper_class='form-floating mb-3', placeholder='Ingredients'),
                css_class='form-floating mb-3'
            ),
            Div(
                Field('steps', css_class='form-control', wrapper_class='form-floating mb-3', placeholder='Steps'),
                css_class='form-floating mb-3'
            ),
            Div(
                Field('preparation_time', css_class='form-control', wrapper_class='form-floating mb-3', placeholder='Preparation Time'),
                css_class='form-floating mb-3'
            ),
            Div(
                Field('image', css_class='form-control-file', wrapper_class='form-floating mb-3'),
                css_class='form-floating mb-3'
            ),
            Div(
                Field('category', css_class='form-control', wrapper_class='form-floating mb-3', placeholder='Category'),
                css_class='form-floating mb-3'
            ),
            Submit('submit', 'Save Recipe', css_class='btn btn-primary')
            )

class RecipeSearchForm(forms.Form):
    query = forms.CharField(label='',max_length=100,required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_class = 'd-flex'
        self.helper.layout = Layout(
            Field('query', css_class='form-control me-2', placeholder='Search'),
            Submit('search', 'Search', css_class='btn btn-primary mb-2')
        )
