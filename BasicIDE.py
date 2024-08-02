import tkinter as tk
from tkinter import scrolledtext, messagebox
import basic

class BasicIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic IDE")
        
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=100, height=30)
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.run_button = tk.Button(self.root, text="Run", command=self.run_code)
        self.run_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.output_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=100, height=10, state='disabled')
        self.output_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
    def run_code(self):
        code = self.text_area.get("1.0", tk.END)
        if code.strip() == "":
            return
        
        result, error = basic.run('<stdin>', code)
        
        self.output_area.config(state='normal')
        self.output_area.delete("1.0", tk.END)
        
        if error:
            self.output_area.insert(tk.INSERT, error.as_string())
        elif result:
            if len(result.elements) == 1:
                self.output_area.insert(tk.INSERT, repr(result.elements[0]))
            else:
                self.output_area.insert(tk.INSERT, repr(result))
        
        self.output_area.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = BasicIDE(root)
    root.mainloop()
