import json
import os
import platform

from datetime import datetime

from ._funcs import check_string, generate_file
from .files import (
    PYPROJECT_TOML,
    MIT_LICENSE,
    README,
    GITIGNORE,
    TEST_EXAMPLE,
    TEST_MAIN,
    COMMIT_PY,
)


def read_struct() -> dict:
    """Loads the structure of the project from the struct.json file

    :return: The structure dictionary
    :rtype: dict

    :raises:
        * FileNotFoundError: If there's no struct.json file in the current folder
    """
    with open("struct.json", mode="r") as struct_file:
        structure = json.load(struct_file)
    return structure


def build_base(structure: dict) -> None:
    """Builds the following:
        - .gitignore file;
        - LICENSE file;
        - pyproject.toml file;
        - README.md file;
        - venv

    :param structure: The structure of the project retreived from struct.json file.
    :type structure: dict

    :raises:
        * RequiredFieldError: Inherited from :func:`check_string()`
    """

    proj_name = check_string(structure.get("project_name_required"), True)
    version = check_string(structure.get("project_version"))
    version = "0.0" if version == "//" else version
    description = check_string(structure.get("project_description"))
    author = check_string(structure.get("author"))
    author_email = check_string(structure.get("author_email"))
    homepage = check_string(structure.get("homepage"))
    github_link = check_string(structure.get("github_link"))
    github_issues = github_link + "/issuses"
    dependencies = structure.get("dependencies")

    generate_file(
        PYPROJECT_TOML.replace("%proj_name%", proj_name)
        .replace("%version%", version)
        .replace("%author%", author)
        .replace("%email%", author_email)
        .replace("%brief%", description)
        .replace("%dependencies%", json.dumps(dependencies))
        .replace("%homepage%", homepage)
        .replace("%github%", github_link)
        .replace("%issues%", github_issues),
        "pyproject.toml",
    )

    generate_file(
        MIT_LICENSE.replace("%author%", author).replace(
            "%year%", str(datetime.now().year)
        ),
        "LICENSE",
    )

    generate_file(README.replace("%github_link%", github_link), "README.md")


def create_venv(structure: dict) -> None:
    """Creates a vistual environment and installs dependencies and dev dependencies

    :param structure: The structure of the project retreived from struct.json file
    :type structure: dict
    """

    dependencies = structure.get("dependencies")
    dev_dependencies = structure.get("dev_dependencies")
    pip = "venv/bin/pip"

    if platform.system() == "Windows":
        os.system("python -m venv venv")

        pip = "venv/Scripts/pip.exe"

    else:
        os.system("python3 -m venv venv")

    for dependency in dependencies:
        os.system(f"{pip} install {dependency}")

    for dependency in dev_dependencies:
        os.system(f"{pip} install {dependency}")


def git_configuration(structure: dict) -> None:
    """Configures git and github

    :param structure: The structure of the project retreived from struct.json file
    :type structure: dict
    """

    git = structure.get("configure_git")
    if not git:
        return

    github = structure.get("configure_github")

    gitignore_files = structure.get("gitignore_files")

    gitignore_files = "\n".join(gitignore_files)

    generate_file(GITIGNORE.replace("%gitignore_files%", gitignore_files), ".gitignore")

    os.system("git init")

    branches = structure.get("git").get("branches")

    for branch in branches:
        os.system(f"git checkout -b {branch}")

    os.system("git checkout master")

    os.system("git add .")

    os.system('git commit -m "Initial commit - $(date)"')

    if not (github):
        return

    remotes = structure.get("git").get("github").get("remotes")

    for name, url in remotes.items():
        os.system(f"git remote add {name} {url}")
        os.system(f"git push {name} master")


class ModulesBuilder:
    """Class made to easily build structure

    :param structure: The structure of the project retreived from struct.json file
    :type structure: dict
    """

    def build_inner_structure(self, structure: dict) -> None:
        """Parses the struct and creates folders / files for the module / submodules

        :param structure: The structure of the project as in struct.json file
        :type structure: dict
        """

        for folder, struct in structure.items():
            os.mkdir(folder)
            os.chdir(folder)
            for element in struct:
                if isinstance(element, dict):
                    self.build_inner_structure(element)
                else:
                    os.system(f"touch {element}")

            os.chdir("..")

    def build_modules_structure(self, structure) -> None:
        """Builds the module structure"""

        structure = structure.get("structure")
        for element in structure:
            if isinstance(element, dict):
                self.build_inner_structure(element)
            else:
                os.system(f"touch {element}")


def sphinx_configuration(structure: dict) -> None:
    """Configures sphinx documentation

    :param structure: The structure of the project retreived from struct.json file
    :type structure: dict
    """

    if not structure.get("user_sphinx"):
        return

    pip = "venv/bin/pip"

    if platform.system() == "Windows":
        pip = "venv/Scripts/pip.exe"

    os.system(f"{pip} install sphinx sphinx-rtd-theme")
    os.mkdir("docs")
    os.chdir("docs")
    os.system("sphinx-quickstart")
    os.chdir("..")
    os.system("sphinx-apidoc -o docs .")

    with open("docs/index.rst", mode="r") as index_rst:
        lines = index_rst.readlines()

    insert_line_index = 0

    for index, line in enumerate(lines):
        if ":caption:" in line:
            insert_line_index = index + 2

    lines.insert(insert_line_index, "modules")

    with open("docs/index.rst", mode="w") as index_rst:
        index_rst.writelines(lines)

    with open("docs/conf.py", mode="r") as conf_py:
        lines = conf_py.readlines()

    insert_line_index = 0

    for index, line in enumerate(lines):
        if "alabaster" in line:
            lines[index] = line.replace("alabaster", "sphinx_rtd_theme")

    for index, line in enumerate(lines):
        if "extensions = []" in line:
            line[index] = (
                'extensions = ["sphinx.ext.todo", "sphinx.ext.viewcode", "sphinx.ext.autodoc"]'
            )

    for index, line in enumerate(lines):
        if "project = " in line:
            insert_line_index = index

    lines.insert(
        insert_line_index,
        """import os
import sys

sys.path.insert(0, os.path.abspath(".."))""",
    )

    with open("docs/conf.py", mode="w") as conf_py:
        conf_py.writelines(lines)

    os.chdir("docs")

    os.system("sphinx-build -M html . _build")


def tests_configuration(structure: dict) -> None:
    """Configures test folder

    :param structure: The structure of the project retreived from struct.json file
    :type structure: dict
    """

    if not (structure.get("configure_test_folder")):
        return

    os.mkdir("tests")
    os.chdir("tests")

    generate_file(TEST_MAIN, "test.py")
    generate_file(TEST_EXAMPLE, "test_example.py")

    os.chdir("..")


def create_commit(structure: dict) -> None:
    """Generates a custom script which makes tests, generates documentation, commits and pushes all in one
    NOTE: The file is generated ONLY if the following flags are set to trye in structure.json:

    * "configure_test_folder"
    * "use_sphinx"
    * "configure_git"
    * "configure_github"

    :param structure: The structure of the project retreived from struct.json file
    :type structure: dict
    """
    configure_test_folder = structure.get("configure_test_folder")
    use_sphinx = structure.get("use_sphinx")
    configure_git = structure.get("configure_git")
    configure_github = structure.get("configure_github")

    if configure_test_folder and use_sphinx and configure_git and configure_github:
        pip = "venv/bin/pip"
        if platform.system() == "Windows":
            pip = "venv/Scripts/pip.exe"

        os.system(f"{pip} install pick")
        generate_file(COMMIT_PY, "commit.py")
