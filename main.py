# Library import
import sys
from typing import List, Dict
# Modules import
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
        self.commands: Dict[str, callable] = {
            "help": self.handle_help,
            "list": self.handle_list,
            "update": self.handle_update,
            "scrape": self.handle_scrape,
            "quit": self.handle_quit,
        }
        self.statuscolor: Dict[str, str] = {
            "offer": "green",
            "rejected": "red",
            "interview": "magenta",
            "applied": "cyan",
            "read": "yellow",
            "fetched": "white"
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
                self.handle_quit()
            except Exception as e:
                self.console.print(f"An unexpected error occured: {e}", style="red")

    def _process_command(self, user_input: str):
        parts = user_input.split()
        command_name = parts[0].lower()
        args = parts[1:]

        if command_name in self.commands:
            self.commands[command_name](args)
        else:
            self.console.print(f"Unknown command: '{command_name}'. Type [white]'help'[/white] for options.", style="yellow")

    
    def handle_quit(self, args: List[str] = None):
        # Exits the program
        self.console.print("Exiting program..", style="red bold u")
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
            internships, error = db_handler.get_all_internships()

            if error is not None:
                self.console.print(f"Error: {error}")
                return

            if not internships:
                table = self._build_table([], title="All Internships")
                self.console.print(table)
                self.console.print("No internship was found. Try [white]'scrape'[/white] first!", style="yellow")
                return
            
            table = self._build_table(internships, title="All Internships")
            self.console.print(table)

        else:
            internship, error = db_handler.get_internship_by_id(target)
            # print(internship)
            # print(error)
            if error is not None:
                self.console.print(f"Error: {error}")
                return 
            
            if not internship or internship == [None]:
                self.console.print(f"Internship with ID {target} not found.", style="red")
                return
            
            table = self._build_table(internship, title=f"Details for ID {target}")
        
            self.console.print(table)

    
    def _build_table(self, data: List[tuple], title: str) -> Table:
        table = Table(title=title, box=box.ROUNDED, show_header=True, show_lines=True, header_style="bold cyan")

        table.add_column("ID", justify="center", style="dim white")
        table.add_column("Company", style="bold white")
        table.add_column("Position")
        table.add_column("Location", justify="center")
        table.add_column("Link", justify="center", style="blue u")
        table.add_column("Date", justify="center")
        table.add_column("Status", justify="right")
        table.add_column("Last update", justify="center")

        # print(data)
        for row in data:
            id, company_name, position, location, link, date_posted, status, last_update = row
            # print(id)
            status_style = self.statuscolor[status]

            table.add_row(
                str(id),
                company_name,
                position,
                location,
                f"[link={link}]LINK[/link]",
                date_posted,
                f"[{status_style}]{status}[/{status_style}]",
                last_update
            )
            
        return table
    
    def _get_status_color(self, status):
        status = status.lower()

        if status in self.statuscolor:
            return self.statuscolor[status]
        

    def handle_update(self, args: List[str]):
        if len(args) != 2:
            self.console.print("Usage: [white]'update <id> <offer / rejected / interview / applied / fetched>'[/white]", style="red")
            return

        internship_id, new_status = args[0], args[1]

        if args[1].lower() not in self.statuscolor:
            self.console.print("Usage: [white]'update <id> <offer / rejected / interview / applied / fetched>'[/white]", style="red")
            return

        
        
        maxID = db_handler.update_check()
        # print(maxID)
        if int(internship_id) <= int(maxID):
            db_handler.update_status(internship_id, new_status)
            self.console.print(f"Updating ID {internship_id} to status '{new_status}'..", style="bold green")
        else:
            self.console.print(f"Error: Internship with ID {internship_id} not found.", style="bold red")

        return
    
    def handle_scrape(self, args: List[str]):
        self.console.print("Starting scraper..", style="cyan")
        
        found_jobs, new_jobs = scraper.get_jobs_raw()

        if found_jobs > 0:
            self.console.print(f"Found {found_jobs} jobs -- {new_jobs} were added to the database ", style="green")
        else:
            self.console.print(f"No jobs were found -- try again later..", style="green")


        # self.console.print(f"Successfully fetched {success} internships.", style="bold green")
    

if __name__ == "__main__":
    app = InternshipCLI()
    app.start()