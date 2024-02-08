from django import forms

# from django.forms import widgets
from django_summernote.widgets import SummernoteInplaceWidget

from .models import Article, Category, Comment

choices = Category.objects.all().values_list("name", "name")

choice_list = []

for item in choices:
    choice_list.append(item)


class ArticleForm(forms.ModelForm):
    # content = forms.CharField(widget=SummernoteInplaceWidget())

    class Meta:
        model = Article
        fields = ["title", "author", "content", "image", "tags", "category", "snippet"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "label": "block text-white text-sm font-bold mb-2",
                    "class": "w-full px-4 py-2 bg-gray-400 border border-gray-600 rounded focus:outline-none focus:border-blue-500",
                }
            ),
            "content": SummernoteInplaceWidget(
                attrs={
                    "class": "w-full px-4 py-2 bg-gray-400 border border-gray-600 rounded focus:outline-none focus:border-blue-500"
                }
            ),
            "category": forms.Select(
                choices=choice_list,
                attrs={
                    "class": "w-full px-4 py-2 bg-gray-400 border border-gray-600 rounded focus:outline-none focus:border-blue-500"
                },
            ),
            "author": forms.TextInput(
                attrs={
                    "class": "block text-white text-sm font-bold mb-2",
                    "value": "",
                    "id": "zayyad",
                    "type": "hidden",
                }
            ),
            "tags": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2 bg-gray-400 border border-gray-600 rounded focus:outline-none focus:border-blue-500"
                }
            ),
            "snippet": forms.Textarea(
                attrs={
                    "class": "w-full px-4 py-2 bg-gray-400 border border-gray-600 rounded focus:outline-none focus:border-blue-500"
                }
            ),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            "content": forms.Textarea(attrs={"placeholder": "Add a comment..."}),
        }


class PostSearchForm(forms.Form):
    q = forms.CharField()
    c = forms.ModelChoiceField(queryset=Category.objects.all().order_by("name"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["c"].label = ""
        self.fields["c"].required = False
        self.fields["c"].label = "Category"
        self.fields["q"].label = "Search For"
        self.fields["q"].widget.attrs.update({"class": "form-control"})
