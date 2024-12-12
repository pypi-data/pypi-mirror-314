import setuptools

# PyPi upload Command
# rm -r dist ; python setup.py sdist ; python -m twine upload dist/*

manifest: dict = {
    "name": "unstructured_expanded",
    "license": "MIT",
    "author": "Isaac Kogan",
    "version": "0.16.5",
    "email": "info@isaackogan.com"
}

if __name__ == '__main__':
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

    setuptools.setup(
        name=manifest["name"],
        packages=setuptools.find_packages(),
        version=manifest["version"],
        license=manifest["license"],
        description="Expansion to the unstructured package, adding support for image extraction.",
        author=manifest["author"],
        author_email=manifest["email"],
        url="https://github.com/isaackogan/unstructured_expanded",
        long_description=long_description,
        long_description_content_type="text/markdown",
        keywords=[
            "nlp", "natural language processing", "text", "documents", "images", "image extraction",
            "pdf", "docx", "pptx", "semantic", "semantic analysis", "semantic parsing", "semantic extraction",
            "unstructured"
        ],
        install_requires=[
            "unstructured>=0.16.4",
        ],
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Topic :: Software Development :: Build Tools",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: English",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
        ]
    )