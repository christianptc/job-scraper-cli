# Library import
import sys
from datetime import datetime

# Modules import
from modules import cli
from modules import db_handler
from modules import scraper

# CLI (command line interface // terminal) tables + colors
from rich.console import Console
from rich.table import Table

console = Console()
def main():
    # console.print("tactu")
    initiated = False
    while True:
        # welcome message
        if not initiated:
            console.print("")
            console.print("Welcome to internship tracker, type [green]help[/green] for commands ([red]quit[/red] to stop)", style="bold u white")
            initiated = True

        command = input("> ").strip()
        if command.lower() in ["exit", "quit", "q", "stop"]:
            console.print("Exiting program...", style="bold red")
            sys.exit()
        elif command.lower() == "list .":
            pass
        elif command.lower().startswith("list "):
            try:
                _, internship_id = command.split()
            except ValueError:
                console.print("[red]Try list <id>[/red]")
        elif command.lower().startswith("update "):
            try:
                _. internship_id, internship_status = command.split()
            except ValueError:
                console.print("[red]Try update <id> <new_status>[/red]")
        elif command.lower() == "scrape":
            pass
        elif command.lower() == "help":
            console.print("Available commands:", style="bold u bright_yellow")
            console.print("[white]'list .'[/white] -- lists all interships stored", style="yellow")
            console.print("[white]'list <id>'[/white] -- gets information about specific internship", style="yellow")
            console.print("[white]'update <id> <new_status>'[/white] -- updates current status of specific internship", style="yellow")
            console.print("[white]'scrape'[/white] -- gets newly posted internships", style="yellow")
        else:
            console.print("Unknown command.", style="yellow")
if __name__ == "__main__":
    main()


