# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'HourlyMantainance'
        db.create_table('mantainance_hourlymantainance', (
            ('expense_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['expense.Expense'], unique=True, primary_key=True)),
            ('mantainance_date', self.gf('django.db.models.fields.DateField')()),
            ('hobbs', self.gf('django.db.models.fields.FloatField')()),
            ('hours', self.gf('django.db.models.fields.IntegerField')()),
            ('obs', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('mantainance', ['HourlyMantainance'])

        # Adding model 'ScheduleMantainance'
        db.create_table('mantainance_schedulemantainance', (
            ('expense_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['expense.Expense'], unique=True, primary_key=True)),
            ('mantainance_date', self.gf('django.db.models.fields.DateField')()),
            ('period', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('mantainance', ['ScheduleMantainance'])

        # Adding model 'EventualMantainance'
        db.create_table('mantainance_eventualmantainance', (
            ('expense_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['expense.Expense'], unique=True, primary_key=True)),
            ('outage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flight.Outage'])),
        ))
        db.send_create_signal('mantainance', ['EventualMantainance'])


    def backwards(self, orm):
        
        # Deleting model 'HourlyMantainance'
        db.delete_table('mantainance_hourlymantainance')

        # Deleting model 'ScheduleMantainance'
        db.delete_table('mantainance_schedulemantainance')

        # Deleting model 'EventualMantainance'
        db.delete_table('mantainance_eventualmantainance')


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
        'expense.expense': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Expense'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['expense.ExpenseCategory']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'expense.expensecategory': {
            'Meta': {'ordering': "('expense_type', 'name')", 'object_name': 'ExpenseCategory'},
            'expense_type': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'flight.flight': {
            'Meta': {'ordering': "['-id']", 'object_name': 'Flight'},
            'cycles': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'destiny': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'end_hobbs': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mantainance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'origin': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'start_hobbs': ('django.db.models.fields.FloatField', [], {})
        },
        'flight.outage': {
            'Meta': {'object_name': 'Outage'},
            'cause': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'discovery_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'flight': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flight.Flight']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'outage_type': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'responsible': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flight.Person']", 'null': 'True', 'blank': 'True'})
        },
        'flight.person': {
            'Meta': {'object_name': 'Person'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'owner': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'system_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'mantainance.eventualmantainance': {
            'Meta': {'ordering': "['-date']", 'object_name': 'EventualMantainance', '_ormbases': ['expense.Expense']},
            'expense_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['expense.Expense']", 'unique': 'True', 'primary_key': 'True'}),
            'outage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flight.Outage']"})
        },
        'mantainance.hourlymantainance': {
            'Meta': {'ordering': "['-date']", 'object_name': 'HourlyMantainance', '_ormbases': ['expense.Expense']},
            'expense_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['expense.Expense']", 'unique': 'True', 'primary_key': 'True'}),
            'hobbs': ('django.db.models.fields.FloatField', [], {}),
            'hours': ('django.db.models.fields.IntegerField', [], {}),
            'mantainance_date': ('django.db.models.fields.DateField', [], {}),
            'obs': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'mantainance.schedulemantainance': {
            'Meta': {'ordering': "['-date']", 'object_name': 'ScheduleMantainance', '_ormbases': ['expense.Expense']},
            'expense_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['expense.Expense']", 'unique': 'True', 'primary_key': 'True'}),
            'mantainance_date': ('django.db.models.fields.DateField', [], {}),
            'period': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['mantainance']
