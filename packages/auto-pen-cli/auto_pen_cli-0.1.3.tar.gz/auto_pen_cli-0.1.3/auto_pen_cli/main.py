from typer import Typer
from auto_pen_cli.passive_scan import app as passive_scan_app
from auto_pen_cli.active_scan import app as active_scan_app
from auto_pen_cli.exploit import app as exploit_app


app = Typer()

# Register subcommands from passive_scan_commands.py
app.add_typer(passive_scan_app, name="passive_scan")
app.add_typer(active_scan_app, name="active_scan")
app.add_typer(exploit_app, name="exploit")

if __name__ == "__main__":
    app()