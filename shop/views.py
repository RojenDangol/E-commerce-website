from django.shortcuts import render
from django.http import HttpResponse
from math import ceil
from .models import Product, Contact, Orders, OrderUpdate, Profile
import json
from django.shortcuts import redirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import CustomUserCreationForm
# from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))

    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    # params = {'no_of_slides': nSlides, 'range': range(1, nSlides), 'product': products}
    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]
    params = {'allProds': allProds}
    return render(request, "shop/index.html", params)


def searchMatch(query, item):
    # return true only if query matches them item
    query = query.lower()
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, 'msg': ""}
    if len(allProds) == 0 or len(query) < 4:
        params = {'msg': "Please make sure to enter relevant search query."}
        # return render(request, "shop/index.html", params)
    return render(request, "shop/search.html", params)


def about(request):
    return render(request, "shop/about.html")


@login_required
def contact(request):
    success = False
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        success = True
        messages.success(request, "Thank you for your feedback.")
    return render(request, 'shop/contact.html',{'success': success})
    # return render(request, "shop/contact.html", )


@login_required
def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({'status': 'success', 'updates': updates, 'itemsJson': order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status": "No item"}')
        except Exception as e:
            return HttpResponse('{"status": "Error"}')
    return render(request, "shop/tracker.html")


def prodView(request,myid):
    # Fetch the product using id
    product = Product.objects.filter(id=myid)
    return render(request, "shop/prodView.html", {'product': product[0]})


@login_required
def checkout(request):
    thank = False
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address,
                       city=city, state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = str(order.order_id)
        messages.warning(request, "Thanks for ordering with us. Your order id is"+id+". Use it to track your order using our tracker.")
        return render(request, "shop/checkout.html", {'thank': thank, 'id': id})
    #     Request paytm to transfer the amount to your account after paytm by user
    return render(request, "shop/checkout.html")

# @csrf_exempt
# def handlerequest(request):
#     # paytm will send you post request here
#     pass


# def registerUser(request):
#     taken = False
#     reg = False
#     if request.method == "POST":
#         fname = request.POST.get('firstName', '')
#         lname = request.POST.get('lastName', '')
#         username = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#         email = request.POST.get('email', '')
#         address = request.POST.get('address', '')
#         phone = request.POST.get('phone', '')
#         users = Profile.objects.filter(username=username)
#         # print(users)
#         if len(users) > 0:
#             taken = True
#             return render(request, "shop/register.html", {'taken': taken, 'msg': 'Username already taken. Please enter another one.'})
#         else:
#             user = Profile(firstName=fname, lastName=lname, username=username, email=email, phone=phone, address=address)
#             user.set_password(password)
#             user.save()
#             reg = True
#             return render(request, "shop/register.html", {'reg': reg})
#     return render(request, "shop/register.html")


# def login_view(request):
#     if request.method == "POST":
#         username = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#
#         # Find the user by email
#         user = Profile.objects.filter(username=username).first()
#         # user = authenticate(request, email=email, password=password)
#
#         if user and user.check_password(password):
#             # login(request, user)
#             validUser = True
#             return render(request, "shop/login.html", {'validUser': validUser})
#         else:
#             validUser = False
#             return render(request, "shop/login.html", {'validUser': validUser})
#
#     return render(request, "shop/login.html")

def login_view(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('/shop')

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        try:
            user = User.objects.get(username=username)
        except:
            messages.warning(request, 'username does not exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,"Welcome to My Awesome Cart.")
            return redirect('/shop')
        else:
            messages.warning(request,"Username or Password is incorrect")

    return render(request, 'shop/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('/shop/')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User Successfully Registered.')

            login(request, user)
            return redirect('/shop')
        else:
            messages.error(request, 'An Error Occurred During Registration.')
    context = {'page': page, 'form': form}
    return render(request, 'shop/login.html', context)
