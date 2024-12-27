from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'condition', 'image', 'size', 'trade_type', 'uniform_type']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500'
            }),
            'name': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500',
                'placeholder': '상품명을 입력하세요'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500',
                'rows': 4,
                'placeholder': '상품 설명을 입력하세요'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500',
                'placeholder': '가격을 입력하세요'
            }),
            'condition': forms.Select(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500'
            }),
            'size': forms.Select(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500'
            }),
            'trade_type': forms.Select(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500'
            }),
            'uniform_type': forms.Select(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100',
                'accept': 'image/*'
            })
        } 