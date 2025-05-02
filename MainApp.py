import time
import customtkinter
import mysql.connector
from PIL import Image
import ollama
import threading
from datetime import datetime



db = mysql.connector.connect(

)
mycursor = db.cursor()
ColorBg = "#181818"
ColorFrame = "#212121"
ColorButton = "#582233"
ColorButtonHover= "#3F1825"
ColorEntry = "#474A4C"
class AISettings(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color=ColorBg

)
        self.columnconfigure(0,weight=5)
        self.columnconfigure(1,weight=5)
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=2)
        self.rowconfigure(3, weight=2)
        self.rowconfigure(4, weight=2)
        self.rowconfigure(5,weight=1)
        self.rowconfigure(6,weight=1)
        self.rowconfigure(7,weight=1)
        customtkinter.CTkLabel(self,text="Yapay Zeka Ayarları",font=("Cascadia Mono Semibold",16),justify="center").grid(row=0,column=0,sticky="nswe",columnspan=2)
        customtkinter.CTkLabel(self,text="Hikaye Seviyesi",font=("Cascadia Mono Semibold",16),justify="center").grid(row=1,column=0)
        mycursor.execute( "SELECT english_level,hobby1,hobby2,hobby3,MaksWordCount from profilesettings where id = 1")
        self.result = mycursor.fetchall()
        db.commit()
        self.englishLevelChecked = customtkinter.StringVar(value=self.result[0][0])
        self.englishLevel = customtkinter.CTkComboBox(self, values=["A1", "A2", "B1", "B2", "C1", "C2"],state="readonly",variable=self.englishLevelChecked,command=self.ChangeLevel)
        self.englishLevelChecked.set(self.result[0][0])
        self.englishLevel.grid(row=1,column=1)
        customtkinter.CTkLabel(self, text="1.İlgi Alanı", font=("Cascadia Mono Semibold", 16),
                               justify="center").grid(row=2, column=0)
        customtkinter.CTkLabel(self, text="2.İlgi Alanı", font=("Cascadia Mono Semibold", 16),
                               justify="center").grid(row=3, column=0)
        customtkinter.CTkLabel(self, text="3.İlgi Alanı", font=("Cascadia Mono Semibold", 16),
                               justify="center").grid(row=4, column=0)
        self.HobbyOneChecked = customtkinter.StringVar(value=self.result[0][1])
        self.HobbyTwoChecked = customtkinter.StringVar(value=self.result[0][2])
        self.HobbyTreeChecked = customtkinter.StringVar(value=self.result[0][3])
        self.HobbyOne = customtkinter.CTkEntry(self,textvariable=self.HobbyOneChecked)
        self.HobbyTwo = customtkinter.CTkEntry(self,textvariable=self.HobbyTwoChecked)
        self.HobbyTree = customtkinter.CTkEntry(self,textvariable=self.HobbyTreeChecked)
        self.HobbyOne.grid(row=2,column=1)
        self.HobbyTwo.grid(row=3,column=1)
        self.HobbyTree.grid(row=4,column=1)
        customtkinter.CTkLabel(self, text="Pratik Ayarları", font=("Cascadia Mono Semibold", 16),
                              justify="center").grid(row=5, column=0, sticky="nswe", columnspan=2)
        customtkinter.CTkLabel(self, text="Maksimum Kelime", font=("Cascadia Mono Semibold", 16),
                               justify="center").grid(row=6, column=0)
        self.PracticeCountChecked = customtkinter.IntVar(value = self.result[0][4])
        self.PracticeCount = customtkinter.CTkEntry(self,textvariable=self.PracticeCountChecked)
        self.PracticeCount.grid(row=6, column=1)
        saveButton = customtkinter.CTkButton(self, text="Değiştir", corner_radius=34, fg_color=ColorButton , hover_color=ColorButtonHover,width=150, font=("Cascadia Mono Semibold", 13), hover=True, cursor="hand2",command=self.Submit)
        saveButton.grid(row=7,column=0,columnspan=2)



    def Submit(self):
        if self.HobbyOne.get() != self.result[0][1]:
            query = "UPDATE profilesettings SET Hobby1 = %s WHERE id = 1"
            mycursor.execute(query,(self.HobbyOne.get(),))
        if self.HobbyTwo.get() != self.result[0][2]:
            query = "UPDATE profilesettings SET Hobby2 = %s WHERE id = 1"
            mycursor.execute(query,(self.HobbyTwo.get(),))
        if self.HobbyTree.get() != self.result[0][3]:
            query = "UPDATE profilesettings SET Hobby3 = %s WHERE id = 1"
            mycursor.execute(query,(self.HobbyTree.get(),))
        try:
            number = int(self.PracticeCount.get())
        except ValueError:
            return
        if self.PracticeCount.get() != self.result[0][4] and int(self.PracticeCount.get()) > 0:
            query = "UPDATE profilesettings SET MaksWordCount = %s WHERE id = 1"
            mycursor.execute(query, (self.PracticeCount.get(),))


    def ChangeLevel(self,choice):
        query = "UPDATE profilesettings SET english_level = %s WHERE id=1"
        mycursor.execute(query,(choice,))
        db.commit()

