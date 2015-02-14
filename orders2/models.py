import datetime
from django.db import models
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.utils import timezone


class Employee(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    def __str__(self):
        return self.last_name + ', ' + self.first_name

class Customer(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=12)
    mobile = models.BooleanField('Mobile', default=True)

    CARRIERS = (
        ('ATT', 'AT&T'),
        ('TMO', 'T-Mobile'),
        ('VZW', 'Verizon'),
        ('SPR', 'Sprint'),
        ('USC', 'U.S. Cellular'),
        ('VRG', 'Virgin'),
        ('TRC', 'Tracfone'),
        ('PCS', 'Metro PCS'),
        ('BOO', 'Boost'),
        ('CRK', 'Cricket'),
        ('NEX', 'Nextel'),
        ('ALL', 'Alltel'),
        ('PTL', 'Ptel'),
        ('SUN', 'Suncom'),
        ('QWS', 'Qwest'),
    )

    phone_carrier = models.CharField(max_length=3, choices=CARRIERS)
    email = models.CharField(max_length=30)
    street_address = models.CharField(max_length=30)
    street_address_2 = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)

    def __str__(self):
        return self.last_name + ', ' + self.first_name

class Vendor(models.Model):
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=12)
    acct = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Item(models.Model):
    sku = models.CharField(max_length=30)

    GENDERS = (
        ('MEN', "Men's"),
        ('WMN', "Women's"),
        ('UNI', "Unisex"),
        ('BOY', "Boy's"),
        ('GRL', "Girl's")
    )

    gender = models.CharField(max_length=3, choices=GENDERS)
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=15, blank=True, null=True)
    color_code = models.CharField(max_length=10, blank=True, null=True)
    width = models.CharField(max_length=10, blank=True, null=True)
    vendor = models.ForeignKey(Vendor)

    def __str__(self):
        return self.name

class EmployeeOrder(models.Model):
    employee_order_date = models.DateTimeField('Date ordered')
    employee_placed = models.ForeignKey(Employee)
    purchase_order_number = models.CharField(max_length=25)

    STATUS_OF_ORDER = (
        ('ORDR', 'Ordered'),
        ('BACK', 'Backordered'),
        ('UNAV', 'Unavailable')
    )

    status = models.CharField(max_length=4, choices=STATUS_OF_ORDER)
    comments = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.employee_placed.last_name + ', ' + self.employee_placed.first_name + ' - ' + self.employee_order_date.strftime('%m/%d/%Y')

    def order_status(self):
        return self.status

class Order(models.Model):
    customer_order_date = models.DateTimeField(editable=False)
    customer_placed = models.ForeignKey(Customer)
    employee_helped = models.ForeignKey(Employee)
    item = models.ForeignKey(Item)
    size = models.CharField(max_length=10)

    #All possible order statuses - ABC index for ordering purposes
    STATUS_OF_ORDER = (
        ('A_IDLE', 'Not yet ordered'),
        ('B_SHIP', 'Awaiting delivery'),
        ('C_PICK', 'Ready for pickup'),
        ('E_UNAV', 'Unavailable for order'),
        ('D_BACK', 'Backordered - awaiting delivery'),
        ('F_CANC', 'Canceled by customer'),
        ('G_ARCH', 'Fulfilled'),
        
    )

    status = models.CharField(max_length=6, choices=STATUS_OF_ORDER,
                              default='A_IDLE', editable=False)
    paid = models.BooleanField('Paid', default=False)
    ship = models.BooleanField('Ship', default=False)
    comments = models.CharField(max_length=200, blank=True, null=True)
    employee_order = models.ForeignKey(EmployeeOrder, blank=True, null=True,
                                       editable=False)

    def __str__(self):
        return self.customer_placed.last_name + ', ' + self.customer_placed.first_name + ' - ' + self.customer_order_date.strftime('%m/%d/%Y')

    #Set order date automatically
    def save(self):
        if not self.id:
            self.customer_order_date = timezone.now()
        super(Order, self).save()

    def is_idle(self):
        return self.status == 'A_IDLE'

    def item_name(self):
        return self.item.name

    def vendor(self):
        return self.item.vendor

    def sku(self):
        return self.item.sku

    def color(self):
        return self.item.color

    def color_code(self):
        return self.item.color_code

    def idle_too_long(self):
        if self.status == 'A_IDLE':
            return (self.customer_order_date <= timezone.now() -
                    datetime.timedelta(days=5))
        else:
            return False
        
    idle_too_long.admin_order_field = 'customer_order_date'
    idle_too_long.boolean = True
    idle_too_long.short_description = 'Idle for 5 days?'

#Update customer order status - marks customer orders as 'ready for pickup'
def update_COstatus(sender, instance, **kwargs):
    if instance.status == 'C_PICK':
        notify_customer(instance, 1)

    elif instance.status == 'D_BACK':
        notify_customer(instance, 2)

    elif instance.status == 'E_UNAV':
        notify_customer(instance, 3)

