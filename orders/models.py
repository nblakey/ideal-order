import datetime
from django.db import models

# Create your models here.

class Employee(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    def __str__(self):
        return self.last_name + ', ' + self.first_name

class Customer(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=12)

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
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)

    def __str__(self):
        return self.last_name + ', ' + self.first_name

##class EmployeesHelpCustomers(models.Model):
##    employee = models.ForeignKey(Employee)
##    customer = models.ForeignKey(Customer)

class Vendor(models.Model):
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=12)
    acct = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Item(models.Model):
    sku = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    cost = models.CharField(max_length=10)
    #order = models.ManyToManyField(Order, through='OrdersHaveItems')
    vendor = models.ForeignKey(Vendor)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer_order_date = models.DateTimeField('Date helped')
    employee_order_date = models.DateTimeField('Date ordered', blank=True)
    customer_placed = models.ForeignKey(Customer)
    employee_helped = models.ForeignKey(Employee)

    STATUS_OF_ORDER = (
        ('IDLE', 'Not yet ordered'),
        ('SHIP', 'Awaiting delivery'),
        ('PICK', 'Ready for pickup'),
    )

    status = models.CharField(max_length=4, choices=STATUS_OF_ORDER,
                              default='IDLE', editable=False)
    paid = models.BooleanField('Paid', default=False)
    ship = models.BooleanField('Ship', default=False)
    comments = models.CharField(max_length=200)
    item = models.ForeignKey(Item)  #####

##    def __str__(self):
##        return self.customer_placed

##class OrdersHaveItems(models.Model):
##    order = models.ForeignKey(Order)
##    item = models.ForeignKey(Item)
##    size = models.CharField(max_length=5)
##    color = models.CharField(max_length=10)
