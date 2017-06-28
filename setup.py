from setuptools import setup

setup(
    name='ss-utilization',
    use_scm_version={'write_to': 'swiftstackapi/version.py'},
    packages=['swiftstackapi'],
    url='https://github.com/swiftstack/ss-utilization',
    author='Trey Duskin',
    author_email='trey@swiftstack.com',
    description='utilization gathering tools for SwiftStack API',
    entry_points={
        'console_scripts': ['ss-util=swiftstackapi.cli:main']
    }
)
