# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DirectExpense'
        db.create_table('expense_directexpense', (
            ('expense_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['finance.Expense'], unique=True, primary_key=True)),
            ('flight', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flight.Flight'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('expense', ['DirectExpense'])

        # Adding model 'VariableExpense'
        db.create_table('expense_variableexpense', (
            ('expense_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['finance.Expense'], unique=True, primary_key=True)),
            ('start', self.gf('django.db.models.fields.DateField')()),
            ('end', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('expense', ['VariableExpense'])

        # Adding model 'FixedExpense'
        db.create_table('expense_fixedexpense', (
            ('expense_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['finance.Expense'], unique=True, primary_key=True)),
            ('start', self.gf('django.db.models.fields.DateField')()),
            ('end', self.gf('django.db.models.fields.DateField')()),
            ('repeat', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('expense', ['FixedExpense'])

        # Adding model 'HourlyMantainance'
        db.create_table('expense_hourlymantainance', (
            ('expense_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['finance.Expense'], unique=True, primary_key=True)),
            ('mantainance_date', self.gf('django.db.models.fields.DateField')()),
            ('hobbs', self.gf('django.db.models.fields.FloatField')()),
            ('hours', self.gf('django.db.models.fields.IntegerField')()),
            ('obs', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('expense', ['HourlyMantainance'])

        # Adding model 'ScheduleMantainance'
        db.create_table('expense_schedulemantainance', (
            ('expense_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['finance.Expense'], unique=True, primary_key=True)),
            ('mantainance_date', self.gf('django.db.models.fields.DateField')()),
            ('period', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('expense', ['ScheduleMantainance'])

        # Adding model 'EventualMantainance'
        db.create_table('expense_eventualmantainance', (
            ('expense_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['finance.Expense'], unique=True, primary_key=True)),
            ('outage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flight.Outage'])),
        ))
        db.send_create_signal('expense', ['EventualMantainance'])


    def backwards(self, orm):
        
        # Deleting model 'DirectExpense'
        db.delete_table('expense_directexpense')

        # Deleting model 'VariableExpense'
        db.delete_table('expense_variableexpense')

        # Deleting model 'FixedExpense'
        db.delete_table('expense_fixedexpense')

        # Deleting model 'HourlyMantainance'
        db.delete_table('expense_hourlymantainance')

        # Deleting model 'ScheduleMantainance'
        db.delete_table('expense_schedulemantainance')

        # Deleting model 'EventualMantainance'
        db.delete_table('expense_eventualmantainance')


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
            'Meta': {'ordering': "['-date']", 'object_name': 'DirectExpense', '_ormbases': ['finance.Expense']},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'expense_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['finance.Expense']", 'unique': 'True', 'primary_key': 'True'}),
            'flight': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flight.Flight']"})
        },
        'expense.eventualmantainance': {
            'Meta': {'ordering': "['-date']", 'object_name': 'EventualMantainance', '_ormbases': ['finance.Expense']},
            'expense_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['finance.Expense']", 'unique': 'True', 'primary_key': 'True'}),
            'outage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flight.Outage']"})
        },
        'expense.fixedexpense': {
            'Meta': {'ordering': "['-date']", 'object_name': 'FixedExpense', '_ormbases': ['finance.Expense']},
            'end': ('django.db.models.fields.DateField', [], {}),
            'expense_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['finance.Expense']", 'unique': 'True', 'primary_key': 'True'}),
            'repeat': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'start': ('django.db.models.fields.DateField', [], {})
        },
        'expense.hourlymantainance': {
            'Meta': {'ordering': "['-date']", 'object_name': 'HourlyMantainance', '_ormbases': ['finance.Expense']},
            'expense_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['finance.Expense']", 'unique': 'True', 'primary_key': 'True'}),
            'hobbs': ('django.db.models.fields.FloatField', [], {}),
            'hours': ('django.db.models.fields.IntegerField', [], {}),
            'mantainance_date': ('django.db.models.fields.DateField', [], {}),
            'obs': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'expense.schedulemantainance': {
            'Meta': {'ordering': "['-date']", 'object_name': 'ScheduleMantainance', '_ormbases': ['finance.Expense']},
            'expense_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['finance.Expense']", 'unique': 'True', 'primary_key': 'True'}),
            'mantainance_date': ('django.db.models.fields.DateField', [], {}),
            'period': ('django.db.models.fields.IntegerField', [], {})
        },
        'expense.variableexpense': {
            'Meta': {'ordering': "['-date']", 'object_name': 'VariableExpense', '_ormbases': ['finance.Expense']},
            'end': ('django.db.models.fields.DateField', [], {}),
            'expense_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['finance.Expense']", 'unique': 'True', 'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {})
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
        'flight.flight': {
            'Meta': {'ordering': "['-number']", 'object_name': 'Flight'},
            'cycles': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'destiny': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'end_hobbs': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mantainance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
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
        }
    }

    complete_apps = ['expense']
