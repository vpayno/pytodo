# pytodo

ToDo tracker CLI written in Python using Typer and Rich.

Starting with a starter tutorial from Patrick Loeber's "Task Tracker".

## Using PDM

- Installing PDM

Use this `runme` playbook task will either install or update `pdm`.

```bash { background=false category=setup closeTerminalOnSuccess=true excludeFromRunAll=true interactive=true interpreter=bash name=setup-pdm-install promptEnv=true terminalRows=10 }
set -ex

if [[ -z ${PYENV_ROOT} ]]; then
    pip install --user --upgrade pdm
else
    pip install --upgrade pdm
fi
printf "\n"
```

- Using PDM's virtual env

Use this `runme` playbook task to sync the project's virtual env.

```bash { background=false category=setup closeTerminalOnSuccess=true excludeFromRunAll=true interactive=true interpreter=bash name=setup-pdm-sync promptEnv=true terminalRows=10 }
set -ex

if [[ ! -d .venv ]]; then
    pdm venv create
    printf "\n"
fi

pdm venv list
printf "\n"

pdm sync
printf "\n"
```

- Update project dependencies

Use this `runme` playbook task to update the projects dependencies.

```bash { background=false category=setup closeTerminalOnSuccess=true excludeFromRunAll=true interactive=true interpreter=bash name=setup-pdm-update-deps promptEnv=true terminalRows=10 }
set -ex

pdm sync
printf "\n"

pdm outdated
printf "\n"

pdm update
printf "\n"

git add pdm.lock
git commit -m 'python: update dependencies'
```
