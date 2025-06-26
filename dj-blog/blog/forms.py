from django import forms

# from django.forms import widgets
from django_summernote.widgets import SummernoteInplaceWidget

from .models import Article, Category, Comment

choices = Category.objects.all().values_list("name", "name")

choice_list = []

for item in choices:
    choice_list.append(item)


# class ArticleForm(forms.ModelForm):
#     # content = forms.CharField(widget=SummernoteInplaceWidget())

#     class Meta:
#         model = Article
#         fields = ["title", "author", "content", "image", "tags", "category", "snippet"]
#         widgets = {
#             "title": forms.TextInput(
#                 attrs={
#                     "label": "block text-white text-sm font-bold mb-2",
#                     "class": "w-full px-4 py-2 bg-gray-400 border border-gray-600 rounded focus:outline-none focus:border-blue-500",
#                 }
#             ),
#             "content": SummernoteInplaceWidget(
#                 attrs={
#                     "class": "w-full px-4 py-2 bg-gray-400 border border-gray-600 rounded focus:outline-none focus:border-blue-500"
#                 }
#             ),
#             "category": forms.Select(
#                 choices=choice_list,
#                 attrs={
#                     "class": "w-full px-4 py-2 bg-gray-400 border border-gray-600 rounded focus:outline-none focus:border-blue-500"
#                 },
#             ),
#             "author": forms.TextInput(
#                 attrs={
#                     "class": "block text-white text-sm font-bold mb-2",
#                     "value": "",
#                     "id": "zayyad",
#                     "type": "hidden",
#                 }
#             ),
#             "tags": forms.TextInput(
#                 attrs={
#                     "class": "w-full px-4 py-2 bg-gray-400 border border-gray-600 rounded focus:outline-none focus:border-blue-500"
#                 }
#             ),
#             "snippet": forms.Textarea(
#                 attrs={
#                     "class": "w-full px-4 py-2 bg-gray-400 border border-gray-600 rounded focus:outline-none focus:border-blue-500"
#                 }
#             ),
#         }

class ArticleForm(forms.ModelForm):
    """
    A simplified and "Crispy-friendly" form for creating articles.
    """
    class Meta:
        model = Article
        # REMOVED 'author' field. This should be handled in the view for security.
        fields = ["title", "content", "image", "tags", "category", "snippet"]

        widgets = {
            # We only define the widget type here, NOT the styling.
            # Crispy-tailwind will handle all the 'class' attributes.
            'content': SummernoteInplaceWidget(),
            
            # For the 'tags' field, if you're using django-taggit, you can add
            # a placeholder to guide the user.
            'tags': forms.TextInput(
                attrs={'placeholder': 'e.g., python, django, webdev'}
            ),

            # Crispy will automatically render other fields correctly.
            # No need to define widgets for 'title', 'category', 'snippet', etc.
            # unless you want to change the widget type (e.g., Textarea).
            'snippet': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        """
        Override the __init__ to add help text if desired.
        This is a cleaner way to add guidance than placeholders alone.
        """
        super().__init__(*args, **kwargs)
        self.fields['tags'].help_text = 'Enter comma-separated tags.'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug"]


class CommentForm(forms.ModelForm):
    # Add this new hidden field for the parent ID
    parent_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Comment
        fields = ('body', 'parent_id') # Add parent_id here
        # Optional: Add a widget for the body textarea if you want
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your comment here...'}),
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
