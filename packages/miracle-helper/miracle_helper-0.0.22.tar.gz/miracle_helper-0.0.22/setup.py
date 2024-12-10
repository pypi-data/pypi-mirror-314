from setuptools import setup, find_packages

setup(
    name='miracle-helper',
    version='0.0.22',
    description='MIRACLE.cowf LangChain Helper',
    author='MIRACLE.cowf',
    author_email='miracle.cowf@gmail.com',
    url='https://github.com/MIRACLE-cowf/Powerful-Auto-Researcher.git',
    install_requires=['langchain', 'langchain-anthropic', 'langchain-openai'],
    packages=find_packages(exclude=[]),
    keywords=['miracle', 'miracle.cowf', 'custom langchain', 'langchain helper', 'pypi'],
    python_requires='>=3.10',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
