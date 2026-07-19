from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Medicine
from .forms import MedicineForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')


def contact_us(request):
    return render(request, 'contactus.html')


@login_required
def medicine_list(request):
    medicines = Medicine.objects.all()
    paginator = Paginator(medicines, 3)  # Show 5 medicines per page
    page_number = request.GET.get('page')  # Get the current page number from the query string
    page_obj = paginator.get_page(page_number)

    # Check if the request is an Ajax request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'medicines': list(page_obj.object_list.values()),
            'has_next': page_obj.has_next(),
        }
        return JsonResponse(data)

    return render(request, 'medicine_list.html', {'page_obj': page_obj})



def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('medicine_list')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medicine_list')
    else:
        form = MedicineForm()
    return render(request, 'add_medicine.html', {'form': form})


@login_required
def update_medicine(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            return redirect('medicine_list')
    else:
        form = MedicineForm(instance=medicine)
    return render(request, 'update_medicine.html', {'form': form})


@login_required
def delete_medicine(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        medicine.delete()
    #return HttpResponse(status=405)
        return redirect('medicine_list')
    return render(request, 'delete_medicine.html', {'medicine': medicine})


@login_required
def view_medicine(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    return render(request, 'medicineinfo.html', {'medicine': medicine})



def live_search(request):
    if 'query' in request.GET:
        query = request.GET['query']
        # Filter bookmarks based on the search query
        medicines = Medicine.objects.filter(name__icontains=query)
        # Prepare the response data
        results = [{"name": medicine.name, "price": medicine.price} for medicine in medicines]
        return JsonResponse({'results': results})
    return JsonResponse({'results':[]})