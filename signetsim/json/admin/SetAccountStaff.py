#!/usr/bin/env python
""" SetAccountStaff.py


	This file...

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

from signetsim.json.JsonRequest import JsonRequest
from signetsim.models import User

class SetAccountStaff(JsonRequest):

	def __init__(self):
		JsonRequest.__init__(self)

	def post(self, request, *args, **kwargs):

		if 'username' in request.POST and 'status' in request.POST:
			username = request.POST['username']
			status = request.POST['status']

			if User.objects.filter(username=username).exists():

				user = User.objects.get(username=username)
				user.is_staff = (status == 'true')
				user.save()

				self.data.update({'result': 'ok'})
			else:
				self.data.update({'result': 'err'})
		else:
			self.data.update({'result': 'err'})

		return JsonRequest.post(self, request, *args, **kwargs)


