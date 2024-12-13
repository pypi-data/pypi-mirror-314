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
Contains wrapper class for shotgrid api.
"""

import socket

import shotgun_api3

from shotgrid import config
from shotgrid.asset import Asset
from shotgrid.base import Entity
from shotgrid.logger import log
from shotgrid.person import Person
from shotgrid.playlist import Playlist
from shotgrid.project import Project
from shotgrid.sequence import Sequence
from shotgrid.shot import Shot
from shotgrid.step import Step
from shotgrid.task import Task
from shotgrid.version import Version

# maps entity type string to wrapper class
entity_type_class_map = dict(
    [(cls.entity_type, cls) for cls in Entity.__subclasses__()]
)


class Shotgrid(shotgun_api3.Shotgun):
    """
    Shotgrid wrapper base class. Managed connection and starting point for
    all operations, e.g. ::

        >>> sg = Shotgrid(name=<name>, apikey=<key>)
        >>> projects = sg.get_projects()

    Shotgrid entity hierarchy:

        Shotgrid
            `- Project
                `- Sequence
                    `- Shot
                        |- Version
                        |    `- Movie
                        `- Task
                            `- Person

    """

    def __init__(
        self,
        url=config.SG_SCRIPT_URL,
        name=config.SG_SCRIPT_NAME,
        apikey=config.SG_SCRIPT_KEY,
    ):
        super(Shotgrid, self).__init__(url, name, apikey)
        self.url = url
        self.name = name
        self.apikey = apikey

    def __repr__(self):
        return '<{0} "{1}">'.format(self.__class__.__name__, self.name)

    def create_project(self, name, **data):
        """Creates and returns a new Project entity.

        :param name: project name
        :return: Project entity object
        """
        data.update({"name": name})
        results = self.create("Project", data=data)
        return Project(self, results)

    def find_entities(self, entity_type, filters):
        """Returns entities matching an entity type and filter list, e.g.
        find an asset with id 1440 ::

            sg.find_entities('Asset', [['id', 'is', 1440]])

        :param entity_type: the entity type string, e.g. Asset
        :param filters: list of filters to apply to the query, e.g. ::
            filters = [['id', 'is', 1440]]
        :returns wrapped entity object
        """
        entities = []
        entity_class = entity_type_class_map.get(entity_type)
        results = self.find(entity_type, filters, fields=entity_class.fields)
        for r in results:
            entity_type = r.get("type")
            entities.append(entity_class(self, data=r))
        return entities

    def get_projects(self, name=None, fields=None):
        """Returns a list of Project entities.

        :param name: project name
        :param fields: which fields to return (optional)
        :return: list of projects
        :raise: socket.gaierror if can't connect to shotgrid.
        """

        fields = fields or Project.fields
        params = []

        if name:
            params.append(["name", "is", name])

        try:
            results = self.find("Project", params, fields=fields)
            projects = list()
            for r in results:
                projects.append(Project(self, data=r))
            return projects

        except socket.gaierror as err:
            log.error(err.message)
            raise

    def parent(self):
        return None

    def type(self):
        """Returns shotgrid entity type as str."""
        return self.__class__.__name__
