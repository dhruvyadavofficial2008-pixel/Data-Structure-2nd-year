import time
import sys
from tkinter import *
from tkinter import messagebox, ttk

# ----------------------------------------------
# Singly Linked List Implementation
# ----------------------------------------------
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def insert_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_end(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            return
        temp = self.head
        while temp.next:
            temp = temp.next
        temp.next = new_node

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
        new_node = Node(data)
        new_node.next = temp.next
        temp.next = new_node

    def delete_value(self, key):
        if self.is_empty():
            return
        temp = self.head
        # If head itself holds the key
        if temp.data == key:
            self.head = temp.next
            temp = None
            return
        # Search for the key
        prev = None
        while temp and temp.data != key:
            prev = temp
            temp = temp.next
        if temp is None:   # key not found
            return
        prev.next = temp.next
        temp = None

    def delete_index(self, position):
        if self.is_empty():
            raise IndexError("List is empty.")
        if position < 0:
            raise IndexError("Position cannot be negative.")
        temp = self.head
        if position == 0:
            self.head = temp.next
            temp = None
            return
        prev = None
        for _ in range(position):
            prev = temp
            temp = temp.next
            if temp is None:
                raise IndexError("Position out of bounds.")
        prev.next = temp.next
        temp = None

    def search(self, key):
        temp = self.head
        index = 0
        while temp:
            if temp.data == key:
                return index
            temp = temp.next
            index += 1
        return -1

    def size(self):
        count = 0
        temp = self.head
        while temp:
            count += 1
            temp = temp.next
        return count

    def to_list(self):
        """Return a list of all data elements (for easy display)."""
        result = []
        temp = self.head
        while temp:
            result.append(temp.data)
            temp = temp.next
        return result

    def display(self):
        """Return a string representation of the list."""
        return " -> ".join(str(x) for x in self.to_list()) if not self.is_empty() else "Empty"


def run_cli():
    # Optional colour (if colorama is installed, otherwise fallback)
    try:
        from colorama import init, Fore, Style
        init(autoreset=True)
        def colored(text, color=Fore.GREEN):
            return color + text + Style.RESET_ALL
    except ImportError:
        # Fallback: no colours – define dummy Fore to avoid NameError
        class Fore:
            GREEN = ''
            RED = ''
            YELLOW = ''
        def colored(text, color=None):
            return text

    linked_list = SinglyLinkedList()

    def display_menu():
        print("\n" + "="*40)
        print("Singly Linked List Operations")
        print("1. Insert at beginning")
        print("2. Insert at end")
        print("3. Insert at position")
        print("4. Delete by value")
        print("5. Delete by index")
        print("6. Search for value")
        print("7. Get size")
        print("8. Display list")
        print("9. Exit")
        print("="*40)

    while True:
        display_menu()
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                data = int(input("Enter data: "))
                linked_list.insert_beginning(data)
                print(colored("Inserted at beginning.", Fore.GREEN))
            elif choice == 2:
                data = int(input("Enter data: "))
                linked_list.insert_end(data)
                print(colored("Inserted at end.", Fore.GREEN))
            elif choice == 3:
                data = int(input("Enter data: "))
                pos = int(input("Enter position (0-indexed): "))
                linked_list.insert_position(data, pos)
                print(colored(f"Inserted at position {pos}.", Fore.GREEN))
            elif choice == 4:
                data = int(input("Enter value to delete: "))
                linked_list.delete_value(data)
                print(colored("Deleted (if found).", Fore.RED))
            elif choice == 5:
                pos = int(input("Enter index to delete: "))
                linked_list.delete_index(pos)
                print(colored(f"Deleted at index {pos}.", Fore.RED))
            elif choice == 6:
                data = int(input("Enter value to search: "))
                idx = linked_list.search(data)
                if idx != -1:
                    print(colored(f"Value found at index {idx}.", Fore.GREEN))
                else:
                    print(colored("Value not found.", Fore.YELLOW))
            elif choice == 7:
                print(f"Size: {linked_list.size()}")
            elif choice == 8:
                print("List:", linked_list.display())
            elif choice == 9:
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

# ----------------------------------------------
# Graphical User Interface (Tkinter)
# ----------------------------------------------
class LinkedListGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Singly Linked List Manager")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        self.linked_list = SinglyLinkedList()

        # ===== Top Frame: Input area =====
        input_frame = Frame(root)
        input_frame.pack(pady=10)

        # Data entry
        Label(input_frame, text="Data:").grid(row=0, column=0, padx=5)
        self.data_entry = Entry(input_frame, width=10)
        self.data_entry.grid(row=0, column=1, padx=5)

        # Position/Index entry (for insert/delete at position)
        Label(input_frame, text="Position/Index:").grid(row=0, column=2, padx=5)
        self.pos_entry = Entry(input_frame, width=5)
        self.pos_entry.grid(row=0, column=3, padx=5)

        # ===== Button Frame =====
        btn_frame = Frame(root)
        btn_frame.pack(pady=5)

        buttons = [
            ("Insert Beginning", self.insert_beginning),
            ("Insert End", self.insert_end),
            ("Insert at Position", self.insert_position),
            ("Delete by Value", self.delete_value),
            ("Delete by Index", self.delete_index),
            ("Search", self.search),
            ("Size", self.show_size),
            ("Display", self.display_list),
            ("Clear All", self.clear_all),
        ]

        # Place buttons in a grid (3 columns)
        row, col = 0, 0
        for text, cmd in buttons:
            btn = Button(btn_frame, text=text, command=cmd, width=18)
            btn.grid(row=row, column=col, padx=2, pady=2)
            col += 1
            if col == 3:
                col = 0
                row += 1

        # ===== Display Area (Listbox with scrollbar) =====
        display_frame = Frame(root)
        display_frame.pack(pady=10, fill=BOTH, expand=True)

        Label(display_frame, text="Current List:", font=("Arial", 12)).pack(anchor=W)

        list_frame = Frame(display_frame)
        list_frame.pack(fill=BOTH, expand=True)

        self.listbox = Listbox(list_frame, font=("Courier", 12), height=12)
        scrollbar = Scrollbar(list_frame, orient=VERTICAL, command=self.listbox.yview)
        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Initially show empty list
        self.update_display()

        # ===== Quit Button =====
        Button(root, text="Quit", command=root.quit, bg="red", fg="white", width=10).pack(pady=5)

    # ---------- Helper methods ----------
    def get_data(self):
        """Return integer from data entry; raise ValueError if empty/invalid."""
        val = self.data_entry.get().strip()
        if val == "":
            raise ValueError("Please enter data.")
        return int(val)

    def get_pos(self):
        """Return integer from position entry; raise ValueError if empty/invalid."""
        val = self.pos_entry.get().strip()
        if val == "":
            return None
        return int(val)

    def update_display(self):
        """Refresh the listbox with current list elements."""
        self.listbox.delete(0, END)
        elems = self.linked_list.to_list()
        if not elems:
            self.listbox.insert(END, " (empty) ")
        else:
            for i, val in enumerate(elems):
                self.listbox.insert(END, f"[{i}] {val}")

    def show_info(self, message, title="Info"):
        messagebox.showinfo(title, message)

    def show_error(self, message, title="Error"):
        messagebox.showerror(title, message)

    # ---------- Button callbacks ----------
    def insert_beginning(self):
        try:
            data = self.get_data()
            self.linked_list.insert_beginning(data)
            self.update_display()
            self.data_entry.delete(0, END)
            self.show_info(f"Inserted {data} at beginning.")
        except ValueError as e:
            self.show_error(str(e))

    def insert_end(self):
        try:
            data = self.get_data()
            self.linked_list.insert_end(data)
            self.update_display()
            self.data_entry.delete(0, END)
            self.show_info(f"Inserted {data} at end.")
        except ValueError as e:
            self.show_error(str(e))

    def insert_position(self):
        try:
            data = self.get_data()
            pos = self.get_pos()
            if pos is None:
                raise ValueError("Please enter a position.")
            self.linked_list.insert_position(data, pos)
            self.update_display()
            self.data_entry.delete(0, END)
            self.pos_entry.delete(0, END)
            self.show_info(f"Inserted {data} at position {pos}.")
        except ValueError as e:
            self.show_error(str(e))
        except IndexError as e:
            self.show_error(str(e))

    def delete_value(self):
        try:
            data = self.get_data()
            self.linked_list.delete_value(data)
            self.update_display()
            self.data_entry.delete(0, END)
            self.show_info(f"Deleted value {data} (if found).")
        except ValueError as e:
            self.show_error(str(e))

    def delete_index(self):
        try:
            pos = self.get_pos()
            if pos is None:
                raise ValueError("Please enter an index.")
            self.linked_list.delete_index(pos)
            self.update_display()
            self.pos_entry.delete(0, END)
            self.show_info(f"Deleted node at index {pos}.")
        except ValueError as e:
            self.show_error(str(e))
        except IndexError as e:
            self.show_error(str(e))

    def search(self):
        try:
            data = self.get_data()
            idx = self.linked_list.search(data)
            if idx != -1:
                self.show_info(f"Value {data} found at index {idx}.", "Search Result")
            else:
                self.show_info(f"Value {data} not found.", "Search Result")
            self.data_entry.delete(0, END)
        except ValueError as e:
            self.show_error(str(e))

    def show_size(self):
        size = self.linked_list.size()
        self.show_info(f"Size of list: {size}", "Size")

    def display_list(self):
        # Just show the current list in a messagebox (or we already have it in listbox)
        self.update_display()
        self.show_info("List updated in display area.", "Display")

    def clear_all(self):
        # Clear the linked list
        self.linked_list = SinglyLinkedList()
        self.update_display()
        self.show_info("All nodes cleared.")


# ----------------------------------------------
# Main program – choose interface
# ----------------------------------------------
def main():
    print("Welcome to Singly Linked List Manager")
    print("Select interface:")
    print("1. Command Line Interface (CLI)")
    print("2. Graphical User Interface (GUI)")
    choice = input("Enter 1 or 2: ").strip()
    if choice == "1":
        run_cli()
    elif choice == "2":
        try:
            root = Tk()
            app = LinkedListGUI(root)
            root.mainloop()
        except ImportError:
            print("Error: tkinter is not available. Please install python3-tk.")
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    main()
