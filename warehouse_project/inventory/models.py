from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
# Відділ
class Department(models.Model):
    name = models.CharField(_("Назва відділу"),max_length=255)
    address = models.CharField(_("Адреса відділу"),max_length=255)
    def __str__(self): return self.name
# Постачальник
class Suppliers(models.Model):
    name = models.CharField(_("Назва постачальника"),max_length=255)
    contact_person = models.CharField(_("Відповідальна особа"),max_length=255)
    phone = models.CharField(_("Телефон"),max_length=20)
    email = models.EmailField(_("Е-маіл"))
    address = models.CharField(_("Адреса"),max_length=255)
    def __str__(self): return self.name
# Одиниці виміру
class Units(models.Model):
    name = models.CharField(_("Назва одиниці"),max_length=50)
    short_name = models.CharField(_("Скорочення"),max_length=10)
    def __str__(self): return self.short_name
# Товари
class Goods(models.Model):
    name = models.CharField(_("Назва товару"),max_length=255)
    unit = models.ForeignKey(Units, on_delete=models.CASCADE)
    def __str__(self): return self.name
# Накладна
class Invoice(models.Model):
    data = models.DateField(_("Дата"),)
    suppliers = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    def __str__(self): return f"Накладна №{self.id} від {self.data}"
# залишки
class Stock(models.Model):
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    amount = models.IntegerField(_("Кількість"),default=0)
    class Meta:
        unique_together = ('goods', 'department')
    def __str__(self): return f"{self.goods} у {self.department}: {self.amount}"
# Деталі приходу
class ArrivalDetails(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    amount = models.IntegerField(_("Кількість"),)
    price_for_unit = models.DecimalField(_("Ціна за одиницю"),max_digits=10, decimal_places=2)
    overall_price = models.DecimalField(_("Загальна ціна"),
        max_digits=10,
        decimal_places=2,
        editable=False,
        null=True,
        blank=True
    )
    def save(self, *args, **kwargs):
        if self.amount and self.price_for_unit:
            self.overall_price = self.amount * self.price_for_unit
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.goods.name} ({self.amount})"
# Обробка для створення нових Деталей і збереження даних до Залишків
@receiver(post_save, sender=ArrivalDetails)
def update_stock(sender, instance, created, **kwargs):
    if created:
        department = instance.invoice.department
        goods = instance.goods
        obj, created_stock = Stock.objects.get_or_create(
            goods=goods,
            department=department,
            defaults={'amount': 0}
        )
        obj.amount += instance.amount
        obj.save()

@receiver(post_save, sender=User)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        group, _ = Group.objects.get_or_create(name='User')
        instance.groups.add(group)

class UserSessionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True) # Тривалість сесії
    def __str__(self):
        return f"{self.user.username} - {self.login_time}"

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    log = UserSessionLog.objects.create(user=user)
    request.session['current_session_log_id'] = log.id