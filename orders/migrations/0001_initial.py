# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Employee'
        db.create_table('orders_employee', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('firstName', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('lastName', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('orders', ['Employee'])

        # Adding model 'Customer'
        db.create_table('orders_customer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('firstName', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('lastName', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('phone_carrier', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('streetAddress', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal('orders', ['Customer'])

        # Adding model 'EmployeesHelpCustomers'
        db.create_table('orders_employeeshelpcustomers', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('employee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['orders.Employee'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['orders.Customer'])),
        ))
        db.send_create_signal('orders', ['EmployeesHelpCustomers'])

        # Adding model 'Order'
        db.create_table('orders_order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customerOrderDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('employeeOrderDate', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('customerPlaced', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['orders.Customer'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=4, default='IDLE')),
            ('isPaid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('willShip', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comments', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('orders', ['Order'])

        # Adding model 'Vendor'
        db.create_table('orders_vendor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('acct', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('orders', ['Vendor'])

        # Adding model 'Item'
        db.create_table('orders_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sku', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('cost', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('vendor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['orders.Vendor'])),
        ))
        db.send_create_signal('orders', ['Item'])

        # Adding model 'OrdersHaveItems'
        db.create_table('orders_ordershaveitems', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['orders.Order'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['orders.Item'])),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('orders', ['OrdersHaveItems'])


    def backwards(self, orm):
        # Deleting model 'Employee'
        db.delete_table('orders_employee')

        # Deleting model 'Customer'
        db.delete_table('orders_customer')

        # Deleting model 'EmployeesHelpCustomers'
        db.delete_table('orders_employeeshelpcustomers')

        # Deleting model 'Order'
        db.delete_table('orders_order')

        # Deleting model 'Vendor'
        db.delete_table('orders_vendor')

        # Deleting model 'Item'
        db.delete_table('orders_item')

        # Deleting model 'OrdersHaveItems'
        db.delete_table('orders_ordershaveitems')


    models = {
        'orders.customer': {
            'Meta': {'object_name': 'Customer'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'employeeHelped': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['orders.Employee']", 'through': "orm['orders.EmployeesHelpCustomers']", 'symmetrical': 'False'}),
            'firstName': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastName': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'phone_carrier': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'streetAddress': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'orders.employee': {
            'Meta': {'object_name': 'Employee'},
            'firstName': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastName': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'orders.employeeshelpcustomers': {
            'Meta': {'object_name': 'EmployeesHelpCustomers'},
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['orders.Customer']"}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['orders.Employee']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'orders.item': {
            'Meta': {'object_name': 'Item'},
            'cost': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'order': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['orders.Order']", 'through': "orm['orders.OrdersHaveItems']", 'symmetrical': 'False'}),
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['orders.Vendor']"})
        },
        'orders.order': {
            'Meta': {'object_name': 'Order'},
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'customerOrderDate': ('django.db.models.fields.DateTimeField', [], {}),
            'customerPlaced': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['orders.Customer']"}),
            'employeeOrderDate': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isPaid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '4', 'default': "'IDLE'"}),
            'willShip': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'orders.ordershaveitems': {
            'Meta': {'object_name': 'OrdersHaveItems'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['orders.Item']"}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['orders.Order']"}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'orders.vendor': {
            'Meta': {'object_name': 'Vendor'},
            'acct': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        }
    }

    complete_apps = ['orders']