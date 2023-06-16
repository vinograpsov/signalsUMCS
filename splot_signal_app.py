import tkinter as tk 
from tkinter import filedialog, OptionMenu, StringVar, Canvas, Scrollbar, Frame
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import own_splot as splot
import os

class Application:
    def __init__(self, root):
        self.root = root
        self.file1 = None 
        self.file2 = None
        self.figures = {}

        root.geometry("1020x500")

        self.button1 = tk.Button(root, text = "Choose first file", command = self.choose_file1)
        self.button1.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.button2 = tk.Button(root, text = "Choose second file", command = self.choose_file2)
        self.button2.grid(row = 0, column = 1, padx = 10, pady = 10)

        self.button3 = tk.Button(root, text = "SPLOT !!!", command = self.splot)
        self.button3.grid(row = 0, column = 2, padx = 10, pady = 10)

        self.canvas1 = self.create_scrollable_canvas(root, 3, 0)
        self.canvas2 = self.create_scrollable_canvas(root, 3, 1)
        self.canvas3 = self.create_scrollable_canvas(root, 3, 2)

        self.from1 = tk.Entry(root)
        self.from1.insert(0, "From")
        self.from1.grid(row = 1, column = 0, padx= 5 , pady = 5)
        self.from1.bind("<FocusIn>", self.clear_entry)
        self.from1.bind("<FocusOut>", self.restore_entry)
        
        self.from2 = tk.Entry(root)
        self.from2.insert(0, "From")
        self.from2.grid(row = 1, column = 1, padx= 5 , pady = 5)
        self.from2.bind("<FocusIn>", self.clear_entry)
        self.from2.bind("<FocusOut>", self.restore_entry)

        self.to1 = tk.Entry(root)
        self.to1.insert(0, "To")
        self.to1.grid(row = 2, column = 0, padx= 5 , pady = 5)
        self.to1.bind("<FocusIn>", self.clear_entry)
        self.to1.bind("<FocusOut>", self.restore_entry)
        
        self.to2 = tk.Entry(root)
        self.to2.insert(0, "To")
        self.to2.grid(row = 2, column = 1, padx= 5 , pady = 5)
        self.to2.bind("<FocusIn>", self.clear_entry)
        self.to2.bind("<FocusOut>", self.restore_entry)
        





        root.mainloop()

    def choose_file1(self):
        self.file1 = filedialog.askopenfilename(filetypes = (("CSV Files", "*.csv"),))
        if self.file1:
            self.create_plot(self.file1, self.canvas1,1)

    def choose_file2(self):
        self.file2 = filedialog.askopenfilename(filetypes = (("CSV Files", "*.csv"),))    
        if self.file1:
            self.create_plot(self.file2, self.canvas2,2)

    def splot(self):
        if self.file1 and self.file2:
            canvas = self.canvas3

            from1, to1 = self.get_range(self.from1, self.to1)
            from2, to2 = self.get_range(self.from2, self.to2)

            df1 = pd.read_csv(self.file1, sep=';', header=None).iloc[from1:to1,:] 
            df2 = pd.read_csv(self.file2, sep=';', header=None).iloc[from2:to2,:]


            if df1.shape[1] == df2.shape[1]:

                fig, axs = plt.subplots(df1.shape[1], 1, figsize=(3, 3 * df1.shape[1])) 
                plt.subplots_adjust(hspace=0.5)
                
                if df1.shape[1] == 1:
                    axs = [axs]
                    
                for i in range (df1.shape[1]):
                    signal1 = df1.iloc[:,i]
                    signal2 = df2.iloc[:,i]
                    result = splot.splot(signal1, signal2)

                    ax = axs[i]
                    ax.plot(range(len(result)), result)
                    ax.set_title(f"Splot part {i + 1}")
                    
                    if canvas in self.figures:
                        self.figures[canvas].get_tk_widget().pack_forget()
                        self.figures[canvas] = None

                    plot_canvas = FigureCanvasTkAgg(fig, master=canvas)
                    plot_canvas.draw()
                    plot_canvas.get_tk_widget().pack()
                    self.figures[canvas] = plot_canvas                                        


                    filename1 = os.path.basename(self.file1)[:-4]
                    filename2 = os.path.basename(self.file2)[:-4]

                    pd.DataFrame(result).to_csv(f"splot_{filename1}_{filename2}.csv", sep=';', header=None, index=False)

            else:
                print("ahahahahhaha man")


    def create_plot(self, path, canvas, signal_nr):

        if signal_nr == 1:
            from1, to1 = self.get_range(self.from1, self.to1)
        else:
            from1, to1 = self.get_range(self.from2, self.to2)

        df = pd.read_csv(path, sep=';', header=None).iloc[from1:to1,:]
        signals_count = df.shape[1]
        fig, axs = plt.subplots(signals_count, 1, figsize=(3, 3 * signals_count)) 
        
        if signals_count == 1:
            axs = [axs]

        for i in range(signals_count):
            ax = axs[i]
            ax.plot(df.index, df[i])
            ax.set_title(f"Signal part {i + 1}")
        
        fig.tight_layout()

        if canvas in self.figures:
            self.figures[canvas].get_tk_widget().pack_forget()
        
        plot_canvas = FigureCanvasTkAgg(fig, master=canvas)
        plot_canvas.draw()
        plot_canvas.get_tk_widget().pack()
        self.figures[canvas] = plot_canvas


    def get_range(self, from_entry, to_entry):
        try:
            from_value = int(from_entry.get())
            to_value = int(to_entry.get())
            return from_value, to_value
        except ValueError:
            return None, None
        

    def restore_entry(self, event):
        entry = event.widget
        if entry.get() == "":
            if entry == self.from1 or entry == self.from2:
                entry.insert(0, "From")
            elif entry == self.to1 or entry == self.to2:
                entry.insert(0, "To")


    def clear_entry(self, event):
        entry = event.widget
        if entry.get() == "From" or entry.get() == "To":
            entry.delete(0, tk.END)



    def create_scrollable_canvas(self, root, row, column):
        frame = Frame(root)
        frame.grid(row = row, column = column, padx = 10, pady = 10)
        frame.grid_propagate(False)

        canvas = Canvas(frame, bg = "lightsteelblue2", width = 300, height = 300)
        canvas.pack(side = "left")

        scrollbar = Scrollbar(frame, orient = "vertical", command = canvas.yview)
        scrollbar.pack(side = "right", fill = "y")

        canvas.configure(yscrollcommand = scrollbar.set)

        frame_plot = Frame(canvas)
        canvas.create_window((0, 0), window = frame_plot, anchor = "nw")

        frame_plot.bind("<Configure>", lambda event, canvas = canvas: canvas.configure(scrollregion = canvas.bbox("all")))

        return frame_plot


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()