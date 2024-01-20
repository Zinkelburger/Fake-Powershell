import tkinter as tk
from tkinter import scrolledtext
import subprocess

def execute_command():
    command = output_box.get("prompt_end", "input_end").strip()
    if command.lower() == "clear":
        output_box.delete(1.0, tk.END)
        display_prompt()
        return

    docker_command = f"docker exec powershell-container powershell -Command {command}"
    try:
        result = subprocess.run(docker_command, shell=True, text=True, capture_output=True)
        if result.stdout:
            output_box.insert("input_end", '\n' + result.stdout)
            output_box.mark_set("input_end", tk.INSERT)

        if result.stderr:
            start_index = output_box.index("input_end+1c linestart")
            output_box.insert("input_end", '\n' + result.stderr)
            format_stderr(result.stderr, start_index)
            output_box.mark_set("input_end", tk.INSERT)

        if not result.stdout and not result.stderr:
            output_box.insert("input_end", '\n')
    except Exception as e:
        start_index = output_box.index("input_end+1c linestart")
        output_box.insert(tk.END, str(e) + '\n')
        end_index = output_box.index(tk.END + "-1c")
        output_box.tag_add("error", start_index, end_index)

    display_prompt()

def format_stderr(stderr_text, start_index):
    lines = stderr_text.split('\n')
    for line in lines:
        # Mark everything up to the newline (or end of the line) with the error tag
        end_of_content = output_box.search('\n', start_index, stopindex=tk.END) or output_box.index(f"{start_index} lineend")
        output_box.tag_add("error", start_index, end_of_content)

        # If there's a newline, mark the rest of the line with the blue_background tag
        if output_box.get(end_of_content) == '\n':
            line_end = output_box.index(f"{end_of_content} lineend")
            output_box.tag_add("blue_background", end_of_content, line_end)

        # Move to the next line
        start_index = f"{line_end}+1c"

def display_prompt():
    output_box.insert(tk.END, "PS C:\\Users\\Administrator> ")
    output_box.mark_set("prompt_end", "end-2c lineend")
    output_box.mark_set("input_end", tk.END)
    output_box.mark_gravity("prompt_end", "left")
    output_box.see(tk.END)

def on_enter_key(event):
    output_box.tag_remove("first_word", "input_end", "input_end")
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
    color_first_word(event) 

def color_first_word(event):
    output_box.tag_remove("first_word", "prompt_end", "input_end")
    
    first_word_end = output_box.search(" ", "prompt_end", "input_end", regexp=True) or output_box.search("\n", "prompt_end", "input_end")
    
    if not first_word_end:
        first_word_end = output_box.index("input_end")
    
    output_box.tag_add("first_word", "prompt_end", first_word_end)
    output_box.tag_configure("first_word", foreground="yellow")

root = tk.Tk()
root.title("Administrator: Windows PowerShell")
bg_color = '#012456'
cursor_color = '#fedcba'
root.configure(bg=bg_color)
root.iconbitmap('powershell.ico')
output_box = scrolledtext.ScrolledText(
    root, 
    bg=bg_color, 
    fg='white', 
    wrap=tk.WORD, 
    font=("Consolas", 10),
    borderwidth=0,
    relief="flat",
    insertbackground=cursor_color,
    insertwidth=7,
    insertontime=0,
    insertofftime=0
)
output_box.pack(fill=tk.BOTH, expand=True)
output_box.bind('<Return>', on_enter_key)
output_box.bind('<KeyPress>', enforce_prompt_readonly)
output_box.bind('<KeyRelease>', color_first_word)
output_box.insert(tk.END, "Windows PowerShell\nCopyright (C) Microsoft Corporation. All rights reserved.\n\n")
display_prompt()
output_box.tag_configure("error", foreground="red", background="black")
output_box.tag_configure("blue_background", background="blue")
root.mainloop()
