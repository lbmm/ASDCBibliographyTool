try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import pubblicazioniASDC

config = {
    'description': 'ASDC Publication portal',
    'author': 'fmoscato',
    'version': pubblicazioniASDC.__version__,
    'download_url': 'Where to download it.',
    'url': 'publications.asdc.asi.it',
    'author_email': 'fmoscato@asdc.asi.it',
    'install_requires': ['nose', 'pymongo', 'reportlab', 'bottle'],
    'packages': ['pubblicazioniASDC'],
    'scripts': [],
    'name': 'PubblicazioniASDC',
    'long_description': open('README.md').read(),
    'entry_points': {
        'console_scripts': [
            'serve = pubblicazioniASDC.publication:run_server',
                           ]
                    },
    'package_data': {
        'pubblicazioniASDC': ['static/*.css',
                              'static/images/*.{png,jpg,gif,html}',
                              'static/images/sdh_files/*',
                              'js/*.js',
                              'views/*.tpl'],
       },
        'include_package_data': True
}

setup(**config)
