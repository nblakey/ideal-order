from django.contrib import admin
from orders.models import Employee, Customer, Item, Order, Vendor

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')
    search_fields = ['last_name']

class ItemInline(admin.TabularInline):
    model = Item
    extra = 1

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')
    search_fields = ['last_name']

class OrderAdmin(admin.ModelAdmin):
    #inlines = [ItemInline]
    list_display = ('customer_order_date', 'customer_placed')
    raw_id_fields = ['customer_placed']
    

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Item)
admin.site.register(Vendor)
