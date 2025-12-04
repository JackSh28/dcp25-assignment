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

- GeeksforGeeks. Python Menu Widget in Tkinter. Retrieved from <https://www.geeksforgeeks.org/python/python-menu-widget-in-tkinter/>  
- GeeksforGeeks. Plot a Pie Chart in Python using Matplotlib. Retrieved from <https://www.geeksforgeeks.org/data-science/plot-a-pie-chart-in-python>
- DataCamp. Python Pie Chart: Build and Style with Pandas and Matplotlib. Retrieved from <https://www.datacamp.com/tutorial/python-pie-chart>  
- Stack Overflow. Tkinter — Create table using database fetched data. Retrieved from <https://stackoverflow.com/questions/77556489/tkinter-create-table-using-database-fetched-data>  
- Duggan, B. Lecture notes for DATA2005: Data Centric Programming TU Dublin, School of Computer Science.  

---

## What I Am Most Proud of in the Assignment

I am most proud of implementing the data visualization charts using Matplotlib. I combined data filtering with visual presentation to clearly highlight tune types and origins.  

### Example

```python
def chart_origins():
    conn = open_connection()
    cur = conn.cursor()
    cur.execute("SELECT O FROM tunes1")
    rows = cur.fetchall()
    conn.close()

    df = pd.DataFrame(rows, columns=["O"])
    freq = df["O"].value_counts().iloc[1:11]
    
    colours = ["#FF0000","#FE5D00","#FFFF00","#0CF200","#2C8503",
                "#00BBFF","#001AFF","#B700FF","#FF00EE","#F96AC0"]

    plt.figure(figsize=(10,6))
    freq.sort_values().plot(kind="barh", color=colours, edgecolor="black")
    plt.title("Top 10 Tune Origins")
    plt.xlabel("Count")
    plt.tight_layout()
    plt.savefig("origins_bar.png")
    plt.show()
```

This code filters out unknown origins and assigns a distinct colour to each bar for clarity.

![Bar Chart Screenshot](origins_bar.png)

What I Learned

I learned how to connect Python to a MySQL database, process files, fix encoding issues, and create a functional GUI. I gained experience with data analysis using pandas and visualization using matplotlib. I also learned how to combine database operations, file handling, and user interfaces into a cohesive program.

Use of AI

I used AI to help format this README and improve grammar and clarity.

Screenshots

![Pie Chart Screenshot](types_pie.png)  
![Bar Chart Screenshot](origins_bar.png)
