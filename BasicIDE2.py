import tkinter as tk
from tkinter import scrolledtext, messagebox
import basic  # Assuming basic is a module you created or imported
import io
import sys

class BasicIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic IDE")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create text area for code input
        self.code_label = tk.Label(self.root, text="Code Editor:")
        self.code_label.pack(padx=10, pady=5, anchor='w')
        
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=100, height=30)
        self.text_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # Create Run button
        self.run_button = tk.Button(self.root, text="Run", command=self.run_code)
        self.run_button.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Create text area for output
        self.output_label = tk.Label(self.root, text="Output:")
        self.output_label.pack(padx=10, pady=5, anchor='w')
        
        self.output_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=100, height=10, state='disabled')
        self.output_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
    
    def run_code(self):
        code = self.text_area.get("1.0", tk.END).strip()
        if not code:
            messagebox.showwarning("Warning", "Code editor is empty!")
            return

        # Redirect stdout to capture print statements
        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()

        result, error = None, None
        try:
            result, error = basic.run('<stdin>', code)
        except Exception as e:
            error = str(e)
        
        # Reset stdout
        sys.stdout = old_stdout

        # Get the printed output
        printed_output = redirected_output.getvalue()

        self.display_output(result, error, printed_output)
        
    def display_output(self, result, error, printed_output):
        self.output_area.config(state='normal')  # Enable editing in the output area
        self.output_area.delete("1.0", tk.END)  # Clear any previous content
        
        if error:
            self.output_area.insert(tk.INSERT, error.as_string())  # Insert error message
        elif printed_output:
            self.output_area.insert(tk.INSERT, printed_output)  # Insert printed output
        elif result:
            # Directly insert the result if it is a string
            if isinstance(result, str):
                self.output_area.insert(tk.INSERT, result)
            elif hasattr(result, 'elements'):
                # If result has elements, handle them appropriately
                if len(result.elements) == 1:
                    self.output_area.insert(tk.INSERT, str(result.elements[0]))
                else:
                    self.output_area.insert(tk.INSERT, str(result))
            else:
                self.output_area.insert(tk.INSERT, str(result))
        
        self.output_area.config(state='disabled')  # Disable editing in the output area

if __name__ == "__main__":
    root = tk.Tk()
    app = BasicIDE(root)
    root.mainloop()
