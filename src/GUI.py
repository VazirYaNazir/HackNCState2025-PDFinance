import tkinter as tk
from tkinter import filedialog, messagebox
import ttkthemes
import shutil
import os
import images

def run_gui() -> None:

    def submit_text(event = None):
        userInput = textEntry.get()
        if userInput == "":
            pass
        else:
            print(userInput) #REPLACE THIS WITH THE FUNCTION THAT WILL TAKE THE PROMPT
            textEntry.delete(0,tk.END)

    def image_clicked():
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])

        # movefile(file_path)
        messagebox.showinfo("Success","File uploaded successfully")

    fontName = "Times New Roman"


    window = tk.Tk()
    window.geometry("1000x1000")
    window.title('JMM Financial PDF Analysis')
    window.configure(bg = "lightgray")

    label = tk.Label(window, text = "Welcome to JMM Financial PDF Analysis\nUpload a PDF and enter your question!", font = (fontName, 18), background="lightgray")
    label.pack(padx = 30, pady = 30)

    FileUploadDescription = tk.Label(window, text = "Click the button below and upload your PDFs.", font = (fontName, 16), background = "lightgray")
    FileUploadDescription.pack(pady = 10)

    image = tk.PhotoImage(file="place_holder")

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
    window.bind("<Return>",submit_text)
    window.mainloop()