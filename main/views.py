import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import Product, Order, Cart, Category, shipment


# Create your views here.


def index(request):
    data = Product.objects.all()
    paginator = Paginator(data, 9)
    page_number = request.GET.get('page')  # new
    page_obj = paginator.get_page(page_number)  # changed
    data2 = 0
    if request.user.is_active:
        user = request.user
        data1 = Cart.objects.filter(user=user, purchased=False)
        data2 = data1.count()
    return render(request, 'index.html', {'first': page_obj, 'sec': data2})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.success(request, 'Invalid username or password !!!')
            return redirect('login')
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first name']
        last_name = request.POST['last name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['confirm password']

        if password == password1:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Is Already Exist')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.success(request, 'Email Is Already Exist')
                return redirect('register')
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name,
                                                username=username, email=email, password=password)
                user.save()

                # form = UserCreationForm(request.POST)
                # new_user = authenticate(username=form['username'],
                #                         password=form['password1'],
                #                        )
                # login(request, new_user)
                return redirect('login')

        else:
            messages.info(request, 'password not match!!!')
            return redirect('register')

    else:
        return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def add_to_cart(request, **kwargs):
    if request.user.is_active:
        slug = kwargs['slug']
        item = get_object_or_404(Product, slug=slug)
        order_item, created = Cart.objects.get_or_create(
            item=item,
            user=request.user,
            defaults={'subtotal': item.price,
                      'quantity': 1,
                      'purchased': 0}
        )
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.orderitems.filter(item__slug=item.slug, purchased=False).exists():
                order_item.quantity += 1
                order_item.subtotal += item.price
                order_item.save()
                messages.info(request, f"The {item.name}'s quantity was updated.")
                return redirect("/")
            elif order.orderitems.filter(item__slug=item.slug, purchased=True).exists():
                newcart = Cart.objects.create(
                    item=item,
                    user=request.user,
                    subtotal=item.price,
                    quantity=1,
                    purchased=0
                )
                newcart.save()
                messages.info(request, f"The {item.name} was added to your cart.")
                return redirect("/")
            else:
                order.orderitems.add(order_item)
                messages.info(request, f"The {item.name} was added to your cart.")
                return redirect("/")
        else:
            order = Order.objects.create(
                user=request.user)
            order.orderitems.add(order_item)
            messages.info(request, f"The {item.name} was added to your cart.")
            return redirect("/")

    else:
        return redirect("login")


@login_required(login_url='login')
def cart(request):
    user = request.user
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    carts = Cart.objects.filter(user=user, purchased=0)
    orders = Order.objects.filter(user=user, ordered=False)

    if carts.exists():
        if orders.exists():
            order_total = order_qs[0].get_totals()
            order = orders[0]
            return render(request, 'cart.html', {"cart": carts, 'order': order, "order_total": order_total})
        else:
            messages.warning(request, "You do not have any item in your cart")
            return redirect("/")

    else:
        messages.warning(request, "You do not have any item in your cart")
        return redirect("/")


def remove_from_cart(request, id):
    cart_id = get_object_or_404(Cart, id=id)
    cart_id.delete()
    return redirect('cart')


def increase(request, id):
    cart_id = id
    cart = get_object_or_404(Cart, id=cart_id)
    cart.quantity += 1
    item = get_object_or_404(Product, name=cart.item)
    cart.subtotal = cart.subtotal + item.price
    cart.save()
    return redirect('cart')


def decrease(request, id):
    cart_id = id
    cart = get_object_or_404(Cart, id=cart_id)
    item = get_object_or_404(Product, name=cart.item)
    if cart.quantity > 1:
        cart.quantity -= 1
        cart.subtotal = cart.subtotal - item.price
        cart.save()
    else:
        cart.quantity = 1
        cart.save()
    return redirect('cart')


def about(request):
    return render(request, 'about.html')


def profile(request):
    user = request.user
    orders = Order.objects.filter(user=user, ordered=True)
    context = {
        "orders": orders,
        "user": user
    }
    return render(request, 'profile.html', context)


