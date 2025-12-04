# Code for Data Centric Programming Assignment 2025

# os is a module that lets us access the file system

# Author: Jack Shanahan C24775089

import os
import mysql.connector
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

# connect to sql server
def open_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ladin?2567",
        database="tunes"
    )

# build table from scratch
def setup_table():
    db = open_connection()
    cur = db.cursor()

    cur.execute("DROP TABLE IF EXISTS tunes1")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tunes1(
            book_number INT,
            X TEXT,
            T TEXT,
            R TEXT,
            O TEXT,
            M TEXT,
            L TEXT,
            Q TEXT,
            K TEXT
        )
    """)

    db.commit()
    cur.close()
    db.close()

# insert a row
def add_record(book_number, tune_data):
    db = open_connection()
    cur = db.cursor()

    sql = """
        INSERT INTO tunes1(book_number, X, T, R, O, M, L, Q, K)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    row = (
        book_number,
        tune_data.get("X",""),
        tune_data.get("T",""),
        tune_data.get("R",""),
        tune_data.get("O",""),
        tune_data.get("M",""),
        tune_data.get("L",""),
        tune_data.get("Q",""),
        tune_data.get("K","")
    )

    cur.execute(sql, row)
    db.commit()

    cur.close()
    db.close()

# encoding replacement table
encoded_map = {
    "\\`A":"À","\\`a":"à","\\`E":"È","\\`e":"è",
    "\\`I":"Ì","\\`i":"ì","\\`O":"Ò","\\`o":"ò",
    "\\`U":"Ù","\\`u":"ù",

    "\\'A":"Á","\\'a":"á","\\'E":"É","\\'e":"é",
    "\\'I":"Í","\\'i":"í","\\'O":"Ó","\\'o":"ó",
    "\\'U":"Ú","\\'u":"ú","\\'Y":"Ý","\\'y":"ý",

    "\\^A":"Â","\\^a":"â","\\^E":"Ê","\\^e":"ê",
    "\\^I":"Î","\\^i":"î","\\^O":"Ô","\\^o":"ô",
    "\\^U":"Û","\\^u":"û",

    "\\~A":"Ã","\\~a":"ã","\\~N":"Ñ","\\~n":"ñ",
    "\\~O":"Õ","\\~o":"õ",

    '\\"A':"Ä",'\\"a':"ä",'\\"E':"Ë",'\\"e':"ë",
    '\\"I':"Ï",'\\"i':"ï",'\\"O':"Ö",'\\"o':"ö",
    '\\"U':"Ü",'\\"u':"ü",'\\"Y':"Ÿ",'\\"y':"ÿ",

    "\\cC":"Ç","\\cc":"ç",
    "\\AA":"Å","\\aa":"å",
    "\\/O":"Ø","\\/o":"ø",

    "\\uA":"Ă","\\ua":"ă","\\uE":"Ĕ","\\ue":"ĕ",

    "\\vS":"Š","\\vs":"š","\\vZ":"Ž","\\vz":"ž",
    "\\vC":"Č","\\vc":"č",

    "\\HO":"Ő","\\Ho":"ő","\\HU":"Ű","\\Hu":"ű",

    "\\ss":"ß","\\AE":"Æ","\\ae":"æ",
    "\\oe":"œ","\\OE":"Œ"
}

# convert encoded abc text
def fix_text(text):
    if not text:
        return text
    out = text

    for k in sorted(encoded_map.keys(), key=len, reverse=True):
        out = out.replace(k, encoded_map[k])

    return out

# read file content
def load_file(path, book_number):
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]

    tune = {}
    all_tunes = []

    for line in lines:
        if line.startswith("X:"):
            if tune:
                all_tunes.append(tune)
                tune = {}
        if ":" in line:
            tag, value = line.split(":", 1)
            tune[tag] = fix_text(value.strip())

    if tune:
        all_tunes.append(tune)

    for t in all_tunes:
        add_record(book_number, t)

def build_table_ui():
    root = tk.Tk()
    root.geometry("420x340")
    root.title("Tunes Viewer")

    frame_top = tk.Frame(root)
    frame_top.pack(pady=5)

    frame_table = tk.Frame(root)
    frame_table.pack(fill="both", expand=True)

    cols = ["book_number","X","T","R","O","M","L","Q","K"]
    tree = ttk.Treeview(frame_table, columns=cols, show="headings")

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=90)

    scroll_y = ttk.Scrollbar(frame_table, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scroll_y.set)

    tree.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")

    frame_table.columnconfigure(0, weight=1)
    frame_table.rowconfigure(0, weight=1)

    return root, frame_top, tree

