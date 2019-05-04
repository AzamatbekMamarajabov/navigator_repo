"""This file is in order to use forms"""
from django import forms


class SearchForm(forms.Form):
    """This class is for Search Form to search repositories  """
    search = forms.CharField(required=False)
