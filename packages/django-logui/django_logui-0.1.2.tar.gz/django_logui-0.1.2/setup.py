import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-logui",
    version="0.1.2",
    author="xlartas",
    author_email="ivanhvalevskey@gmail.com",
    description="Flexible, fast and productive UI for logging in Django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Artasov/django-logui",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=4.0,<5.3",
        "adjango>=0.2.8",
    ],
    classifiers=[
        "Framework :: Django",
        "Framework :: Django :: 4.0",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    python_requires='>=3.8',
    keywords='django-logui django utils funcs features logs logging logger',
    project_urls={
        'Source': 'https://github.com/Artasov/django-logui',
        'Tracker': 'https://github.com/Artasov/django-logui/issues',
    },
)
