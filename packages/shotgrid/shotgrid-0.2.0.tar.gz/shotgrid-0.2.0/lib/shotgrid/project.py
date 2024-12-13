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
Contains Project class.
"""

import socket

from shotgrid.asset import Asset
from shotgrid.base import Entity
from shotgrid.logger import log
from shotgrid.playlist import Playlist
from shotgrid.sequence import Sequence
from shotgrid.shot import Shot


class Project(Entity):
    """Shotgrid Project entity."""

    entity_type = "Project"

    fields = [
        "id",
        "sg_description",
        "code",
        "name",
        "sg_status",
        "sg_type",
    ]

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)

    def create_asset(self, code, **data):
        """Creates a new Asset entity.

        :param code: asset code
        :return: Asset object
        """
        data.update({"code": code})
        results = self.create("Asset", data=data)
        return Asset(self, results)

    def create_playlist(self, code, versions, **data):
        """Creates a new Playlist that lives on this sequence.

        :param code: Playlist code
        :param versions: list of Versions to add to Playlist
        :return: Playlist object
        """
        data.update({"code": code, "versions": [v.data for v in versions]})
        results = self.create("Playlist", data=data)
        return Playlist(self, results)

    def create_sequence(self, code, **data):
        """Creates a new sequence.

        :param code: sequence code
        :return: Sequence object
        """
        data.update({"code": code})
        results = self.create("Sequence", data=data)
        return Sequence(self, results)

    def create_shot(self, code, sequence, **data):
        """Creates a new Shot.

        :param code: shot code
        :param sequence: Sequence class object
        :return: Shot object
        """
        data.update({"sg_sequence": sequence.data, "code": code})
        results = self.create("Shot", data=data)
        return Shot(self, results)

    def get_assets(self, code=None, fields=None):
        """Returns a list of assets from shotgrid for this project.

        :param code: asset code
        :param fields: which fields to return (optional)
        :return: asset list from shotgrid for given project
        :raise: socket.gaierror if can't connect to shotgrid
        """

        fields = fields or Asset.fields
        params = [["project", "is", self.data]]

        if code is not None:
            params.append(["code", "is", code])

        try:
            results = self.api().find("Asset", params, fields=fields)
            assets = list()
            for r in results:
                assets.append(Asset(self, data=r))
            return assets

        except socket.gaierror as e:
            raise

    def get_playlists(self, code=None, fields=None):
        """Returns a list of playlists from shotgrid for this project.

        :param code: sequence code
        :param fields: which fields to return (optional)
        :return: list of Playlists
        """

        fields = fields or Playlist.fields
        params = [["project", "is", self.data]]

        if code is not None:
            params.append(["code", "is", code])

        try:
            results = self.api().find("Playlist", params, fields=fields)
            playlists = list()
            for r in results:
                playlists.append(Playlist(self, data=r))
            return playlists

        except socket.gaierror as e:
            raise

    def get_sequences(self, code=None, fields=None):
        """Returns a list of sequences from shotgrid for this project.

        :param code: sequence code
        :param fields: which fields to return (optional)
        :return: sequence list from shotgrid for this project
        :raise: socket.gaierror if can't connect to shotgrid
        """

        fields = fields or Sequence.fields
        params = [["project", "is", self.data]]

        if code is not None:
            params.append(["code", "is", code])

        try:
            results = self.api().find("Sequence", params, fields=fields)
            seqs = list()
            for r in results:
                seqs.append(Sequence(self, data=r))
            return seqs

        except socket.gaierror as e:
            raise

    def get_shots(self, code=None, fields=None):
        """Returns a list of shots from shotgrid for this project.

        :param code: shot code
        :param fields: which fields to return (optional)
        :return: shot list from shotgrid for given project
        :raise: socket.gaierror if can't connect to shotgrid
        """

        fields = fields or Shot.fields
        params = [["project", "is", self.data]]

        if code is not None:
            params.append(["code", "is", code])

        try:
            results = self.api().find("Shot", params, fields=fields)
            shots = list()
            for r in results:
                shots.append(Shot(self, data=r))
            return shots

        except socket.gaierror as e:
            raise

    def get_steps(self, short_name=None, filters=None, fields=None):
        """Returns a list of pipeline steps for this project.

        :param short_name: step short name
        :param filters: list of filters to apply to the query
        :param fields: which fields to return (optional)
        :return: list of steps for this entity
        :raise: gaierror if can't connect to shotgrid
        """
        from shotgrid.step import Step

        fields = fields or Step.fields
        params = []

        if short_name is not None:
            params.append(["short_name", "is", short_name])

        if filters is not None:
            params.extend(filters)

        try:
            results = self.api().find("Step", params, fields=fields)
            steps = list()
            for r in results:
                steps.append(Step(self, data=r))
            return steps

        except socket.gaierror as err:
            log.error(err.message)
            raise
