"""Nox sessions."""

from nox_poetry import Session, session

PYTHON_VERSIONS = "3.8", "3.9"


@session(python=PYTHON_VERSIONS)
def tests(session: Session) -> None:
    session.install(".")
    session.install("pytest")
    session.run("pytest")
