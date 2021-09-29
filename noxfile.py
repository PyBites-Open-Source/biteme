from nox_poetry import session
from nox_poetry import Session


@session(python=["3.8", "3.9"])
def tests(session: Session) -> None:
    session.install(".", "pytest")
    session.run("pytest", *session.posargs)
