# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CaseForm'
        db.create_table(u'CaseEntry_caseform', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('patient', self.gf('django.db.models.fields.CharField')(max_length=90)),
            ('age', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('ip', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('surgeon', self.gf('django.db.models.fields.CharField')(max_length=90, blank=True)),
            ('admission_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('surgery_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('discharge_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('weight', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('menache_age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('main_telephone', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('other_telephone', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('regular_period', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('last_period', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('marital_status', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('social_status', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('first_pregnancy_age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('first_pregnancy_fathers_age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('pregnancy_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('living_children_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('stillbirth_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('early_neonatal_death_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('last_pregnancy_age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('treatment_center_travel', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('treatment_center_travel_cost', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('age_fistula_started', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('labor_duration', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('baby_birth_location', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('delivery_type', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('delivery_outcome', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('fistula_cause', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('urine_leak_frequency', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('urine_leak_amount', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('urine_leak_interference', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'CaseEntry', ['CaseForm'])

        # Adding model 'Case'
        db.create_table(u'CaseEntry_case', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='NEW', max_length=30)),
            ('caseform', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['CaseEntry.CaseForm'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'CaseEntry', ['Case'])


    def backwards(self, orm):
        # Deleting model 'CaseForm'
        db.delete_table(u'CaseEntry_caseform')

        # Deleting model 'Case'
        db.delete_table(u'CaseEntry_case')


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
        }
    }

    complete_apps = ['CaseEntry']