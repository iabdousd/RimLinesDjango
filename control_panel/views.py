import datetime

from django.shortcuts import render, redirect

from django.utils import timezone

from .decorators import unauthenticated_required, role_required
from .models import *
from .forms import *
from .filters import ProductFilter

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required(login_url='login')
@role_required(allowed_roles=['admin', 'coordinator'])
def dashboard(request):
    restricted = ['coordinator']
    if request.user.groups.exists():
        groups = request.user.groups.all()
        for group in groups:
            for role in restricted:
                if group.name == role:
                    return redirect('orders')
    else:
        return redirect('home')

    products_ = Product.objects.all()
    customers_ = Customer.objects.all()
    orders_ = Order.objects.all()
    pending_orders = Order.objects.filter(status__in=["Out for delivery", "Pending"]).count()
    delivered_orders = Order.objects.filter(status="Delivered").count()
    orders_this_week = Order.objects.filter(date_created__range=[timezone.now() - datetime.timedelta(days=7), timezone.now()]).count()
    orders_this_month = Order.objects.filter(date_created__range=[timezone.now() - datetime.timedelta(days=30), timezone.now()]).all()
    earnings_month = 0
    users = User.objects.all()
    for order_ in orders_this_month:
        earnings_month += order_.quantity * order_.product.price

    context = {
        "products": products_,
        "customers": customers_,
        "orders": orders_,
        "pending_orders": pending_orders,
        "delivered_orders": delivered_orders,
        "orders_this_week": orders_this_week,
        "earnings_month": earnings_month,
        "users": users,
        "roles": Group.objects.all(),
    }

    return render(request, 'control_panel/index.html', context)


@unauthenticated_required
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.groups.all()[0].name == 'customer':
                return redirect('home')
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid Username / Password")

    context = {}
    return render(request, 'control_panel/login.html', context)


@unauthenticated_required
def register_page(request):
    form = CreateUserForm

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            login(user)
            return redirect('home')
        else:
            if form.cleaned_data.get('password1') != form.cleaned_data.get('password2'):
                messages.error(request, "Passwords don't match.")
            else:
                messages.error(request, "Username already exists.")

    context = {"form": form}
    return render(request, 'control_panel/register.html', context)


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
@role_required(allowed_roles=['admin', 'coordinator'])
def customers(request):
    customers_ = Customer.objects.all()
    context = {'customers': customers_}
    return render(request, 'control_panel/customers.html', context)


@login_required(login_url='login')
@role_required(allowed_roles=['admin', 'coordinator'])
def products(request):
    products_ = Product.objects.all()
    product_filter = ProductFilter(request.GET, queryset=products_)
    products_ = product_filter.qs
    context = {"products": products_, 'filter': product_filter}
    return render(request, 'control_panel/products.html', context)


@login_required(login_url='login')
@role_required(allowed_roles=['admin', 'coordinator'])
def orders(request):
    orders_ = Order.objects.all().order_by('-id')

    page = request.GET.get('page', 1)
    paginator = Paginator(orders_, 10)
    try:
        orders_ = paginator.page(page)
    except PageNotAnInteger:
        orders_ = paginator.page(1)
    except EmptyPage:
        orders_ = paginator.page(paginator.num_pages)

    context = {"orders": orders_}
    return render(request, 'control_panel/orders.html', context)


@login_required(login_url='login')
@role_required(allowed_roles=['admin', 'coordinator'])
def customer(request, customer_id):
    customer_ = Customer.objects.get(id=customer_id)
    orders_ = customer_.order_set.all()
    context = {'customer': customer_, 'orders': orders_}
    return render(request, 'control_panel/customer.html', context)


@login_required(login_url='login')
@role_required(allowed_roles=['admin', 'coordinator'])
def product(request, product_id):
    product_ = Product.objects.get(id=product_id)
    orders_ = product_.order_set.all()
    context = {'product': product_, 'orders': orders_}
    return render(request, 'control_panel/product.html', context)


@login_required(login_url='login')
@role_required(allowed_roles=['admin', 'coordinator'])
def order(request, order_id):
    order_ = Order.objects.get(id=order_id)
    context = {'order': order_, 'card': order_.giftcard_set.all()}
    return render(request, 'control_panel/order.html', context)


