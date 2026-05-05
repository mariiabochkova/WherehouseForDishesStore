from django.contrib.auth import views as auth_views
from django.urls import path, include

from . import views
from .forms import MyPasswordChangeForm, MyLoginForm

urlpatterns = [
    # Товари
    path('goods/', views.goods_list, name='goods_list'),
    path('goods/create/', views.goods_create, name='goods_create'),
    path('goods/<int:pk>/edit/', views.goods_update, name='goods_edit'),
    path('goods/<int:pk>/delete/', views.GoodsDeleteView.as_view(), name='goods_delete'),

    # Відділи
    path('department/', views.department_list, name='department_list'),
    path('department/create/', views.departments_create, name='department_create'),
    path('department/<int:pk>/edit/', views.DepartmentUpdateView.as_view(), name='dept_edit'),
    path('department/<int:pk>/delete/', views.DepartmentDeleteView.as_view(), name='dept_delete'),

    # Постачальники
    path('suppliers/', views.suppliers_list, name='suppliers_list'),
    path('suppliers/create/', views.suppliers_create, name='suppliers_create'),
    path('suppliers/<int:pk>/edit/', views.SuppliersUpdateView.as_view(), name='suppliers_edit'),
    path('suppliers/<int:pk>/delete/', views.SuppliersDeleteView.as_view(), name='suppliers_delete'),

    # Накладні
    path('invoice/', views.invoice_list, name='invoice_list'),
    path('invoice/create/', views.invoice_create, name='invoice_create'),
    path('invoice/<int:pk>/edit/', views.InvoiceUpdateView.as_view(), name='invoice_edit'),
    path('invoice/<int:pk>/delete/', views.InvoiceDeleteView.as_view(), name='invoice_delete'),

    # Залишки
    path('stock/', views.stock_list, name='stock_list'),

    # Одиниці
    path('units/', views.units_list, name='units_list'),
    path('units/create/', views.units_create, name='units_create'),
    path('units/<int:pk>/edit/', views.UnitsUpdateView.as_view(), name='units_edit'),
    path('units/<int:pk>/delete/', views.UnitsDeleteView.as_view(), name='units_delete'),

    # Деталі приходу
    path('invoice/<int:invoice_id>/details/', views.details_list, name='details_list'),
    path('invoice/<int:invoice_id>/details/create/', views.details_create, name='details_create'),
    path('invoice/<int:invoice_id>/details/<int:pk>/edit/', views.ArrivalDetailsUpdateView.as_view(), name='details_edit'),
    path('invoice/<int:invoice_id>/details/<int:pk>/delete/', views.ArrivalDetailsDeleteView.as_view(), name='details_delete'),

    # Юзери
    path('', views.goods_list, name='goods_list'),
    path('register/', views.register, name='register'),
    # Реєстрація
    path('register/', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('profile/', views.profile_view, name='profile'),
    path('profile/change-username/', views.change_username, name='change_username'),

    # Вбудоване представлення для зміни пароля
    path('profile/change-password/', auth_views.PasswordChangeView.as_view(
        form_class=MyPasswordChangeForm,
        template_name='registration/change_password.html',
        success_url='/profile/'
    ), name='password_change'),

    path('i18n/', include('django.conf.urls.i18n')),

    path('accounts/login/', auth_views.LoginView.as_view(
    form_class=MyLoginForm,
    template_name='registration/login.html'
    ), name='login'),
]