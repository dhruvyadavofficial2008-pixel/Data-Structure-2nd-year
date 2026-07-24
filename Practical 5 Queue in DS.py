import os
import tkinter as tk
from tkinter import simpledialog, messagebox

# ---------------- Queue Class ----------------
class Queue:
    def __init__(self, max_size):
        self.queue = []
        self.max_size = max_size

    def is_empty(self):
        return len(self.queue) == 0

    def is_full(self):
        return len(self.queue) == self.max_size

    def enqueue(self, item):
        if self.is_full():
            return "Queue is Full!"
        self.queue.append(item)
        return f'"{item}" added successfully.'

    def dequeue(self):
        if self.is_empty():
            return "Queue is Empty!"
        return f'"{self.queue.pop(0)}" removed successfully.'

    def peek(self):
        if self.is_empty():
            return "Queue is Empty!"
        return f'Front Book: {self.queue[0]}'

    def traverse(self):
        if self.is_empty():
            return "Queue is Empty!"
        return "Books in Queue: " + " -> ".join(self.queue)

# ---------------- CLI ----------------
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def command_line():
    size = int(input("Enter Maximum Queue Size: "))
    q = Queue(size)

    while True:
        clear()
        print("===== LIBRARY BOOK QUEUE =====")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. View First Book")
        print("4. Display Queue")
        print("5. Check Empty")
        print("6. Check Full")
        print("7. Exit")

        choice = input("Enter Choice: ")

        if choice == "1":
            book = input("Enter Book Name: ")
            print(q.enqueue(book))

        elif choice == "2":
            print(q.dequeue())

        elif choice == "3":
            print(q.peek())

        elif choice == "4":
            print(q.traverse())

        elif choice == "5":
            print("Queue Empty" if q.is_empty() else "Queue Not Empty")

        elif choice == "6":
            print("Queue Full" if q.is_full() else "Queue Not Full")

        elif choice == "7":
            print("Thank You!")
            break

        else:
            print("Invalid Choice!")

        input("\nPress Enter to Continue...")

# ---------------- GUI ----------------
def gui():
    import tkinter as tk
    from tkinter import messagebox, simpledialog

    root = tk.Tk()
    root.title("📚 Library Queue Management")
    root.geometry("650x500")
    root.configure(bg="#EAF6FF")

    size = simpledialog.askinteger("Queue Size", "Enter Maximum Queue Size:")
    if size is None:
        return

    q = Queue(size)

    # ---------- Title ----------
    title = tk.Label(
        root,
        text="📚 LIBRARY QUEUE MANAGEMENT",
        font=("Arial", 20, "bold"),
        bg="#1976D2",
        fg="white",
        pady=10
    )
    title.pack(fill="x")

    # ---------- Queue Display ----------
    display = tk.Text(
        root,
        width=50,
        height=10,
        font=("Consolas", 13),
        bg="white",
        fg="#1565C0"
    )
    display.pack(pady=15)

    status = tk.Label(
        root,
        text="Queue Size: 0",
        font=("Arial", 12, "bold"),
        bg="#EAF6FF",
        fg="green"
    )
    status.pack()

    def update_display():
        display.delete(1.0, tk.END)

        if q.is_empty():
            display.insert(tk.END, "Queue is Empty")
        else:
            for i, item in enumerate(q.queue, start=1):
                display.insert(tk.END, f"{i}. {item}\n")

        status.config(text=f"Queue Size: {len(q.queue)}/{q.max_size}")

    # ---------- Button Hover ----------
    def enter(e):
        e.widget["background"] = "#90CAF9"

    def leave(color):
        return lambda e: e.widget.config(background=color)

    # ---------- Functions ----------
    def add_book():
        book = simpledialog.askstring("Add Book", "Enter Book Name:")
        if book:
            messagebox.showinfo("Result", q.enqueue(book))
            update_display()

    def issue_book():
        messagebox.showinfo("Result", q.dequeue())
        update_display()

    def first_book():
        messagebox.showinfo("Front Book", q.peek())

    def show_books():
        messagebox.showinfo("Books", q.traverse())

    def clear_queue():
        q.queue.clear()
        update_display()
        messagebox.showinfo("Done", "Queue Cleared")

    # ---------- Buttons ----------
    frame = tk.Frame(root, bg="#EAF6FF")
    frame.pack(pady=10)

    buttons = [
        ("➕ Add Book", add_book, "#4CAF50"),
        ("📖 Issue Book", issue_book, "#FF9800"),
        ("👀 View First", first_book, "#2196F3"),
        ("📋 Show Queue", show_books, "#9C27B0"),
        ("🗑 Clear Queue", clear_queue, "#F44336"),
        ("❌ Exit", root.destroy, "#607D8B")
    ]

    for text, command, color in buttons:
        b = tk.Button(
            frame,
            text=text,
            width=18,
            font=("Arial", 11, "bold"),
            bg=color,
            fg="white",
            relief="raised",
            command=command
        )
        b.pack(pady=5)

        b.bind("<Enter>", enter)
        b.bind("<Leave>", leave(color))

    update_display()

    root.mainloop()
# ---------------- Main ----------------
if __name__ == "__main__":
    print("====== QUEUE APPLICATION ======")
    print("1. Command Line Version")
    print("2. GUI Version")

    option = input("Choose Mode (1/2): ")

    if option == "1":
        command_line()
    elif option == "2":
        gui()
    else:
        print("Invalid Option")
