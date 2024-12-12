from setuptools import setup, find_packages

with open("requirements.txt", encoding="utf8") as f:
    requirements = f.readlines()

setup(
    name='dguard_oss',
    version=open("VERSION", encoding="utf8").read(),
    description='A command-line tool for interacting with MinIO.',
    author="Zhao Sheng",
    author_email="zhaosheng@lyxxkj.com.cn",
    long_description=open("README.md", encoding="utf8").read(),
    long_description_content_type="text/markdown",

    url='https://github.com/nuaazs/dguard_oss',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'oss=dguard_oss.cli:main',
            'oss-config=dguard_oss.config:check_config_cli',
            'oss-config-new=dguard_oss.config:create_new_config_cli',
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    include_package_data=True,

)
