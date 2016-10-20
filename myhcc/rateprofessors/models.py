# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desidered behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class College(models.Model):
    college_short_name = models.CharField(unique=True, max_length=5)
    college_long_name = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
		college_name = "(%s)%s"% (self.college_short_name, self.college_long_name)
		return college_name

    class Meta:
        managed = True
        db_table = 'rateprofessors_college'

class Campus(models.Model):
    campus_short_name = models.CharField(unique=True, max_length=5)
    campus_long_name = models.CharField(max_length=20, blank=True, null=True)
    college = models.ForeignKey(College, blank=True, null=True)
    #instructor = models.ForeignKey(Instructor, on_delete = models.CASCADE)
    
    def __str__(self):
		campus_name = "(%s)%s"% (self.campus_short_name, self.campus_long_name)
		return campus_name

    class Meta:
        managed = True
        db_table = 'rateprofessors_campus'


class Subject(models.Model):
    subject_short_name = models.CharField(unique=True, max_length=5)
    subject_long_name = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
		subject_name = "(%s)%s"% (self.subject_short_name, self.subject_long_name)
		return subject_name

    class Meta:
        managed = True
        db_table = 'rateprofessors_subject'

class Classes(models.Model):
    class_short_name = models.CharField(unique=True, max_length=20)
    class_long_name = models.CharField(max_length=40)
    subject = models.ForeignKey(Subject, blank=True, null=True)
    
    def __str__(self):
		class_name = "(%s)%s"% (self.class_short_name, self.class_long_name)
		return class_name

    class Meta:
        managed = True
        db_table = 'rateprofessors_classes'


class Instructor(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    link_id = models.IntegerField(blank=True, null=True)
    ranking = models.FloatField(max_length=5, blank=True, null=True)
    college = models.ForeignKey(College, blank=True, null=True)
    
    def __str__(self):
		instructor_name = "%s %s"% (self.first_name, self.last_name)
		return instructor_name

    class Meta:
        managed = True
        db_table = 'rateprofessors_instructor'
        unique_together = (('first_name', 'last_name'),)

class Session(models.Model):
    session_short_name = models.CharField(unique=True, max_length=5)
    session_long_name = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
		session_name = "(%s)%s"% (self.session_short_name, self.session_long_name)
		return session_name

    class Meta:
        managed = True
        db_table = 'rateprofessors_session'


class Status(models.Model):
    status_name = models.CharField(unique=True, max_length=15)
    
    def __str__(self):
		return self.status_name

    class Meta:
        managed = True
        db_table = 'rateprofessors_status'

class Term(models.Model):
    term_name = models.CharField(unique=True, max_length=10)

    class Meta:
        managed = True
        db_table = 'rateprofessors_term'
class Section(models.Model):
    section_number = models.IntegerField(unique=True)
    section_name = models.CharField(max_length=20)
    schedule = models.CharField(max_length=30)
    link = models.CharField(max_length=40)
    class_id = models.ForeignKey(Classes, blank=True, null=True, db_column = "class_id")
    session = models.ForeignKey(Session, blank=True, null=True)
    instructor = models.ForeignKey(Instructor, blank=True, null=True)
    campus = models.ForeignKey(Campus, blank=True, null=True)
    status = models.ForeignKey(Status, blank=True, null=True)
    term = models.ForeignKey(Term, blank=True, null=True)
    
    def __str__(self):
		section = "%s(%s)"% (self.section_name, self.section_number)
		return section

    class Meta:
        managed = True
        db_table = 'rateprofessors_section'
