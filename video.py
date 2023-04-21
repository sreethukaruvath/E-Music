import os
from atexit import register
from tkinter import*
from tkinter import messagebox
import cv2
from deepface import DeepFace
from PIL import ImageTk, Image
class App():
    screen=None
    def __init__(self):
        root=Tk()
        root.title('Login')
        root.geometry('925x500+300+200')
        root.configure(bg="#fff")
        root.resizable(False,False)
        self.screen=root
        self.screen.title("App")
        self.screen.resizable(False,False)
        self.screen.geometry('925x500+300+200')
        self.screen.config(bg="white")
        # Label(self.screen,text='Hello Everyone!',bg='#fff',font=('Calibri(Body)',50,'bold')).pack(expand=True) 
        bgimg= PhotoImage(file = "logoimg1.png")
        limg= Label(self.screen, i=bgimg,bg="white")
        limg.pack(fill=BOTH, expand=YES)
        Button(self.screen,width=34,pady=7,text='scan',bg='#C70039',fg='white',highlightthickness=0,border=0,command=self.capture_face).place(x=300,y=420)
        self.screen.mainloop()
    def capture_face(self):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        video = cv2.VideoCapture(0)
        dected_imotions=[]
        last_imotion=''
        while True:
            try:
                _, frame = video.read()
                cv2.imshow('video',frame)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                face = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
                for x, y, w, h in face:
                    img = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
                    analyze = DeepFace.analyze(frame,actions=['emotion'])
                    if analyze['dominant_emotion'] not in dected_imotions:
                        dected_imotions.append(analyze['dominant_emotion'])
                    # print(analyze['dominant_emotion'])
                    cv2.putText(frame, analyze['dominant_emotion'], (x+5, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                    cv2.imshow('video',frame)
                    last_imotion=str(analyze['dominant_emotion'])
                key=cv2.waitKey(0) & 0xFF
                if key==113:
                    break
                else:
                    continue
            except Exception as e:
                # print("no face",e)
                pass
        video.release()
        cv2.destroyAllWindows()
        print("OKKKK",last_imotion)
        print(".......dected_imotions.....",dected_imotions)
        f_name = f'songs/{last_imotion}'
        s_name = ""
        for i in os.listdir(f"./{f_name}"):
            if i[-3:] in ["mp3", "wav", "pga","mpga"]:
                s_name = i
                break
        path = f"./{f_name}/{s_name}"
        print(f"playing {s_name}")
        os.system("vlc "+path)
render=App()