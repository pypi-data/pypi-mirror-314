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
Contains Playlist base class.
"""

from shotgrid.base import Entity
from shotgrid.logger import log
from shotgrid.version import Version


class Playlist(Entity):
    """Shotgrid Playlist entity."""

    entity_type = "Playlist"

    fields = [
        "id",
        "code",
        "description",
        "locked",
        "versions",
    ]

    def __init__(self, *args, **kwargs):
        super(Playlist, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<{0} "{1}">'.format(self.__class__.__name__, self.data.code)

    def add_versions(self, versions):
        """Adds a list of Versions to this playlist.

        :param versions: list of Versions
        """
        return self.update(
            versions=[v.data for v in versions], update_mode={"versions": "add"}
        )

    def get_versions(self, code=None, filters=None, fields=None):
        """Gets a list of versions for this playlist.

        :param code: sg version code
        :param filters: additional filters (optional)
        :param fields: which fields to return (optional)
        :return: list of versions for this playlist
        :raise: gaierror if can't connect to shotgrid.
        """
        versions = []

        fields = fields or Version.fields
        params = [["playlists", "is", self.data]]

        if code:
            params.append(["code", "is", code])

        if filters:
            params.extend(filters)

        results = self.api().find("Version", params, fields)

        for r in results:
            versions.append(Version(self, r))

        return versions

    def remove_versions(self, versions):
        """Removes a list of Versions from this playlist.

        :param versions: list of Versions
        """
        return self.update(
            versions=[v.data for v in versions], update_mode={"versions": "remove"}
        )
