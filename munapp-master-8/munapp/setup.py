from setuptools import setup, find_packages
setup(
    name="app",
    version="0.1",
    packages=find_packages(),

    # Check that a package for install is available from PyPI
    install_requires=[
            'flask>=0.12',
            'alembic==0.9.8',
            'click==6.7',
            'dominate==2.3.1',
            'Flask==0.12.2',
            'Flask-Bootstrap==3.3.7.1',
            'Flask-Login==0.4.1',
            'Flask-Migrate==2.1.1',
            'Flask-SQLAlchemy==2.3.2',
            'Flask-WTF==0.14.2',
            'itsdangerous==0.24',
            'Jinja2==2.10',
            'Mako==1.0.7',
            'MarkupSafe==1.0',
            'python-dateutil==2.7.0',
            'python-editor==1.0.3',
            'six==1.11.0',
            'SQLAlchemy==1.2.5',
            'visitor==0.1.3',
            'Werkzeug==0.14.1',
            'WTForms==2.1',
    ], 

    package_data={
        '': ['*.txt', '*.pdf', '*.css', '*.db','*.ini','*.html','*.png','*.pod'],
        # And everything in the test, doc, static and jinja folders:
        'app': ['migrations/*.py','migrations/versions/*','templates/*','static/*','tests/*','docs/*','tests/*'],
    },

    # metadata for upload to PyPI
    author="Justin Heffernan, Taswaf Rahman, Scott Jennings, Tim Griffin",
    author_email="",
    description="This is MUNAPP",
    license="COMP2005 students", # this is incorrect usage
    keywords="flask forum website",
    url="",  

    # could also include project_urls, long_description, download_url, classifiers, etc.

    # setup_requires=['pytest-runner',], # suggested from flaskr tutorial - but not needed
    # tests_require=['pytest',], # suggested from flaskr tutorial - but not needed
)