def toys(request):
    data3 = Product.objects.all()
    paginator = Paginator(data3, 9)
    page_number = request.GET.get('page')  # new
    page_obj = paginator.get_page(page_number)  # changed
    data2 = 0
    if request.user.is_active:
        user = request.user
        data1 = Cart.objects.filter(user=user, purchased=False)
        data2 = data1.count()
    a = Category.objects.get(title='Babies & Toys')
    data = Product.objects.filter(category_id=a.id)
    return render(request, "toys.html", {'data': data, 'first': page_obj, 'sec': data2})


def accessories(request):
    data3 = Product.objects.all()
    paginator = Paginator(data3, 9)
    page_number = request.GET.get('page')  # new
    page_obj = paginator.get_page(page_number)  # changed
    data2 = 0
    if request.user.is_active:
        user = request.user
        data1 = Cart.objects.filter(user=user, purchased=False)
        data2 = data1.count()
    a = Category.objects.get(title='Electronic Accessories')
    data = Product.objects.filter(category_id=a.id)
    return render(request, "accessories.html", {'data': data, 'first': page_obj, 'sec': data2})


def gadgets(request):
    data3 = Product.objects.all()
    paginator = Paginator(data3, 9)
    page_number = request.GET.get('page')  # new
    page_obj = paginator.get_page(page_number)  # changed
    data2 = 0
    if request.user.is_active:
        user = request.user
        data1 = Cart.objects.filter(user=user, purchased=False)
        data2 = data1.count()
    a = Category.objects.get(title='Electronic Gadgets')
    data = Product.objects.filter(category_id=a.id)
    return render(request, "gadgets.html", {'data': data, 'first': page_obj, 'sec': data2})


def groceries(request):
    data3 = Product.objects.all()
    paginator = Paginator(data3, 9)
    page_number = request.GET.get('page')  # new
    page_obj = paginator.get_page(page_number)  # changed
    data2 = 0
    if request.user.is_active:
        user = request.user
        data1 = Cart.objects.filter(user=user, purchased=False)
        data2 = data1.count()
    a = Category.objects.get(title='Groceries')
    data = Product.objects.filter(category_id=a.id)
    return render(request, "groceries.html", {'data': data, 'first': page_obj, 'sec': data2})


def health(request):
    data3 = Product.objects.all()
    paginator = Paginator(data3, 9)
    page_number = request.GET.get('page')  # new
    page_obj = paginator.get_page(page_number)  # changed
    data2 = 0
    if request.user.is_active:
        user = request.user
        data1 = Cart.objects.filter(user=user, purchased=False)
        data2 = data1.count()
    a = Category.objects.get(title='Health & Beauty')
    data = Product.objects.filter(category_id=a.id)
    return render(request, "health.html", {'data': data, 'first': page_obj, 'sec': data2})


def home(request):
    data3 = Product.objects.all()
    paginator = Paginator(data3, 9)
    page_number = request.GET.get('page')  # new
    page_obj = paginator.get_page(page_number)  # changed
    data2 = 0
    if request.user.is_active:
        user = request.user
        data1 = Cart.objects.filter(user=user, purchased=False)
        data2 = data1.count()
    a = Category.objects.get(title='Home Appliances')
    data = Product.objects.filter(category_id=a.id)
    return render(request, "home.html", {'data': data, 'first': page_obj, 'sec': data2})


def liquor(request):
    data3 = Product.objects.all()
    paginator = Paginator(data3, 9)
    page_number = request.GET.get('page')  # new
    page_obj = paginator.get_page(page_number)  # changed
    data2 = 0
    if request.user.is_active:
        user = request.user
        data1 = Cart.objects.filter(user=user, purchased=False)
        data2 = data1.count()
    a = Category.objects.get(title='liquor')
    data = Product.objects.filter(category_id=a.id)
    return render(request, "liquor.html", {'data': data, 'first': page_obj, 'sec': data2})


def MenFashion(request):
    data3 = Product.objects.all()
    paginator = Paginator(data3, 9)
    page_number = request.GET.get('page')  # new
    page_obj = paginator.get_page(page_number)  # changed
    data2 = 0
    if request.user.is_active:
        user = request.user
        data1 = Cart.objects.filter(user=user, purchased=False)
        data2 = data1.count()
    a = Category.objects.get(title="Men's Fashion")
    data = Product.objects.filter(category_id=a.id)
    return render(request, "MenFashion.html", {'data': data, 'first': page_obj, 'sec': data2})


