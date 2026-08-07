"""S123 Dhruv Yadav - Huffman Coding GUI (Tkinter). Run: python3 huffman_gui.py"""
import heapq
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from collections import Counter


class Node:
    def __init__(self, char=None, freq=None):
        self.char, self.freq, self.left, self.right = char, freq, None, None

    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("S123 Dhruv Yadav - Huffman Coding")
        self.root.geometry("880x680")
        self.root.configure(bg="#1e1e2e")
        self.codebook, self.encoded_data = {}, ""
        self._build_styles()
        self._build_layout()

    def _build_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#1e1e2e")
        style.configure("TLabel", background="#1e1e2e", foreground="#cdd6f4", font=("Segoe UI", 10))
        style.configure("Header.TLabel", background="#1e1e2e", foreground="#89b4fa", font=("Segoe UI", 16, "bold"))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
        style.configure("Treeview", background="#313244", fieldbackground="#313244", foreground="#cdd6f4", rowheight=24)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    def _build_layout(self):
        ttk.Label(self.root, text="Huffman Coding Visualizer", style="Header.TLabel").pack(pady=(15, 5))
        ttk.Label(self.root, text="S123 Dhruv Yadav").pack(pady=(0, 10))

        input_frame = ttk.Frame(self.root)
        input_frame.pack(fill="x", padx=20, pady=5)
        ttk.Label(input_frame, text="Enter text:").pack(side="left")
        self.text_entry = ttk.Entry(input_frame, font=("Segoe UI", 11))
        self.text_entry.pack(side="left", fill="x", expand=True, padx=10)
        self.text_entry.insert(0, "hello world")
        ttk.Button(input_frame, text="Encode", command=self.on_encode).pack(side="left", padx=5)
        ttk.Button(input_frame, text="Decode", command=self.on_decode).pack(side="left", padx=5)
        ttk.Button(input_frame, text="Clear", command=self.on_clear).pack(side="left")

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=20, pady=10)

        table_tab = ttk.Frame(notebook)
        notebook.add(table_tab, text="Frequencies & Codebook")
        self.tree = ttk.Treeview(table_tab, columns=("char", "freq", "code"), show="headings", height=12)
        for col, txt, w in (("char", "Character", 150), ("freq", "Frequency", 150), ("code", "Huffman Code", 250)):
            self.tree.heading(col, text=txt)
            self.tree.column(col, anchor="center", width=w)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        log_tab = ttk.Frame(notebook)
        notebook.add(log_tab, text="Tree Merge Steps")
        self.merge_log = scrolledtext.ScrolledText(
            log_tab, bg="#313244", fg="#f9e2af", font=("Consolas", 10), wrap="word"
        )
        self.merge_log.pack(fill="both", expand=True, padx=10, pady=10)

        output_tab = ttk.Frame(notebook)
        notebook.add(output_tab, text="Encoded / Decoded Output")
        ttk.Label(output_tab, text="Encoded bitstring:").pack(anchor="w", padx=10, pady=(10, 0))
        self.encoded_box = scrolledtext.ScrolledText(
            output_tab, height=6, bg="#313244", fg="#a6e3a1", font=("Consolas", 10), wrap="word"
        )
        self.encoded_box.pack(fill="x", padx=10, pady=5)
        ttk.Label(output_tab, text="Decode steps:").pack(anchor="w", padx=10, pady=(10, 0))
        self.decode_log = scrolledtext.ScrolledText(
            output_tab, height=8, bg="#313244", fg="#f38ba8", font=("Consolas", 10), wrap="word"
        )
        self.decode_log.pack(fill="both", expand=True, padx=10, pady=5)

        self.status_var = tk.StringVar(value="Enter text and click Encode to begin.")
        ttk.Label(self.root, textvariable=self.status_var, font=("Segoe UI", 10, "italic")).pack(pady=(0, 12))

    def build_huffman_tree(self, frequencies):
        heap = [Node(c, f) for c, f in frequencies.items()]
        heapq.heapify(heap)
        if len(heap) == 1:
            root = Node(freq=heap[0].freq)
            root.left = heap[0]
            return root
        while len(heap) > 1:
            left, right = heapq.heappop(heap), heapq.heappop(heap)
            merged = Node(freq=left.freq + right.freq)
            merged.left, merged.right = left, right
            heapq.heappush(heap, merged)
            ll = left.char if left.char is not None else "internal"
            rl = right.char if right.char is not None else "internal"
            msg = (
                f"Merging: {ll!r} (freq={left.freq})  +  {rl!r} (freq={right.freq})  "
                f"->  new node (freq={merged.freq})\n"
            )
            self.merge_log.insert("end", msg)
        return heap[0]

    def generate_codes(self, node, prefix="", codebook=None):
        if codebook is None:
            codebook = {}
        if node:
            if node.char is not None:
                codebook[node.char] = prefix if prefix else "0"
            self.generate_codes(node.left, prefix + "0", codebook)
            self.generate_codes(node.right, prefix + "1", codebook)
        return codebook

    def huffman_encoding(self, data):
        if not data:
            return "", {}, Counter()
        frequencies = Counter(data)
        root = self.build_huffman_tree(frequencies)
        codebook = self.generate_codes(root)
        encoded_data = "".join(codebook[char] for char in data)
        return encoded_data, codebook, frequencies

    def huffman_decoding(self, encoded_data, codebook):
        reverse_codebook = {v: k for k, v in codebook.items()}
        decoded_data, current_code = "", ""
        for bit in encoded_data:
            current_code += bit
            if current_code in reverse_codebook:
                char = reverse_codebook[current_code]
                decoded_data += char
                self.decode_log.insert("end", f"{current_code} -> {char!r}\n")
                current_code = ""
        return decoded_data

    def on_encode(self):
        data = self.text_entry.get()
        if not data:
            messagebox.showwarning("Input needed", "Please enter some text to encode.")
            return
        self.on_clear(keep_entry=True)
        self.encoded_data, self.codebook, frequencies = self.huffman_encoding(data)
        for char, freq in frequencies.items():
            display_char = char if char != " " else "␣ (space)"
            self.tree.insert("", "end", values=(repr(display_char), freq, self.codebook[char]))
        self.encoded_box.insert("end", self.encoded_data)
        self.status_var.set(
            f"Encoded {len(data)} characters into {len(self.encoded_data)} bits "
            f"({len(self.codebook)} unique symbols)."
        )

    def on_decode(self):
        if not self.encoded_data or not self.codebook:
            messagebox.showwarning("Nothing to decode", "Please click Encode first.")
            return
        self.decode_log.delete("1.0", "end")
        decoded = self.huffman_decoding(self.encoded_data, self.codebook)
        original = self.text_entry.get()
        if decoded == original:
            self.status_var.set(f"Success: decoded text matches the original -> {decoded!r}")
        else:
            self.status_var.set(f"Error: decoded text does NOT match the original! Got {decoded!r}")

    def on_clear(self, keep_entry=False):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.merge_log.delete("1.0", "end")
        self.encoded_box.delete("1.0", "end")
        self.decode_log.delete("1.0", "end")
        self.encoded_data, self.codebook = "", {}
        if not keep_entry:
            self.text_entry.delete(0, "end")
        self.status_var.set("Enter text and click Encode to begin.")


if __name__ == "__main__":
    print("S123 Dhruv Yadav")
    root = tk.Tk()
    app = HuffmanApp(root)
    root.mainloop()
