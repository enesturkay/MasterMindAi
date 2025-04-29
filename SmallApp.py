import time

import mysql.connector
import customtkinter

import mysql.connector

mycursor = db.cursor()

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("200x200")
        self.wm_iconbitmap('logom.ico')
        self.title('MasterMindAi - Kolay Ekle')
        self.configure(fg_color="#212121")
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight = 3)
        self.rowconfigure(1,weight = 3)
        self.rowconfigure(2,weight = 3)
        self.resizable(False, False)
        self.attributes("-topmost", True)


        self.EnglishEntryCheck = customtkinter.StringVar(value = "İngilizce")
        self.EnglishEntry  = customtkinter.CTkEntry(self,placeholder_text="İngilizce",fg_color="#474A4C",width=50,text_color="white",corner_radius=9,placeholder_text_color="white",font=('Cascadia Mono Semibold',13),textvariable=self.EnglishEntryCheck)
        self.EnglishEntry.grid(row = 0 ,column =0,sticky="we",padx=10)
        self.TurkishEntryCheck = customtkinter.StringVar(value="Türkçe")
        self.TurkishEntry = customtkinter.CTkEntry(self, placeholder_text="Türkçe", fg_color="#474A4C", width=50,text_color="white", corner_radius=9, placeholder_text_color="white",font=('Cascadia Mono Semibold',13),textvariable=self.TurkishEntryCheck)
        self.TurkishEntry.grid(row=1, column=0, sticky="we", padx=10 )
        self.MoreButton = customtkinter.CTkButton(self,text="Kelime Ekle",corner_radius=34 ,fg_color="#582233",hover_color="#3F1825",width=150,font=("Cascadia Mono Semibold",13),hover=True,cursor="hand2",command=self.AddDataBase)
        self.MoreButton.grid(row=2,column=0)
        self.TurkishEntry.bind("<FocusIn>", self.on_focus_in_Turkish)
        self.TurkishEntry.bind("<FocusOut>", self.on_focus_out_Turkish)
        self.EnglishEntry.bind("<FocusIn>", self.on_focus_in_English)
        self.EnglishEntry.bind("<FocusOut>",self.on_focus_out_English)
        self.bind("<ButtonPress>", self.make_opaque)

        # Başlangıçta zamanlayıcıyı başlat
        self.timer = self.after(5000, self.make_transparent)

    def make_opaque(self, event=None):
        self.attributes("-alpha", 1.0)  # %100 görünür yap
        self.reset_timer()

    def make_transparent(self):
        self.attributes("-alpha", 0.5)

    def reset_timer(self):
        self.after_cancel(self.timer)
        self.timer = self.after(5000, self.make_transparent)
    def AddDataBase(self):
        sqlQuery = "INSERT INTO forapptable (English,Turkish ) VALUES (%s, %s)"
        val = (self.EnglishEntryCheck.get().lower(),self.TurkishEntryCheck.get().lower())
        mycursor.execute("SELECT 1 FROM forapptable  WHERE English = %s", (val[0],))
        sonuc = mycursor.fetchone()
        if val[0] == "" or val[1] =="" or val[0] == "ingilizce" or val[1] == "türkçe":
            return
        if sonuc:
            self.EnglishEntry.configure(text_color="Red")
            self.TurkishEntryCheck.set(value="Kelime Kayıtlı")
            self.after(2000, lambda: self.EnglishEntry.configure(text_color="white"))
            return
        mycursor.execute(sqlQuery,val)
        db.commit()
        self.TurkishEntryCheck.set("")
        self.EnglishEntryCheck.set("")

    def on_focus_in_Turkish(self,event):
        if self.TurkishEntryCheck.get() == "Türkçe":
            self.TurkishEntryCheck.set("")

    def on_focus_out_Turkish(self,event):
        if self.TurkishEntryCheck.get() == "":
            self.TurkishEntryCheck.set("Türkçe")
        self.focus()
    def on_focus_in_English(self,event):
        if self.EnglishEntryCheck.get() == "İngilizce":
            self.EnglishEntryCheck.set("")

    def on_focus_out_English(self,event):
        if self.EnglishEntryCheck.get() == "":
            self.EnglishEntryCheck.set("İngilizce")


app = App()
app.mainloop()