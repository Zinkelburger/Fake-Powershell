import tkinter as tk
from tkinter import scrolledtext
import subprocess

RECOGNIZED_CMDLETS = ["get", "set", "clear", "new", "add", "remove"]

def execute_command():
    # Extract the command input after the prompt
    command = output_box.get("prompt_end", "input_end").strip()

    # Handle the 'clear' command separately
    if command.lower() == "clear":
        output_box.delete(1.0, tk.END)
        display_prompt()
        return

    try:
        result = subprocess.run(["powershell", "-Command", command], text=True, capture_output=True)

        # Display stdout
        if result.stdout:
            output_box.insert("input_end", '\n' + result.stdout)
            output_box.mark_set("input_end", tk.INSERT)

        # Display stderr
        if result.stderr:
            start_index = output_box.index("input_end+1c linestart")
            output_box.insert("input_end", '\n' + result.stderr)
            end_index = output_box.index(tk.INSERT)
            output_box.tag_add("error", start_index, end_index)
            output_box.tag_configure("error", foreground="red", background="black")
            output_box.mark_set("input_end", tk.INSERT)

        # Insert a newline for separation
        output_box.insert(tk.END, '\n')

    except Exception as e:
        start_index = output_box.index("input_end+1c linestart")
        output_box.insert(tk.END, str(e) + '\n')
        end_index = output_box.index(tk.END + "-1c")
        output_box.tag_add("error", start_index, end_index)
        output_box.tag_configure("error", foreground="red", background="black")

    display_prompt()

def display_prompt():
    # Insert the prompt.
    output_box.insert(tk.END, "PS C:\\Users\\Administrator> ")
    output_box.mark_set("prompt_end", "end-2c lineend")
    output_box.mark_set("input_end", tk.END)
    output_box.mark_gravity("prompt_end", "left")
    output_box.see(tk.END)


def on_enter_key(event):
    first_word = output_box.get("prompt_end", "prompt_end wordend").strip()
    if first_word.lower() in RECOGNIZED_CMDLETS:
        output_box.tag_add("cmdlet", "prompt_end", "prompt_end wordend")
        output_box.tag_configure("cmdlet", foreground="yellow")

    execute_command()
    return 'break'

def enforce_prompt_readonly(event):
    if event.keysym == "BackSpace" and output_box.compare(tk.INSERT, "<=", "prompt_end"):
        return 'break'
    elif event.keysym in ["Left", "Right", "Up", "Down"] and output_box.compare(tk.INSERT, "<=", "prompt_end"):
        return 'break'
    elif output_box.compare(tk.INSERT, "<=", "prompt_end"):
        output_box.mark_set(tk.INSERT, "input_end")
    else:
        output_box.mark_set("input_end", tk.INSERT)

root = tk.Tk()
root.title("Administrator: Windows PowerShell")
root.iconbitmap('powershell.ico')
root.configure(bg='#012456')

output_box = scrolledtext.ScrolledText(root, bg='#012456', fg='white', wrap=tk.WORD, font=("Consolas", 10), borderwidth=0, relief="flat", insertbackground='white', insertwidth=8)
output_box.pack(fill=tk.BOTH, expand=True)
output_box.bind('<Return>', on_enter_key)
output_box.bind('<KeyPress>', enforce_prompt_readonly)

output_box.insert(tk.END, "Windows PowerShell\nCopyright (C) Microsoft Corporation. All rights reserved.\n\n")
display_prompt()

root.mainloop()
