# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Airport'
        db.create_table('flight_airport', (
            ('remote_id', self.gf('django.db.models.fields.IntegerField')(unique=True, null=True)),
            ('icao', self.gf('django.db.models.fields.CharField')(max_length=8, primary_key=True)),
            ('atype', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('elevation', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('flight', ['Airport'])

        # Renaming column for 'Flight.origin' to match new field type.
        db.rename_column('flight_flight', 'origin', 'origin_id')
        # Changing field 'Flight.origin'
        db.alter_column('flight_flight', 'origin_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flight.Airport']))

        # Adding index on 'Flight', fields ['origin']
        db.create_index('flight_flight', ['origin_id'])

        # Renaming column for 'Flight.destiny' to match new field type.
        db.rename_column('flight_flight', 'destiny', 'destiny_id')
        # Changing field 'Flight.destiny'
        db.alter_column('flight_flight', 'destiny_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flight.Airport']))

        # Adding index on 'Flight', fields ['destiny']
        db.create_index('flight_flight', ['destiny_id'])


    def backwards(self, orm):
        
        # Removing index on 'Flight', fields ['destiny']
        db.delete_index('flight_flight', ['destiny_id'])

        # Removing index on 'Flight', fields ['origin']
        db.delete_index('flight_flight', ['origin_id'])

        # Deleting model 'Airport'
        db.delete_table('flight_airport')

        # Renaming column for 'Flight.origin' to match new field type.
        db.rename_column('flight_flight', 'origin_id', 'origin')
        # Changing field 'Flight.origin'
        db.alter_column('flight_flight', 'origin', self.gf('django.db.models.fields.CharField')(max_length=4))

        # Renaming column for 'Flight.destiny' to match new field type.
        db.rename_column('flight_flight', 'destiny_id', 'destiny')
        # Changing field 'Flight.destiny'
        db.alter_column('flight_flight', 'destiny', self.gf('django.db.models.fields.CharField')(max_length=4))


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
        'flight.airport': {
            'Meta': {'object_name': 'Airport'},
            'atype': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'elevation': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'icao': ('django.db.models.fields.CharField', [], {'max_length': '8', 'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'remote_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True'})
        },
        'flight.flight': {
            'Meta': {'ordering': "['-number']", 'object_name': 'Flight'},
            'copilot': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'copilots'", 'null': 'True', 'to': "orm['flight.Person']"}),
            'cycles': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'destiny': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'arriving_flights'", 'to': "orm['flight.Airport']"}),
            'end_hobbs': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mantainance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'origin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'departing_flights'", 'to': "orm['flight.Airport']"}),
            'pilot': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pilots'", 'null': 'True', 'to': "orm['flight.Person']"}),
            'remarks': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'start_hobbs': ('django.db.models.fields.FloatField', [], {}),
            'takeoff_time': ('django.db.models.fields.TimeField', [], {'null': 'True'})
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
            'pilot': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'system_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['flight']
