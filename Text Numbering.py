# Import the required libraries
from tkinter import *
import tkinter.filedialog as fd
from tkinter import messagebox
from PIL import ImageTk, Image, ImageFont, ImageDraw

# Create an instance of tkinter frame or window
path = None
numberPrint = 0
def createFrame():
   global root, img, atas, bawah, label, showImg, path, number
   root = Tk()
   # Set the geometry of tkinter frame
   root.title("Text Numbering")
   root.maxsize(800,1500)
   root.config(bg="skyblue")

   # Create left and right frames
   left_frame = Frame(root, width=200, height=400, bg='grey')
   left_frame.grid(row=0, column=0, padx=10, pady=5)

   right_frame = Frame(root, width=300, height=500, bg='grey')
   right_frame.grid(row=0, column=1, padx=10, pady=5)

   toolbar = Frame(left_frame, width=180, height=185)
   toolbar.grid(row=2, column=0, padx=5, pady=5)

   atas = Frame(right_frame, width=300, height=450, bg='grey')
   atas.grid(row=0, column=1, padx=10, pady=5)

   bawah = Frame(right_frame, width=300, height=50, bg='grey')
   bawah.grid(row=1, column=1, padx=10, pady=5)

   #Test Image
   if (path != None):
      number = 0
      img = Image.open(path[number])

      insert_img()
      showImg = Label(atas, image=img).grid(row=0,column=0, padx=5, pady=5)

   #Toolbar
   Label(toolbar, text="Toolbar", width=20).grid(row=0,column=0,columnspan = 2,padx=5,pady=5)
   Button(toolbar, text="Pilih gambar", command=open_file, width = 20).grid(row=1,column=0, columnspan = 2,padx=5, pady= 5)

   ##Start and End
   Label(toolbar, text="Judul :", width=10).grid(row=2,column=0, padx=5, pady= 5)
   judulTxt = Text(toolbar, width=10, height=1)
   Label(toolbar, text="Nomor Awal :", width=10).grid(row=3,column=0, padx=5, pady= 5)
   startTxt = Text(toolbar, width=10, height=1)
   Label(toolbar, text="Nomor Akhir :", width=10).grid(row=4,column=0, padx=5, pady=5)
   endTxt = Text(toolbar, width=10, height=1)
   
   ##Save Button
   save = Button(toolbar, text="Simpan Hasil", command = lambda:saveToPDF(startTxt.get(1.0, "end-1c"), endTxt.get(1.0, "end-1c"),judulTxt.get(1.0, "end-1c")),width = 20)
      
   #Some Tweaking
   if (path == None):
      judulTxt['state'] = DISABLED
      startTxt['state'] = DISABLED
      endTxt['state'] = DISABLED
      save['state'] = DISABLED
   judulTxt.grid(row=2,column=1, padx=5, pady= 5)
   startTxt.grid(row=3,column=1, padx=5, pady= 5)
   endTxt.grid(row=4,column=1, padx=5, pady = 5)
   save.grid(row=5,column=0, columnspan = 2,padx=5, pady= 5)

   #Left and Right Button
   b1 = Button(bawah, text="Kiri",command=left_file, width=5)
   b2 = Button(bawah, text="Kanan",command=right_file, width=5)
   if(path == None):
      b1["state"] = DISABLED
      label = Label(bawah,text = "0/0", width=5).grid(row=0,column=1, padx=5, pady=5)
      b2["state"] = DISABLED
   else:
      label = Label(bawah,text = str(number+1)+"/"+str(len(path)), width=5).grid(row=0,column=1, padx=5, pady=5)
   b1.grid(row=0,column=0, padx=5, pady=5)
   b2.grid(row=0,column=2, padx=5, pady=5)

   root.mainloop()

def open_file():
   global path
   file = fd.askopenfilenames(parent=root, title='Choose a File',filetypes = (("Pictures", ".png"), ("Pictures",".jpg"),("Pictures",".jpeg")))
   path = root.splitlist(file)
   if(len(path)>0):
      root.destroy()
      createFrame()

def insert_img():
   global img, width, height
   width, height = img.size
   while(width>500 or height>800):
      width = int(width/2)
      height = int(height/2)
   setImage()

def right_file():
   global img, showImg, number, label
   number += 1
   if(number>=len(path)):
       number=0
   print(number)
   print(path[number])
   img = Image.open(path[number])
   setImage()
   showImg = Label(atas, image=img).grid(row=0,column=0, padx=5, pady=5)
   label = Label(bawah,text = str(number+1)+"/"+str(len(path)), width=5).grid(row=0,column=1, padx=5, pady=5)

def left_file():
   global img, showImg, number, label
   number -= 1
   if(number<0):
       number=len(path)-1
   img = Image.open(path[number])
   print(img.size)
   setImage()
   showImg = Label(atas, image=img).grid(row=0,column=0, padx=5, pady=5)
   label = Label(bawah,text = str(number+1)+"/"+str(len(path)), width=5).grid(row=0,column=1, padx=5, pady=5)

def watermark(img):
   img = img.convert("RGBA")
   txt = Image.new('RGBA', img.size, (255,255,255,0))

   font = ImageFont.truetype("arial.ttf", 25)
   d = ImageDraw.Draw(txt)    

   w, h = img.size
   x, y = int(w / 2), int(h / 2)

   if x > y:
      font_size = y
   elif x <= y:
      font_size = x
   
   dot_x = x - (font_size/2)/2
   dot_y = y - (font_size/2)/2
   font = ImageFont.truetype("arial.ttf", int(font_size/2))
   if(numberPrint<10):
      d.text((dot_x, dot_y), "0"+str(numberPrint), fill=(0, 0, 0, 50), font=font)
   else:
      d.text((dot_x, dot_y), str(numberPrint), fill=(0, 0, 0, 50), font=font)
   img = Image.alpha_composite(img, txt)    
   img = img.convert("RGB")
   return img

def setImage():
   global img
   img = img.resize((width,height))
   img = watermark(img)
   img =  ImageTk.PhotoImage(img)

def saveToPDF(input1, input2, judul):
   global numberPrint
   numberPrint = int(input1)
   endPrint = int(input2)
   out_path = fd.askdirectory(parent=root, title='Choose a File')
   while(numberPrint<=endPrint):
      images = [watermark(Image.open(f).resize((2480,3508))) for f in path]
      images[0].save(
         out_path+"/"+judul+" - "+str(numberPrint)+".pdf", "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
      )
      numberPrint += 1
   messagebox.showinfo("Informasi", "Proses Telah Selesai")

createFrame()