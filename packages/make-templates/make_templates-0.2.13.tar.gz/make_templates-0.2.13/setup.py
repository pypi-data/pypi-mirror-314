from setuptools import setup, find_packages

def find_version():
    with open("README.md", "r") as f:
        return f.readline()[17:].strip()

setup(
    name='make-templates',
    version=find_version(),
    py_modules=['make_templates'],
    packages=find_packages(),
    package_data={'make_templates': ['README.md']},
    install_requires=[
        "antlr4-python3-runtime==4.13.1",
        "pyyaml"
    ],
    url='http://olinfo.it',
    license='BSD',
    author='Giorgio Audrito',
    author_email='giorgio.audrito@unito.it',
    entry_points={'console_scripts': [
        'make-templates=make_templates.main:script'
    ]
    },
    description='Tool to produce templates for IOI-style tasks from an input/output description.',
    long_description_content_type='text/markdown',
)
