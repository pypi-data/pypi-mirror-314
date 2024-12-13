from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
import subprocess
from os import path, getenv, getcwd

meta_file = path.join(path.dirname(path.abspath(__file__)), 'zcatalyst_sdk', '__version__.py')
zcatalyst_dir = path.join(path.dirname(path.abspath(__file__)), 'zcatalyst_sdk')
meta = {}
with open(meta_file) as fp:
    exec(fp.read(), meta)

docs_dir = getenv('DOCS_OUTPUT_DIR', path.join(getcwd(), 'docs'))
class BuildWithDocs(build_py):
    def run(self):
        subprocess.run(
                ["pdoc", "-o", docs_dir, "--include-undocumented", zcatalyst_dir],
                check=True
        )

setup(
    name='zcatalyst_sdk',
    version=meta['__version__'],
    description='Zoho Catalyst SDK for Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Catalyst by Zoho',
    author_email= 'support@zohocatalyst.com',
    url='https://catalyst.zoho.com/',
    scripts=[],
    packages=find_packages(exclude=['tests*']),
    install_requires=['requests==2.28.1', 'typing-extensions==4.10.0'],
    license='Apache License 2.0',
    python_requires=">= 3.9",
    keywords=['zcatalyst', 'zoho', 'catalyst', 'serverless', 'cloud', 'SDK', 'development'],
    cmdclass={"build_py": BuildWithDocs},
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers'
    ],
)