class OpenSettings(customtkinter.CTkToplevel):
    def __init__(self,master):
        super().__init__(master)
        self.title("Kullanıcı Ayarları")
        self.geometry("400x600")
        self.after(300, self.set_icon)
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.configure(fg_color=ColorFrame)
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        self.AiSettings = AISettings(self)
        self.AiSettings.grid(row=0,column = 0,sticky="nswe",padx=14,pady=14)


    def set_icon(self):
        self.iconbitmap("logom.ico")


class TLPracticeWord(customtkinter.CTkToplevel):
    def __init__(self,master):
        super().__init__(master)
        self.title("Kelime Pratiği")
        self.geometry("400x600")
        self.after(300, self.set_icon)
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=2)
        self.rowconfigure(3,weight=0)
        self.rowconfigure(4,weight = 0)
        self.rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.configure(fg_color=ColorFrame)
        time = datetime.now().date()
        mycursor.execute("SELECT MaksWordCount FROM profilesettings WHERE id=1")
        resultCount = mycursor.fetchone()
        db.commit()
        self.Kalan = resultCount[0]
        sql = "SELECT English,Turkish,AdAi,Repeats FROM forapptable WHERE Checked < %s LIMIT %s"
        mycursor.execute(sql, (time,self.Kalan,))
        self.results = mycursor.fetchall()
        self.i = 0
        self.multiple = 0
        self.changed = self.results[self.i][2]
        self.EntryOneChecked = customtkinter.StringVar(value=self.results[self.i][0])
        self.EntryOne = customtkinter.CTkEntry(self,state="disabled",textvariable=self.EntryOneChecked,fg_color=ColorEntry,text_color="white",font=("Cascadia Mono Semibold",16),justify="center",border_color="white",border_width=2)
        self.EntryOne.grid(row= 0,column = 0,columnspan = 3,sticky="nswe",padx=30,pady=15)
        profile_img_pil = Image.open("swap.png")
        profile_img = customtkinter.CTkImage(light_image=profile_img_pil, size=(32, 32))
        self.switched = False
        self.switch = customtkinter.CTkButton(self, image=profile_img, text="", fg_color="transparent",hover=False,cursor="hand2",width=10,height=10,anchor="center",command=self.Switch)
        self.switch.grid(row=1,column=0,sticky="nswe",columnspan=3)
        self.EntryTwoChecked = customtkinter.StringVar(value="")
        self.EntryTwoBTN = customtkinter.CTkButton(self,textvariable=self.EntryTwoChecked,cursor="hand2",fg_color=ColorEntry,text_color="white",hover_color="#3E4142",font=("Cascadia Mono Semibold",16),command=self.Show,border_color="white",border_width=2)
        self.EntryTwoBTN.grid(row= 2,column = 0,columnspan = 3,sticky="nswe",padx=30,pady=15)
        self.ButtonFrame = customtkinter.CTkFrame(self)
        self.ButtonFrame.grid(row = 3,column=0,padx=10,pady=15)
        self.ButtonFrame.grid_columnconfigure(0, weight=1)
        self.ButtonFrame.grid_columnconfigure(1, weight=1)
        self.ButtonFrame.grid_columnconfigure(2, weight=1)
        self.ButtonFrame.configure(fg_color=ColorFrame)
        self.GoodButton = customtkinter.CTkButton(self.ButtonFrame, corner_radius=20,fg_color="#529E6C", text="İyi",font=("Cascadia Mono Semibold", 13), hover=False, cursor="hand2",height=35,command=self.ScaleGoodButton)
        self.GoodButton.grid(row=0,column=0,padx=10)
        self.MedButton = customtkinter.CTkButton(self.ButtonFrame, text="Orta",
                                                  font=("Cascadia Mono Semibold", 13), hover=False, cursor="hand2",height=35,corner_radius=20,fg_color="#C75C25",command=self.ScaleMidButton)
        self.MedButton.grid(row=0, column=1)
        self.BadButton = customtkinter.CTkButton(self.ButtonFrame, corner_radius=20,fg_color="#DF3C28", text="Kötü",
                                                  font=("Cascadia Mono Semibold", 13), hover=False, cursor="hand2",height=35,command=self.ScaleBadButton)
        self.BadButton.grid(row=0, column=2,padx=10)
        self.ButtonsTwoFrame = customtkinter.CTkFrame(self)
        self.ButtonsTwoFrame.grid(row=4,column=0,columnspan=3,pady=15)
        self.ButtonsTwoFrame.grid_columnconfigure(0, weight=1)
        self.ButtonsTwoFrame.grid_columnconfigure(1, weight=1)
        self.ButtonsTwoFrame.configure(fg_color=ColorFrame)
        self.AddAiStoryCheck = customtkinter.StringVar()
        self.AddAiText()
        self.AddAiStory = customtkinter.CTkButton(self.ButtonsTwoFrame,fg_color=ColorBg

,font=("Cascadia Mono Semibold",13),hover=False,cursor="hand2",height=34,command=self.AddAi,textvariable=self.AddAiStoryCheck)
        self.AddAiStory.grid(row=0, column=0, padx=10)
        self.ChangeBtn = customtkinter.CTkButton(self.ButtonsTwoFrame, fg_color=ColorBg

, text="Düzenle",
                                                  font=("Cascadia Mono Semibold", 13), hover=False, cursor="hand2",
                                                  height=34,command=self.Change)
        self.ChangeBtn.grid(row=0, column=1, padx=10)
        self.EntryKalanCheck = customtkinter.StringVar(value=f"Kalan Kelime {self.Kalan-1}")
        self.EntryKalan = customtkinter.CTkEntry(self,textvariable=self.EntryKalanCheck,state="disabled",fg_color=ColorFrame,justify="center",font=("Cascadia Mono Semibold", 13))
        self.EntryKalan.grid(row=5,column=0,columnspan=3)
    def Change(self):
        def BtnChange():
            Eng = self.CheckEnglishİnput.get()
            Tr = self.CheckTurkishİnput.get()
            query = "UPDATE forapptable SET English = %s, Turkish = %s WHERE English = %s"
            val = (Eng,Tr,self.results[self.i][0])
            mycursor.execute(query,val)
            self.EntryOneChecked.set(value=Eng)
            self.EntryTwoChecked.set(value=Tr)
            db.commit()


        def set_icon():
            root.iconbitmap("logom.ico")
        root = customtkinter.CTkToplevel(self)
        root.geometry("300x300")
        root.resizable(False, False)
        root.attributes("-topmost", True)
        root.title('Değiştir')
        root.configure(fg_color=ColorFrame)
        root.after(300, set_icon)
        root.columnconfigure(0,weight=1)
        root.rowconfigure(0,weight=4)
        root.rowconfigure(1,weight=4)
        root.rowconfigure(2,weight=2)

        self.CheckEnglishİnput = customtkinter.StringVar(value=self.results[self.i][0])
        self.CheckTurkishİnput = customtkinter.StringVar(value=self.results[self.i][1])
        Englishİnput = customtkinter.CTkEntry(root, textvariable=self.CheckEnglishİnput, fg_color=ColorEntry, width=100,
                                              text_color="white", corner_radius=9, placeholder_text_color="white",
                                              font=('Cascadia Mono Semibold', 13))
        Englishİnput.grid(row=0, column=0, sticky="WE", padx=50, pady=50)
        Turkishİnput = customtkinter.CTkEntry(root, textvariable=self.CheckTurkishİnput, fg_color=ColorEntry, width=100,
                                              text_color="white", corner_radius=9, placeholder_text_color="white",
                                              font=('Cascadia Mono Semibold', 13))
        Turkishİnput.grid(row=1, column=0, sticky="WE", padx=50)
        ChangesBtn = customtkinter.CTkButton(root, text="Değiştir", corner_radius=34, fg_color=ColorButton ,
                                             hover_color=ColorButtonHover, width=150, font=("Cascadia Mono Semibold", 13),
                                             hover=True, cursor="hand2",command=BtnChange)
        ChangesBtn.grid(row=3, column=0, pady=50)
        root.mainloop()

    def AddAiText(self):
        if self.changed == 1:
            self.AddAiStoryCheck.set(value="Hikayeden Çıkar")
        else:
            self.AddAiStoryCheck.set(value="Hikayeye Ekle")
    def AddAi(self):
        if self.changed == 1:
            self.changed=0
            self.AddAiStoryCheck.set("Hikayeye Ekle")
        else:
            self.changed=1
            self.AddAiStoryCheck.set("Hikayeden Çıkar")
        query = f"UPDATE forapptable SET AdAi = {self.changed} WHERE English = %s"
        value = (self.results[self.i][0],)
        mycursor.execute(query,value)
        db.commit()
        self.AddAiStory.configure(fg_color="#3F7D58")
        self.after(500,lambda: self.AddAiStory.configure(fg_color=ColorBg

))

    def Switch(self):
        if self.EntryTwoChecked.get() !="":
            if self.switched== False:
                self.switched = True
            else:self.switched= False
            self.Show()
            if self.switched:
                self.EntryOneChecked.set(value=self.results[self.i][1])
            else:
                self.EntryOneChecked.set(value=self.results[self.i][0])
    def Show(self):
        if self.switched:
            self.EntryTwoChecked.set(value=self.results[self.i][0])
        else:
            self.EntryTwoChecked.set(value=self.results[self.i][1])
    def ScaleGoodButton(self):
        self.multiple = 2
        self.AfterRepeatSettings()
    def ScaleBadButton(self):
        self.multiple = 0.5
        self.AfterRepeatSettings()
    def ScaleMidButton(self):
        self.multiple = 1
        self.AfterRepeatSettings()
    def AfterRepeatSettings(self):
        if self.EntryTwoChecked.get() == "":
            return
        if self.Kalan > 0 :
            afterRepeatTime = 24*self.multiple*(self.results[self.i][3]+1)
            query = f"UPDATE forapptable SET Checked = DATE_ADD(NOW(),INTERVAL %s HOUR) WHERE English = %s"
            value = (afterRepeatTime,self.results[self.i][0],)
            mycursor.execute(query,value)
            db.commit()
            query = f"UPDATE forapptable SET Repeats = %s + 1 Where English =%s"
            value = (self.results[self.i][3],self.results[self.i][0])
            mycursor.execute(query,value)
            db.commit()
            self.NextFunc()
        else:
            self.destroy()


    def NextFunc(self):
        if self.EntryTwoChecked.get() !="":
            self.i = self.i+1
            if self.switched:
                self.EntryOneChecked.set(value=self.results[self.i][1])
            else:
                self.EntryOneChecked.set(value=self.results[self.i][0])
            self.EntryTwoChecked.set(value="")
            self.changed = self.results[self.i][2]
            self.AddAiText()
            self.Kalan = self.Kalan-1
            self.EntryKalanCheck.set(value =f"Kalan Kelime = {self.Kalan}")

    def set_icon(self):
        self.iconbitmap("logom.ico")
