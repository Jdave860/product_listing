from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import F, Subquery, OuterRef
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from .forms import SignupForm
from .models import Product
    
def landing_page(request):
    """Renders the landing page of the application."""

    return render(request, '../templates/landing.html')

@login_required
def buyer_product_list(request):
    """
    Displays a list of products available to buyers.
    Ensures that only users buyers can access the product listing.
    """

    # Check if the user is a supplier, if yes they should not access the buyers products
    if hasattr(request.user, 'supplier'):
        return HttpResponseForbidden("Suppliers are not allowed to view the buyer's product list.")
    
    # Retrieve all products that are currently in stock, along with their associated supplier details.
    products = Product.objects.filter(in_stock=True).select_related('supplier')

    # Render the buyer's product list page with the fetched products
    return render(request, '../templates/buyer_product_list.html', {'products': products})

@login_required
def supplier_product_list(request):
    """
    Displays a list of products associated with a specific supplier.
    Ensures that only users with a supplier role can access their own product listing.
    Identifies cheaper product analogues offered by other suppliers.
    """

    # Check if the user is a supplier, buyers should not have access to suppliers product views. 
    if not hasattr(request.user, 'supplier'):
        return HttpResponseForbidden("Buyers are not allowed to view the supplier's product list.")
    
    # Get the current supplier's information from the logged-in user.
    supplier = request.user.supplier
    # Fetch all products that belong to the current supplier.
    products = Product.objects.filter(supplier=supplier)

    #Get cheaper Analogues from other suppliers based on the same product code
    cheaper_analogs_subquery = Product.objects.filter(
        code = OuterRef('code'),
        in_stock = True,
    ).exclude(supplier=supplier).order_by('price').values('price')[:1]
    
    # Annotate the supplier's products with the details of the cheapest analogue products.
    products_with_analogs = products.annotate(
        cheapest_analog_code=Subquery(cheaper_analogs_subquery.values('code')[:1]),
        cheapest_analog_name=Subquery(cheaper_analogs_subquery.values('name')[:1]),
        cheapest_analog_price = Subquery(cheaper_analogs_subquery)
    )

    # Filter to get only products that have a cheaper analogue available
    cheaper_analogs = products_with_analogs.filter(price__gt=F('cheapest_analog_price'))
    
    # Render the supplier's product list page along with the list of cheaper analogues.
    return render(request, '../templates/supplier_product_list.html', {
        'products': products,
        'cheaper_analogs': cheaper_analogs
    })


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('landing')
        return super().get(request, *args, **kwargs)
    
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = SignupForm()

    return render(request, 'registration/signup.html', {'form': form})