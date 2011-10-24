# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Job'
        db.create_table('django_cron_job', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('run_frequency', self.gf('django.db.models.fields.PositiveIntegerField')(default=86400)),
            ('last_run', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 10, 24, 13, 21, 51))),
            ('instance', self.gf('django.db.models.fields.TextField')()),
            ('args', self.gf('django.db.models.fields.TextField')()),
            ('kwargs', self.gf('django.db.models.fields.TextField')()),
            ('queued', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
        ))
        db.send_create_signal('django_cron', ['Job'])

        # Adding model 'Cron'
        db.create_table('django_cron_cron', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('executing', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
        ))
        db.send_create_signal('django_cron', ['Cron'])


    def backwards(self, orm):
        
        # Deleting model 'Job'
        db.delete_table('django_cron_job')

        # Deleting model 'Cron'
        db.delete_table('django_cron_cron')


    models = {
        'django_cron.cron': {
            'Meta': {'object_name': 'Cron'},
            'executing': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'django_cron.job': {
            'Meta': {'object_name': 'Job'},
            'args': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.TextField', [], {}),
            'kwargs': ('django.db.models.fields.TextField', [], {}),
            'last_run': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 10, 24, 13, 21, 51)'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'queued': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'run_frequency': ('django.db.models.fields.PositiveIntegerField', [], {'default': '86400'})
        }
    }

    complete_apps = ['django_cron']
