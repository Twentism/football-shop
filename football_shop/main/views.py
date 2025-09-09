from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'app_name' : 'Football Shop',
        'name': 'Melanton Gabriel Siregar',
        'class': 'PBP KI'
    }

    return render(request, "main.html", context)