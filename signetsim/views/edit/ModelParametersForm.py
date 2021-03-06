#!/usr/bin/env python
""" ModelParametersForm.py


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

from libsignetsim.model.ModelException import ModelException
from signetsim.views.edit.ModelParentForm import ModelParentForm


class ModelParametersForm(ModelParentForm):

	def __init__(self, parent):

		ModelParentForm.__init__(self, parent)

		self.name = None
		self.reactionId = None
		self.sbmlId = None
		self.value = None
		self.constant = True
		self.unit = None
		self.notes = None
		self.SBOTerm = None

	def save(self, parameter):

		try:
			parameter.setName(self.name)
			parameter.setSbmlId(self.sbmlId)
			parameter.setValue(self.value)
			parameter.constant = self.constant

			if self.unit is not None:
				parameter.setUnits(self.parent.listOfUnits[self.unit])
			else:
				parameter.setUnits(None)

			parameter.setNotes(self.notes)

			if self.SBOTerm is not None:
				parameter.getAnnotation().setSBOTerm(self.SBOTerm)

		except ModelException as e:
			self.addError(e.message)

			self.printErrors()

	def read(self, request):

		self.id = self.readInt(request, 'parameter_id',
								"The indice of the parameter",
								required=False)

		self.name = self.readString(request, 'parameter_name',
								"The name of the parameter")

		self.sbmlId = self.readString(request, 'parameter_sbml_id',
								"The identifier of the parameter")

		self.value = self.readMath(request, 'parameter_value',
								"The size of the parameter",
								   required=False)

		self.unit = self.readInt(request, 'parameter_unit',
								"The indice of the unit of the parameter",
								max_value=len(self.parent.listOfUnits),
								required=False)

		self.constant = self.readOnOff(request, 'parameter_constant',
								"The constant property of the parameter")

		self.scope = self.readInt(request, 'parameter_scope',
								  "The scope of the parameter",
								  max_value=(len(self.parent.listOfReactions)+1))

		self.SBOTerm = self.readInt(request, 'parameter_sboterm',
									"The SBO term of the parameter",
									required=False)
