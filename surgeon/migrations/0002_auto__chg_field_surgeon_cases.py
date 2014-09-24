# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Surgeon.cases'
        db.alter_column(u'surgeon_surgeon', 'cases_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['CaseEntry.Case'], null=True))

    def backwards(self, orm):

        # Changing field 'Surgeon.cases'
        db.alter_column(u'surgeon_surgeon', 'cases_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['CaseEntry.Case']))

    models = {
        u'CaseEntry.case': {
            'Meta': {'object_name': 'Case'},
            'caseform': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['CaseEntry.CaseForm']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'NEW'", 'max_length': '30'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'CaseEntry.caseform': {
            'Meta': {'object_name': 'CaseForm'},
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'admission_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'age': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'age_fistula_started': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'baby_birth_location': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'delivery_outcome': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'delivery_type': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'discharge_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'early_neonatal_death_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'first_pregnancy_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'first_pregnancy_fathers_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fistula_cause': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'labor_duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'last_period': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'last_pregnancy_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'living_children_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'main_telephone': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'marital_status': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'menache_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'other_telephone': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'patient': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'pregnancy_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'regular_period': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'social_status': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'stillbirth_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'surgeon': ('django.db.models.fields.CharField', [], {'max_length': '90', 'blank': 'True'}),
            'surgery_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'treatment_center_travel': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'treatment_center_travel_cost': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'urine_leak_amount': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'urine_leak_frequency': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'urine_leak_interference': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'surgeon.surgeon': {
            'Meta': {'object_name': 'Surgeon'},
            'cases': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['CaseEntry.Case']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['surgeon']