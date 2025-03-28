import tkinter as tk
from tkinter import ttk


class LabelInput(tk.Frame):
    """A widget containing a label and input together."""

    def __init__(self, parent, label='', input_class=ttk.Entry, input_var=None, input_args=None, label_args=None, **kwargs):
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        self.variable = input_var

        if input_class in (ttk.Checkbutton, ttk.Button, ttk.Radiobutton):
            input_args["text"] = label
            input_args["variable"] = input_var
        else:
            self.label = ttk.Label(self, text=label, **label_args)
            self.label.grid(row=0, column=0, sticky=(tk.W + tk.E))
            input_args["textvariable"] = input_var

        self.input = input_class(self, **input_args)
        self.input.grid(row=1, column=0, sticky=(tk.W + tk.E))
        self.columnconfigure(0, weight=1)

    def grid(self, sticky=(tk.E + tk.W), **kwargs):
        super().grid(sticky=sticky, **kwargs)

    def get(self):
        try:
            if self.variable:
                return self.variable.get()
            elif isinstance(self.input, tk.Text):
                return self.input.get('1.0', tk.END).strip()
            else:
                return self.input.get()
        except (TypeError, tk.TclError):
            return ''

    def set(self, value, *args, **kwargs):
        if isinstance(self.variable, tk.BooleanVar):
            self.variable.set(bool(value))
        elif self.variable:
            self.variable.set(value, *args, **kwargs)
        elif isinstance(self.input, (ttk.Checkbutton, ttk.Radiobutton)):
            if value:
                self.input.select()
            else:
                self.input.deselect()
        elif isinstance(self.input, tk.Text):
            self.input.delete('1.0', tk.END)
            self.input.insert('1.0', value)
        else:
            self.input.delete(0, tk.END)
            self.input.insert(0, value)


class DataRecordForm(tk.Frame):
    """The input form for our widgets"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.inputs = {}

        # Record Information Section
        recordinfo = tk.LabelFrame(self, text="Record Information")
        recordinfo.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        self.inputs['Date'] = LabelInput(
            recordinfo, "Date", input_var=tk.StringVar())
        print(self.inputs['Date'].)
        self.inputs['Date'].grid(row=0, column=0, padx=5, pady=5)

        self.inputs['Time'] = LabelInput(
            recordinfo, "Time", input_class=ttk.Combobox, input_var=tk.StringVar(),
            input_args={"values": ["8:00", "12:00", "16:00", "20:00"]}
        )
        self.inputs['Time'].grid(row=0, column=1, padx=5, pady=5)

        self.inputs['Technician'] = LabelInput(
            recordinfo, "Technician", input_var=tk.StringVar())
        self.inputs['Technician'].grid(row=0, column=2, padx=5, pady=5)

        self.inputs['Lab'] = LabelInput(
            recordinfo, "Lab", input_class=ttk.Combobox, input_var=tk.StringVar(),
            input_args={"values": ["A", "B", "C", "D", "E"]}
        )
        self.inputs['Lab'].grid(row=1, column=0, padx=5, pady=5)

        self.inputs['Plot'] = LabelInput(
            recordinfo, "Plot", input_class=ttk.Combobox, input_var=tk.StringVar(),
            input_args={"values": list(map(str, range(1, 21)))}
        )
        self.inputs['Plot'].grid(row=1, column=1, padx=5, pady=5)

        self.inputs['Seed sample'] = LabelInput(
            recordinfo, "Seed sample", input_var=tk.StringVar())
        self.inputs['Seed sample'].grid(row=1, column=2, padx=5, pady=5)

        # Environment Information Section
        environmentinfo = tk.LabelFrame(self, text="Environment Information")
        environmentinfo.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.inputs['Equipment Fault'] = LabelInput(
            environmentinfo, "Equipment Fault", input_class=ttk.Checkbutton, input_var=tk.BooleanVar()
        )
        self.inputs['Equipment Fault'].grid(
            row=0, column=0, columnspan=3, padx=5, pady=5)

        self.reset()

    def reset(self):
        """Reset all input fields."""
        for widget in self.inputs.values():
            widget.set('')


class Application(tk.Tk):
    """Application root window"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("ABQ Data Entry Application")

        ttk.Label(self, text="ABQ Data Entry Application", font=(
            "TkDefaultFont", 16)).grid(row=0, padx=10, pady=5)

        self.recordform = DataRecordForm(self)
        self.recordform.grid(row=1, padx=10, pady=5)

        self.savebutton = ttk.Button(self, text="Save", command=self.save)
        self.savebutton.grid(sticky=tk.E, row=2, padx=10, pady=5)

        self.status = tk.StringVar(value="Ready")
        self.statusbar = ttk.Label(
            self, textvariable=self.status, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.grid(sticky=(tk.W + tk.E), row=3, padx=10, pady=5)

    def save(self):
        """Save data (currently just prints the values)."""
        data = {key: widget.get()
                for key, widget in self.recordform.inputs.items()}
        print("Saved Data:", data)
        self.status.set("Data saved successfully!")


if __name__ == "__main__":
    app = Application()
    app.mainloop()
