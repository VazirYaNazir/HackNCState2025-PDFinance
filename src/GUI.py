import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os
import main
import querymaker
import test
global_value = 1


def run_gui() -> None:
    
    def update_output(text):
        output_box.config(state=tk.NORMAL)  # Allow editing
        output_box.insert(tk.END, text + "\n")  # Add new text with a newline
        output_box.config(state=tk.DISABLED)  # Disable editing
        output_box.see(tk.END)

    def image_clicked():
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        pdf_to_move = main.File_Handler(path=file_path)
        pdf_to_move.move_file(file_path)
        if file_path == "":
            messagebox.showerror("Error","File was not uploaded.")
        else:
            messagebox.showinfo("Success","File uploaded successfully")
            file_words = file_path.split("/")
            file_name = file_words[-1]
            update_output(file_name + " " + "uploaded successfully")

    def submit_broadness(value=None):
        global global_value
        value = broadness_entry.get().strip()
        global_value = value
        if value == "":
            pass
        if value.isdigit():
            update_output(f"Broadness set to: {value}")
            broadness_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Invalid Input", "Please enter a numerical value.")

    def submit_text(event = None):
        userInput = textEntry.get()
        if userInput == "":
            pass
        else:
            test.generatevectors()
            update_output(querymaker.askPrompt(userInput, global_value))
            textEntry.delete(0,tk.END)

    fontName = "Times New Roman"

    window = tk.Tk()
    window.geometry("1000x1000")
    window.title('PDFinance PDF Analysis Tool')
    window.configure(bg = "lightgray")

    label = tk.Label(window, text = "Welcome to PDFinance PDF Analysis Tool\nUpload a PDF and enter your question!", font = (fontName, 18), background="lightgray")
    label.pack(padx = 30, pady = 30)

    FileUploadDescription = tk.Label(window, text = "Click the button below and upload your PDFs.", font = (fontName, 16), background = "lightgray")
    FileUploadDescription.pack(pady = 10)

    current_dir = os.path.dirname(__file__)
    image_path = os.path.join(current_dir, "..", "images", "image-removebg-preview.png")
    image = tk.PhotoImage(file=image_path)

    PDFbutton = tk.Button(window, image=image, command = image_clicked, width = 200, height = 200)
    PDFbutton.pack(pady = 15)

    QnDescription = tk.Label(window, text = "Enter your query here!", font = (fontName, 16), background="lightgray")
    QnDescription.pack()

    textEntry = tk.Entry(window, font = (fontName, 14), width = 100)
    textEntry.pack(pady = 10)

    SubmitButton = tk.Button(window, text = "Submit", font = (fontName, 14), anchor = "center", command = submit_text)
    SubmitButton.pack(pady = 20)

    output_frame = tk.Frame(window)
    output_frame.pack(pady = 20)

    output_box = tk.Text(output_frame, font = (fontName, 14), wrap = "word", state = tk.DISABLED, background = "lightgray", width = 100)
    output_box.pack(side = "left", fill = "both", expand = True)

    scrollbar = tk.Scrollbar(output_frame, command = output_box.yview)
    scrollbar.pack(side = "right", fill = "y")

    output_box.config(yscrollcommand=scrollbar.set)

    sidebar_width = 200
    sidebar = tk.Frame(window, bg="blue", width=sidebar_width, height=800)
    sidebar.place(x=927, y=0)

    broadness_label = tk.Label(sidebar, text="Broadness", bg="blue", fg="white", font=(fontName, 14, "bold"))
    broadness_label.pack(pady=15)

    broadness_entry = tk.Entry(sidebar, font=(fontName, 12), width=10, justify="center")
    broadness_entry.pack(pady=5)

    broadness_submit = tk.Button(sidebar, text="Set", font=(fontName, 12), command=submit_broadness)
    broadness_submit.pack(pady=5)

    window.bind("<Return>",submit_text)

    window.mainloop()