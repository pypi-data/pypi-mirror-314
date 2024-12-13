#!/usr/bin/env python
#
# Copyright (c) 2024, Ryan Galloway (ryan@rsgalloway.com)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
#  - Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
#  - Neither the name of the software nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

__doc__ = """
Contains Task base class.
"""

from shotgrid.base import Entity
from shotgrid.logger import log


class Task(Entity):
    """Shotgrid Task entity."""

    entity_type = "Task"

    fields = [
        "id",
        "code",
        "content",
        "name",
        "step",
        "sg_status_list",
        "task_assignees",
        "versions",
    ]

    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<{0} "{1}">'.format(self.__class__.__name__, self.data.content)

    def get_assignees(self, deep=False):
        """Returns a list of Person objects from shotgrid.

        If deep is False, returned data is shallow, only containing the
        following fields: id, name, and type.

        :param deep: return default Person fields (default False)
        :return: list of Persons assigned to this task
        :raise: gaierror if can't connect to shotgrid.
        """
        from shotgrid.person import Person

        if not deep:
            return [Person(self, r) for r in self.data.task_assignees]

        filters = [["id", "in", [p["id"] for p in self.data.task_assignees]]]
        return self.api().find_entities(Person.entity_type, filters)

    def step(self):
        """Returns the Task's Step object.

        :return: Step object for this Task
        :raise: gaierror if can't connect to shotgrid.
        """
        from shotgrid.step import Step

        step = Step(self, self.data.step)
        step.refetch()
        return step
