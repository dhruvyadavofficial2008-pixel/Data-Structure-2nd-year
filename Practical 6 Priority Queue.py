import tkinter as tk
from tkinter import messagebox, ttk

class LinearQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front = -1
        self.rear = -1
        self.count = 0

    def is_empty(self):
        return self.count == 0

    def is_full(self):
        return self.count == self.capacity

    def enqueue(self, item):
        if self.is_full():
            raise OverflowError("LinearQueue is full")
        if self.front == -1:
            self.front = 0
        self.rear += 1
        self.queue[self.rear] = item
        self.count += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("LinearQueue is empty")
        item = self.queue[self.front]
        self.front += 1
        self.count -= 1
        if self.front > self.rear:
            self.front = self.rear = -1
        return item

    def traverse(self):
        if self.is_empty():
            return []
        return self.queue[self.front:self.rear+1]

    def size(self):
        return self.count


class CircularQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front = 0
        self.rear = 0
        self.count = 0

    def is_empty(self):
        return self.count == 0

    def is_full(self):
        return self.count == self.capacity

    def enqueue(self, item):
        if self.is_full():
            raise OverflowError("CircularQueue is full")
        self.queue[self.rear] = item
        self.rear = (self.rear + 1) % self.capacity
        self.count += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("CircularQueue is empty")
        item = self.queue[self.front]
        self.front = (self.front + 1) % self.capacity
        self.count -= 1
        return item

    def traverse(self):
        if self.is_empty():
            return []
        result = []
        idx = self.front
        for _ in range(self.count):
            result.append(self.queue[idx])
            idx = (idx + 1) % self.capacity
        return result

    def size(self):
        return self.count


class QueueGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Queue Simulator (Task Scheduling)")
        self.root.geometry("700x500")

        top_frame = tk.Frame(root)
        top_frame.pack(pady=10)
        tk.Label(top_frame, text="Queue Type:").pack(side=tk.LEFT, padx=5)
        self.queue_var = tk.StringVar(value="Linear")
        tk.Radiobutton(top_frame, text="Linear", variable=self.queue_var,
                       value="Linear", command=self.reset_queue).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(top_frame, text="Circular", variable=self.queue_var,
                       value="Circular", command=self.reset_queue).pack(side=tk.LEFT, padx=5)
        tk.Label(top_frame, text="Capacity:").pack(side=tk.LEFT, padx=(20,5))
        self.capacity_entry = tk.Entry(top_frame, width=5)
        self.capacity_entry.insert(0, "5")
        self.capacity_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Create Queue", command=self.reset_queue).pack(side=tk.LEFT, padx=5)

        self.display_frame = tk.Frame(root)
        self.display_frame.pack(pady=10)
        self.queue_label = tk.Label(self.display_frame, text="Queue: [ ]", font=("Courier", 14))
        self.queue_label.pack()

        stats_frame = tk.Frame(root)
        stats_frame.pack(pady=5)
        self.size_label = tk.Label(stats_frame, text="Size: 0 / 0", font=("Arial", 12))
        self.size_label.pack(side=tk.LEFT, padx=20)
        self.empty_label = tk.Label(stats_frame, text="Empty: Yes", font=("Arial", 12))
        self.empty_label.pack(side=tk.LEFT, padx=20)
        self.full_label = tk.Label(stats_frame, text="Full: No", font=("Arial", 12))
        self.full_label.pack(side=tk.LEFT, padx=20)

        op_frame = tk.Frame(root)
        op_frame.pack(pady=10)
        tk.Label(op_frame, text="Item:").pack(side=tk.LEFT, padx=5)
        self.item_entry = tk.Entry(op_frame, width=20)
        self.item_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(op_frame, text="Enqueue", command=self.enqueue_action).pack(side=tk.LEFT, padx=5)
        tk.Button(op_frame, text="Dequeue", command=self.dequeue_action).pack(side=tk.LEFT, padx=5)
        tk.Button(op_frame, text="Reset", command=self.reset_queue).pack(side=tk.LEFT, padx=5)

        bottom_frame = tk.Frame(root)
        bottom_frame.pack(pady=10)
        tk.Button(bottom_frame, text="Simulate Tasks (add 3 tasks)", command=self.simulate_tasks).pack(pady=5)
        self.log_text = tk.Text(root, height=6, width=70, state=tk.DISABLED)
        self.log_text.pack(pady=10)

        self.queue = None
        self.reset_queue()

    def reset_queue(self):
        """Create a new queue based on selected type and capacity."""
        try:
            cap = int(self.capacity_entry.get())
            if cap < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Capacity", "Capacity must be a positive integer.")
            return
        qtype = self.queue_var.get()
        if qtype == "Linear":
            self.queue = LinearQueue(cap)
        else:
            self.queue = CircularQueue(cap)
        self.update_display()
        self.log("Queue reset to {} with capacity {}".format(qtype, cap))

    def update_display(self):
        """Refresh the GUI elements to reflect current queue state."""
        if self.queue is None:
            return
        items = self.queue.traverse()
        display_str = "Queue: [ " + " -> ".join(str(i) for i in items) + " ]"
        self.queue_label.config(text=display_str)
        self.size_label.config(text=f"Size: {self.queue.size()} / {self.queue.capacity}")
        self.empty_label.config(text=f"Empty: {'Yes' if self.queue.is_empty() else 'No'}")
        self.full_label.config(text=f"Full: {'Yes' if self.queue.is_full() else 'No'}")

    def log(self, message):
        """Append a message to the log area."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def enqueue_action(self):
        """Enqueue the item from entry field."""
        if self.queue is None:
            return
        item = self.item_entry.get().strip()
        if not item:
            messagebox.showwarning("Empty Item", "Please enter an item.")
            return
        try:
            self.queue.enqueue(item)
            self.log(f"Enqueued: {item}")
            self.item_entry.delete(0, tk.END)
            self.update_display()
        except OverflowError as e:
            messagebox.showerror("Queue Full", str(e))
            self.log(f"Error: {e}")

    def dequeue_action(self):
        """Dequeue the front item."""
        if self.queue is None:
            return
        try:
            item = self.queue.dequeue()
            self.log(f"Dequeued: {item}")
            self.update_display()
        except IndexError as e:
            messagebox.showerror("Queue Empty", str(e))
            self.log(f"Error: {e}")

    def simulate_tasks(self):
        """Add three predefined tasks to simulate scheduling."""
        tasks = ["Task-A", "Task-B", "Task-C"]
        for t in tasks:
            try:
                self.queue.enqueue(t)
                self.log(f"Simulated enqueue: {t}")
            except OverflowError:
                self.log(f"Simulation aborted: queue full at {t}")
                break
        self.update_display()

    def run(self):
        self.root.mainloop()


def run_cli():
    print("\n=== Queue Simulator (CLI) ===\n")
    qtype = input("Select queue type (linear/circular): ").strip().lower()
    while qtype not in ("linear", "circular"):
        qtype = input("Invalid. Choose 'linear' or 'circular': ").strip().lower()
    try:
        cap = int(input("Enter capacity: "))
        if cap < 1:
            raise ValueError
    except ValueError:
        print("Invalid capacity. Using default 5.")
        cap = 5

    if qtype == "linear":
        q = LinearQueue(cap)
    else:
        q = CircularQueue(cap)

    print(f"\nQueue created ({qtype}, capacity {cap}). Commands: enqueue <item>, dequeue, traverse, empty, full, size, exit")

    while True:
        cmd = input("\n> ").strip().split()
        if not cmd:
            continue
        op = cmd[0].lower()
        if op == "exit":
            print("Exiting.")
            break
        elif op == "enqueue" and len(cmd) > 1:
            item = " ".join(cmd[1:])
            try:
                q.enqueue(item)
                print(f"Enqueued: {item}")
            except OverflowError as e:
                print(e)
        elif op == "dequeue":
            try:
                item = q.dequeue()
                print(f"Dequeued: {item}")
            except IndexError as e:
                print(e)
        elif op == "traverse":
            items = q.traverse()
            if items:
                print("Queue content:", " -> ".join(str(i) for i in items))
            else:
                print("Queue is empty.")
        elif op == "empty":
            print("Is empty?", q.is_empty())
        elif op == "full":
            print("Is full?", q.is_full())
        elif op == "size":
            print("Size:", q.size(), "/", q.capacity)
        else:
            print("Unknown command. Available: enqueue, dequeue, traverse, empty, full, size, exit")


def main():
    print("Queue Simulator - Task Scheduling")
    print("Choose interface:")
    print("  1. Command‑Line Interface (CLI)")
    print("  2. Graphical User Interface (GUI)")
    choice = input("Enter 1 or 2: ").strip()
    if choice == "1":
        run_cli()
    elif choice == "2":
        root = tk.Tk()
        app = QueueGUI(root)
        app.run()
    else:
        print("Invalid choice. Defaulting to GUI.")
        root = tk.Tk()
        app = QueueGUI(root)
        app.run()

if __name__ == "__main__":
    main()
