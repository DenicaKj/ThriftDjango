from pyexpat.errors import messages
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.forms import formset_factory
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from Thrift.forms import NewUserForm, StyledAuthenticationForm, ProductForm, ImageFormSet, ImageForm, ProductFormEdit
from Thrift.models import Product, Favorites, ShoppingCart, CustomUser, ShoppingItem, Order, Comment, ImageProd, \
    Delivery
from django.contrib.auth.decorators import login_required

def index(request):
    user=request.user
    if user.is_anonymous:
        queryset = Product.objects.filter(sold=False).all()[:5]
        context = {"products": queryset}
    else:
        queryset = Product.objects.filter(sold=False).exclude(user=request.user).all()[:5]
        fav = Favorites.objects.filter(user=request.user).all()
        favorites_ = []
        for f in fav:
            favorites_.append(f.product)
        cart_ = ShoppingCart.objects.filter(user=request.user).first()
        prod = ShoppingItem.objects.filter(cart=cart_).all()
        products = []
        for p in prod:
            if not p.item.sold:
                products.append(p.item)
        context = {"products": queryset,'cartItems':products,'favorites':favorites}
    return render(request, "index.html", context=context)


def female(request):
    if request.user.is_anonymous:
        queryset = Product.objects.filter(gender='F', sold=False).all()
        context = {"products": queryset}
    else:
        queryset = Product.objects.filter(gender='F',sold=False).exclude(user=request.user).all()
        user = request.user
        fav = Favorites.objects.filter(user=request.user).all()
        favorites_=[]
        for f in fav:
            if not f.product.sold:
                favorites_.append(f.product)
        cart_ = ShoppingCart.objects.filter(user=request.user).first()
        prod = ShoppingItem.objects.filter(cart=cart_).all()
        products = []
        for p in prod:
            if not p.item.sold:
                products.append(p.item)
        context = {"products": queryset,'user':user,'favorites':favorites,'cartItems':products}
    return render(request, "female.html", context=context)

def product_details(request, pk):
    if request.user.is_anonymous:
        product = get_object_or_404(Product, pk=pk)
        context = {
            'product': product,
            'userProduct': product.user
        }
    else:
        product = get_object_or_404(Product, pk=pk)
        logged_in=request.user
        fav = Favorites.objects.filter(user=request.user).all()
        favorites = []
        for f in fav:
            if not f.product.sold:
                favorites.append(f.product)
        cart = ShoppingCart.objects.filter(user=request.user).first()
        prod = ShoppingItem.objects.filter(cart=cart).all()
        products = []
        for p in prod:
            if not p.item.sold:
                products.append(p.item)
        colors=product.colors.all()
        context = {
            'logged_in':logged_in,
        'product': product,
        'favorites':favorites,
        'cartItems':products,
        'userProduct':product.user
        }
    return render(request, 'product_details.html', context)

@login_required()
def profile(request, pk):
    user = get_object_or_404(CustomUser, id=pk)
    products = Product.objects.filter(user=user,sold=False).all()
    comments = Comment.objects.filter(userTo=user).all()
    context={'userProfile':user,'logged_in':request.user,'products':products,'comments':comments}
    return render(request, 'profile.html',context)

@login_required()
def for_sending(request):
    orders = Order.objects.filter(user=request.user).all()
    products=[]
    for o in orders:
        if o.product.sold and not o.product.sent:
            products.append(o.product)
    context={'products':products}
    return render(request, 'for_sending.html',context)
@login_required()
def sent(request):
    orders = Order.objects.filter(user=request.user).all()
    products = []
    for o in orders:
        if o.product.sold and o.product.sent and not o.product.accepted:
            products.append(o.product)
    context={'products':products}
    return render(request, 'sent.html',context)
@login_required()
def sent_2(request):
    products = Product.objects.filter(user=request.user, sold=True, sent=True,accepted=False).all()
    context={'products':products}
    return render(request, 'sent_2.html',context)
@login_required()
def sold(request):
    products = Product.objects.filter(user=request.user, sold=True, sent=False, accepted=False).all()
    context = {'products': products}
    return render(request, 'sold.html', context)
@login_required()
def accepted(request):
    products = Product.objects.filter(user=request.user, sold=True, sent=True, accepted=True).all()
    context = {'products': products}
    return render(request, 'accepted.html', context)
@login_required()
def all_bought(request):
    orders = Order.objects.filter(user=request.user).all()
    products = []
    for o in orders:
        if o.product.sold:
            products.append(o.product)
    context = {'products': products}
    return render(request, 'all_bought.html', context)
