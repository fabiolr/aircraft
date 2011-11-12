# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        create = orm['expense.expensecategory'].objects.create

        create(expense_type=1, name=u'Comissária')
        create(expense_type=1, name=u'Taxa aeroportuária')
        create(expense_type=1, name=u'Receptivo')
        create(expense_type=1, name=u'Gorjeta')
        create(expense_type=1, name=u'Hospedagem')
        create(expense_type=1, name=u'Alimentação')
        create(expense_type=1, name=u'Transporte terrestre')
        
        create(expense_type=2, name=u'Combustível')
        create(expense_type=2, name=u'Lubrificante')
        create(expense_type=2, name=u'Limpeza')
        create(expense_type=2, name=u'Aeronave')
        create(expense_type=2, name=u'CTM')
        
        create(expense_type=3, name=u'Hangar')
        create(expense_type=3, name=u'Salário Piloto')
        create(expense_type=3, name=u'Salário Copiloto')
        create(expense_type=3, name=u'Encargos Salariais')
        create(expense_type=3, name=u'CTM')
        create(expense_type=3, name=u'Monitoramento')
        create(expense_type=3, name=u'Seguro Casco')
        create(expense_type=3, name=u'Seguro Reta')
        create(expense_type=3, name=u'Taxas e Emolumentos')
        create(expense_type=3, name=u'Despachante')


    def backwards(self, orm):
        for category in orm['expense.expensecategory'].objects.all():
            category.delete()

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'expense.directexpense': {
            'Meta': {'object_name': 'DirectExpense', '_ormbases': ['expense.Expense']},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'expense_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['expense.Expense']", 'unique': 'True', 'primary_key': 'True'}),
            'flight': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['expense.Flight']"})
        },
        'expense.eventualmantainance': {
            'Meta': {'object_name': 'EventualMantainance'},
            'expense': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['expense.Expense']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'outage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['expense.Outage']"})
        },
        'expense.expense': {
            'Meta': {'object_name': 'Expense'},
            'ammount': ('django.db.models.fields.FloatField', [], {}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['expense.ExpenseCategory']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'paid'", 'to': "orm['expense.Share']"}),
            'responsibility': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'responsible'", 'to': "orm['expense.Share']"})
        },
        'expense.expensecategory': {
            'Meta': {'object_name': 'ExpenseCategory'},
            'expense_type': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'expense.fixedexpense': {
            'Meta': {'object_name': 'FixedExpense', '_ormbases': ['expense.Expense']},
            'end': ('django.db.models.fields.DateField', [], {}),
            'expense_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['expense.Expense']", 'unique': 'True', 'primary_key': 'True'}),
            'repeat': ('django.db.models.fields.IntegerField', [], {}),
            'start': ('django.db.models.fields.DateField', [], {})
        },
        'expense.flight': {
            'Meta': {'object_name': 'Flight'},
            'cycles': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'destiny': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'end_hobbs': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mantainance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'origin': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'responsibility': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['expense.Share']"}),
            'start_hobbs': ('django.db.models.fields.FloatField', [], {})
        },
        'expense.hourlymantainance': {
            'Meta': {'object_name': 'HourlyMantainance'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'expense': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['expense.Expense']"}),
            'hobbs': ('django.db.models.fields.FloatField', [], {}),
            'hours': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'obs': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'expense.outage': {
            'Meta': {'object_name': 'Outage'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'cause': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'flight': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['expense.Flight']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'expense.owner': {
            'Meta': {'object_name': 'Owner', '_ormbases': ['auth.User']},
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'expense.payments': {
            'Meta': {'object_name': 'Payments'},
            'ammount': ('django.db.models.fields.FloatField', [], {}),
            'by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payments_made'", 'to': "orm['expense.Owner']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payments_received'", 'to': "orm['expense.Owner']"})
        },
        'expense.schedulemantainance': {
            'Meta': {'object_name': 'ScheduleMantainance'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'expense': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['expense.Expense']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'period': ('django.db.models.fields.IntegerField', [], {})
        },
        'expense.share': {
            'Meta': {'object_name': 'Share'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'through': "orm['expense.UserShare']", 'symmetrical': 'False'})
        },
        'expense.usershare': {
            'Meta': {'object_name': 'UserShare'},
            'ammount': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'share': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['expense.Share']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'expense.variableexpense': {
            'Meta': {'object_name': 'VariableExpense', '_ormbases': ['expense.Expense']},
            'end': ('django.db.models.fields.DateField', [], {}),
            'expense_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['expense.Expense']", 'unique': 'True', 'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['expense']
