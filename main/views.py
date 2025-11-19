from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from main.forms import ProductForm
from main.models import Product
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.html import strip_tags
from django.core import serializers
import requests
import datetime
import json

# Create your views here.
@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")  # default 'all'

    if filter_type == "all":
        products = Product.objects.all()
    else:
        products = Product.objects.filter(user=request.user)

    context = {
        'app_name' : 'Football Shop',
        'name': request.user.username,
        'class': 'PBP KI',
        'product_list': products,
        'last_login': request.COOKIES.get('last_login', 'Never'),
    }

    # Check for a toast message from a previous page (like login)
    if 'toast_message' in request.session:
        context['toast_message'] = request.session['toast_message']
        del request.session['toast_message']
        
    return render(request, "main.html", context)

def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product_entry = form.save(commit = False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_product.html", context)

@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.increment_views()

    context = {
        'product': product
    }
    return render(request, "product_detail.html", context)

def show_xml(request):
    product_list = Product.objects.all()
    xml_data = serializers.serialize("xml", product_list)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    product_list = Product.objects.all()
    data = [
        {
            'id': str(product.id),
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'category': product.category,
            'thumbnail': product.thumbnail,
            'is_featured': product.is_featured,
            'is_hot': product.is_hot,
            'views': product.views,
            'user_id': product.user.id if product.user else None,
        }
        for product in product_list
    ]

    return JsonResponse(data, safe=False)

def show_xml_by_id(request, pk):
    try:
        product_item = Product.objects.get(pk=pk)
        xml_data = serializers.serialize("xml", [product_item])
        return HttpResponse(xml_data, content_type="application/xml")
    except Product.DoesNotExist:
        return HttpResponse(status=404)

def show_json_by_id(request, pk): 
    try:
        # And use 'pk' in the query as well
        product = Product.objects.select_related('user').get(pk=pk) 
        data = {
            'id': str(product.id),
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'category': product.category,
            'thumbnail': product.thumbnail,
            'is_featured': product.is_featured,
            'is_hot': product.is_hot,
            'views': product.views,
            'user_id': product.user_id,
            'user_username': product.user.username if product.user_id else None,
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)
    
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)
    context = {'form': form}
    
    # Check for an incoming toast message from register or logout
    if 'toast_message' in request.session:
        context['toast_message'] = request.session.pop('toast_message')

    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        
        # This is for the non-AJAX form submission, which we'll unify just in case
        request.session['toast_message'] = {"text": "Logged in successfully!", "type": "success"}
        
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response

    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    
    # This correctly sets the session message before redirecting
    request.session['toast_message'] = {"text": "You have been successfully logged out.", "type": "info"}

    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return redirect(reverse('main:show_main'))

@login_required
@csrf_exempt # Add this decorator since you're using fetch POST
def add_product_entry_ajax(request):
    if request.method == 'POST':
        name = strip_tags(request.POST.get("name"))
        price = request.POST.get("price")
        description = strip_tags(request.POST.get("description"))
        category = strip_tags(request.POST.get("category"))
        thumbnail = strip_tags(request.POST.get("thumbnail"))
        
        # FIXED: Check for the string 'true' from the form data
        is_featured = request.POST.get("is_featured") == 'true'
        user = request.user

        new_product = Product.objects.create(
            name=name,
            price=price,
            description=description,
            category=category,
            thumbnail=thumbnail,
            is_featured=is_featured,
            user=user
        )

        # IMPORTANT: We no longer need serializers.serialize.
        # Returning the data in the same format as your show_json view makes your API consistent.
        data = {
            'id': str(new_product.id),
            'name': new_product.name,
            'price': new_product.price,
            'description': new_product.description,
            'category': new_product.category,
            'thumbnail': new_product.thumbnail,
            'is_featured': new_product.is_featured,
            'is_hot': new_product.is_hot,
            'views': new_product.views,
            'user_id': new_product.user.id if new_product.user else None,
        }
        
        return JsonResponse(data, status=201)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

@csrf_exempt
@require_POST
def update_product_ajax(request, id):
    try:
        product = Product.objects.get(pk=id)
        product.name = strip_tags(request.POST.get("name"))
        product.description = strip_tags(request.POST.get("description"))
        product.price = request.POST.get("price")
        product.category = strip_tags(request.POST.get("category"))
        product.thumbnail = strip_tags(request.POST.get("thumbnail"))
        product.is_featured = request.POST.get("is_featured") == 'true'
        product.is_hot = request.POST.get("is_hot") == 'true'
        product.save()
        return JsonResponse({"status": "success", "message": "Product updated!"})
    except Product.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Product not found!"}, status=404)

@csrf_exempt
@require_POST
def delete_product_ajax(request, id):
    try:
        product = Product.objects.get(pk=id)
        product.delete()
        return JsonResponse({"status": "success", "message": "Product deleted!"})
    except Product.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Product not found!"}, status=404)
    
@csrf_exempt
@require_POST
def ajax_login_user(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(username=username, password=password)

    if user:
        login(request, user)

        # Optionally set last_login cookie using response if you plan to redirect later
        request.session['toast_message'] = {"text": "Logged in successfully!", "type": "success"}
        request.session.save()

        # Return JSON with message and optional user info (client uses it)
        return JsonResponse({"status": "success", "message": "Logged in successfully!"})
    else:
        return JsonResponse({"status": "error", "message": "Invalid username or password"}, status=400)

@csrf_exempt
@require_POST
def ajax_register_user(request):
    username = request.POST.get("username")
    password1 = request.POST.get("password1")
    password2 = request.POST.get("password2")

    if not username or not password1 or not password2:
        return JsonResponse({"status": "error", "message": "Missing fields"}, status=400)

    if password1 != password2:
        return JsonResponse({"status": "error", "message": "Passwords do not match!"}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({"status": "error", "message": "Username already exists!"}, status=400)

    # Create user
    User.objects.create_user(username=username, password=password1)

    request.session['toast_message'] = {"text": "Account created! Please log in.", "type": "success"}
    request.session.save()

    return JsonResponse({"status": "success", "message": "Account created! Please log in."})

def proxy_image(request):
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse('No URL provided', status=400)
    
    try:
        # Fetch image from external source
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Return the image with proper content type
        return HttpResponse(
            response.content,
            content_type=response.headers.get('Content-Type', 'image/jpeg')
        )
    except requests.RequestException as e:
        return HttpResponse(f'Error fetching image: {str(e)}', status=500)

@csrf_exempt
def create_product_flutter(request):
    """Create a product from a Flutter mobile app client.
    
    Expects JSON POST with fields: name, price, description, category,
    thumbnail, is_featured (optional). Returns JSON with status.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = strip_tags(data.get("name", ""))
            price = data.get("price", "")
            description = strip_tags(data.get("description", ""))
            category = data.get("category", "")
            thumbnail = data.get("thumbnail", "")
            is_featured = data.get("is_featured", False)
            user = request.user
            
            new_product = Product(
                name=name,
                price=price,
                description=description,
                category=category,
                thumbnail=thumbnail,
                is_featured=is_featured,
                user=user
            )
            new_product.save()
            
            return JsonResponse({"status": "success", "message": "Product created successfully!"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)