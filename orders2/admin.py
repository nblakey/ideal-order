from django.contrib import admin, messages
from django.utils import timezone
from django.http import HttpResponseRedirect
from django import forms
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.forms import ModelForm
from django.contrib.auth.models import User,Group
from orders2.models import Employee, Customer, Item, Order, EmployeeOrder, Vendor

class CreateEmployeeOrderForm(forms.Form):
##    class Meta:
##        model = EmployeeOrder
##        #Add calendar widget in separately
##        exclude = ['employee_order_date']
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        employee_placed = forms.ModelChoiceField(Employee.objects)
        purchase_order_number = forms.CharField(max_length=25)

        STATUS_OF_ORDER = (
            ('ORDR', 'Ordered'),
            ('BACK', 'Backordered'),
            ('UNAV', 'Unavailable')
        )

        status = forms.CharField(max_length=4, widget=forms.Select(choices=STATUS_OF_ORDER))
        comments = forms.CharField(max_length=200, required=False)

def create_employee_order(self, request, queryset):
    index = 0
    checked = False
    vendor_name = ' '
    print(vendor_name)
    
    for item in queryset:
        #Determine brand of first item
        if checked == False:
                vendor_name = item.item.vendor.name
                checked = True
        #Only idle orders should be added to an employee order
        if item.status != 'A_IDLE':
                print("Not idle")
                index = 1
                break
        #Only items of the same brand should be added to an employee order
        elif item.item.vendor.name != vendor_name:
                print("Not same brand")
                index = 1
                break
    if index == 0:
            form = None
            if 'apply' in request.POST:
                form = CreateEmployeeOrderForm(request.POST)
                if form.is_valid():
                    employee = form.cleaned_data['employee_placed']
                    po = form.cleaned_data['purchase_order_number']
                    stat = form.cleaned_data['status']
                    comment = form.cleaned_data['comments']
                    date = timezone.now()

                    #Create EmployeeOrder object
                    employee_order_object = EmployeeOrder()
                    employee_order_object.employee_order_date = date
                    employee_order_object.employee_placed = employee
                    employee_order_object.purchase_order_number = po
                    employee_order_object.status = stat
                    employee_order_object.comments = comment
                    employee_order_object.save()

                    queryset.update(employee_order=employee_order_object)

                    #Update customer order status - will send messages if backordered or NA
                    for item in queryset:
                        if stat == 'ORDR':
                            item.status = 'B_SHIP'
                            item.save()
                        elif stat == 'BACK':
                            item.status = 'D_BACK'
                            item.comments = comment
                            item.save()
                        elif stat == 'UNAV':
                            item.status = 'E_UNAV'
                            item.comments = comment
                            item.save()

                    return HttpResponseRedirect(request.get_full_path())

            if not form:
                form = CreateEmployeeOrderForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
                
            return render_to_response('admin/create_employee_order.html', {'items': queryset,
                                                                           'create_order_form': form},
                                                                          context_instance=RequestContext(request))
        
create_employee_order.short_description = "Create employee order with selected orders"

#Save item to call post_save function
def mark_as_arrived(modeladmin, request, queryset):

    index = 0

    #Only certain items can be checked in
    for item in queryset:
        if item.status != 'A_IDLE' and item.status != 'B_SHIP' and item.status != 'D_BACK':
                index = 1
    if index == 0:
        for item in queryset:
                item.status = 'C_PICK'
                item.save()
        
mark_as_arrived.short_description = "Mark selected orders as arrived"

#Update item status
def mark_as_picked_up(modeladmin, request, queryset):

    index = 0

    for item in queryset:
        if item.status != 'C_PICK':
                index = 1
    if index == 0:
        queryset.update(status='G_ARCH')
        
mark_as_picked_up.short_description = "Mark selected orders as picked up"

#Mark order as cancelled
def cancel_order(modeladmin, request, queryset):
    queryset.update(status='F_CANC')
cancel_order.short_description = "Cancel selected orders"

class OrderInline(admin.StackedInline):
    model = Order
    extra = 0
    raw_id_fields = ('customer_placed', 'item')
    verbose_name = 'Customer Order - '

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')
    ordering = ('last_name', 'first_name')

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'street_address',
                    'street_address_2', 'city', 'state', 'zip_code', 'phone',
                    'mobile')
    search_fields = ['last_name']
    ordering = ('last_name', 'first_name')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_order_date', 'status', 'customer_placed', 'sku',
                    'color_code', 'color', 'item_name', 'size', 'vendor', 'paid',
                    'ship', 'comments', 'idle_too_long')
    search_fields = ('customer_placed__last_name',)
    raw_id_fields = ('customer_placed', 'item')
    list_filter = ('item__vendor', 'status', 'customer_order_date')
    ordering = ('status', 'customer_order_date')
    actions = [mark_as_arrived, mark_as_picked_up, cancel_order,
               create_employee_order]

class EmployeeOrderAdmin(admin.ModelAdmin):
    list_display = ('employee_order_date', 'employee_placed', 'status',
                    'purchase_order_number', 'comments')
    inlines = [OrderInline]
    #raw_id_fields = ['order']
    #list_filter = ('order__status',)

    #Remove 'add' functionality - employee orders are created through orders page
    def has_add_permission(self, request):
        return False
    
class ItemAdmin(admin.ModelAdmin):
    list_display = ('sku', 'gender', 'vendor', 'name', 'color', 'color_code')
    search_fields = ('sku', 'name')
    list_filter = ('vendor',)
    ordering = ('vendor', 'name')

class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'acct')
    search_fields = ('name',)
    ordering = ('name',)
    

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(EmployeeOrder, EmployeeOrderAdmin)
admin.site.register(Item,ItemAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.unregister(User)
admin.site.unregister(Group)
