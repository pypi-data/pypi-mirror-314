from dataclasses import dataclass, field


@dataclass
class BaseStructure:
    @dataclass
    class ProjectStructure:
        name: str
        version: str
        description: str
        readme: str

        @dataclass
        class AuthorStructure:
            name: str
            email: str

        authors: list[AuthorStructure]
        requires_python: str = field(metadata={"name": "requires-python"})
        dependencies: list

    project: ProjectStructure

    @dataclass
    class BuildSystemStructure:
        requires: list[str]
        build_backend: str = field(metadata={"name": "build-backend"})

    build_system: BuildSystemStructure = field(metadata={"name": "build-system"})


EXAMPLE_TOML = """
[project]
name = "tattl"
version = "dev"
description = "Totally Awesome Type-aware TOML Loader"
readme = "README.md"
authors = [
    { name = "thcrt", email = "110127860+thcrt@users.noreply.github.com" }
]
requires-python = ">=3.12"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[dependency-groups]
dev = [
    "mypy>=1.13.0",
    "pytest>=8.3.4",
    "ruff>=0.8.2",
]
"""


def test_example():
    import tattl
    import tomllib

    data = tattl.unpack_dict(tomllib.loads(EXAMPLE_TOML), BaseStructure)
    print(data)
    assert data == BaseStructure(
        project=BaseStructure.ProjectStructure(
            name="tattl",
            version="dev",
            description="Totally Awesome Type-aware TOML Loader",
            readme="README.md",
            authors=[
                BaseStructure.ProjectStructure.AuthorStructure(
                    name="thcrt", email="110127860+thcrt@users.noreply.github.com"
                )
            ],
            requires_python=">=3.12",
            dependencies=[],
        ),
        build_system=BaseStructure.BuildSystemStructure(
            requires=["hatchling"], build_backend="hatchling.build"
        ),
    )
