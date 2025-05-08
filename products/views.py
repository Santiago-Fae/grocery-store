from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Product, Customer, Basket, BasketItem, Purchase

# Helper functions
def is_staff(user):
    return user.is_staff

# User Registration
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    is_staff = forms.BooleanField(required=False, label='Register as Staff')
    phone = forms.CharField(max_length=15, required=False, label='Phone Number')
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label='Address')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'phone', 'address']

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = form.cleaned_data.get('is_staff')
            user.save()
            phone = form.cleaned_data.get('phone')
            address = form.cleaned_data.get('address')
            Customer.objects.create(
                user=user,
                phone=phone,
                address=address
            )
            
            messages.success(request, f'Account created for {user.username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})

# Product Views
class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class ProductCreateView(StaffRequiredMixin, CreateView):
    model = Product
    template_name = 'products/product_form.html'
    fields = ['name', 'price']
    success_url = reverse_lazy('product_list')

class ProductUpdateView(StaffRequiredMixin, UpdateView):
    model = Product
    template_name = 'products/product_form.html'
    fields = ['name', 'price']
    success_url = reverse_lazy('product_list')

# Customer
@login_required
def customer_profile(request):
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=request.user)
    
    baskets = customer.baskets.exclude(status='completed').order_by('-created_at')
    purchases = Purchase.objects.filter(basket__customer=customer).order_by('-purchase_date')
    
    return render(request, 'products/customer_profile.html', {
        'customer': customer,
        'baskets': baskets,
        'purchases': purchases
    })

# Basket
@login_required
def basket_view(request):
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=request.user)
    
    active_basket = Basket.objects.filter(customer=customer, status='pending').first()
    if not active_basket:
        active_basket = Basket.objects.create(customer=customer)
    
    return render(request, 'products/basket.html', {'basket': active_basket})

@login_required
def add_to_basket(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=request.user)
    
    active_basket = Basket.objects.filter(customer=customer, status='pending').first()
    if not active_basket:
        active_basket = Basket.objects.create(customer=customer)
    
    basket_item, created = BasketItem.objects.get_or_create(
        basket=active_basket,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        basket_item.quantity += 1
        basket_item.save()
    
    messages.success(request, f"{product.name} added to your basket.")
    return redirect('product_list')

@login_required
def update_basket_item(request, item_id):
    item = get_object_or_404(BasketItem, id=item_id)
    
    if item.basket.customer.user != request.user:
        messages.error(request, "You don't have permission to modify this basket.")
        return redirect('basket')
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()
        
        messages.success(request, "Basket updated successfully.")
    
    return redirect('basket')

@login_required
def remove_from_basket(request, item_id):
    item = get_object_or_404(BasketItem, id=item_id)
    
    if item.basket.customer.user != request.user:
        messages.error(request, "You don't have permission to modify this basket.")
        return redirect('basket')
    
    item.delete()
    messages.success(request, "Item removed from basket.")
    return redirect('basket')

# Staff Views
@user_passes_test(is_staff)
def staff_dashboard(request):
    pending_baskets = Basket.objects.filter(status='pending').order_by('-created_at')
    approved_baskets = Basket.objects.filter(status='approved').order_by('-created_at')
    denied_baskets = Basket.objects.filter(status='denied').order_by('-created_at')
    
    return render(request, 'products/staff_dashboard.html', {
        'pending_baskets': pending_baskets,
        'approved_baskets': approved_baskets,
        'denied_baskets': denied_baskets
    })

@user_passes_test(is_staff)
def basket_detail_staff(request, basket_id):
    basket = get_object_or_404(Basket, id=basket_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            basket.status = 'approved'
            basket.save()
            messages.success(request, f"Basket #{basket.id} approved successfully.")
        elif action == 'deny':
            basket.status = 'denied'
            basket.save()
            messages.success(request, f"Basket #{basket.id} denied.")
        elif action == 'complete':
            basket.status = 'completed'
            basket.save()
            
            # Create a purchase record
            Purchase.objects.create(
                basket=basket,
                total_amount=basket.total_price()
            )
            
            messages.success(request, f"Basket #{basket.id} marked as completed and purchase recorded.")
    
    return render(request, 'products/basket_detail_staff.html', {'basket': basket})

@user_passes_test(is_staff)
def customer_search(request):
    query = request.GET.get('q', '')
    customers = []
    
    if query:
        customers = Customer.objects.filter(
            Q(user__username__icontains=query) | 
            Q(user__email__icontains=query) |
            Q(phone__icontains=query)
        )
    
    return render(request, 'products/customer_search.html', {
        'customers': customers,
        'query': query
    })

@user_passes_test(is_staff)
def customer_detail_staff(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    baskets = customer.baskets.all().order_by('-created_at')
    pending_baskets = baskets.filter(status='pending')
    approved_baskets = baskets.filter(status='approved')
    denied_baskets = baskets.filter(status='denied')
    purchases = Purchase.objects.filter(basket__customer=customer).order_by('-purchase_date')
    
    return render(request, 'products/customer_detail_staff.html', {
        'customer': customer,
        'baskets': baskets,
        'pending_baskets': pending_baskets,
        'approved_baskets': approved_baskets,
        'denied_baskets': denied_baskets,
        'purchases': purchases
    })
