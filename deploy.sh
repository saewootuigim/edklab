#!/usr/bin/env bash
#
# Deploy the latest pushed commit on PythonAnywhere. Run it in a PythonAnywhere
# Bash console after `git push`, with the site's virtualenv activated:
#
#   source ~/Venv/django612/bin/activate
#   bash ~/edklab/deploy.sh
#
set -euo pipefail

step() { printf '\n==> %s\n' "$*"; }
fail() { printf '\nERROR: %s\n' "$*" >&2; exit 1; }

main() {
    step "Checking the virtualenv"
    if [[ -z "${VIRTUAL_ENV:-}" ]]; then
        fail "No virtualenv is active. Run: source ~/Venv/django612/bin/activate"
    fi
    if [[ "$(command -v python)" != "$VIRTUAL_ENV/bin/python" ]]; then
        fail "'python' is not the one in $VIRTUAL_ENV. Run: source $VIRTUAL_ENV/bin/activate"
    fi
    if ! python -m pip --version >/dev/null 2>&1; then
        fail "pip is missing in $VIRTUAL_ENV (built for a different Python version?). Activate the right virtualenv or rebuild this one."
    fi
    echo "Using $VIRTUAL_ENV ($(python --version))."
    echo "This must be the virtualenv set on the PythonAnywhere Web tab."

    # Run from the repo this script lives in.
    cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

    step "Pulling the latest code"
    if ! git diff --quiet || ! git diff --cached --quiet; then
        git status --short
        fail "This copy has uncommitted changes (listed above). Commit or discard them first."
    fi
    local before after
    before=$(git rev-parse --short HEAD)
    git pull --ff-only
    after=$(git rev-parse --short HEAD)
    if [[ "$before" == "$after" ]]; then
        echo "Already at $after."
    else
        echo "Updated $before -> $after:"
        git log --oneline "$before..$after"
    fi

    step "Installing requirements"
    python -m pip install --disable-pip-version-check -r requirements.txt
    echo "Django $(python -m django --version)"

    step "Running Django's deployment checks"
    python manage.py check --deploy

    step "Applying migrations"
    python manage.py migrate --noinput

    step "Collecting static files"
    python manage.py collectstatic --noinput

    step "Reloading the web app"
    # PythonAnywhere reloads a web app when its WSGI file in /var/www/ is touched.
    local wsgi_files=(/var/www/*_wsgi.py)
    if [[ ${#wsgi_files[@]} -eq 1 && -f "${wsgi_files[0]}" ]]; then
        touch "${wsgi_files[0]}"
        echo "Touched ${wsgi_files[0]}."
    else
        echo "Couldn't find exactly one WSGI file in /var/www/; click Reload on the Web tab instead."
    fi

    step "Done. Check the site and the admin."
}

# Calling main and exit on the same line stops bash from reading the rest of
# this file after `git pull` has replaced it.
main "$@"; exit
