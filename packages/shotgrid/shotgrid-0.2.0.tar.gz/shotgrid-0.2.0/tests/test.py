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
Contains shotgrid wrapper unit tests.
"""

import os
import time
import tempfile
import unittest

from shotgrid import Shotgrid

from shotgrid.sequence import Sequence
from shotgrid.shot import Shot
from shotgrid.task import Task


class TestBasic(unittest.TestCase):
    sg = None

    @classmethod
    def setUpClass(cls):
        cls.sg = Shotgrid()

    def test_demo(self):
        projects = self.sg.get_projects(name="Demo: Animation")
        self.assertEqual(len(projects), 1)

        assets = projects[0].get_assets()
        self.assertTrue(len(assets) > 0)

        seqs = projects[0].get_sequences()
        self.assertTrue(len(seqs) > 0)
        self.assertTrue(seqs[0].data.keys(), Sequence.fields)

        shots = projects[0].get_shots(code="bunny_080_0200")
        self.assertEqual(len(shots), 1)
        self.assertEqual(shots[0].data.code, "bunny_080_0200")
        self.assertEqual(shots[0].get_project().data.name, "Demo: Animation")

        playlists = projects[0].get_playlists()
        self.assertTrue(len(playlists) > 0)
        self.assertTrue(len(playlists[0].get_versions()) > 0)
        self.assertEqual(len(playlists[0].get_versions(code="abc123")), 0)
        v = playlists[0].get_versions()[0]
        self.assertTrue(hasattr(v.data, "sg_uploaded_movie"))

        seq_shots = seqs[0].get_shots()
        self.assertTrue(len(shots) != len(seq_shots))
        self.assertEqual(seq_shots[0].sequence().id(), seqs[0].id())
        self.assertTrue(seq_shots[0].data.keys(), Shot.fields)

        tasks = shots[0].get_tasks()
        self.assertTrue(len(tasks) > 0)
        self.assertTrue(tasks[0].data.keys(), Task.fields)

        versions = shots[0].get_versions()
        self.assertTrue(len(versions) > 0)
        self.assertEqual(versions[0].get_project().data.name, "Demo: Animation")

        mov = versions[0].movie
        self.assertEqual(mov.data.name, "BBB_08_a-team_020_ANIM_001.mov")

        fp = mov.download(folder=tempfile.mkdtemp())
        self.assertTrue(os.path.exists(fp))

        os.remove(fp)
        self.assertFalse(os.path.exists(fp))

    def test_create(self):
        projects = self.sg.get_projects(name="Template Project")
        self.assertEqual(len(projects), 1)

        asset_code = "foobar"
        asset = projects[0].create_asset(asset_code)
        self.assertEqual(asset.data.code, asset_code)

        # get a second instance of the new asset
        asset2 = projects[0].get_assets(asset_code)[0]
        self.assertEqual(asset.id(), asset2.id())
        self.assertEqual(asset.data.code, asset2.data.code)

        # update asset name on first instance
        asset.update(code="elmerfudd")
        self.assertEqual(asset.id(), asset2.id())
        self.assertNotEqual(asset.data.code, asset2.data.code)

        # refetch asset2, and get different fields
        asset2.refetch(fields=["id", "code", "image"])
        self.assertEqual(asset.id(), asset2.id())
        self.assertEqual(asset.data.code, asset2.data.code)
        self.assertTrue("image" in asset2.data.keys())

        seq_code = str(int(time.time()))
        seq = projects[0].create_sequence(seq_code)
        self.assertEqual(seq.data.code, seq_code)

        shot_code = "{}_010".format(seq_code)
        shot = seq.create_shot(shot_code)
        self.assertEqual(shot.data.code, shot_code)

        task = shot.create_task("MyTask", sg_status_list="wtg")
        self.assertEqual(task.data.content, "MyTask")
        self.assertEqual(task.data.sg_status_list, "wtg")

        task.update(sg_status_list="ip")
        self.assertEqual(task.data.sg_status_list, "ip")
        task = shot.get_tasks("MyTask")[0]
        self.assertEqual(task.data.sg_status_list, "ip")

        version_code = shot_code + "_MyTask_001"
        version = shot.create_version(version_code, task=task)
        self.assertTrue(version is not None)
        self.assertEqual(len(shot.get_versions()), 1)

        play_code = "{} review".format(seq_code)
        play = projects[0].create_playlist(play_code, versions=[version])
        self.assertTrue(play is not None)
        self.assertEqual(len(play.get_versions()), 1)

        version_code_2 = shot_code + "_MyTask_002"
        version_2 = shot.create_version(version_code_2, task=task)
        self.assertEqual(len(shot.get_versions()), 2)
        play.add_versions([version_2])
        self.assertEqual(len(play.get_versions()), 2)
        play.remove_versions([version_2])
        self.assertEqual(len(play.get_versions()), 1)

        asset.delete()
        play.delete()
        seq.delete()
        shot.delete()
        task.delete()
        version.delete()

        seqs = projects[0].get_sequences(code=seq_code)
        self.assertEqual(len(seqs), 0)

        shots = projects[0].get_shots(code=shot_code)
        self.assertEqual(len(shots), 0)
        self.assertEqual(len(shot.get_versions()), 0)

        plays = projects[0].get_playlists(play_code)
        self.assertEqual(len(plays), 0)

        assets = projects[0].get_playlists(asset_code)
        self.assertEqual(len(assets), 0)


if __name__ == "__main__":
    unittest.main()