def sport(request):
    data3 = Product.objects.all()
    paginator = Paginator(data3, 9)
    page_number = request.GET.get('page')  # new
    page_obj = paginator.get_page(page_number)  # changed
    data2 = 0
    if request.user.is_active:
        user = request.user
        data1 = Cart.objects.filter(user=user, purchased=False)
        data2 = data1.count()
    a = Category.objects.get(title="Sports & Outdoor")
    data = Product.objects.filter(category_id=a.id)
    return render(request, "sport.html", {'data': data, 'first': page_obj, 'sec': data2})


def WomenFashion(request):
    data3 = Product.objects.all()
    paginator = Paginator(data3, 9)
    page_number = request.GET.get('page')  # new
    page_obj = paginator.get_page(page_number)  # changed
    data2 = 0
    if request.user.is_active:
        user = request.user
        data1 = Cart.objects.filter(user=user, purchased=False)
        data2 = data1.count()
    a = Category.objects.get(title="Women's Fashion")
    data = Product.objects.filter(category_id=a.id)
    return render(request, "WomenFashion.html", {'data': data, 'first': page_obj, 'sec': data2})


def Shipment(request):
    user = request.user
    order = Order.objects.get(user=user, ordered=False)
    order_id = order.id
    shipping = shipment.objects.filter(order=order_id)
    shipping.delete()
    if request.method == 'POST':
        address = request.POST['address']
        city = request.POST['city']
        contact = request.POST['contact']
        landmark = request.POST['landmark']
        shipment.objects.create(address=address, city=city, contact=contact, landmark=landmark, user=user,
                                order_id=order_id)
        return redirect('checkout')

    else:
        return redirect('checkout')


@login_required(login_url='login')
def checkout(request):
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].orderitems.all()
    order_total = order_qs[0].get_totals()
    order = Order.objects.get(user=request.user, ordered=False)
    savedAddress = len(shipment.objects.filter(user=request.user, order=order.id))
    if savedAddress == 0:
        return render(request, 'checkout.html',
                      {"order_items": order_items, "order": order, "order_total": order_total})
    else:
        savedAddress = shipment.objects.get(user=request.user, order=order.id)
        return render(request, 'checkout.html',
                      {"order_items": order_items, "order": order, "order_total": order_total,
                       "savedAddress": savedAddress})


def search(request):
    if request.method == 'POST':
        abc = request.POST['item']
        data = Product.objects.filter(name__icontains=abc)  # item searched
        if data:
            messages.info(request, f'Search Result: found {abc}')
            return render(request, 'search.html',
                      {'item': abc, 'data': data, 'abc': abc})
        else:
            messages.info(request, f'search result: not found {abc}')
            return render(request, 'search.html',
                          {'item': abc, 'data': data, 'abc': abc})
    else:
        return render(request, 'search.html')


def khaltiverify(request, *args, **kwargs):
    token = request.GET.get("token")
    amount = request.GET.get("amount")
    o_id = request.GET.get("order_id")
    print(token, amount, o_id)

    url = "https://khalti.com/api/v2/payment/verify/"
    payload = {
        "token": token,
        "amount": amount
    }
    headers = {
        "Authorization": "test_secret_key_d080043a53d24829b64a458cf3054c6c"
    }

    order_obj = Order.objects.get(id=o_id)
    response = requests.post(url, payload, headers=headers)
    resp_dict = response.json()
    if resp_dict.get("token"):
        success = True
        order_obj.ordered = 1
        order_obj.save()
        cartItems = Cart.objects.filter(user=request.user)
        for item in cartItems:
            item.purchased = True
            item.save()
    else:
        success = False
    data = {
        "success": success
    }
    return JsonResponse(data)


def admin(request):
    shipping = shipment.objects.all()
    context = {
        "shipping": shipping,
    }
    return render(request, 'admin.html', context)


def pan():
    return "kfdslkdslk"