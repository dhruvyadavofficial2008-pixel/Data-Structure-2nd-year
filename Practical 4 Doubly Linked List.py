import time
import sys
from tkinter import *
from tkinter import messagebox, ttk

# ============================================
# Doubly Linked List Implementation
# ============================================
class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return self.head is None

    # ---------- Insertion ----------
    def insert_beginning(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def insert_end(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

    def insert_position(self, data, position):
        if position < 0:
            raise IndexError("Position cannot be negative.")
        if position == 0:
            self.insert_beginning(data)
            return
        temp = self.head
        for _ in range(position - 1):
            if temp is None:
                raise IndexError("Position out of bounds.")
            temp = temp.next
        if temp is None:
            raise IndexError("Position out of bounds.")
        # Insert after temp
        if temp == self.tail:
            self.insert_end(data)
            return
        new_node = Node(data)
        new_node.prev = temp
        new_node.next = temp.next
        temp.next.prev = new_node
        temp.next = new_node

    # ---------- Deletion ----------
    def delete_value(self, key):
        if self.is_empty():
            return
        temp = self.head
        while temp and temp.data != key:
            temp = temp.next
        if temp is None:      # not found
            return
        # Remove temp
        if temp.prev:
            temp.prev.next = temp.next
        else:
            self.head = temp.next
        if temp.next:
            temp.next.prev = temp.prev
        else:
            self.tail = temp.prev
        temp.prev = temp.next = None

    def delete_index(self, position):
        if self.is_empty():
            raise IndexError("List is empty.")
        if position < 0:
            raise IndexError("Position cannot be negative.")
        temp = self.head
        for _ in range(position):
            if temp is None:
                raise IndexError("Position out of bounds.")
            temp = temp.next
        if temp is None:
            raise IndexError("Position out of bounds.")
        # Remove temp
        if temp.prev:
            temp.prev.next = temp.next
        else:
            self.head = temp.next
        if temp.next:
            temp.next.prev = temp.prev
        else:
            self.tail = temp.prev
        temp.prev = temp.next = None

    # ---------- Search ----------
    def search(self, key):
        temp = self.head
        index = 0
        while temp:
            if temp.data == key:
                return index
            temp = temp.next
            index += 1
        return -1

    # ---------- Utility ----------
    def size(self):
        count = 0
        temp = self.head
        while temp:
            count += 1
            temp = temp.next
        return count

    def to_list_forward(self):
        """Return list of data in forward order."""
        result = []
        temp = self.head
        while temp:
            result.append(temp.data)
            temp = temp.next
        return result

    def to_list_reverse(self):
        """Return list of data in reverse order."""
        result = []
        temp = self.tail
        while temp:
            result.append(temp.data)
            temp = temp.prev
        return result

    def display_forward(self):
        return " -> ".join(str(x) for x in self.to_list_forward()) if not self.is_empty() else "Empty"

    def display_reverse(self):
        return " <- ".join(str(x) for x in self.to_list_reverse()) if not self.is_empty() else "Empty"

    def clear(self):
        self.head = self.tail = None


# ============================================
# Command Line Interface
# ============================================
def run_cli():
    # Coloured output (if colorama is available)
    try:
        from colorama import init, Fore, Style
        init(autoreset=True)
        def colored(text, color=Fore.GREEN):
            return color + text + Style.RESET_ALL
    except ImportError:
        # Fallback: dummy Fore class to avoid NameError
        class Fore:
            GREEN = RED = YELLOW = ''
        def colored(text, color=None):
            return text

    dll = DoublyLinkedList()

    def display_menu():
        print("\n" + "=" * 50)
        print("          DOUBLY LINKED LIST OPERATIONS")
        print("=" * 50)
        print("1. Insert at beginning")
        print("2. Insert at end")
        print("3. Insert at position")
        print("4. Delete by value")
        print("5. Delete by index")
        print("6. Search for value")
        print("7. Get size")
        print("8. Display forward")
        print("9. Display reverse")
        print("10. Clear all")
        print("11. Exit")
        print("=" * 50)

    while True:
        display_menu()
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                data = int(input("Enter data: "))
                dll.insert_beginning(data)
                print(colored("Inserted at beginning.", Fore.GREEN))
            elif choice == 2:
                data = int(input("Enter data: "))
                dll.insert_end(data)
                print(colored("Inserted at end.", Fore.GREEN))
            elif choice == 3:
                data = int(input("Enter data: "))
                pos = int(input("Enter position (0-indexed): "))
                dll.insert_position(data, pos)
                print(colored(f"Inserted at position {pos}.", Fore.GREEN))
            elif choice == 4:
                data = int(input("Enter value to delete: "))
                dll.delete_value(data)
                print(colored("Deleted (if found).", Fore.RED))
            elif choice == 5:
                pos = int(input("Enter index to delete: "))
                dll.delete_index(pos)
                print(colored(f"Deleted at index {pos}.", Fore.RED))
            elif choice == 6:
                data = int(input("Enter value to search: "))
                idx = dll.search(data)
                if idx != -1:
                    print(colored(f"Value found at index {idx}.", Fore.GREEN))
                else:
                    print(colored("Value not found.", Fore.YELLOW))
            elif choice == 7:
                print(f"Size: {dll.size()}")
            elif choice == 8:
                print("Forward  :", dll.display_forward())
            elif choice == 9:
                print("Reverse  :", dll.display_reverse())
            elif choice == 10:
                dll.clear()
                print(colored("List cleared.", Fore.RED))
            elif choice == 11:
                print("Exiting CLI...")
                break
            else:
                print(colored("Invalid choice.", Fore.YELLOW))
        except ValueError:
            print(colored("Please enter a valid integer.", Fore.YELLOW))
        except IndexError as e:
            print(colored(f"Error: {e}", Fore.RED))
        except Exception as e:
            print(colored(f"Unexpected error: {e}", Fore.RED))
        time.sleep(1)


# ============================================
# Graphical User Interface (Tkinter)
# ============================================
class DoublyLinkedListGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Doubly Linked List Manager")
        self.root.geometry("700x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        self.dll = DoublyLinkedList()

        # ---------- Top Frame: Input ----------
        input_frame = LabelFrame(root, text="Input Data", font=("Arial", 10, "bold"), bg="#f0f0f0")
        input_frame.pack(pady=10, padx=10, fill=X)

        Label(input_frame, text="Data:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        self.data_entry = Entry(input_frame, width=15, font=("Arial", 10))
        self.data_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(input_frame, text="Position/Index:", bg="#f0f0f0").grid(row=0, column=2, padx=5, pady=5)
        self.pos_entry = Entry(input_frame, width=5, font=("Arial", 10))
        self.pos_entry.grid(row=0, column=3, padx=5, pady=5)

        # ---------- Button Frame ----------
        btn_frame = Frame(root, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        # Buttons arranged in a grid (4 columns)
        buttons = [
            ("Insert Beginning", self.insert_beginning),
            ("Insert End", self.insert_end),
            ("Insert at Position", self.insert_position),
            ("Delete by Value", self.delete_value),
            ("Delete by Index", self.delete_index),
            ("Search", self.search),
            ("Size", self.show_size),
            ("Display Reverse", self.show_reverse),
            ("Clear All", self.clear_all),
            ("Quit", self.quit_app)
        ]

        row, col = 0, 0
        for text, cmd in buttons:
            btn = Button(btn_frame, text=text, command=cmd, width=16, bg="#e0e0e0", relief=RAISED)
            btn.grid(row=row, column=col, padx=4, pady=4)
            col += 1
            if col == 4:
                col = 0
                row += 1

        # ---------- Display Area ----------
        display_frame = Frame(root, bg="#f0f0f0")
        display_frame.pack(pady=10, padx=10, fill=BOTH, expand=True)

        # Left side: Listbox with scrollbar (forward view)
        left_frame = Frame(display_frame, bg="#f0f0f0")
        left_frame.pack(side=LEFT, fill=BOTH, expand=True)

        Label(left_frame, text="List (Forward with Indices)", font=("Arial", 11, "bold"), bg="#f0f0f0").pack(anchor=W)

        list_frame = Frame(left_frame)
        list_frame.pack(fill=BOTH, expand=True)

        self.listbox = Listbox(list_frame, font=("Courier", 11), height=12, bg="#ffffff")
        scrollbar = Scrollbar(list_frame, orient=VERTICAL, command=self.listbox.yview)
        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Right side: Size label
        right_frame = Frame(display_frame, bg="#f0f0f0", width=150)
        right_frame.pack(side=RIGHT, fill=Y, padx=10)
        right_frame.pack_propagate(False)

        Label(right_frame, text="Status / Info", font=("Arial", 11, "bold"), bg="#f0f0f0").pack(pady=5)
        self.size_label = Label(right_frame, text="Size: 0", font=("Arial", 10), bg="#f0f0f0")
        self.size_label.pack(pady=5)

        # A small text area for messages (optional)
        self.info_label = Label(right_frame, text="Ready", font=("Arial", 9), bg="#f0f0f0", fg="#333333", wraplength=140)
        self.info_label.pack(pady=10)

        # Initially update display
        self.update_display()

    # ---------- Helper Methods ----------
    def get_data(self):
        val = self.data_entry.get().strip()
        if val == "":
            raise ValueError("Please enter data.")
        return int(val)

    def get_pos(self):
        val = self.pos_entry.get().strip()
        if val == "":
            return None
        return int(val)

    def update_display(self):
        """Refresh the listbox and size label."""
        self.listbox.delete(0, END)
        elems = self.dll.to_list_forward()
        if not elems:
            self.listbox.insert(END, " (empty) ")
        else:
            for i, val in enumerate(elems):
                self.listbox.insert(END, f"[{i}] {val}")
        self.size_label.config(text=f"Size: {self.dll.size()}")

    def show_info(self, msg, title="Info"):
        messagebox.showinfo(title, msg)

    def show_error(self, msg, title="Error"):
        messagebox.showerror(title, msg)

    def set_status(self, msg):
        self.info_label.config(text=msg)

    # ---------- Button Callbacks ----------
    def insert_beginning(self):
        try:
            data = self.get_data()
            self.dll.insert_beginning(data)
            self.update_display()
            self.data_entry.delete(0, END)
            self.set_status(f"Inserted {data} at beginning.")
            self.show_info(f"Inserted {data} at beginning.")
        except ValueError as e:
            self.show_error(str(e))

    def insert_end(self):
        try:
            data = self.get_data()
            self.dll.insert_end(data)
            self.update_display()
            self.data_entry.delete(0, END)
            self.set_status(f"Inserted {data} at end.")
            self.show_info(f"Inserted {data} at end.")
        except ValueError as e:
            self.show_error(str(e))

    def insert_position(self):
        try:
            data = self.get_data()
            pos = self.get_pos()
            if pos is None:
                raise ValueError("Please enter a position.")
            self.dll.insert_position(data, pos)
            self.update_display()
            self.data_entry.delete(0, END)
            self.pos_entry.delete(0, END)
            self.set_status(f"Inserted {data} at position {pos}.")
            self.show_info(f"Inserted {data} at position {pos}.")
        except (ValueError, IndexError) as e:
            self.show_error(str(e))

    def delete_value(self):
        try:
            data = self.get_data()
            self.dll.delete_value(data)
            self.update_display()
            self.data_entry.delete(0, END)
            self.set_status(f"Deleted value {data} (if found).")
            self.show_info(f"Deleted value {data} (if found).")
        except ValueError as e:
            self.show_error(str(e))

    def delete_index(self):
        try:
            pos = self.get_pos()
            if pos is None:
                raise ValueError("Please enter an index.")
            self.dll.delete_index(pos)
            self.update_display()
            self.pos_entry.delete(0, END)
            self.set_status(f"Deleted node at index {pos}.")
            self.show_info(f"Deleted node at index {pos}.")
        except (ValueError, IndexError) as e:
            self.show_error(str(e))

    def search(self):
        try:
            data = self.get_data()
            idx = self.dll.search(data)
            if idx != -1:
                self.show_info(f"Value {data} found at index {idx}.", "Search Result")
                self.set_status(f"Found {data} at index {idx}.")
            else:
                self.show_info(f"Value {data} not found.", "Search Result")
                self.set_status(f"{data} not found.")
            self.data_entry.delete(0, END)
        except ValueError as e:
            self.show_error(str(e))

    def show_size(self):
        size = self.dll.size()
        self.show_info(f"Size of list: {size}", "Size")
        self.set_status(f"Size = {size}")

    def show_reverse(self):
        rev = self.dll.to_list_reverse()
        if not rev:
            self.show_info("List is empty.", "Reverse View")
        else:
            rev_str = " <- ".join(str(x) for x in rev)
            self.show_info(f"Reverse order:\n{rev_str}", "Reverse View")
        self.set_status("Displayed reverse order.")

    def clear_all(self):
        if messagebox.askyesno("Clear All", "Are you sure you want to clear the entire list?"):
            self.dll.clear()
            self.update_display()
            self.set_status("List cleared.")
            self.show_info("List cleared.", "Clear")

    def quit_app(self):
        if messagebox.askyesno("Quit", "Do you really want to quit?"):
            self.root.quit()


# ============================================
# Main program – choose interface
# ============================================
def main():
    print("Welcome to Doubly Linked List Manager")
    print("Select interface:")
    print("1. Command Line Interface (CLI)")
    print("2. Graphical User Interface (GUI)")
    choice = input("Enter 1 or 2: ").strip()
    if choice == "1":
        run_cli()
    elif choice == "2":
        try:
            root = Tk()
            app = DoublyLinkedListGUI(root)
            root.mainloop()
        except ImportError:
            print("Error: tkinter is not available. Please install python3-tk.")
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    main()