class TLRemainWordFrame(customtkinter.CTkScrollableFrame):
    def __init__(self,master,frame):
        super().__init__(master)
        self.frame = frame
        self.columnconfigure(0,weight = 1,minsize=200)
        self.columnconfigure(1,weight=1,minsize=200)
        self.columnconfigure(2,weight = 0)
        self.configure(fg_color=ColorBg

)
        customtkinter.CTkLabel(self,text="İngilizce",fg_color=ColorFrame,font=("Cascadia Mono Semibold",13),corner_radius=7,height=35).grid(row=0,column=0,sticky="NSWE",padx=1,pady=6)
        customtkinter.CTkLabel(self,text="Türkçe",fg_color=ColorFrame,font=("Cascadia Mono Semibold",13),corner_radius=7,height=35).grid(row=0,column=1,sticky="NSWE",padx=1,pady=6)
        self.NewData()
    def NewData(self):
        for widget in self.winfo_children():
            if widget.grid_info()["row"] > 0:
                widget.destroy()
        mycursor.execute("SELECT COUNT(id) FROM forapptable")
        row_count = mycursor.fetchone()[0]
        sqlQuest = "select English,Turkish from forapptable order by id DESC"
        mycursor.execute(sqlQuest)
        result = mycursor.fetchall()
        for i in range(row_count):
            colored = ColorFrame
            if i % 2 == 0:
                colored=ColorButtonHover
            self.EnglishWord = customtkinter.CTkLabel(self,text=result[i][0],fg_color=colored,font=("Cascadia Mono Semibold",12),corner_radius=5,width=25,cursor="hand2")
            self.EnglishWord.grid(row=i+1,column=0,sticky="NSWE",padx=1,pady=1)
            self.TurkishWord = customtkinter.CTkLabel(self,text=result[i][1],fg_color=colored,font=("Cascadia Mono Semibold",12),corner_radius=5,width=25)
            self.TurkishWord.grid(row=i+1,column=1,sticky="NSWE",padx=1,pady=1)
            self.EnglishWord.bind("<Button-1>",self.ClickedLabel )

    def ClickedLabel(self, event):
        clicked_label = event.widget
        text = clicked_label.cget("text")
        self.frame.CheckChoiceButton.set(text)
        return text
    def SearchNewData(self,event):
        for widget in self.winfo_children():
            if widget.grid_info()["row"] > 0:
                widget.destroy()
        sql = "SELECT English,Turkish FROM forapptable WHERE English LIKE %s"
        mycursor.execute(sql, (f"%{event}%",))
        result= mycursor.fetchall()
        for i in range(len(result)):
            colored = ColorFrame
            if i % 2 == 0:
                colored = ColorButtonHover
            self.EnglishWord = customtkinter.CTkLabel(self, text=result[i][0], fg_color=colored,
                                                      font=("Cascadia Mono Semibold", 12), corner_radius=5, width=25,
                                                      cursor="hand2")
            self.EnglishWord.grid(row=i + 1, column=0, sticky="NSWE", padx=1, pady=1)
            self.TurkishWord = customtkinter.CTkLabel(self, text=result[i][1], fg_color=colored,
                                                      font=("Cascadia Mono Semibold", 12), corner_radius=5, width=25)
            self.TurkishWord.grid(row=i + 1, column=1, sticky="NSWE", padx=1, pady=1)
            self.EnglishWord.bind("<Button-1>", self.ClickedLabel)
    def NewAiData(self):
        for widget in self.winfo_children():
            if widget.grid_info()["row"] > 0:
                widget.destroy()
        query = "SELECT English,Turkish from forapptable WHERE AdAi = 1"
        mycursor.execute(query)
        result = mycursor.fetchall()
        for i in range(len(result)):
            colored = ColorFrame
            if i % 2 == 0:
                colored = ColorButtonHover
            self.EnglishWord = customtkinter.CTkLabel(self, text=result[i][0], fg_color=colored,
                                                      font=("Cascadia Mono Semibold", 12), corner_radius=5,
                                                      width=25,
                                                      cursor="hand2")
            self.EnglishWord.grid(row=i + 1, column=0, sticky="NSWE", padx=1, pady=1)
            self.TurkishWord = customtkinter.CTkLabel(self, text=result[i][1], fg_color=colored,
                                                      font=("Cascadia Mono Semibold", 12), corner_radius=5,
                                                      width=25)
            self.TurkishWord.grid(row=i + 1, column=1, sticky="NSWE", padx=1, pady=1)
            self.EnglishWord.bind("<Button-1>", self.ClickedLabel)
