import nox

nox.options.sessions = ["test", "lint"]


@nox.session
def test(session: nox.Session):
    session.install("-e", ".[testing]")
    session.run("pytest")


@nox.session
def lint(session: nox.Session):
    session.install("-e", ".[dev]")
    session.run("ruff", "check", "kenallclient")
    session.run("ruff", "format", "--check", "kenallclient")
    session.run("mypy", "kenallclient")


@nox.session
def pack(session: nox.Session):
    session.install("build")
    session.run("python", "-m", "build")
