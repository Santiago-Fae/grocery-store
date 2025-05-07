from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Product
from django.views.generic import ListView, CreateView, UpdateView

# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

class ProductCreateView(CreateView):
    model = Product
    template_name = 'products/product_form.html'
    fields = ['name', 'price']
    success_url = reverse_lazy('product_list')

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'products/product_form.html'
    fields = ['name', 'price']
    success_url = reverse_lazy('product_list')
