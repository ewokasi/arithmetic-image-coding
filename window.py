import customtkinter
from customtkinter import filedialog
import alg_source
import to_base64

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("400x240")


def compression():
    Work_Path = to_base64.to_64(filedialog.askopenfilename())
    alg_source.long_compression(str(Work_Path))

def decompression():
     
    alg_source.uncode_pure("pure_data.json", "pure_prob.json")
    res = alg_source.long_decompression("recovered_from_pure.json")
    tt = str(res).replace("b'","")
    tt = tt.replace("'","")
    with open("recovered.png", "wb") as fh:
            fh.write(to_base64.base64.b64decode(str(tt)))
            fh.close()
    print(res)

# Use CTkButton instead of tkinter Button
pack_button = customtkinter.CTkButton(master=app, text="Архивировать", command=compression)
unpack_button = customtkinter.CTkButton(master=app, text="Распаковать", command=decompression)
pack_button.place(relx=0.5, rely=0.2, anchor=customtkinter.CENTER)
unpack_button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)


if __name__=="__main__":

    app.mainloop()
