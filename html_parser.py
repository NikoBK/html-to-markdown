import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from bs4 import BeautifulSoup

def convert_to_markdown():
    html_content = html_text.get("1.0", "end").strip()
    if not html_content:
        messagebox.showerror("Error", "Please paste HTML content.")
        return
    
    # Preprocess HTML content to replace "|" with "/"
    html_content = html_content.replace("|", "/")
    
    markdown_content = html_to_markdown(html_content)
    save_file(markdown_content)

def html_to_markdown(html):
    soup = BeautifulSoup(html, 'html.parser')
    markdown = ''
    tables = soup.find_all('table')
    for table in tables:
        rows = table.find_all('tr')
        header_row = rows[0]
        headers = [header.get_text().strip() for header in header_row.find_all(['th', 'td'])]
        markdown += '| ' + ' | '.join(headers) + ' |\n'
        markdown += '| ' + ' | '.join(['---'] * len(headers)) + ' |\n'
        for row in rows[1:]:
            cells = row.find_all(['th', 'td'])
            row_data = [cell.get_text().strip() for cell in cells]
            markdown += '| ' + ' | '.join(row_data) + ' |\n'
        markdown += '\n'
    return markdown

def save_file(content):
    filename = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown files", "*.md")], initialfile="table.md")
    if filename:
        with open(filename, 'w') as file:
            file.write(content)
        messagebox.showinfo("Success", f"Markdown content saved to {filename}")

# Create main window
root = tk.Tk()
root.title("HTML to Markdown Converter")

# Create text area for HTML input
html_text = tk.Text(root, height=10, width=50)
html_text.pack(pady=10)

# Create button to convert HTML to Markdown and save to file
convert_button = tk.Button(root, text="Convert to Markdown and Save", command=convert_to_markdown)
convert_button.pack()

# Run the application
root.mainloop()