class TopLevelFrameSettingsRecent(customtkinter.CTkFrame):
    def __init__(self,master,ScrollFrame):
        super().__init__(master)
        self.scrollFrame = ScrollFrame
        self.configure(fg_color=ColorFrame)
        self.columnconfigure(0,weight = 2,minsize = 40)
        self.columnconfigure(1,weight = 4,minsize = 100)
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight = 1)
        self.CheckChoiceButton =customtkinter.StringVar(value="Henüz seçilmedi")
        self.ChoiceButton = customtkinter.CTkButton(self,fg_color=ColorFrame,textvariable=self.CheckChoiceButton,font=("Cascadia Mono Semibold",13),hover=False)
        self.ChoiceButton.grid(row=0,column=0,padx=10)
        self.DeleteButton = customtkinter.CTkButton(self,fg_color=ColorBg

,text="Sil",font=("Cascadia Mono Semibold",13),hover=False,cursor="hand2",command=self.Delete)
        self.DeleteButton.grid(row=0,column = 1,padx=10)
        self.ChangeButton = customtkinter.CTkButton(self,fg_color=ColorBg

,text="Değiştir",font=("Cascadia Mono Semibold",13),hover=False,cursor="hand2",command=self.Changes)
        self.ChangeButton.grid(row=1,column = 1,padx=10)
        self.SearchEntryCheck = customtkinter.StringVar(value="Ara..")
        self.SearchEntry = customtkinter.CTkEntry(self,width=50,font=("Cascadia Mono Semibold",13),textvariable=self.SearchEntryCheck)
        self.SearchEntry.grid(row=1,column=0,sticky="NSWE",padx=10,pady=10)
        self.AddAiBtn = customtkinter.CTkButton(self,fg_color=ColorBg

,text="Hikayeye Ekle/Çıkar",font=("Cascadia Mono Semibold",13),hover=False,cursor="hand2",command=self.AddAi)
        self.AddAiBtn.grid(row=2,column=0)
        self.ShowAddedAiBtn = customtkinter.CTkButton(self,fg_color=ColorBg

,text="Göster/Gizle",font=("Cascadia Mono Semibold",13),hover=False,cursor="hand2",command=self.ShowAi)
        self.ShowAddedAiBtn.grid(row=2,column=1)
        self.Check=0
        self.SearchEntry.bind("<FocusIn>",self.EntryFocusIn)
        self.SearchEntry.bind("<FocusOut>",self.EntryFocusOut)
        self.SearchEntry.bind("<KeyRelease>",self.Search)

    def ShowAi(self):
        if self.Check == 0:
            self.scrollFrame.NewAiData()
            self.Check =1
        elif self.Check == 1:
            self.scrollFrame.NewData()
            self.Check= 0

    def AddAi(self):
        forAdd = self.CheckChoiceButton.get()

        query = "SELECT AdAi FROM forapptable WHERE English = %s"
        mycursor.execute(query, (forAdd,))
        resultOne = mycursor.fetchone()

        if resultOne is None:
            print("Hata: Veri bulunamadı!")
            return

        queryToAdd = "UPDATE forapptable SET AdAi = %s WHERE English = %s"


        new_value = 1 if resultOne[0] == 0 else 0
        mycursor.execute(queryToAdd, (new_value, forAdd))


        db.commit()

    def Search(self,event):
        searchFor = self.SearchEntry.get()
        self.scrollFrame.SearchNewData(searchFor)
    def EntryFocusIn(self,event):
        if self.SearchEntryCheck.get() =="Ara..":
            self.SearchEntryCheck.set("")
    def EntryFocusOut(self,event):
        if self.SearchEntryCheck.get() == "":
            self.SearchEntryCheck.set("Ara..")
    def Changes(self):
        def ChangeBtn():
            query = "UPDATE forapptable SET English = %s, Turkish = %s WHERE English = %s"
            mycursor.execute(query, (self.CheckEnglishİnput.get(), self.CheckTurkishİnput.get(), self.desiredForChangeWord,))
            db.commit()
            self.scrollFrame.NewData()
            root.destroy()
        def set_icon():
            root.iconbitmap("logom.ico")
        root = customtkinter.CTkToplevel(self)
        root.geometry("300x300")
        root.resizable(False, False)
        root.attributes("-topmost", True)
        root.title('Değiştir')
        root.configure(fg_color=ColorFrame)
        root.after(300, set_icon)
        root.columnconfigure(0,weight=1)
        root.rowconfigure(0,weight=4)
        root.rowconfigure(1,weight=4)
        root.rowconfigure(2,weight=2)
        self.desiredForChangeWord = self.CheckChoiceButton.get()
        query = "SELECT English,Turkish FROM forapptable WHERE English = %s"
        mycursor.execute(query,(self.desiredForChangeWord,))
        result = mycursor.fetchall()
        self.CheckEnglishİnput = customtkinter.StringVar(value=result[0][0])
        self.CheckTurkishİnput =customtkinter.StringVar(value=result[0][1])
        Englishİnput = customtkinter.CTkEntry(root,textvariable=self.CheckEnglishİnput,fg_color=ColorEntry,width=100,text_color="white",corner_radius=9,placeholder_text_color="white",font=('Cascadia Mono Semibold',13))
        Englishİnput.grid(row=0,column=0,sticky="WE",padx=50,pady=50)
        Turkishİnput = customtkinter.CTkEntry(root,textvariable=self.CheckTurkishİnput,fg_color=ColorEntry,width=100,text_color="white",corner_radius=9,placeholder_text_color="white",font=('Cascadia Mono Semibold',13))
        Turkishİnput.grid(row=1, column=0, sticky="WE", padx=50)
        ChangesBtn = customtkinter.CTkButton(root, text="Değiştir", corner_radius=34, fg_color=ColorButton , hover_color=ColorButtonHover,width=150, font=("Cascadia Mono Semibold", 13), hover=True, cursor="hand2",command=ChangeBtn)
        ChangesBtn.grid(row=3, column=0,pady=50)
        root.mainloop()

    def Delete(self):
        query = "DELETE FROM forapptable WHERE English = %s"
        value = (self.CheckChoiceButton.get(),)
        mycursor.execute(query, value)
        db.commit()
        self.after(100,self.scrollFrame.NewData())
        self.CheckChoiceButton.set("Silindi")
