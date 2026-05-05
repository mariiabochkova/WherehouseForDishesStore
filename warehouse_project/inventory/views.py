from django.shortcuts import render, redirect, get_object_or_404  # Додано redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import UpdateView, DeleteView, CreateView  # Додано базові класи для CBV
from .forms import RegisterForm
from django.contrib.auth import login
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UsernameChangeForm, MyUserCreationForm
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.utils import timezone
from .models import UserSessionLog

from .models import Goods, Department, Suppliers, Invoice, Stock, Units, ArrivalDetails
from .forms import GoodsForm, DepartmentForm, SuppliersForm, InvoiceForm, UnitsForm, ArrivalDetailsForm
@login_required
def goods_list(request):
    items = Goods.objects.all()  # Отримуємо всі товари з БД
    return render(request, 'inventory/goods_list.html', {'items': items})
def goods_create(request):
    if request.method == "POST":
        form = GoodsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('goods_list')
    else:
        form = GoodsForm()
    return render(request, 'inventory/form.html', {'form': form})
def goods_update(request, pk):
    # Знаходимо товар за ID або видаємо помилку 404
    obj = get_object_or_404(Goods, pk=pk)
    if request.method == "POST":
        form = GoodsForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('goods_list')
    else:
        form = GoodsForm(instance=obj)
    return render(request, 'inventory/form.html', {'form': form})
class GoodsDeleteView(DeleteView):
    model = Goods
    template_name = 'inventory/confirm_delete.html'
    success_url = reverse_lazy('goods_list')
@login_required
def department_list(request):
    items = Department.objects.all()
    return render(request, 'inventory/department_list.html', {'items': items})
def departments_create(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'inventory/form.html', {'form': form})
class DepartmentUpdateView( UpdateView):
    model = Department
    fields = ['name', 'address']
    template_name = 'inventory/form.html'
    success_url = reverse_lazy('department_list')
class DepartmentDeleteView(DeleteView):
    model = Department
    template_name = 'inventory/confirm_delete.html'
    success_url = reverse_lazy('department_list')
@login_required
def suppliers_list(request):
    items = Suppliers.objects.all()
    return render(request, 'inventory/suppliers_list.html', {'items': items})
def suppliers_create(request):
    if request.method == "POST":
        form = SuppliersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('suppliers_list')
    else:
        form = SuppliersForm()
    return render(request, 'inventory/form.html', {'form': form})
class SuppliersUpdateView(UpdateView):
    model = Suppliers
    fields = ['name', 'contact_person', 'phone', 'email', 'address']
    template_name = 'inventory/form.html'
    success_url = reverse_lazy('suppliers_list')
class SuppliersDeleteView(DeleteView):
    model = Suppliers
    template_name = 'inventory/confirm_delete.html'
    success_url = reverse_lazy('suppliers_list')
@login_required
def invoice_list(request):
    items = Invoice.objects.all()
    return render(request, 'inventory/invoice_list.html', {'items': items})
def invoice_create(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('invoice_list')
    else:
        form = InvoiceForm()
    return render(request, 'inventory/form.html', {'form': form})
class InvoiceUpdateView(UpdateView):
    model = Invoice
    fields = ['data', 'suppliers', 'department']
    template_name = 'inventory/form.html'
    success_url = reverse_lazy('invoice_list')
class InvoiceDeleteView(DeleteView):
    model = Invoice
    template_name = 'inventory/confirm_delete.html'
    success_url = reverse_lazy('invoice_list')
@login_required
def stock_list(request):
    items = Stock.objects.all()
    return render(request, 'inventory/stock_list.html', {'items': items})
@login_required
def units_list(request):
    items = Units.objects.all()
    return render(request, 'inventory/units_list.html', {'items': items})
def units_create(request):
    if request.method == "POST":
        form = UnitsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('units_list')
    else:
        form = UnitsForm()
        return render(request, 'inventory/form.html', {'form': form})
class UnitsUpdateView(UpdateView):
    model = Units
    fields = ['name', 'short_name']
    template_name = 'inventory/form.html'
    success_url = reverse_lazy('units_list')
class UnitsDeleteView(DeleteView):
    model = Units
    template_name = 'inventory/confirm_delete.html'
    success_url = reverse_lazy('units_list')
@login_required
def details_list(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    details = ArrivalDetails.objects.filter(invoice=invoice)
    return render(request, 'inventory/details_list.html', {
        'details': details,
        'invoice': invoice
    })
def details_create(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    if request.method == "POST":
        form = ArrivalDetailsForm(request.POST)
        if form.is_valid():
            detail = form.save(commit=False)
            detail.invoice = invoice
            detail.save()
            return redirect('details_list', invoice_id=invoice.id)
    else:
        form = ArrivalDetailsForm()
    return render(request, 'inventory/form.html', {'form': form, 'invoice': invoice})
class ArrivalDetailsUpdateView(UpdateView):
    model = ArrivalDetails
    fields = ['goods', 'amount', 'price_for_unit']
    template_name = 'inventory/form.html'
    def get_success_url(self):
        invoice_id = self.object.invoice.id
        return reverse('details_list', kwargs={'invoice_id': invoice_id})
class ArrivalDetailsDeleteView(DeleteView):
    model = ArrivalDetails
    template_name = 'inventory/confirm_delete.html'
    def get_success_url(self):
        invoice_id = self.object.invoice.id
        return reverse('details_list', kwargs={'invoice_id': invoice_id})



def register(request):
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Автоматичний вхід після реєстрації
            return redirect('goods_list')
    else:
        form = MyUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class GoodsCreateView(PermissionRequiredMixin, CreateView):
    model = Goods
    permission_required = 'inventory.add_goods'
    template_name = 'inventory/goods_form.html'

@login_required
def profile_view(request):
    # Відображає інформацію про логін та групи користувача
    return render(request, 'registration/profile.html')

@login_required
def change_username(request):
    if request.method == 'POST':
        form = UsernameChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Логін успішно змінено!")
            return redirect('profile')
    else:
        form = UsernameChangeForm(instance=request.user)
    return render(request, 'registration/change_username.html', {'form': form})

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    log_id = request.session.get('current_session_log_id')
    if log_id:
        try:
            log = UserSessionLog.objects.get(id=log_id)
            log.logout_time = timezone.now()
            log.duration = log.logout_time - log.login_time
            log.save()
        except UserSessionLog.DoesNotExist:
            pass