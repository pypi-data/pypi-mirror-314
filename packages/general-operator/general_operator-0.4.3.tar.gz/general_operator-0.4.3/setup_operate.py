from setuptools import setup

setup(
    name='general_operator',
    version='0.4.3',
    packages=['general_operator', 'general_operator.app', 'general_operator.app.SQL', 'general_operator.app.influxdb',
              'general_operator.app.redis_db', 'general_operator.dependencies', 'general_operator.function', 'general_operator.routers',],
    install_requires=[
        'fastapi>=0.83.0',
        'influxdb-client>=1.22.0',
        'redis>=5.0.1',
        'SQLAlchemy>=2.0.10'
    ],
    author='wilson',
    author_email='wwilson008@gmail.com',
    description='general operator for fastapi write sql and redis',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/littlebluewhite/node_object_module',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.8',
)
