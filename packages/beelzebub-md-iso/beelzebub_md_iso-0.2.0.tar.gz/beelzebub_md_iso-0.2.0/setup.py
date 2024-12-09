# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['md_iso']

package_data = \
{'': ['*'], 'md_iso': ['templates/*']}

install_requires = \
['beelzebub>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['beelzebub_md_iso = beelzebub.md_iso.__main__:main']}

setup_kwargs = {
    'name': 'beelzebub-md-iso',
    'version': '0.2.0',
    'description': 'Translate between mdJson and ISO19115-2',
    'long_description': "# beelzebub-md-iso\n\nBeelzebub-md-iso is a subpackage of [beelzebub](https://github.com/paul-breen/beelzebub).  Given a metadata record in [mdJSON](https://www.adiwg.org/projects/#mdjson-schemas) format, it will translate it to [ISO19115-2](https://www.iso.org/standard/67039.html) format.\n\n## Example Usage\n\n```\nfrom beelzebub.md_iso import MdjsonToISO19115_2\n\nconf = {\n    'reader': {'iotype': 'file'},\n    'writer': {'iotype': 'file'}\n}\nin_file = '/path/to/mdjson/metadata.json'\nout_file = '/path/to/iso19115-2/metadata.xml'\n\nx = MdjsonToISO19115_2(conf=conf)\nx.run(in_file, out_file)\n```\n\n#### References\n\nNOAA have useful [metadata resources](https://www.ncei.noaa.gov/resources/metadata), including this [ISO Workbook](http://www.ncei.noaa.gov/sites/default/files/2020-04/ISO%2019115-2%20Workbook_Part%20II%20Extentions%20for%20imagery%20and%20Gridded%20Data.pdf) and this [collection level metadata template](https://data.noaa.gov/waf/templates/iso_u/xml/ncei_template.xml).\n\n",
    'author': 'Paul Breen',
    'author_email': 'paul.breen6@btinternet.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/paul-breen/beelzebub-md-iso',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
