from django.db import models

class PERSON(models.Model):
	id = models.IntegerField(primary_key=True,)
	Name = models.CharField(default=None,max_length=32)
	Surname = models.CharField(default=None,max_length=32)
	BirthDate = models.DateField(default=None,max_length=20 )
	Sex = models.CharField(default=None,max_length=1)
