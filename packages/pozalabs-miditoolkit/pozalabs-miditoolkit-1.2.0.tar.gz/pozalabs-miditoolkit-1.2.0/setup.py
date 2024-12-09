# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['miditoolkit', 'miditoolkit.midi', 'miditoolkit.pianoroll']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5,<4.0', 'mido>=1.1.16,<2.0.0', 'numpy>=1.19,<2.0']

setup_kwargs = {
    'name': 'pozalabs-miditoolkit',
    'version': '1.2.0',
    'description': 'A python package for working with MIDI data files. (POZAlabs forked)',
    'long_description': "# Miditoolkit\n\nA Python package for working with MIDI files.\n\n[![PyPI version fury.io](https://badge.fury.io/py/miditoolkit.svg)](https://pypi.python.org/pypi/miditoolkit/)\n[![Python 3.7](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/release/)\n[![GitHub CI](https://github.com/YatingMusic/miditoolkit/actions/workflows/pytest.yml/badge.svg)](https://github.com/YatingMusic/miditoolkit/actions/workflows/pytest.yml)\n[![GitHub license](https://img.shields.io/github/license/YatingMusic/miditoolkit.svg)](https://github.com/YatingMusic/miditoolkit/blob/main/LICENSE)\n[![Downloads](https://static.pepy.tech/badge/miditoolkit)](https://pepy.tech/project/miditoolkit)\n[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nMiditoolkit works by loading/writing MIDIs with [mido](https://github.com/mido/mido) in a user-friendly way. It is inspired from [pretty_midi](https://github.com/craffel/pretty-midi), with similar usage and core features, but handles the MIDI events in native **[ticks](https://www.recordingblogs.com/wiki/midi-tick)** time unit instead of seconds. It also comes with a few optimizations and speed-ups, and can parse MIDI tracks into **piano-rolls** for computation or visualization purposes.\nIf you are working with seconds time units (for e.g. music transcription), you'll be likely better with pretty_midi. Otherwise, if you are working solely on MIDI and symbolic music, miditoolkit should provide slightly faster performances.\n\n## Main Features\n\n* MIDI\n    * Global\n        * ticks per beat\n        * tempo changes\n        * key signatures\n        * time signatures\n        * lyrics\n        * markers\n    * Instruments\n        * control changes\n        * pitch bend\n    * Editing\n        * chunk/cropping\n    * IO\n        * BytesIO\n* Piano-rolls\n    * Tools\n        * notes to piano-rolls\n        * piano-rolls to notes\n        * chromagram\n    * Visualization\n* External Library\n   * [structure analysis](https://github.com/wayne391/sf_segmenter)\n\n## TODO\n\n* better documentation;\n* finish the code cleaning of the pianoroll methods (vis);\n* a way to switch the time in seconds across the whole MidiFile object;\n* cropping Control Changes and bars;\n* symbolic features\n* new structural analysis\n\n## Installation\n\nYou can install miditoolkit via [PYPI](https://pypi.org/project/miditoolkit/):\n\n```bash\npip install miditoolkit\n```\n\n... or directly from git if you want to get the latest features or fixes (only recommended if you need it):\n\n```bash\npip install git+https://github.com/YatingMusic/miditoolkit\n```\n\n## Example Usage\n\n```python\nfrom miditoolkit import MidiFile\nfrom miditoolkit.midi.utils import example_midi_file\n\npath_midi = example_midi_file()\nmidi_obj = MidiFile(path_midi)\n\nprint(midi_obj)\n```\n\nOutput:\n\n```\nticks per beat: 480\nmax tick: 72002\ntempo changes: 68\ntime sig: 2\nkey sig: 0\nmarkers: 71\nlyrics: False\ninstruments: 2\n```\n\nA. [Parse and create MIDI files](examples/parse_and_create_MIDI_files.ipynb)\nB. [Piano-roll Manipulation](examples/pinoroll_manipulation.ipynb)\n\n## Philosophy\n\n* [mido](https://github.com/mido/mido) processes MIDI files in the lower level such as messages and ports, and is the backend pretty_midi and miditoolkit;\n* [pretty_midi](https://github.com/craffel/pretty-midi) parses MIDI files and pianorolls in seconds time unit, plus has audio related features;\n* [pypianoroll](https://github.com/salu133445/pypianoroll) parses MIDI files into pianorolls in ticks time unit.\n\n**Miditoolkit** is designed for handling MIDI in **[ticks](https://www.recordingblogs.com/wiki/midi-tick)**, the native time unit of the MIDI protocol. We keep the midi parser as simple as possible, and offer several important functions to complete the versatility. For example, piano-rolls, tick-to-second, chromagram, etc.\n",
    'author': 'pozalabs',
    'author_email': 'contact@pozalabs.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