@login_required()
def all_sold(request):
    products = Product.objects.filter(user=request.user, sold=True).all()
    context = {'products': products}
    return render(request, 'all_sold.html', context)
@login_required()
def buy_products(request):
    if request.method=='POST':
        cart = ShoppingCart.objects.filter(user=request.user).first()
        prod = ShoppingItem.objects.filter(cart=cart).all()
        phone=request.POST.get('phone')
        address = request.POST.get('address')
        postal = request.POST.get('postal')
        city = request.POST.get('city')
        delivery=Delivery(cart=cart,phone=phone,address=address,postal=postal,city=city)
        delivery.save()
        for p in prod:
            p.item.sold=True
            p.item.save()
            order=Order(user=request.user,product=p.item,date_order=datetime.now())
            order.save()
        shoppingCart = ShoppingCart.objects.all().filter(user=request.user).first()
        shoppingCart.user = None
        shoppingCart.save()
        create_new_shopping_cart_for_user(request.user)
    return render(request,'successful_order.html')

@login_required()
def delivery_info(request,pk):
    prod=Product.objects.filter(id=pk).first()
    cart=ShoppingItem.objects.filter(item=prod).first().cart
    delivery=Delivery.objects.filter(cart=cart,finished=False).first()
    user=Order.objects.filter(product=prod).first().user
    return render(request,'delivery_info.html',{'delivery':delivery,'product':prod,'userBought':user})




@login_required()
def arrived_product(request,pk):
    product = Product.objects.filter(id=pk).first()
    product.accepted=True
    product.date_accepted=datetime.now()
    product.save()
    return redirect('arrived')
@login_required()
def sent_product(request,pk):
    product = Product.objects.filter(id=pk).first()
    product.sent=True
    product.date_sent=datetime.now()
    product.save()
    return redirect('sent_2')
@login_required()
def arrived(request):
    orders = Order.objects.filter(user=request.user).all()
    products = []
    for o in orders:
        if o.product.sold and o.product.sent and o.product.accepted:
            products.append(o.product)
    context = {'products': products}
    return render(request, 'arrived.html', context)
@login_required()
def add_comment(request):
    if request.method == 'POST':
        id=request.POST.get('id')
        text=request.POST.get('text')
        userFrom=CustomUser.objects.filter(id=request.user.id).first()
        userTo=CustomUser.objects.filter(id=id).first()
        comment=Comment(userTo=userTo,userFrom=userFrom,text=text,date=datetime.now())
        comment.save()
        return redirect('profile',id)
    return redirect('index')
@login_required()
def delete_comment(request):
    if request.method == 'POST':
        id=request.POST.get('id')
        user=request.POST.get('user')
        Comment.objects.filter(id=id).delete()
        return redirect('profile', user)
    return redirect('index')

@login_required()
def delete_product(request,pk):
    if request.method == 'POST':
        product=Product.objects.filter(id=pk).first()
        Product.objects.filter(pk=pk).delete()
        return redirect('profile', request.user.id)
    return redirect('profile',request.user.id)


@login_required()
def favorites(request):
    user=request.user
    fav = Favorites.objects.filter(user=request.user).all()
    favorites=[]
    for f in fav:
        if not f.product.sold:
            favorites.append(f.product)
    cart = ShoppingCart.objects.filter(user=request.user).first()
    prod = ShoppingItem.objects.filter(cart=cart).all()
    products = []
    for p in prod:
        if not p.item.sold:
            products.append(p.item)
    context = {'user': user, 'favorites': favorites,'cartItems':products}
    return render(request, "favorites.html", context=context)

def male(request):
    if request.user.is_anonymous:
        queryset = Product.objects.filter(gender='M', sold=False).all()
        context = {"products": queryset}
    else:
        queryset = Product.objects.filter(gender='M',sold=False).exclude(user=request.user).all()
        user = request.user
        fav = Favorites.objects.filter(user=request.user).all()
        favorites = []
        for f in fav:
            if not f.product.sold:
                favorites.append(f.product)
        cart = ShoppingCart.objects.filter(user=request.user).first()
        prod = ShoppingItem.objects.filter(cart=cart).all()
        products = []
        for p in prod:
            if not p.item.sold:
                products.append(p.item)
        context = {"products": queryset, 'user': user, 'favorites': favorites, 'cartItems': products}
    return render(request, "female.html", context=context)

@csrf_exempt
def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save()
            user.image = form.cleaned_data['image']
            return redirect("login")
    else:
        form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form":form})

