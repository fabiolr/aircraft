# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        create = orm['finance.expensecategory'].objects.create

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
        "Write your backwards methods here."


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
        'finance.expense': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Expense'},
            'calculated': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['finance.ExpenseCategory']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'finance.expensecategory': {
            'Meta': {'ordering': "('expense_type', 'name')", 'object_name': 'ExpenseCategory'},
            'expense_type': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'finance.interpayment': {
            'Meta': {'ordering': "('paid', '-date')", 'object_name': 'Interpayment'},
            'ammount': ('django.db.models.fields.FloatField', [], {}),
            'by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transferences_made'", 'to': "orm['flight.Person']"}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transferences_received'", 'to': "orm['flight.Person']"})
        },
        'finance.payment': {
            'Meta': {'object_name': 'Payment'},
            'ammount': ('django.db.models.fields.FloatField', [], {}),
            'expense': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['finance.Expense']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flight.Person']"})
        },
        'finance.responsibility': {
            'Meta': {'ordering': "[u'owner__name']", 'object_name': 'Responsibility'},
            'ammount': ('django.db.models.fields.FloatField', [], {}),
            'expense': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['finance.Expense']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flight.Person']"})
        },
        'flight.person': {
            'Meta': {'object_name': 'Person'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'owner': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'system_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['finance']