class ToplevelRemainWord(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("400x600")
        self.resizable(False,False)
        self.attributes("-topmost", True)
        self.title('Son Eklenen Kelimeler')
        self.configure(fg_color=ColorFrame)
        self.after(300, self.set_icon)
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=9)
        self.rowconfigure(1,weight=1)
        self.buttonSettings=TopLevelFrameSettingsRecent(self,None)
        self.buttonSettings.grid(row=1,column=0)
        self.KelimeList = TLRemainWordFrame(self,self.buttonSettings)
        self.KelimeList.grid(row = 0,column=0,sticky="NSWE",padx=10,pady=10)
        self.buttonSettings.scrollFrame = self.KelimeList


    def set_icon(self):
        self.iconbitmap("logom.ico")
class TopLevelCreateStoryPage(customtkinter.CTkToplevel):
    def __init__(self,master):
        super().__init__(master)
        self.rowconfigure(0,weight =9)
        self.rowconfigure(1,weight = 1)
        self.columnconfigure(0,weight=1)
        self.configure(fg_color=ColorFrame)
        self.after(300, self.set_icon)
        self.geometry("900x600")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.title('Hikaye Oluştur')
        self.TextBox = customtkinter.CTkTextbox(self,state="disabled",fg_color=ColorBg

)
        self.TextBox.grid(row = 0,column= 0,sticky="NSWE",padx=15,pady=15)

        self.createBtn = customtkinter.CTkButton(self,text="Hikaye Oluştur",corner_radius=34 ,fg_color=ColorButton ,hover_color=ColorButtonHover,width=150,font=("Cascadia Mono Semibold",13),hover=True,cursor="hand2",command=self.QueryAi)
        self.createBtn.grid(row=1,column=0,padx=15,pady=15)




    def change(self):
        """Change fonksiyonunda yeni thread açarak API çağrısını yap"""
        print("Change çağrıldı, API isteği başlatılıyor...")
        threading.Thread(target=self.QueryAi, daemon=True).start()


    def QueryAi(self):
        query = "SELECT english_level,hobby1,hobby2,hobby3 FROM profilesettings"
        mycursor.execute(query)
        result = mycursor.fetchall()
        try:
            user_input = f"Create an {result[0][0]}-level English story for someone interested in {result[0][1]}, {result[0][2]}, and {result[0][3]}. It should not exceed 300 words.don't create title"
            response = ollama.chat(model='mistral', messages=[{'role': 'user', 'content': user_input}])
            time.sleep(2)
            res = response.get('message', {}).get('content','')
            res = res.replace("\n", " ")
            self.after(1, lambda: self.update_text(res))
            print("Döngüye girildi")
            self.update_idletasks()


        except Exception as e:
            print("Hata ",e)
    def update_text(self, new_text):
        self.TextBox.destroy()
        self.newText = customtkinter.CTkLabel(self,text = new_text,wraplength=700,font=("Cascadia Mono Semibold", 15),fg_color=ColorBg

,corner_radius=9)
        self.newText.grid(row = 0,column= 0,sticky="NSWE",padx=15,pady=15)





    def set_icon(self):
        self.iconbitmap("logom.ico")


