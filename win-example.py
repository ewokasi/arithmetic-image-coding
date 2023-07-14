import tkinter
from tkinter import  *
import tkinter.messagebox
import customtkinter
import alg_source
import to_base64
import os
from customtkinter import filedialog
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.Work_Path="Empty"
        self.sep_counter=9
        # configure window
        self.title("Арифметическое кодирование")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Действия", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.compress_button = customtkinter.CTkButton(self.sidebar_frame, command=self.compression ,text="Закодировать")
        self.compress_button.grid(row=1, column=0, padx=20, pady=10)
        self.decompress_button = customtkinter.CTkButton(self.sidebar_frame, command=self.decompression, text="Раскодировать")
        self.decompress_button.grid(row=2, column=0, padx=20, pady=10)
        
       

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text=self.Work_Path )
        self.entry.configure(state="normal")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.explorer_button = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text= "Open",command=self.open_explorer)
        self.explorer_button.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")


        # create slider
        
        self.slider_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_frame.grid(row=2, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_frame.grid_columnconfigure(0, weight=1)
        self.slider_frame.grid_rowconfigure(4, weight=1)
        #=================================
        self.slider = customtkinter.CTkSlider(self.slider_frame, from_=1, to=13, number_of_steps=13, command= self.slider_count)
        self.counter_label = customtkinter.CTkLabel(self.slider_frame, text="separator counter: "+ str(self.sep_counter))
        self.counter_label.grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
    
        self.textbox.insert("0.0", "log info" )
       

    def slider_count(self, val):
        self.sep_counter=int(val)
        self.counter_label.configure(text="separator counter: "+str(int(val)))
    
    def open_explorer(self):
        self.Work_Path = str(filedialog.askopenfilename())
        
        print(self.Work_Path)
        self.entry.delete(0, END)
        self.entry.insert(0,string =self.Work_Path)

    def compression(self):
        self.textbox.insert("0.0","in progress\n")
        to_compress=to_base64.to_64(self.Work_Path)
       
        alg_source.long_compression(str(to_compress), self.sep_counter)
        stats_data = os.stat('pure_data.json')
        stats_prob = os.stat('pure_prob.json')
        stats_start = os.stat(self.Work_Path)
        self.textbox.insert("0.0", f'filename {self.Work_Path}\n')
        self.textbox.insert("0.0", f"compression done with separator counter {int(self.sep_counter)}"+'\n')
        self.textbox.insert("0.0", f'total data size is {stats_data.st_size}\n')
        self.textbox.insert("0.0", f'total prob size is {stats_prob.st_size}\n')
        self.textbox.insert("0.0", f'start image size is {stats_start.st_size}\n')
        self.textbox.insert("0.0", f'data biger x{(stats_data.st_size)/stats_start.st_size} times\n')
        self.textbox.insert("0.0", '--------------------------------\n\n')

    def decompression(self):
        path = str(filedialog.askdirectory())
        alg_source.uncode_pure(f"{path}//pure_data.json", f"{path}//pure_prob.json")
        res = alg_source.long_decompression("recovered_from_pure.json")
        tt = str(res).replace("b'","")
        tt = tt.replace("'","")
        with open("recovered.png", "wb") as fh:
                fh.write(to_base64.base64.b64decode(str(tt)))
                fh.close()
        #print(res)
        self.textbox.insert("0.0", '--------------------------------\n\n')
        self.textbox.insert("0.0", 'decompressed\n\n')
        self.textbox.insert("0.0", '--------------------------------\n\n')


        

if __name__ == "__main__":
    app = App()
    
    app.mainloop()