# search title
def find_title():
    conn = open_connection()
    root, top, tree = build_table_ui()

    tk.Label(top, text="Search title").pack(side="left")
    entry = tk.Entry(top, width=25)
    entry.pack(side="left", padx=4)

    def run():
        tree.delete(*tree.get_children())
        q = entry.get().strip()
        if not q:
            messagebox.showwarning("Input", "Need a title")
            return

        try:
            df = pd.read_sql("SELECT * FROM tunes1 WHERE T LIKE %s", conn, params=[f"%{q}%"])
            if df.empty:
                messagebox.showinfo("Info", "Nothing found")
                return

            for _, r in df.iterrows():
                tree.insert("", tk.END, values=list(r))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(top, text="Go", command=run).pack(side="left", padx=4)
    entry.bind("<Return>", lambda e: run())

    tk.Button(root, text="Close", command=lambda:[conn.close(), root.destroy()]).pack(pady=10)

    root.mainloop()

# show all entries
def list_all():
    conn = open_connection()
    root, top, tree = build_table_ui()

    top.pack_forget()

    df = pd.read_sql("SELECT * FROM tunes1", conn)
    for _, r in df.iterrows():
        tree.insert("", tk.END, values=list(r))

    tk.Button(root, text="Close", command=lambda:[conn.close(), root.destroy()]).pack(pady=10)
    root.mainloop()

# search by book number
def find_book():
    conn = open_connection()
    root, top, tree = build_table_ui()

    tk.Label(top, text="Book number").pack(side="left")
    entry = tk.Entry(top, width=25)
    entry.pack(side="left", padx=4)

    def run():
        tree.delete(*tree.get_children())
        q = entry.get().strip()
        if not q:
            messagebox.showwarning("Input", "Need a number")
            return

        try:
            df = pd.read_sql("SELECT * FROM tunes1 WHERE book_number=%s", conn, params=[q])
            if df.empty:
                messagebox.showinfo("Info", "Nothing found")
                return

            for _, r in df.iterrows():
                tree.insert("", tk.END, values=list(r))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(top, text="Search", command=run).pack(side="left", padx=4)
    entry.bind("<Return>", lambda e: run())

    tk.Button(root, text="Close", command=lambda:[conn.close(), root.destroy()]).pack(pady=10)

    root.mainloop()

# pie chart of tune types
def chart_types():
    conn = open_connection()
    df = pd.read_sql("SELECT R FROM tunes1", conn)
    conn.close()

    freq = df["R"].value_counts().head(15)

    plt.figure(figsize=(9,6))
    plt.pie(freq.values, labels=freq.index, autopct="%1.1f%%")
    plt.title("Top 15 tune types")
    plt.tight_layout()
    plt.savefig("types_pie.png")
    plt.show()

# bar chart of origins
def chart_origins():
    conn = open_connection()
    cur = conn.cursor()
    cur.execute("SELECT O FROM tunes1")
    rows = cur.fetchall()
    conn.close()

    df = pd.DataFrame(rows, columns=["O"])
    freq = df["O"].value_counts().iloc[1:11]
    
    colours = ["#00BBFF","#001AFF","#B700FF","#FF00EE","#F96AC0"
               "#FF0000","#FE5D00","#FFFF00","#0CF200","#2C8503",]

    plt.figure(figsize=(10,6))
    freq.sort_values().plot(kind="barh", color=colours, edgecolor="black")
    plt.title("Top 10 Tune Origins")
    plt.xlabel("Count")
    plt.tight_layout()
    plt.savefig("origins_bar.png")
    plt.show()

# main menu
def main_menu():
    win = tk.Tk()
    win.title("Tunes Menu")
    win.geometry("450x480")

    tk.Label(win, text="Tunes system").pack(pady=20)

    def add_btn(text, cmd):
        tk.Button(
            win,
            text=text,
            width=28,
            height=2,
            command=cmd,
            bg="#aef2ff"
        ).pack(pady=6)

    add_btn("Show all tunes", list_all)
    add_btn("Search by title", find_title)
    add_btn("Search by book number", find_book)
    add_btn("Chart origins", chart_origins)
    add_btn("Chart tune types", chart_types)
    add_btn("Exit", win.destroy)

    win.mainloop()

# run setup
setup_table()

base_dir = "abc_books"

for folder in os.listdir(base_dir):
    p = os.path.join(base_dir, folder)
    if os.path.isdir(p) and folder.isdigit():
        num = int(folder)
        for f in os.listdir(p):
            if f.endswith(".abc"):
                load_file(os.path.join(p, f), num)

main_menu()
