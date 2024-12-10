from enum import Enum
from os import getcwd
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, Union

import click
from tornado.template import Template

from tinybird.feedback_manager import FeedbackManager


class Provider(Enum):
    GitHub = 0
    GitLab = 1


WORKFLOW_VERSION = "v3.1.0"

DEFAULT_REQUIREMENTS_FILE = "tinybird-cli>=5,<6"

GITHUB_CI_YML = """
name: Tinybird - CI Workflow

on:
  workflow_dispatch:
  pull_request:
    branches:
      - main
      - master
    types: [opened, reopened, labeled, unlabeled, synchronize, closed]{% if data_project_dir != '.' %}
    paths:
      - '{{ data_project_dir }}/**'{% end %}

concurrency: ${{! github.workflow }}-${{! github.event.pull_request.number }}

jobs:
  ci:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: '{{ data_project_dir }}'
    services:
      tinybird:
        image: tinybirdco/tinybird-local:latest
        ports:
          - 80:80
    steps:
      - uses: actions/checkout@v3
      - name: Install Tinybird CLI
        run: curl -LsSf https://api.tinybird.co/static/install.sh | sh
      - name: Build project
        run: tb build
"""


GITLAB_YML = """
include:
  - local: .gitlab/tinybird/*.yml

stages:
  - tests
"""


GITLAB_CI_YML = """
tinybird_ci_workflow:
  stage: tests
  interruptible: true
  needs: []
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"{% if data_project_dir != '.' %}
      changes:
        - .gitlab/tinybird/*
        - {{ data_project_dir }}/*
        - {{ data_project_dir }}/**/*{% end %}
  before_script:
    - curl -LsSf https://api.tinybird.co/static/install.sh | sh
  script:
    - cd $CI_PROJECT_DIR/{{ data_project_dir }}
    - tb build
  services:
    - name: tinybirdco/tinybird-local:latest
      alias: tinybird-local
"""


EXEC_TEST_SH = """
#!/usr/bin/env bash
set -euxo pipefail

export TB_VERSION_WARNING=0

run_test() {
    t=$1
    echo "** Running $t **"
    echo "** $(cat $t)"
    tmpfile=$(mktemp)
    retries=0
    TOTAL_RETRIES=3

    # When appending fixtures, we need to retry in case of the data is not replicated in time
    while [ $retries -lt $TOTAL_RETRIES ]; do
        # Run the test and store the output in a temporary file
        bash $t $2 >$tmpfile
        exit_code=$?
        if [ "$exit_code" -eq 0 ]; then
            # If the test passed, break the loop
            if diff -B ${t}.result $tmpfile >/dev/null 2>&1; then
                break
            # If the test failed, increment the retries counter and try again
            else
                retries=$((retries+1))
            fi
        # If the bash command failed, print an error message and break the loop
        else
            break
        fi
    done

    if diff -B ${t}.result $tmpfile >/dev/null 2>&1; then
        echo "✅ Test $t passed"
        rm $tmpfile
        return 0
    elif [ $retries -eq $TOTAL_RETRIES ]; then
        echo "🚨 ERROR: Test $t failed, diff:";
        diff -B ${t}.result $tmpfile
        rm $tmpfile
        return 1
    else
        echo "🚨 ERROR: Test $t failed with bash command exit code $?"
        cat $tmpfile
        rm $tmpfile
        return 1
    fi
    echo ""
}
export -f run_test

fail=0
find ./tests -name "*.test" -print0 | xargs -0 -I {} -P 4 bash -c 'run_test "$@"' _ {} || fail=1

if [ $fail == 1 ]; then
  exit -1;
fi
"""

APPEND_FIXTURES_SH = """
#!/usr/bin/env bash
set -euxo pipefail

directory="datasources/fixtures"
extensions=("csv" "ndjson")

absolute_directory=$(realpath "$directory")

for extension in "${extensions[@]}"; do
  file_list=$(find "$absolute_directory" -type f -name "*.$extension")

  for file_path in $file_list; do
    file_name=$(basename "$file_path")
    file_name_without_extension="${file_name%.*}"

    command="tb datasource append $file_name_without_extension datasources/fixtures/$file_name"
    echo $command
    $command
  done
done
"""


class CICDFile:
    def __init__(
        self,
        template: str,
        file_name: str,
        dir_path: Optional[str] = None,
        warning_message: Optional[str] = None,
    ):
        self.template = template
        self.file_name = file_name
        self.dir_path = dir_path
        self.warning_message = warning_message

    @property
    def full_path(self) -> str:
        return f"{self.dir_path}/{self.file_name}" if self.dir_path else self.file_name


class CICDGeneratorBase:
    cicd_files: List[CICDFile] = []

    def __call__(self, path: str, params: Dict[str, Any]):
        for cicd_file in self.cicd_files:
            if cicd_file.dir_path:
                Path(f"{path}/{cicd_file.dir_path}").mkdir(parents=True, exist_ok=True)
            content = Template(cicd_file.template).generate(**params)
            if Path(f"{path}/{cicd_file.full_path}").exists():
                continue
            with open(f"{path}/{cicd_file.full_path}", "wb") as f:
                f.write(content)
            click.echo(FeedbackManager.info_cicd_file_generated(file_path=cicd_file.full_path))
            if cicd_file.warning_message is not None:
                return FeedbackManager.warning_for_cicd_file(
                    file_name=cicd_file.file_name, warning_message=cicd_file.warning_message.format(**params)
                )

    def is_already_generated(self, path: str) -> bool:
        for cicd_file in self.cicd_files:
            if cicd_file.file_name and Path(f"{path}/{cicd_file.full_path}").exists():
                return True
        return False

    @classmethod
    def build_generator(cls, provider: str) -> Union["GitHubCICDGenerator", "GitLabCICDGenerator"]:
        builder: Dict[str, Union[Type[GitHubCICDGenerator], Type[GitLabCICDGenerator]]] = {
            Provider.GitHub.name: GitHubCICDGenerator,
            Provider.GitLab.name: GitLabCICDGenerator,
        }
        return builder[provider]()


class GitHubCICDGenerator(CICDGeneratorBase):
    cicd_files = [
        CICDFile(
            template=GITHUB_CI_YML,
            file_name="tinybird-ci.yml",
            dir_path=".github/workflows",
        ),
    ]


class GitLabCICDGenerator(CICDGeneratorBase):
    cicd_files = [
        CICDFile(
            template=GITLAB_YML,
            file_name=".gitlab-ci.yml",
            dir_path=".",
        ),
        CICDFile(
            template=GITLAB_CI_YML,
            file_name="tinybird-ci.yml",
            dir_path=".gitlab/tinybird",
            warning_message="Make sure to import the file in your .gitlab-ci.yml file, e.g., `include: '.gitlab/tinybird/*.yml'`.",
        ),
    ]


async def init_cicd(
    path: Optional[str] = None,
    data_project_dir: Optional[str] = None,
):
    for provider in Provider:
        path = path if path else getcwd()
        data_project_dir = data_project_dir if data_project_dir else "."
        generator = CICDGeneratorBase.build_generator(provider.name)
        params = {
            "data_project_dir": data_project_dir,
            "workflow_version": WORKFLOW_VERSION,
        }
        warning_message = generator(path, params)
        if warning_message:
            click.echo(warning_message)


async def check_cicd_exists(path: Optional[str] = None) -> Optional[Provider]:
    path = path if path else getcwd()
    for provider in Provider:
        generator = CICDGeneratorBase.build_generator(provider.name)
        if generator.is_already_generated(path):
            return provider
    return None