@csrf_exempt
def login_request(request):
    error=False
    if request.method == "POST":
        form = StyledAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                cart = ShoppingCart.objects.filter(
                    user=CustomUser.objects.all().filter(id=form.get_user().id).first()).first()
                if not cart:
                    create_new_shopping_cart_for_user(form.get_user())
                return redirect("index")
            else:
                form = StyledAuthenticationForm()
                error=True
                return render(request=request, template_name="login.html", context={"login_form":form,'error':error})
        else:
            form = StyledAuthenticationForm()
            error = True
            return render(request=request, template_name="login.html", context={"login_form": form, 'error': error})
    form = StyledAuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form,'error':error})

def create_new_shopping_cart_for_user(current_user):
    cart = ShoppingCart(user=CustomUser.objects.all().filter(id=current_user.id).first())
    cart.save()

@csrf_exempt
@login_required
def add_product(request):
    ImageFormSet = formset_factory(ImageForm,extra=3)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user=request.user
            product.sold=False
            product.sent=False
            product.accepted=False
            product.save()
            updated_colors = form.cleaned_data['colors']
            product.colors.set(updated_colors)


            for form in formset:
                image = form.save(commit=False)
                image.product = product
                image.save()
            return render(request,'successful_add.html')
    else:
        form = ProductForm()
        formset = ImageFormSet()
    return render(request, 'add_product.html', {'form': form, 'formset': formset})


def edit_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    ImageFormSet = formset_factory(ImageForm, extra=3)

    if request.method == 'POST':
        form = ProductFormEdit(request.POST, instance=product)
        formset = ImageFormSet(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            ImageProd.objects.filter(product=product).delete()
            for form in formset:

                image = form.save(commit=False)
                image.product = product
                image.save()

            return redirect('product-details',product.id)
    else:
        form = ProductFormEdit(instance=product)
        formset = ImageFormSet()

    return render(request, 'edit_product.html', {'form': form, 'formset': formset})


def payment(request):
    cart = ShoppingCart.objects.filter(user=request.user).first()
    prod = ShoppingItem.objects.filter(cart=cart).all()
    sum = 0
    for p in prod:
        if not p.item.sold:
            sum += p.item.price
    return render(request,'payment.html',{'total':sum})

def logout_request(request):
    logout(request)

    return redirect("index")

@login_required()
def add_to_favorites(request):
    if request.method=='POST' and request.user!=Product.objects.filter(id=int(request.POST.get('id'))).first().user:
        id=int(request.POST.get('id'))
        fav=Favorites()
        fav.user=request.user
        fav.product=Product.objects.filter(id=id).first()
        fav.save()
    else:
        raise Http404("Page not found")
    referer = request.META.get('HTTP_REFERER')
    return redirect(referer)

@login_required()
def remove_from_favorites(request):
    if request.method=='POST':
        product=Product.objects.filter(id=int(request.POST.get('id'))).first()
        Favorites.objects.filter(user=request.user,product=product).delete()

    referer = request.META.get('HTTP_REFERER')
    return redirect(referer)

@login_required()
def cart(request):
    user=request.user
    cart= ShoppingCart.objects.filter(user=request.user).first()
    prod=ShoppingItem.objects.filter(cart=cart).all()
    products=[]
    sum=0
    for p in prod:
        if not p.item.sold:
            products.append(p.item)
            sum+=p.item.price

    fav = Favorites.objects.filter(user=request.user).all()
    favorites = []
    for f in fav:
        if not f.product.sold:
            favorites.append(f.product)
    context = {'user': user, 'products': products,'favorites':favorites,'total':sum,'cartItems':products,'num':len(products)}
    return render(request, "cart.html", context=context)

@login_required()
def add_to_cart(request):
    if request.method=='POST' and request.user!=Product.objects.filter(id=int(request.POST.get('id'))).first().user:
        cart = ShoppingCart.objects.filter(user=request.user).first()
        shopitem=ShoppingItem()
        shopitem.cart=cart
        shopitem.item=Product.objects.filter(id=int(request.POST.get('id'))).first()
        shopitem.save()
    else:
        raise Http404("Page not found")
    referer = request.META.get('HTTP_REFERER')
    return redirect(referer)

@login_required()
def remove_from_cart(request):
    if request.method=='POST':
        cart = ShoppingCart.objects.filter(user=request.user).first()
        product=Product.objects.filter(id=int(request.POST.get('id'))).first()
        ShoppingItem.objects.filter(cart=cart,item=product).delete()
    referer = request.META.get('HTTP_REFERER')
    return redirect(referer)

def error_404(request, exception):
    return render(request, 'error.html', status=404)

def error_500(request):
    return render(request, 'error.html', status=500)
