# 6th
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Customer
from .forms import CustomerForm
from django.urls import reverse
from django.views.generic import ListView
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import (
    CreateView, UpdateView
)

from .forms import (
    ProductForm, VariantFormSet
)
from .models import (
    Image,
    Product,
    Variant
)



def customer_list(request):
    query = request.GET.get('q')
    customers = Customer.objects.all()

    if query:
        # If a search query is provided, filter customers based on name or any other relevant field
        customers = customers.filter(
            Q(full_name__icontains=query) |  # Change 'full_name' to the actual field you want to search
            Q(phone_number__icontains=query)  # Add more fields as needed
            # Add more fields as needed
        )

    current_datetime = timezone.now()

    # Configure pagination
    paginator = Paginator(customers, 10)
    page = request.GET.get('page')

    try:
        customers = paginator.page(page)
    except PageNotAnInteger:
        customers = paginator.page(1)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)

    return render(request, 'products/customer_list.html', {'customers': customers, 'current_datetime': current_datetime})

def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:customer_list')  # Redirect to a customer list view
    else:
        form = CustomerForm()

    return render(request, 'products/create_customer.html', {'form': form})

def customer_detail(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    products = customer.product_set.all()  # Access products through the reverse relationship

    paginator = Paginator(products, 10)
    page = request.GET.get('page')

    try:
        paginated_products = paginator.page(page)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)

    return render(request, 'products/customer_detail.html', {'customer': customer, 'products': products})



class ProductInline():
    form_class = ProductForm
    model = Product
    template_name = "products/product_create_or_update.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect(reverse('products:customer_product_list', args=[self.object.customer.id]))

    def formset_variants_valid(self, formset):
        """
        Hook for custom formset saving.. useful if you have multiple formsets
        """
        variants = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this, if you have can_delete=True parameter set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for variant in variants:
            variant.product = self.object
            variant.save()

    def formset_images_valid(self, formset):
        """
        Hook for custom formset saving.. useful if you have multiple formsets
        """
        images = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this, if you have can_delete=True parameter set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for image in images:
            image.product = self.object
            image.save()


class ProductCreate(ProductInline, CreateView):

    def get_context_data(self, **kwargs):
        ctx = super(ProductCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer_id = self.kwargs.get('customer_id')
        customer = get_object_or_404(Customer, id=customer_id)
        context['customer'] = customer
        context['named_formsets'] = self.get_named_formsets()
        return context

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'variants': VariantFormSet(prefix='variants'),
 #               'images': ImageFormSet(prefix='images'),
            }
        else:
            return {
                'variants': VariantFormSet(self.request.POST or None, self.request.FILES or None, prefix='variants'),
 #               'images': ImageFormSet(self.request.POST or None, self.request.FILES or None, prefix='images'),
            }
    
     
class EditCustomerProductsView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_edit.html'  # Update with your actual template name
    success_url = None  # Keep it as None to handle redirection in the form_valid method

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        return context

    def get_named_formsets(self):
        return {
            'variants': VariantFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='variants'),
 #           'images': ImageFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='images'),
        }

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()

        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        # Save formsets
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, f'formset_{name}_valid', None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()

        # Redirect to customer product list
        customer_id = self.object.customer.id
        redirect_url = reverse('products:customer_product_list', kwargs={'customer_id': customer_id})
        return redirect(redirect_url)
    
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    images = product.image_set.all()  # Access related images
    variants = product.variant_set.all()  # Access related variants

    return render(request, 'products/product_detail.html', {
        'product': product,
        'images': images,
        'variants': variants,
    })


def delete_image(request, pk):
    try:
        image = Image.objects.get(id=pk)
    except Image.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'
            )
        return redirect('products:update_product', pk=image.product.id)

    image.delete()
    messages.success(
            request, 'Image deleted successfully'
            )
    return redirect('products:update_product', pk=image.product.id)


def delete_variant(request, pk):
    try:
        variant = Variant.objects.get(id=pk)
    except Variant.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'
            )
        return redirect('products:update_product', pk=variant.product.id)

    variant.delete()
    messages.success(
            request, 'Variant deleted successfully'
            )
    return redirect('products:update_product', pk=variant.product.id)


def customer_product_list(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    products = Product.objects.filter(customer=customer)

    return render(request, 'products/customer_product_list.html', {'customer': customer, 'products': products})

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('products:customer_product_list', customer_id=product.customer.id)

    return render(request, 'products/product_confirm_delete.html', {'product': product})

