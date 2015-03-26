from setuptools import setup

setup(name='Training planer',
      version='0.1',
      description='Plan your training and track the progress.',
      author='Anze Kolar',
      author_email='me@akolar.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=[
          'Django==1.7.3',
          'Pint==0.6',
          'django-jsonfield==0.9.13',
          'django-bootstrap3==5.0.3',
          'django-allauth==0.19.0',
          'djorm-pgarray==1.2',
          'fitparse',
          'django-extensions'
      ],
)