@login_required(login_url='login')
@role_required(allowed_roles=['admin'])
def add_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {"form": form}
    return render(request, 'control_panel/product_form.html', context)


@login_required(login_url='login')
@role_required(allowed_roles=['admin'])
def edit_product(request, product_id):
    product_ = Product.objects.get(id=product_id)
    form = ProductForm(instance=product_)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product_)
        if form.is_valid():
            form.save()
            return redirect('/cp')
        else:
            print("Error", form.errors)
    context = {'form': form}
    return render(request, 'control_panel/product_form.html', context)


@login_required(login_url='login')
@role_required(allowed_roles=['admin'])
def delete_product(request, product_id):
    if request.method == 'POST':
        product_ = Product.objects.get(id=product_id)
        product_.delete()
        return redirect('/cp')


@login_required(login_url='login')
@role_required(allowed_roles=['admin'])
def gift_cards(request):
    giftCards = GiftCard.objects.all()
    context = {'cards': giftCards}
    return render(request, 'control_panel/cards.html', context)


@login_required(login_url='login')
@role_required(allowed_roles=['admin', 'coordinator'])
def gift_card(request, giftCard_id):
    giftCard = GiftCard.objects.get(id=giftCard_id)
    context = {'card': giftCard}
    return render(request, 'control_panel/card.html', context)


@login_required(login_url='login')
@role_required(allowed_roles=['admin'])
def add_gift_cards(request):
    form = GiftCardForm()
    if request.method == 'POST':
        form = GiftCardForm(request.POST)
        if form.is_valid():
            giftCard = form.save()
            giftCard.date_created = timezone.now()
            orders_ = Order.objects.filter(status='Pending', product=giftCard.product)
            for order_ in orders_:
                giftCard.order = order_
                giftCard.used = True
                order_.save()
                if order_.quantity == order_.giftcard_set.count():
                    order_.status = 'Delivered'
                    order_.save()

            giftCard.save()
            return redirect('giftcards')

    context = {"form": form}
    return render(request, 'control_panel/giftcard_form.html', context)


@login_required(login_url='login')
@role_required(allowed_roles=['admin', 'coordinator'])
def add_order(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            customer_number = form.cleaned_data['customer_number']
            customer_name = form.cleaned_data['customer_name']
            from_destination = form.cleaned_data['from_destination']
            quantity = form.cleaned_data['quantity']
            product = form.cleaned_data['product']

            customer_id = ''
            if 'PUBG' in product.name:
                customer_id = form.cleaned_data['customer_id']

            method = form.cleaned_data['method']
            # status = form.cleaned_data['status']
            verified = form.cleaned_data['verified']
            customer_ = Customer.create(customer_name, customer_number, '', timezone.now())
            if Customer.objects.filter(phone=customer_number).count() == 0:
                customer_ = customer_.save()

            else:
                customer_ = Customer.objects.get(phone=customer_number)
                if customer_name and customer_name != '':
                    customer_.name = customer_name
                    customer_.save()

            total_price = product.price * quantity
            transaction_cred_ = TransactionCredentials.create(method, timezone.now(), customer_number, from_destination, total_price)
            transaction_cred_.save()
            transaction_ = Transaction.create(transaction_cred_, timezone.now(), verified)
            transaction_.save()
            order_ = Order.create(customer=customer_, product=product, date_created=timezone.now(), quantity=quantity, status='Delivered' if verified else 'Out for delivery', transaction=transaction_, customer_id=customer_id)
            order_.save()
            unused_gift_cards = GiftCard.objects.filter(product=product, used=False).all()
            if not unused_gift_cards:
                order_.status = 'Pending'
                order_.save()
                return redirect('order', order_.id)
            unused_gift_card = unused_gift_cards[0]
            unused_gift_card.order = Order.objects.get(id=order_.id)
            unused_gift_card.used = True
            unused_gift_card.save()
            if verified:
                order_.status = 'Delivered'
            else:
                order_.status = 'Out for delivery'
            order_.save()

            return redirect('order', order_.id)

    context = {"form": form}
    return render(request, 'control_panel/order_form.html', context)


@login_required(login_url='login')
@role_required(allowed_roles=['admin'])
def transactions(request):
    transactions_ = Transaction.objects.all()
    context = {'transactions': transactions_}
    return render(request, 'control_panel/transactions.html', context)

