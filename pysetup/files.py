PYPROJECT_TOML = """[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "%proj_name%"
version = "%version%"
authors = [
    { name="%author%", email="%email%" },
]
description = "%brief%"
readme = "README.md"
dependencies = %dependencies%

requires-python = ">=3.8"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

[project.urls]
Homepage = "%homepage%"
Github = "%github%"
Issues = "%issues%"

[tool.setuptools.packages]
find={}
"""

MIT_LICENSE = """MIT License

Copyright (c) "%year%" "%author%"

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

GITIGNORE = """__pycache__
venv
tests
*.egg-info
%gitignore_files%"
"""

README = """# Install in editable mode:
```
pip install -e .
```

# Install from github:
```
pip install project_name@git+"%github_link%"
```
"""


TEST_MAIN = """import unittest

try:
    from tests.text_example import TestExampleClass
except Exception:
    from test_example import TestExampleClass

tests = ["Example"] # Write here the conditions to test TestClasses


def suite(*to_do):
    to_do = [todo[0] for todo in to_do]
    suite = unittest.TestSuite()
    if "Example" in to_do:
        for test in TestExampleClass.test_methods:
            suite.addTest(TestExampleClass(test))
    return suite


runner = unittest.TextTestRunner(verbosity=2)

if __name__ == "__main__":
    result = runner.run(suite(*tests))"""


TEST_EXAMPLE = """import unittest

class TestExampleClass(unittest.TestCase):
    test_methods = [
        "test_example1",
        "text_example2",
    ] # Write here all the functions to test

    def test_example1(self):
        self.assertEqual(1, 1)

    @unittest.expectedFailure
    def test_example2(self):
        self.assertEqual(2, 4)
"""


COMMIT_PY = """import platform
from os import system, chdir
from pick import pick
from tests.test import suite, runner, tests
from increase_proj_version import run as increase_version

if __name__ == "__main__":

    if platform.system()=="Windows":
        raise NotImplementedError("Commit.py does not work on windows")

    _, commit_if_test_not_passed = pick(
        [
            "DON'T COMMIT (Recommended)",
            "Commit anyway",
            "Don't run tests (Not recommended)",
        ],
        "Choose tests handling:",
    )

    _, generate_documentation_before_committing = pick(
        ["Generate", "Don't generate"], "Wether to generate documentation or not:"
    )

    _, push_to_origin = pick(
        ["Push to GitHub", "Don't push to GitHub"],
        "Wether to push this commit to GitHub or not:",
    )

    match commit_if_test_not_passed:

        case 0:
            tests_to_do = pick(tests, "Choos what you want to test:", "->", 0, True)
            result = runner.run(suite(*tests_to_do))
            if not result.wasSuccessful():
                print("Tests were not successful, commit aborted!")
                system("rm database.sqlite")
                quit()
            else:
                system("rm database.sqlite")

        case 1:
            tests_to_do = pick(tests, "Choos what you want to test:", "->", 0, True)
            result = runner.run(suite(*tests_to_do))
            system("rm database.sqlite")

        case 3:
            pass

    if generate_documentation_before_committing == 0:
        print("Generating documentation")
        chdir("ncdbtht_server")
        system("sphinx-apidoc -o ../docs .")
        chdir("../docs")
        system("sphinx-build -M html . _build")
        chdir("..")

    message = input("Commit message: ")
    increase_version()

    system("git add .")
    system(f'git commit -m "{message} - $(date)"')

    if push_to_origin == 0:
        system("git branch>branches")
        with open("branches", mode="r") as branches:
            lines = branches.readlines()

        for line in lines:
            if "*" in line:
                branch = line.replace("* ", "").replace(" ", "")
        system("rm branches")
        system(f"git push origin {branch}")
"""


STRUCT = """{
    "project_name_required":"Your project name here",
    "project_version": "0.0",
    "project_description":"Project brief description",
    "author":"Author",
    "author_email":"Your email here",
    "homepage":"Homepage of the project",
    "github_link":"Github repo link",
    "github_issues":"Github issues link here",
    "gitignore_files":[
        "scripts",
        "struct.json",
        "docs/*",
        "!dics/_build",
        "docs/_build/doctrees",
        "logs",
        ".vscode"
    ],
    "dependencies":[],
    "dev_dependencies":["pylogger@git+https://github.com/GBiondo1310/pylogger.git"],
    "use_commit_script":true,
    "configure_test_folder":true,
    "use_sphinx":true,
    "configure_git":true,
    "configure_github":true,
    "git":{
        "branches":[
            "master",
            "dev"
        ],
        "github":{
            "remotes":{
                "origin":"github_link"
            }
        }
    },
    "structure":[
        {
            "scripts":[
                "main.py"
            ]
        },
            {
                "package_name":[
                    "__init__.py",
                    "__main__.py",
                    {
                        "subpackage1":[
                            "__init__.py"
                        ],
                        "subpackage2":[
                            "__init__.py"
                        ]
                    }
                ]
            },
        "other.file",
        "other.file2"
    ]

}"""
