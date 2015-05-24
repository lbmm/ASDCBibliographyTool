try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'ASDC Publication portal',
    'author': 'fmoscato',
    'version': 2.12,
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
        'pubblicazioniASDC': ['static/*', 'static/images/*', 'js/*.js', 'views/*.tpl'],
       },
        'include_package_data': True
}

setup(**config)