class CreateNewCart(customtkinter.CTkFrame):
    def __init__(self,master):
        super().__init__(master)
        self.configure(fg_color=ColorBg

)
        self.columnconfigure(0,weight =1)
        self.rowconfigure(0,weight=3)
        self.rowconfigure(1,weight=2)
        self.rowconfigure(2,weight=2)
        self.rowconfigure(3,weight=3)

        createhead = customtkinter.CTkLabel(self,text="Hemen Kart Oluştur",text_color="white",font=("Cascadia Mono Semibold",16))
        createhead.grid(row = 0,column = 0)
        self.EnglishEntryCheck = customtkinter.StringVar(value = "İngilizce")
        self.EnglishEntry  = customtkinter.CTkEntry(self,placeholder_text="İngilizce",fg_color=ColorEntry,width=50,text_color="white",corner_radius=9,placeholder_text_color="white",font=('Cascadia Mono Semibold',13),textvariable=self.EnglishEntryCheck)
        self.EnglishEntry.grid(row = 1 ,column =0,sticky="we",padx=50)
        self.TurkishEntryCheck = customtkinter.StringVar(value="Türkçe")
        self.TurkishEntry = customtkinter.CTkEntry(self, placeholder_text="Türkçe", fg_color=ColorEntry, width=50,text_color="white", corner_radius=9, placeholder_text_color="white",font=('Cascadia Mono Semibold',13),textvariable=self.TurkishEntryCheck)
        self.TurkishEntry.grid(row=2, column=0, sticky="we", padx=50 )
        self.MoreButton = customtkinter.CTkButton(self,text="Kelime Ekle",corner_radius=34 ,fg_color=ColorButton ,hover_color=ColorButtonHover,width=150,font=("Cascadia Mono Semibold",13),hover=True,cursor="hand2",command=self.AddDataBase)
        self.MoreButton.grid(row=3,column=0)
        self.TurkishEntry.bind("<FocusIn>", self.on_focus_in_Turkish)
        self.TurkishEntry.bind("<FocusOut>", self.on_focus_out_Turkish)
        self.EnglishEntry.bind("<FocusIn>", self.on_focus_in_English)
        self.EnglishEntry.bind("<FocusOut>",self.on_focus_out_English)
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
        self.master.RecentToCreate()
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

