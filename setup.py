# Copyright (c) 2020 Adobe Inc.  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from setuptools import setup, find_packages

version_namespace = {}
with open('flask_proxy/version.py') as f:
    exec(f.read(), version_namespace)

test_deps = ['mock', 'pytest']

setup(name='ust-proxy',
      version=version_namespace['__version__'],
      description='Web proxy for HTTP testing',
      classifiers=[
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
          'Intended Audience :: Developers',
      ],
      url='https://github.com/vossen-adobe/flask_proxy',
      maintainer='Danimae Vossen',
      maintainer_email='per38285@adobe.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'Werkzeug',
          'flask',
          'PyYAML',
          'requests',
          'qparse'
      ],
      extras_require={
          'test': test_deps,
      },
      tests_require=test_deps,
      # entry_points={
      #     'console_scripts': [
      #         'user_sync = user_sync.app:main'
      #     ]
      # },
      )
