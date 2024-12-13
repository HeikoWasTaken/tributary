#!/usr/bin/env sh

set +x
set +u
set +e


# Setup/teardown script for local development
# because poetry > pip+venv ¯\_(ツ)_/¯


function setup_poetry {
    poetry init                                             \
        --no-interaction                                    \
        --python=^3.11                                      \
        --description="Ford virtual work experience project"
    poetry add $(cat requirements.txt)
}

function teardown_poetry {
    poetry remove $(poetry show --top-level | awk {'print $1'})
    poetry env remove --all
    rm ./pyproject.toml ./poetry.lock
}

function arg_description {
    echo -e "    $1:\t$2"
}

function get_help {
    normal="\033[0m"; bold="\033[1m"
    echo -e "${bold}Usage:${normal}"
    echo "   ./$(basename $0) [setup|teardown|help]"
    echo -e "${bold}arguments:${normal}"
    arg_description "help"     "Show help"
    arg_description "setup"    "Setup poetry environment"
    arg_description "teardown" "Teardown poetry environment"
}

# Make sure this script is executed from the correct directory
function check_exec_dir {
    if [[ ! "$0" -ef "./$(basename $0)" ]]; then
        echo "Error: $(basename $0) must be executed from the" \
            "$(basename $(dirname $0)) git repository root directory"
        exit 1
    fi
}

case $1 in
    "setup")    check_exec_dir && setup_poetry ;;
    "teardown") check_exec_dir && teardown_poetry ;;
    *)          get_help ;;
esac


