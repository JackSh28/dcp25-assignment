# Assignment 1: Tunes Database Analysis and GUI

- [Assignment Brief](assignment.md)

---

## Information

- **Module:** Data Centric Programming DATA2005  
- **Course:** TU850/2 – Data Science & AI  
- **Lecturer:** Bryan Duggan  
- **Name:** Jack Shanahan  
- **Student Number:** C24775089

---

## Description of the Project

This project processes ABC music notation files stored in folders and imports them into a MySQL database. It provides a GUI that allows searching, viewing, and analyzing the tunes, including charts for tune types and origins.

---

## Instructions for Use

1. Place your ABC files inside the `abc_books` folder.  
2. Ensure MySQL is running and a database named `tunes` exists.  
3. Run `assignment_code.py` to set up the table, load files, and launch the GUI.  
4. Use the menu buttons to view all tunes, search by title or book number, and see charts.  

---

## How It Works

### Database Connection and Table Setup

The program connects to the MySQL database each time a function needs to access data. It creates the `tunes1` table if it does not exist, with columns matching the tune attributes.

### Processing ABC Files

The program includes a function to replace encoded characters in ABC files with Unicode equivalents. Files are parsed line by line to extract tunes, storing each tune in a dictionary. All tunes are then inserted into the database.

### User Interface

A Tkinter GUI displays the data with scrollable tables. Users can:

- **View All Tunes:** Shows all records in the database.  
- **Search by Title:** Allows partial matches for the tune title.  
- **Search by Book Number:** Filters tunes by numeric book number.  

### Data Visualization

Charts are created using Matplotlib and Pandas:

- **Pie Chart:** Displays the top 15 tune types by frequency with percentages.  
- **Bar Chart:** Shows the top 10 known origins of tunes. Empty or unknown origins are excluded, and each bar is colored differently.  

### File Discovery

The program scans the `abc_books` folder, identifying numbered subfolders and loading all `.abc` files.

---

## List of Files in the Project

- `abc_books/` – Dataset of ABC files  
- `assignment_code.py` – Main program file  
- `assignment.md` – Assignment brief  
- `piechart.png` – Pie chart image  
- `barchart.png` – Bar chart image  
- `.gitignore` – Git ignore file  
- `LICENSE` – License file  
- `README.md` – Project documentation  

---

## References

- GeeksforGeeks. Python Menu Widget in Tkinter. Retrieved from https://www.geeksforgeeks.org/python/python-menu-widget-in-tkinter/  
- GeeksforGeeks. Plot a Pie Chart in Python using Matplotlib. Retrieved from https://www.geeksforgeeks.org/data-science/plot-a-pie-chart-in-python