class RecentWord(customtkinter.CTkFrame):
    def __init__(self,master):
        super().__init__(master)
        self.configure(fg_color=ColorBg

)
        self.columnconfigure(0,weight =1)
        self.rowconfigure(0,weight=3)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5,weight=3)
        createhead =customtkinter.CTkLabel(self,text="Son Eklenen Kelimeler",text_color="white",font=("Cascadia Mono Semibold",16))
        createhead.grid(row = 0,column = 0)
        self.labelOneCheck = customtkinter.StringVar(value="Liste boş görünüyor")
        labelONe = customtkinter.CTkLabel(self, text="• Regardless", font=("Cascadia Mono Semibold", 13),textvariable =self.labelOneCheck)
        labelONe.grid(row=1, column=0)

        self.labelTwoCheck = customtkinter.StringVar()
        labelTwo = customtkinter.CTkLabel(self, text="• Another Label", font=("Cascadia Mono Semibold", 13),textvariable = self.labelTwoCheck)
        labelTwo.grid(row=2, column=0)
        self.toplevel_window = None
        self.labelThreeCheck = customtkinter.StringVar()
        labelThree = customtkinter.CTkLabel(self, text="• Yet Another Label", font=("Cascadia Mono Semibold", 13),textvariable=self.labelThreeCheck)
        labelThree.grid(row=3, column=0)
        self.labelFourCheck = customtkinter.StringVar()
        labelFour = customtkinter.CTkLabel(self, text="• And One More", font=("Cascadia Mono Semibold", 13),textvariable = self.labelFourCheck)
        labelFour.grid(row=4, column=0)
        self.MoreButton = customtkinter.CTkButton(self, text="Daha Fazla", corner_radius=34, fg_color=ColorButton ,hover_color=ColorButtonHover, width=150, font=("Cascadia Mono Semibold", 13),hover=True, cursor="hand2",command=lambda: self.open_toplevel())
        self.MoreButton.grid(row=5, column=0)
        self.RecentWordCheck()


    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelRemainWord(self)
        else:
            self.toplevel_window.focus()
    def RecentWordCheck(self):
        sqlQuest = "select English from forapptable order by id DESC LIMIT 5"
        mycursor.execute(sqlQuest)
        result = mycursor.fetchall()
        try:
            self.labelOneCheck.set('• ' + result[0][0])
        except IndexError:
            pass
        try:
            self.labelTwoCheck.set('• ' + result[1][0])
        except IndexError:
            pass

        try:
            self.labelThreeCheck.set('• ' + result[2][0])
        except IndexError:
            pass
        try:
            self.labelFourCheck.set('• ' + result[3][0])
        except IndexError:
            pass
