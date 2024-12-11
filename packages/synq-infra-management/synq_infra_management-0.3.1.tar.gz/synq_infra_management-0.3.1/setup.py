from setuptools import setup, find_packages

setup(
    name="synq_infra_management",
    version="0.3.1",
    packages=find_packages(),
    install_requires=[
        "getsynq-api-grpc-python",
        "grpcio",
        "grpcio-tools",
        "requests_oauthlib",
        "PyYAML",
    ],
    dependency_links=[
        "https://buf.build/gen/python",
    ],
    description="A package to compare and manage Synq SQL tests from YAML files",
    author="Bruno Farias",
    author_email="bruno.farias@avios.com",
    url="https://github.com/IAG-Loyalty/synq-infra-management/synq_infra_management",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
