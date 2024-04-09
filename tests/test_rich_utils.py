import typer
import typer.completion
from typer.testing import CliRunner

runner = CliRunner()


def test_rich_utils_click_rewrapp():
    app = typer.Typer(rich_markup_mode="markdown")

    @app.command()
    def main():
        """
        \b
        Some text

        Some unwrapped text
        """
        print("Hello World")

    @app.command()
    def secondary():
        """
        \b
        Secondary text

        Some unwrapped text
        """
        print("Hello Secondary World")

    result = runner.invoke(app, ["--help"])
    assert "Some text" in result.stdout
    assert "Secondary text" in result.stdout
    assert "\b" not in result.stdout
    result = runner.invoke(app, ["main"])
    assert "Hello World" in result.stdout
    result = runner.invoke(app, ["secondary"])
    assert "Hello Secondary World" in result.stdout


def test_rich_utils_no_error_no_commands():
    app = typer.Typer(rich_markup_mode="markdown")

    @app.callback(no_args_is_help=True)
    def main():
        """Some main callback"""

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Some main callback" in result.stdout
