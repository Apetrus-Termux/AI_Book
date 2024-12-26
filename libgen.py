import os
import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel

# Inisialisasi konsol untuk tampilan keren
console = Console()

def banner():
    os.system("clear")
    console.print(
        Panel.fit(
            "[bold green]LIBRARY BOOK  DOWNLOAD LINK UNIVERSAL[/bold green]\n[blue]Powered by Fandy * languange python[/blue]",
            border_style="bright_red",
        )
    )

def search_books(keyword):
    search_url = f"https://libgen.is/search.php?req={keyword}&open=0&res=25&view=simple&phrase=1&column=def"
    try:
        response = requests.get(search_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            rows = soup.select("table.c > tr")[1:]  # Skip header row
            books = []
            for row in rows[:10]:  # Ambil 10 hasil teratas
                cols = row.find_all("td")
                books.append({
                    "title": cols[2].text.strip(),
                    "author": cols[1].text.strip(),
                    "year": cols[4].text.strip(),
                    "format": cols[8].text.strip(),
                    "link": cols[9].find("a")["href"] if cols[9].find("a") else None,
                })
            return books
        else:
            return f"Failed to fetch data. Status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {e}"

def get_direct_download_link(download_link):
    try:
        response = requests.get(download_link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            direct_link = soup.find("a", string="GET")["href"]
            return direct_link
        else:
            console.print(f"[bold red]Failed to fetch direct link. Status code: {response.status_code}[/bold red]")
            return None
    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")
        return None

def main():
    banner()
    while True:
        keyword = Prompt.ask("[bold cyan]Enter keyword to search books or type 'exit' to quit[/bold cyan]")
        if keyword.lower() == "exit":
            console.print("[bold red]Goodbye![/bold red]")
            break
        
        console.print("[bold yellow]Searching for books...[/bold yellow]")
        books = search_books(keyword)
        if isinstance(books, str):
            console.print(f"[bold red]{books}[/bold red]")
            continue
        
        if not books:
            console.print("[bold red]No books found![/bold red]")
            continue

        table = Table(title="Book Recommendations")
        table.add_column("No", style="cyan", justify="center")
        table.add_column("Title", style="green")
        table.add_column("Author", style="blue")
        table.add_column("Year", style="magenta")
        table.add_column("Format", style="yellow")

        for i, book in enumerate(books):
            table.add_row(str(i + 1), book["title"], book["author"], book["year"], book["format"])
        
        console.print(table)

        choice = Prompt.ask("[bold cyan]Enter the number of the book to get download link or 'skip' to search again[/bold cyan]")
        if choice.lower() == "skip":
            continue

        try:
            choice = int(choice) - 1
            if 0 <= choice < len(books):
                selected_book = books[choice]
                if selected_book["link"]:
                    direct_link = get_direct_download_link(selected_book["link"])
                    if direct_link:
                        console.print(f"[bold green]Download link: {direct_link}[/bold green]")
                        console.print(f"[bold yellow]Copy this link and paste it in your browser to download the book.[/bold yellow]")
                    else:
                        console.print("[bold red]Failed to generate direct download link.[/bold red]")
                else:
                    console.print("[bold red]No download link available for this book.[/bold red]")
            else:
                console.print("[bold red]Invalid choice.[/bold red]")
        except ValueError:
            console.print("[bold red]Please enter a valid number.[/bold red]")

if __name__ == "__main__":
    main()
