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
            "move": self.handle_move,
            "update": self.handle_update,
            "scrape": self.handle_scrape,
            "settings": self.handle_settings,
            "clear": self.handle_clear,
            "delete": self.handle_delete,
            "quit": self.handle_quit
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
            ("[white]'list .'[/white]", "[yellow]lists all interships scraped[yellow]"),
            ("[white]'move <id>'[/white]", "[yellow]moves and saves intership with <id> in main database[yellow]"),
            ("[white]'clear'[/white]", "[yellow]clears the whole temporary database[yellow]"),
            ("[white]'list main'[/white]", "[yellow]lists all interships saved in main database[yellow]"),
            ("[white]'list <id>'[/white]", "[yellow]gets information about specific internship from main database[yellow]"),
            ("[white]'update <id> <new_status>'[/white]", "[yellow]updates current status of specific internship[yellow]"),
            ("[white]'scrape'[/white]", "[yellow]gets newly posted internships[yellow]"),
            ("[white]'settings .'[/white]", "[yellow]shows the current search filters when scraping[yellow]"),
            ("[white]'settings <search/region/radius/amount> <new_value>'[/white]", "[yellow]changes specific setting[yellow]"),
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
            internships, error = db_handler.get_all_scrapes()
            # print(internships)
            if error is not None:
                self.console.print(f"Error: {error}")
                return

            if not internships or internships == [None]:
                table = self._build_table([], title="All Scraped Jobs")
                self.console.print(table)
                self.console.print("No job was found. Try [white]'scrape'[/white] first!", style="yellow")
                return
            
            table = self._build_table(internships, title="All Scraped Jobs")
            self.console.print(table)

        elif target == "main":
            # Fetch data
            internships, error = db_handler.get_all_internships()

            if error is not None:
                self.console.print(f"Error: {error}")
                return

            if not internships:
                table = self._build_table([], title="All Saved Jobs")
                self.console.print(table)
                self.console.print("No job was found. Try [white]'move <id>'[/white] first!", style="yellow")
                return
            
            table = self._build_table(internships, title="All Saved Jobs")
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
        # print(data)
        if not data:
            return table
        elif len(data[0]) == 8:
            table.add_column("Status", justify="right")
            table.add_column("Last update", justify="center")
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
        elif len(data[0]) == 6:
            for row in data:
                # print("b")
                id, company_name, position, location, link, date_posted = row
                # print("c")
                table.add_row(
                    str(id),
                    company_name,
                    position,
                    location,
                    f"[link={link}]LINK[/link]",
                    date_posted
                )
            return table
        else:
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

        search, ort, umkreis, search_amount = db_handler.get_all_settings()[0]

        found_jobs, new_jobs = scraper.get_jobs_raw(search, ort, umkreis, search_amount)

        if found_jobs > 0:
            self.console.print(f"Found {found_jobs} jobs -- {new_jobs} were added to the database ", style="green")
        else:
            self.console.print(f"No jobs were found -- try again later or try to update search settings by using [white]'settings .'[/white]..", style="red")


        # self.console.print(f"Successfully fetched {success} internships.", style="bold green")
    
    def handle_settings(self, args: List[str]):
        valid_settings: Dict[str, str] = {
            'search':'search',
            'region':'ort',
            'radius':'umkreis',
            'amount':'search_amount'
        }
        if not args:
            self.console.print(f"Usage: [white]'settings .' [red]or[/red] 'settings  <{'/'.join(valid_settings)}> <new_value>'[/white]", style="red")
            return

        if len(args) == 1 and args[0] == '.':
            self.console.print("Current SEARCH settings:", style="bold u bright_yellow")
            search, ort, umkreis, search_amount = db_handler.get_all_settings()[0]
            self.console.print(f"[yellow]{'Search:':<7}[/yellow] {search}")
            self.console.print(f"[yellow]{'Region:':<7}[/yellow] {ort}")
            self.console.print(f"[yellow]{'Radius:':<7}[/yellow] {umkreis} [yellow](in km)[/yellow]")
            self.console.print(f"[yellow]{'Amount:':<7}[/yellow] {search_amount} [yellow](Maximum amount of how many jobs can get extracter - the higher the amount, the older the posts will get scraped)[/yellow]")
            self.console.print()
            self.console.print("Use [white]'settings  <search/region/radius/amount> <new_value>'[/white] to update each setting", style="bold red")
        
        else: 
            setting, new_setting = args[0], " ".join(args[1:])
            if setting not in valid_settings:
                self.console.print(f"Usage: [white]'settings .' [red]or[/red] 'settings  <{'/'.join(valid_settings)}> <new_value>'[/white]", style="red")
                return
            
            valid_update = db_handler.update_setting(valid_settings[setting.lower()], new_setting)
            if valid_update:
                self.console.print(f"Successfully updated [white]{setting}[/white] to [white]{new_setting}[/white]",style="green b")
            else:
                self.console.print(f"Something went wrong, try again", style="red b")
            return
    
    def handle_move(self, args: List[str]) -> None:
        if not args or len(args) > 1:
            self.console.print(f"Usage: [white]'move <id>'[/white]", style="red")
            return

        target = args[0]

        check, new_id = db_handler.move_internship(target)

        if check:
            self.console.print(f"Successfully moved internship with ID [white]{target}[/white] to main database, it's new ID is [white]{new_id}[/white]", style="green b")
        else:
            self.console.print(f"Internship with ID [white]{target}[/white] was not able to get moved (either the id is wrond or it already is stored in main database).", style="red b")
        return
    
    
    def handle_clear(self, args: List[str]) -> None:
        try:
            if db_handler.clear_temp_database():
                self.console.print("Cleared the temporary table", style="green")
            else:
                self.console.print("Something went wrong, try again later", style="red b")
            return
        except Exception as e:
            print(f"Error: {e}")
            return
        
    def handle_delete(self, args:List[str]) -> None:
        try:
            if not args or len(args) > 1:
                self.console.print(f"Usage: [white]'delete <id>'[/white]", style="red")

            targetID = args[0]

            if db_handler.delete_internship(targetID):
                self.console.print(f"Deleted internship with ID {targetID} from main database.", style="green")
            else:
                self.console.print(f"Something went wrong with deleting internship with id {targetID}, try again later", style="red b")
            return
        except Exception as e:
            print(f"Error: {e}")
            return
if __name__ == "__main__":
    app = InternshipCLI()
    app.start()