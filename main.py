# Library import
import sys
from datetime import datetime

# Modules import
from modules import cli
from modules import db_handler
from modules import scraper

# CLI (command line interface // terminal) tables + colors
from rich import box
from rich.console import Console
from rich.table import Table

class InternshipCLI:
    def __init__(self):
        self.console = Console()
        # Map command strings to methods
        self.commands: Dict[str, Callable] = {
            "help": self.handle_help,
            "list": self.handle_list,
            "update": self.handle_update,
            "scrape": self.handle_scrape,
            "quit": self.handle_quit,
        }
    
    def start(self):
        self.console.print()
        # Ensures the table is created
        db_handler.table_create()

        self.console.print(
                "Welcome to Internship Tracker, type [white]'help'[/white] for commands ([white]'quit'[/white] to stop)",
                style="bold yellow"
            )
        
        while True:
            try:
                user_input = input(">>> ").strip()
                if not user_input:
                    continue
                
                self._process_command(user_input)
            except KeyboardInterrupt:
                self.console.print("Interrupted", style="red")
                self.handle_quit
            except Exception as e:
                self.console.print(f"An unexpected error occured: {e}", style="red")

    def _process_command(self, user_input: str):
        parts = user_input.split()
        command_name = parts[0]
        args = parts[1:]

        if command_name in self.commands:
            self.commands[command_name](args)
        else:
            self.console.print(f"Unknown command: '{command_name}'. Type [white]'help'[/white] for options.", style="yellow")

    
    def handle_quit(self, args: List[str] = None):
        # Exits the program
        self.console.print("Exiting program...", style="red bold u")
        sys.exit()

    
    def handle_help(self, args: List[str]):
        self.console.print("Available commands:", style="bold u bright_yellow")

        help_text = [
            ("[white]'list .'[/white]", "[yellow]lists all interships stored[yellow]"),
            ("[white]'list <id>'[/white]", "[yellow]gets information about specific internship[yellow]"),
            ("[white]'update <id> <new_status>'[/white]", "[yellow]updates current status of specific internship[yellow]"),
            ("[white]'scrape'[/white]", "[yellow]gets newly posted internships[yellow]"),
            ("[white]'quit'[/white]", "[yellow]Exits tbe program[yellow]"),
        ]

        for command, desc in help_text:
            self.console.print(f"{command} -- {desc}", style="yellow")
    
    
    def handle_list(self, args: List[str]):
        if not args:
            self.console.print("Usage: [white]'list .'[/white] (for all) OR [white]'list <id>'[/white]", style="red")
            return
        
        target = args[0]

        if target == ".":
            # Fetch data
            internships = db_handler.get_all_internships()

            if not internships:
                self.console.print("No internship was found. Try [white]'scrape'[/white] first!", style="yellow")
                return
            
            table = self._build_table(internships, title="All Internships")

        else:
            internship = db_handler.get_internship_by_id(target)

            if not internship:
                self.console.print(f"Internship with ID {target} not found.", style="red")
                return
            
            table = self._build_table(internship, title=f"Details for ID {target}")
        
            self.console.print(table)

    
    def _build_table(self, data: List[tuple], title: str) -> Table:
        table = Table(title=title, box=box.ROUNDED, show_header=True, header_style="bold cyan")

        table.add_column("ID", justify="center", style="dim white")
        table.add_column("Company", style="bold white")
        table.add_column("Position")
        table.add_column("Location")
        table.add_column("Link", style="blue u")
        table.add_column("Tech Stack")
        table.add_column("Date", justify="center")
        table.add_column("Status", justify="right")

        for row in data:
            id, company_name, position, location, link, tech_stack, date_posted, status = row

            status_style = self._get_status_color(status)

            table.add_row(
                str(id),
                company_name,
                position,
                location,
                link,
                tech_stack,
                date_posted,
                f"[{status_style}]{status}[/{status_style}]"
            )
            
        return table
    
    def _get_status_color(self, status):
        status = status.lower()

        if status == "offer":
            return "green"
        elif status == "rejected":
            return "red"
        elif status == "interview":
            return "magenta"
        elif status == "applied":
            return "cyan"
        else:
            return "yellow"
        

    def handle_update(self, args: List[str]):
        if len(args) != 2:
            self.console.print("Usage: [white]'update <id> <new_status>'[/white]", style="red")
            return

        internship_id, new_status = args[0], args[1]

        success = db_handler.update_status(internship_id, new_status)
        
        if success:
            self.console.print(f"Updating ID {internship_id} to status '{new_status}'...", style="bold green")
            pass
        else:
            self.console.print(f"Error: Internship with ID {internship_id} not found.", style="bold red")
            pass
    
    def handle_scrape(self):
        self.console.print("Starting scraper...", style="cyan")
        success = db_handler.scrape()
        self.console.print(f"Successfully fetched {success} internships.", style="bold green")
        pass
    

if __name__ == "__main__":
    app = InternshipCLI()
    app.start()
        
# console = Console()
# def main():
#     # welcome message
#     console.print()
#     db_handler.table_create()
#     console.print(
#             "Welcome to internship tracker, type [green]help[/green] for commands ([red]quit[/red] to stop)",
#             style="bold u white",
#             highlight=False
#         )
    
#     while True:
#         command = input("> ").strip()
#         if command.lower() in ["exit", "quit", "q", "stop"]:
#             console.print("Exiting program...", style="bold red")
#             sys.exit()
#         elif command.lower() == "list .":
#             pass
#         elif command.lower().startswith("list "):
#             try:
#                 _, internship_id = command.split()
#             except ValueError:
#                 console.print("[red]Try list <id>[/red]")
#         elif command.lower().startswith("update "):
#             try:
#                 _. internship_id, internship_status = command.split()
#             except ValueError:
#                 console.print("[red]Try update <id> <new_status>[/red]")
#         elif command.lower() == "scrape":
#             pass
#         elif command.lower() == "help":
#             console.print("Available commands:", style="bold u bright_yellow")
#             console.print("[white]'list .'[/white] -- lists all interships stored", style="yellow")
#             console.print("[white]'list <id>'[/white] -- gets information about specific internship", style="yellow")
#             console.print("[white]'update <id> <new_status>'[/white] -- updates current status of specific internship", style="yellow")
#             console.print("[white]'scrape'[/white] -- gets newly posted internships", style="yellow")
#         else:
#             console.print("Unknown command.", style="yellow")
# if __name__ == "__main__":
#     main()