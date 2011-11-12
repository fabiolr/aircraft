# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Owner'
        db.create_table('expense_owner', (
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('expense', ['Owner'])

        # Adding model 'Share'
        db.create_table('expense_share', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('expense', ['Share'])

        # Adding model 'UserShare'
        db.create_table('expense_usershare', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('share', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['expense.Share'])),
            ('ammount', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('expense', ['UserShare'])

        # Adding model 'Flight'
        db.create_table('expense_flight', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('origin', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('destiny', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('start_hobbs', self.gf('django.db.models.fields.FloatField')()),
            ('end_hobbs', self.gf('django.db.models.fields.FloatField')()),
            ('cycles', self.gf('django.db.models.fields.IntegerField')()),
            ('responsibility', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['expense.Share'])),
            ('mantainance', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('expense', ['Flight'])

        # Adding model 'ExpenseCategory'
        db.create_table('expense_expensecategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('expense_type', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('expense', ['ExpenseCategory'])

        # Adding model 'Expense'
        db.create_table('expense_expense', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ammount', self.gf('django.db.models.fields.FloatField')()),
            ('paid_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='paid', to=orm['expense.Share'])),
            ('responsibility', self.gf('django.db.models.fields.related.ForeignKey')(related_name='responsible', to=orm['expense.Share'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['expense.ExpenseCategory'])),
        ))
        db.send_create_signal('expense', ['Expense'])

        # Adding model 'DirectExpense'
        db.create_table('expense_directexpense', (
            ('expense_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['expense.Expense'], unique=True, primary_key=True)),
            ('flight', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['expense.Flight'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('expense', ['DirectExpense'])

        # Adding model 'VariableExpense'
        db.create_table('expense_variableexpense', (
            ('expense_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['expense.Expense'], unique=True, primary_key=True)),
            ('start', self.gf('django.db.models.fields.DateField')()),
            ('end', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('expense', ['VariableExpense'])

        # Adding model 'FixedExpense'
        db.create_table('expense_fixedexpense', (
            ('expense_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['expense.Expense'], unique=True, primary_key=True)),
            ('start', self.gf('django.db.models.fields.DateField')()),
            ('end', self.gf('django.db.models.fields.DateField')()),
            ('repeat', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('expense', ['FixedExpense'])

        # Adding model 'HourlyMantainance'
        db.create_table('expense_hourlymantainance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('hobbs', self.gf('django.db.models.fields.FloatField')()),
            ('hours', self.gf('django.db.models.fields.IntegerField')()),
            ('expense', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['expense.Expense'])),
            ('obs', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('expense', ['HourlyMantainance'])

        # Adding model 'ScheduleMantainance'
        db.create_table('expense_schedulemantainance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('period', self.gf('django.db.models.fields.IntegerField')()),
            ('expense', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['expense.Expense'])),
        ))
        db.send_create_signal('expense', ['ScheduleMantainance'])

        # Adding model 'Outage'
        db.create_table('expense_outage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('flight', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['expense.Flight'], blank=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('cause', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('expense', ['Outage'])

        # Adding model 'EventualMantainance'
        db.create_table('expense_eventualmantainance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('outage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['expense.Outage'])),
            ('expense', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['expense.Expense'])),
        ))
        db.send_create_signal('expense', ['EventualMantainance'])

        # Adding model 'Payments'
        db.create_table('expense_payments', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='payments_made', to=orm['expense.Owner'])),
            ('to', self.gf('django.db.models.fields.related.ForeignKey')(related_name='payments_received', to=orm['expense.Owner'])),
            ('ammount', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('expense', ['Payments'])


    def backwards(self, orm):
        
        # Deleting model 'Owner'
        db.delete_table('expense_owner')

        # Deleting model 'Share'
        db.delete_table('expense_share')

        # Deleting model 'UserShare'
        db.delete_table('expense_usershare')

        # Deleting model 'Flight'
        db.delete_table('expense_flight')

        # Deleting model 'ExpenseCategory'
        db.delete_table('expense_expensecategory')

        # Deleting model 'Expense'
        db.delete_table('expense_expense')

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

        # Deleting model 'Outage'
        db.delete_table('expense_outage')

        # Deleting model 'EventualMantainance'
        db.delete_table('expense_eventualmantainance')

        # Deleting model 'Payments'
        db.delete_table('expense_payments')


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
