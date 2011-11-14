# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Person'
        db.create_table('flight_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('system_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('flight', ['Person'])

        # Adding model 'Flight'
        db.create_table('flight_flight', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('origin', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('destiny', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('start_hobbs', self.gf('django.db.models.fields.FloatField')()),
            ('end_hobbs', self.gf('django.db.models.fields.FloatField')()),
            ('cycles', self.gf('django.db.models.fields.IntegerField')()),
            ('mantainance', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('flight', ['Flight'])

        # Adding model 'PAX'
        db.create_table('flight_pax', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('flight', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flight.Flight'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flight.Person'])),
            ('ammount', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('flight', ['PAX'])

        # Adding model 'Outage'
        db.create_table('flight_outage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('flight', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flight.Flight'], null=True)),
            ('outage_type', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('discovery_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('cause', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('responsible', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flight.Person'], null=True, blank=True)),
        ))
        db.send_create_signal('flight', ['Outage'])


    def backwards(self, orm):
        
        # Deleting model 'Person'
        db.delete_table('flight_person')

        # Deleting model 'Flight'
        db.delete_table('flight_flight')

        # Deleting model 'PAX'
        db.delete_table('flight_pax')

        # Deleting model 'Outage'
        db.delete_table('flight_outage')


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
        'flight.pax': {
            'Meta': {'object_name': 'PAX'},
            'ammount': ('django.db.models.fields.IntegerField', [], {}),
            'flight': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flight.Flight']"}),
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

    complete_apps = ['flight']
