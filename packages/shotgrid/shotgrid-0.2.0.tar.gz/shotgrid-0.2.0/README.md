shotgrid
========

This is an object-oriented wrapper around the shotun api3 Python API, that
includes classes for each shotgrid entity type with convenience methods.

## Installation

The easiest way to install:

```bash
$ pip install -U shotgrid
```

Alternatively, use distman to dist to a deployment area using options defined
in the `dist.json`:

```bash
$ distman [-d]
```

Files and directories can be distributed from any folder or git repo containing
a `dist.json` file.

## Configuration

Default settings are stored in an [envstack](https://github.com/rsgalloway/envstack)
.env file. They can be stored in the default stack, or in a namespaced `shotgrid.env`
stack file to keep settings separate.

Start by renaming or copying the `example_shotgrid.env` file:

```bash
$ cp example_shotgrid.env shotgrid.env
```

Then edit it's contents with the appropriate values:

```yaml
LOG_LEVEL: INFO
SG_SCRIPT_URL: https://example.shotgunstudio.com
SG_SCRIPT_NAME: script_name
SG_SCRIPT_KEY: XXXXXX
```

## Usage

Basic usage:

```python
>>> from shotgrid import Shotgrid
>>> sg = Shotgrid()
>>> show = sg.get_projects("Demo: Animation")[0]
>>> shot = show.get_shots("bunny_080_0200")[0]
>>> tasks = shot.get_tasks()
```

Requests can be strung together:

```python
>>> sg.get_projects("Demo: Animation")[0].get_sequences("080")[0].get_shots()
[<Shot "bunny_080_0100">, <Shot "bunny_080_0200">, <Shot "bunny_080_0300">]
```

#### Core API

The Shotgrid class is a subclass of shotgrid_api3.Shotgrid, so you can drop down
to the core API at any time or from any object:

```python
>>> sg.find(filters, fields)
>>> shot.api().find("Task", [["id", "is", 12345]])
[{'type': 'Task', 'id': 12345}]
```

#### Download Versions

```python
>>> version = sg.get_projects(show)[0].get_shots(shot)[0].get_versions()[0]
>>> version.movie
<Movie "bunny_080_0200_v001.mov">
>>> version.movie.download("/var/tmp")
```