class StartPractice(customtkinter.CTkFrame):
    def __init__(self,master):
        super().__init__(master)
        self.configure(fg_color=ColorBg

)
        self.columnconfigure(0,weight =1)
        self.rowconfigure(0,weight=2)
        self.rowconfigure(1,weight=5)
        self.rowconfigure(2,weight=3)
        createhead = customtkinter.CTkLabel(self,text="Kelime Pratiği Yap",text_color="white",font=customtkinter.CTkFont('Cascadia Mono Semibold',15))
        createhead.grid(row = 0,column = 0,pady=5)
        text = "Yeni öğrendiğin ingilizce kelimeleri unutmamak için düzenli olarak tekrar yapmalısın."
        customtkinter.CTkLabel(self,text=text,font=("Cascadia Mono Semibold",12),wraplength=220).grid(row=1,column=0)
        self.toplevel_window = None
        doPracticeButton = customtkinter.CTkButton(self, text="Pratik Yap", corner_radius=34, fg_color=ColorButton ,
                                                  hover_color=ColorButtonHover, width=150, font=("Cascadia Mono Semibold", 13),
                                                  hover=True, cursor="hand2",command=lambda : self.open_toplevel())
        doPracticeButton.grid(row=2,column=0,pady=10)

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = TLPracticeWord(self)
        else:
            self.toplevel_window.focus()
class StartAi(customtkinter.CTkFrame):
    def __init__(self,master):
        super().__init__(master)
        self.configure(fg_color=ColorBg

)
        self.columnconfigure(0,weight =1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=5)
        self.rowconfigure(2, weight=2)
        createhead = customtkinter.CTkLabel(self, text="Hikayeyle Öğren", text_color="white",
                                            font=customtkinter.CTkFont('Cascadia Mono Semibold', 15))
        createhead.grid(row=0, column=0, pady=5)
        text = "Yapay zeka senin için kaydettiğin kelimelerle ilgi alanına göre hikaye oluştursun."
        customtkinter.CTkLabel(self, text=text, font=("Cascadia Mono Semibold", 12), wraplength=220).grid(row=1,
                                                                                                          column=0)
        self.toplevel_window = None
        doPracticeButton = customtkinter.CTkButton(self, text="Hikaye Oluştur", corner_radius=34, fg_color=ColorButton ,
                                                   hover_color=ColorButtonHover, width=150,
                                                   font=("Cascadia Mono Semibold", 13),
                                                   hover=True, cursor="hand2",command=lambda: self.open_toplevel())
        doPracticeButton.grid(row=2, column=0, pady=10)
    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = TopLevelCreateStoryPage(self)
        else:
            self.toplevel_window.focus()
class RightSettings(customtkinter.CTkFrame):
    def __init__(self,master):
        super().__init__(master)

class SettingsPage(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.label = customtkinter.CTkLabel(self, text="Settings Page", font=("Arial", 20))
        self.label.pack(pady=20)

        self.back_button = customtkinter.CTkButton(self, text="Back", command=master.go_back)
        self.back_button.pack(pady=10)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("900x600")
        self.wm_iconbitmap('logom.ico')
        self.title('MasterMindAi')
        self.configure(fg_color=ColorFrame)
        self.columnconfigure(0,weight =4)
        self.columnconfigure(1,weight =4)
        self.columnconfigure(2,weight =0)
        self.rowconfigure(0,weight = 5)
        self.rowconfigure(1,weight = 5)
        self.createCart = CreateNewCart(self)
        self.createCart.grid(row = 0,column = 0,sticky = 'nswe',padx = 20,pady=20)
        self.recentWord = RecentWord(self)
        self.recentWord.grid(row = 1 ,column = 0,sticky = 'nswe',padx = 20,pady=20 )
        self.startPractice = StartPractice(self)
        self.startPractice.grid(row = 0,column =1,sticky = 'nswe',padx = 20,pady=20)
        self.startAi = StartAi(self)
        self.startAi.grid(row = 1,column = 1 , sticky = 'nswe',padx = 20,pady=20)
        #For Settings logo
        self.toplevel_window = None
        profile_img_pil = Image.open("Settings.png")
        profile_img = customtkinter.CTkImage(light_image=profile_img_pil, size=(30, 30))
        self.profile_button = customtkinter.CTkButton(self, image=profile_img, text="", fg_color="transparent",hover=False,cursor="hand2",width=50,command=lambda : self.open_toplevel())
        self.profile_button.grid(row=0,column=2,pady=30,sticky="NWE",padx=10)
        self.bind("<Configure>", lambda event: self.update_padding())

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = OpenSettings(self)
        else:
            self.toplevel_window.focus()
    def RecentToCreate(self):
        self.recentWord.RecentWordCheck()
    def update_padding(self):

        width = self.winfo_width()
        height = self.winfo_height()

        padx = int(width * 0.05)
        pady = int(height * 0.05)

        self.startAi.grid_configure(padx=padx, pady=pady)
        self.startPractice.grid_configure(padx=padx, pady=pady)
        self.recentWord.grid_configure(padx=padx, pady=pady)
        self.createCart.grid_configure(padx=padx, pady=pady)

app = App()
app.mainloop()