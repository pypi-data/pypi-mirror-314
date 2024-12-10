from setuptools import setup

setup(
    name="axiomatic_pic",
    version="0.1.6",
    packages=["axiomatic_pic"],
    license="MIT",
    author="Leopoldo S.",
    author_email="leopoldo@axiomatic-ai.com",
    description="Axiomatic PIC magic assistant",
    keywords="PIC, Axiomatic, AI",
    url="https://www.axiomatic-ai.com",
    install_requires=["axiomatic", "ipython", "platformdirs"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Framework :: IPython",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