#Send email/text to customer
def notify_customer(order, status_of_item):

    sender_email = 'Body N Sole Sports <blakeyn09@gmail.com>'

    #Item arrived at store
    if status_of_item == 1:
        email_subject = 'Your order has arrived at Body N Sole!'
        email_body = ('Dear ' + order.customer_placed.first_name + ', \n\n'
                     'The item you ordered on ' +
                      order.customer_order_date.strftime('%m/%d/%Y') +
                     ' is now available for pickup: ' + order.item_name() + '. '
                     'Please arrange to pick up your item within the '
                     'next week. We cannot guarantee your item beyond this '
                     'time period. Thank you for shopping with us! \n\n '
                     'Sincerely, \n\n The Body N Sole Team'
                     '\n 1317 N. Dunlap Ave. \n Savoy, IL 61874'
                     '\n 217-356-8926')

        #Send email message to customer
        send_mail(email_subject, email_body, sender_email,
                  [order.customer_placed.email,], fail_silently=False)

        #Send text message if customer has mobile phone
        if order.customer_placed.mobile == True:
            text_subject = ''
            text_body = ('Your order has arrived at Body N Sole! '
                         'Please pick up your item within the next week. '
                         'Call 217-356-8926 if you have any questions. '
                         'Thanks for shopping with us!')

            send_mail(text_subject, text_body, sender_email,
                      [get_text_address(order.customer_placed),],
                      fail_silently=False)
        
    #Item is backordered
    elif status_of_item == 2:
        email_subject = 'Your order is backordered!'
        email_body = ('Dear ' + order.customer_placed.first_name + ', \n\n'
                     'The item you ordered on ' +
                      order.customer_order_date.strftime('%m/%d/%Y') +
                     ' is backordered: ' + order.item_name() + '. '
                     'Your Body N Sole representative had this to say: \n\n' +
                      order.comments + '\n\nIf you have any questions, please '
                     "don't hesitate to give us a call. Thank you for shopping "
                     'with us! \n\n'
                     'Sincerely, \n\nThe Body N Sole Team'
                     '\n1317 N. Dunlap Ave. \nSavoy, IL 61874'
                     '\n217-356-8926')
        
        #Send email message to customer
        send_mail(email_subject, email_body, sender_email,
                  [order.customer_placed.email,], fail_silently=False)

        #Send text message if customer has mobile phone
        if order.customer_placed.mobile == True:
            text_subject = ''
            text_body = ('Your order from Body N Sole is backordered! '
                         'Call 217-356-8926 if you have any questions. '
                         'Thanks for shopping with us!')

            send_mail(text_subject, text_body, sender_email,
                      [get_text_address(order.customer_placed),],
                      fail_silently=False)
        
    #Item is unavailable
    elif status_of_item == 3:
        email_subject = 'Your order is unavailable!'
        email_body = ('Dear ' + order.customer_placed.first_name + ', \n\n'
                     'The item you ordered on ' +
                      order.customer_order_date.strftime('%m/%d/%Y') +
                     ' is unavailable for order: ' + order.item_name() + '. '
                     'Your Body N Sole representative had this to say: \n\n' +
                      order.comments + '\n\nIf you have any questions, please '
                     "don't hesitate to give us a call. Thank you for shopping "
                     'with us! \n\n'
                     'Sincerely, \n\nThe Body N Sole Team'
                     '\n1317 N. Dunlap Ave. \nSavoy, IL 61874'
                     '\n217-356-8926')
        
        #Send email message to customer
        send_mail(email_subject, email_body, sender_email,
                  [order.customer_placed.email,], fail_silently=False)

        #Send text message if customer has mobile phone
        if order.customer_placed.mobile == True:
            text_subject = ''
            text_body = ('Your order from Body N Sole is unavailable! '
                         'Call 217-356-8926 if you have any questions. '
                         'Thanks for shopping with us!')

            send_mail(text_subject, text_body, sender_email,
                      [get_text_address(order.customer_placed),],
                      fail_silently=False)
        
#Determine the customer's email-text address
def get_text_address(customer):

    if customer.mobile == True:
        if customer.phone_carrier == 'ATT':
            return customer.phone + '@txt.att.net'
        elif customer.phone_carrier == 'TMO':
            return customer.phone + '@tmomail.net'
        elif customer.phone_carrier == 'VZW':
            return customer.phone + '@vtext.com'
        elif customer.phone_carrier == 'SPR':
            return customer.phone + '@pm.sprint.com'
        elif customer.phone_carrier == 'USC':
            return customer.phone + '@email.uscc.net'
        elif customer.phone_carrier == 'VRG':
            return customer.phone + '@vmobl.com'
        elif customer.phone_carrier == 'TRC':
            return customer.phone + '@mmst5.tracfone.com'
        elif customer.phone_carrier == 'PCS':
            return customer.phone + '@mymetropcs.com'
        elif customer.phone_carrier == 'BOO':
            return customer.phone + '@myboostmobile.com'
        elif customer.phone_carrier == 'CRK':
            return customer.phone + '@sms.mycricket.com'
        elif customer.phone_carrier == 'NEX':
            return customer.phone + '@messaging.nextel.com'
        elif customer.phone_carrier == 'ALL':
            return customer.phone + '@message.alltel.com'
        elif customer.phone_carrier == 'PTL':
            return customer.phone + '@ptel.com'
        elif customer.phone_carrier == 'SUN':
            return customer.phone + '@tms.suncom.com'
        elif customer.phone_carrier == 'QWS':
            return customer.phone + '@qwestmp.com'

post_save.connect(update_COstatus, sender=Order)
        
