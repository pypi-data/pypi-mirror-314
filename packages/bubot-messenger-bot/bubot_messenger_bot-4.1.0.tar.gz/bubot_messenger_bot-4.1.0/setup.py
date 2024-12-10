import setuptools
from src.bubot_messenger_bot import __version__

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

setuptools.setup(
    name='bubot_messenger_bot',
    version=__version__,
    author="Razgovorov Mikhail",
    author_email="1338833@gmail.com",
    description="",
    # long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/razgovorov/bubot_messenger_bot.git",
    package_dir={'': 'src'},
    package_data={
        '': ['*.md', '*.json'],
    },
    packages=setuptools.find_namespace_packages(where='src'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: AsyncIO",
    ],
    python_requires='>=3.8',
    zip_safe=False,
    install_requires=[
        'bubot_core>=4.1.0',
        'bubot_helpers>=4.0.3',
    ]
)
