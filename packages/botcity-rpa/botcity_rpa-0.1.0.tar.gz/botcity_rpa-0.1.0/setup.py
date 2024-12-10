from setuptools import setup, find_packages

setup(
    name='botcity-rpa',  # Name of your package
    version='0.1.0',    # Version of your package
    packages=find_packages(),  # This will automatically find all packages in the directory
    install_requires=[   # List any dependencies here
        'some_dependency',  # Example
        # 'other_dependency',
    ],
    entry_points={  # This allows setting an entry point (if needed)
        'console_scripts': [
            'my-bot=bot:main',  # You can point this to the main function in bot.py
        ],
    },
    description='My bot project description',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your_email@example.com',
    url='https://github.com/jpzinn654/my-package',  # Link to your project repository
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
