#!/usr/bin/env python
""" models.py


	This file ...


	Copyright (C) 2016 Vincent Noel (vincent.noel@butantan.gov.br)

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU Affero General Public License as published
	by the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU Affero General Public License for more details.

	You should have received a copy of the GNU Affero General Public License
	along with this program. If not, see <http://www.gnu.org/licenses/>.

"""

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from random import choice
from string import ascii_uppercase, ascii_lowercase, digits
from os.path import dirname, basename, join

def new_model_filename():
	rand_string = ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(6))
	return "model{0}.xml".format(rand_string)

def new_sedml_filename():
	rand_string = ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(6))
	return "simulation{0}.xml".format(rand_string)

def new_archive_filename():
	rand_string = ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(6))
	return "archive{0}.omex".format(rand_string)

def new_project_folder():
	rand_string = ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(6))
	while os.path.isdir(os.path.join(settings.MEDIA_ROOT, rand_string)):
		rand_string = ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(6))
	return rand_string


def archive_filename(instance, filename):

	path = dirname(filename)
	filename = basename(filename)
	# full_path = join(join(path, str(instance.project.folder)), "models")
	full_path = join(str(instance.project.folder), "models")
	full_filename = join(full_path, filename)

	while os.path.isfile(full_filename):
		full_filename = join(full_path, new_archive_filename())
	return full_filename


def model_filename(instance, filename):

	path = dirname(filename)
	filename = basename(filename)

	full_path = join(str(instance.project.folder), "models")
	full_filename = join(full_path, filename)

	while os.path.isfile(full_filename):
		full_filename = join(full_path, new_model_filename())
	return full_filename

def sedml_filename(instance, filename):

	path = dirname(filename)
	filename = basename(filename)

	full_path = join(str(instance.project.folder), "models")
	full_filename = join(full_path, filename)

	while os.path.isfile(full_filename):
		full_filename = join(full_path, new_sedml_filename())
	return full_filename


class User(AbstractUser):
	"""
	Custom user class.
	"""
	organization = models.CharField(max_length=255, null=True)
	used_cores = models.IntegerField(null=False, default=0)
	max_cores = models.IntegerField(null=False, default=2)
	used_cpu_time = models.IntegerField(null=False, default=0)
	max_cpu_time = models.IntegerField(null=False, default=1000)

class Project(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=255, null=True)
	folder = models.CharField(max_length=255, default=new_project_folder)
	PUBLIC = 'PU'
	PRIVATE = 'PR'

	ACCESS_CHOICES = (
		(PUBLIC, 'Public'),
		(PRIVATE, 'Private'),
	)

	access = models.CharField(max_length=2,
									  choices=ACCESS_CHOICES,
									  default=PRIVATE)



class SbmlModel(models.Model):
	project = models.ForeignKey(Project)
	name = models.CharField(max_length=255, null=True)
	sbml_file = models.FileField(upload_to=model_filename)


class CombineArchiveModel(models.Model):
	project = models.ForeignKey(Project)
	archive_file = models.FileField(upload_to=archive_filename)

class SEDMLSimulation(models.Model):
	project = models.ForeignKey(Project)
	name = models.CharField(max_length=255, null=True)
	sedml_file = models.FileField(upload_to=sedml_filename)


class Optimization(models.Model):
	project = models.ForeignKey(Project)
	model = models.ForeignKey(SbmlModel)
	optimization_id = models.CharField(max_length=255)


class ContinuationComputation(models.Model):
	project = models.ForeignKey(Project)
	model = models.ForeignKey(SbmlModel)

	variable = models.CharField(max_length=255, default="")
	parameter = models.CharField(max_length=255, default="")

	figure = models.CharField(max_length=10240, default="")

	BUSY = 'BU'
	ENDED = 'EN'
	ERROR = 'ER'

	STATUSES = (
		(BUSY, 'Busy'),
		(ENDED, 'Ended'),
		(ERROR, 'Error')
	)

	status = models.CharField(max_length=2,
									  choices=STATUSES,
									  default=BUSY)


#######################################################################################
# Experimental data v2
#######################################################################################
class Experiment(models.Model):
	project = models.ForeignKey(Project)
	name = models.CharField(max_length=255)
	notes = models.CharField(max_length=2048, null=True)

class Condition(models.Model):
	experiment = models.ForeignKey(Experiment)
	name = models.CharField(max_length=255)
	notes = models.CharField(max_length=2048, null=True)


class Observation(models.Model):
	condition = models.ForeignKey(Condition)
	species = models.CharField(max_length=255)

	time = models.FloatField()
	value = models.FloatField()
	stddev = models.FloatField()
	steady_state = models.BooleanField()
	min_steady_state = models.FloatField(null=True)
	max_steady_state = models.FloatField(null=True)

	def create(cls, species, time, value, stddev, steady_state, min_steady_state, max_steady_state):
		data_point = cls(species=species, time=time, value=value, stddev=stddev,
							steady_state=steady_state,
							min_steady_state=min_steady_state,
							max_steady_state=max_steady_state)
		return data_point

class Treatment(models.Model):
	condition = models.ForeignKey(Condition)
	species = models.CharField(max_length=255)

	time = models.FloatField()
	value = models.FloatField()

	def create(cls, species, time, value):
		data_point = cls(species=species, time=time, value=value)
		return data_point
