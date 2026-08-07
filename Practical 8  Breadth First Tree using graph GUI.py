import tkinter as tk
from tkinter import messagebox
import heapq

class Node:
    def __init__(self, k):
        self.key = k
        self.left = self.right = None
        self.h = 1

class AVL:
    def ht(self, n): return n.h if n else 0
    def bal(self, n): return self.ht(n.left)-self.ht(n.right) if n else 0

    def rr(self, z):
        y = z.left
        z.left = y.right
        y.right = z
        z.h = 1 + max(self.ht(z.left), self.ht(z.right))
        y.h = 1 + max(self.ht(y.left), self.ht(y.right))
        return y

    def lr(self, z):
        y = z.right
        z.right = y.left
        y.left = z
        z.h = 1 + max(self.ht(z.left), self.ht(z.right))
        y.h = 1 + max(self.ht(y.left), self.ht(y.right))
        return y

    def insert(self, r, k):
        if not r: return Node(k)
        if k < r.key: r.left = self.insert(r.left, k)
        else: r.right = self.insert(r.right, k)
        r.h = 1 + max(self.ht(r.left), self.ht(r.right))
        b = self.bal(r)
        if b > 1 and k < r.left.key: return self.rr(r)
        if b < -1 and k > r.right.key: return self.lr(r)
        if b > 1 and k > r.left.key:
            r.left = self.lr(r.left)
            return self.rr(r)
        if b < -1 and k < r.right.key:
            r.right = self.rr(r.right)
            return self.lr(r)
        return r

    def preorder(self, r):
        return [] if not r else [r.key]+self.preorder(r.left)+self.preorder(r.right)

# ---------- GUI ----------
avl = AVL()
root_node = None
tasks = []

def add_avl():
    global root_node
    try:
        v = int(avl_entry.get())
        root_node = avl.insert(root_node, v)
        out.config(text="AVL: " + " ".join(map(str, avl.preorder(root_node))))
        avl_entry.delete(0, tk.END)
    except:
        messagebox.showerror("Error", "Enter integer")

def heap_demo():
    try:
        nums = list(map(int, heap_entry.get().split()))
        mn = nums[:]
        heapq.heapify(mn)
        mx = [-i for i in nums]
        heapq.heapify(mx)
        out.config(text=f"Min:{mn}\nMax:{[-i for i in mx]}")
    except:
        messagebox.showerror("Error", "Space separated integers")

def add_task():
    try:
        p = int(priority.get())
        d = task.get()
        heapq.heappush(tasks, (p, d))
        priority.delete(0, tk.END)
        task.delete(0, tk.END)
        show_tasks()
    except:
        messagebox.showerror("Error", "Invalid input")

def run_task():
    if tasks:
        p, d = heapq.heappop(tasks)
        out.config(text=f"Running:\nPriority {p} -> {d}")
        show_tasks()

def show_tasks():
    lst.delete(0, tk.END)
    for p, d in sorted(tasks):
        lst.insert(tk.END, f"{p} : {d}")

app = tk.Tk()
app.title("AVL • Heap • Priority Queue")
app.geometry("500x560")

tk.Label(app, text="AVL Tree", font=("Arial", 12, "bold")).pack()

avl_entry = tk.Entry(app)
avl_entry.pack()

tk.Button(app, text="Insert", command=add_avl).pack(pady=3)

tk.Label(app, text="Heap (Space separated numbers)",
         font=("Arial", 12, "bold")).pack(pady=8)

heap_entry = tk.Entry(app, width=35)
heap_entry.pack()

tk.Button(app, text="Create Heap", command=heap_demo).pack()

tk.Label(app, text="Priority Queue",
         font=("Arial", 12, "bold")).pack(pady=8)

priority = tk.Entry(app, width=10)
priority.pack()

task = tk.Entry(app, width=35)
task.pack(pady=2)

tk.Button(app, text="Add Task", command=add_task).pack()

tk.Button(app, text="Run Highest Priority", command=run_task).pack(pady=3)

lst = tk.Listbox(app, width=50, height=6)
lst.pack(pady=5)

out = tk.Label(app, text="", justify="left",
               bg="white", width=55, height=8, anchor="nw")
out.pack(pady=8)

app.mainloop()
