# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ExpenseCategory'
        db.create_table('finance_expensecategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('expense_type', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('finance', ['ExpenseCategory'])

        # Adding model 'Expense'
        db.create_table('finance_expense', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['finance.ExpenseCategory'], null=True, blank=True)),
        ))
        db.send_create_signal('finance', ['Expense'])

        # Adding model 'Payment'
        db.create_table('finance_payment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('expense', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['finance.Expense'])),
            ('paid_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flight.Person'])),
            ('ammount', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('finance', ['Payment'])

        # Adding model 'Responsibility'
        db.create_table('finance_responsibility', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('expense', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['finance.Expense'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flight.Person'])),
            ('ammount', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('finance', ['Responsibility'])

        # Adding model 'Interpayment'
        db.create_table('finance_interpayment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transferences_made', to=orm['flight.Person'])),
            ('to', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transferences_received', to=orm['flight.Person'])),
            ('ammount', self.gf('django.db.models.fields.FloatField')()),
            ('paid', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('finance', ['Interpayment'])


    def backwards(self, orm):
        
        # Deleting model 'ExpenseCategory'
        db.delete_table('finance_expensecategory')

        # Deleting model 'Expense'
        db.delete_table('finance_expense')

        # Deleting model 'Payment'
        db.delete_table('finance_payment')

        # Deleting model 'Responsibility'
        db.delete_table('finance_responsibility')

        # Deleting model 'Interpayment'
        db.delete_table('finance_interpayment')


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
