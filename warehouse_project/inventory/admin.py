from django.contrib import admin
from .models import Department, Suppliers, Units, Goods, Invoice, Stock, ArrivalDetails
from .models import UserSessionLog

admin.site.register(Department)
admin.site.register(Suppliers)
admin.site.register(Units)
admin.site.register(Goods)
admin.site.register(Invoice)
admin.site.register(Stock)
admin.site.register(ArrivalDetails)

@admin.register(UserSessionLog)
class UserSessionLogAdmin(admin.ModelAdmin):
    # Відображаємо колонки, включаючи роль користувача
    list_display = ('user', 'get_role', 'login_time', 'logout_time', 'duration')
    list_filter = ('user__groups', 'login_time') # Фільтр за групами (Менеджери/Юзери)

    def get_role(self, obj):
        return ", ".join([g.name for g in obj.user.groups.all()])
    get_role.short_description = 'Роль'