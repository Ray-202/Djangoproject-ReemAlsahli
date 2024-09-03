from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from .models import Storetype, items, itemsdetails, Coffee
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login ,authenticate
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm,LoginUserForm
# Create your views here.

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({'request': request}))

def listitems(request): 
    p = items.objects.filter(stypetype=2)
    template = loader.get_template('listitems.html')
    return HttpResponse(template.render({'items': p, 'request': request}))

def details(request,id):
    template = loader.get_template('details.html')
    data = itemsdetails.objects.select_related('items').filter(items_id=id).first()
    data.total=data.quantity*data.items.price
    return HttpResponse(template.render({'data': data, 'request': request}))



def add_to_cart(request, id):
    cart = request.session.get('cart', {})

    if not isinstance(cart, dict):
        cart = {}

    product = get_object_or_404(Coffee, id=id)

    # Adding items to the cart
    if str(product.id) in cart:
        cart[str(product.id)]['quantity'] += 1
    else:
        cart[str(product.id)] = {'quantity': 1}

    # Save the cart back into the session
    request.session['cart'] = cart

    # Update the cart item count
    request.session['cart_item_count'] = sum(item['quantity'] for item in cart.values())

    return JsonResponse({'cartItemCount': request.session['cart_item_count']})

def checkout(request):
    cart_items = []
    cart_total = 0

    # Retrieve the cart from the session
    cart = request.session.get('cart', {})

    if not isinstance(cart, dict):
        cart = {}

    # Process the cart items
    for item_id, item_data in cart.items():
        product = Coffee.objects.get(id=item_id)
        quantity = item_data['quantity']
        total_price = product.price * quantity
        cart_total += total_price
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': total_price,
        })

    return render(request, 'checkout.html', {'cart_items': cart_items, 'cart_total': cart_total})


def Coffee_shop(request):
    products = Coffee.objects.all()
    cart_item_count = request.session.get('cart_item_count', 0)  # Retrieve the cart item count from the session
    return render(request, 'CoffeeShop.html', {'products': products, 'cart_item_count': cart_item_count})


def details_coffee(request, id):
    product = get_object_or_404(Coffee, id=id)
    cart_item_count = request.session.get('cart_item_count', 0)  # Retrieve the cart item count from the session
    return render(request, 'detailsCoffee.html', {'product': product, 'cart_item_count': cart_item_count})


@login_required(login_url='/auth_login/')
def checkout(request):
    cart_items = []
    cart_total = 0

    cart = request.session.get('cart', {})

    if not isinstance(cart, dict):
        cart = {}

    for item_id, item_data in cart.items():
        product = Coffee.objects.get(id=item_id)
        quantity = item_data['quantity']
        total_price = product.price * quantity
        cart_total += total_price
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': total_price,
        })

    return render(request, 'checkout.html', {'cart_items': cart_items, 'cart_total': cart_total})

@csrf_exempt
def auth_login(request):
    form = LoginUserForm()
    if request.method == "POST":
        form = LoginUserForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    # Save the current cart
                    old_cart = request.session.get('cart', {})
                    
                    # Log in the user (this may regenerate the session)
                    login(request, user)
                    
                    # Restore the cart to the new session
                    request.session['cart'] = old_cart
                    request.session['cart_item_count'] = sum(item['quantity'] for item in old_cart.values())
                    
                    return redirect('checkout')  # Redirect to checkout after login
    context = {'form': form}
    return render(request, 'auth_login.html', context)

    
def auth_register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('auth_login')  # Redirect to login page after successful registration

    context = {'form': form}
    return render(request, 'auth_register.html', context)
     