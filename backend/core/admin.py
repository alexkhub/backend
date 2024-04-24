from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin


class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone', 'is_staff', 'phone', 'telegram_id')
    list_display_links = ('id', 'username', 'email', 'phone',)
    search_fields = ('id', 'username', 'phone', 'email')
    list_filter = ('is_staff',)



class OrderAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user', 'delivery_date', 'status', 'expiration_date', 'order_size')
    search_fields = ('user__username', 'user__phone')
    list_filter = ('status', 'order_size', 'delivery_date')
    list_editable = ('expiration_date',)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'rating')
    search_fields = ('user__username',)


class CellAdmin(ImportExportModelAdmin):
    list_display = ('id', 'get_orders', 'free_place')
    list_filter = ('free_place',)

    @admin.display(description='Заказы')
    def get_orders(self, obj):
        return [order.pk for order in obj.orders.all()]


class RackAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'get_cell')
    list_filter = ('employee',)
    search_fields = ('employee__user__username',)

    @admin.display(description='Стеллажи')
    def get_cell(self, obj):
        return [cell.pk for cell in obj.cells.all()]


class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'area')
    search_fields = ('address',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'employee', 'date', 'text', 'rating')
    list_filter = ('rating',)
    search_fields = ('employee__user__username', 'user__username', 'text')


admin.site.register(User, UsersAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Cell, CellAdmin)
admin.site.register(Rack, RackAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Comment, CommentAdmin)
