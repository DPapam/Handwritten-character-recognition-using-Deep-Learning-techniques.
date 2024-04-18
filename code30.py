import tkinter as tk
import random
import time
import tkinter.messagebox
from tkinter import filedialog
from PIL import ImageTk, Image, ImageDraw, ImageOps
import PIL
import winsound

#=============================================== DEFINITIONS ===============================================#
# ΑΡΧΙΚΗ
def modes():
    #bt_numbers.place(x=res_w/5*2,y=res_h/6,width=res_w/5,height=res_h/3)
    bt_numbers.place(x=res_w/5*2,y=res_h/6,width=cat_w,height=cat_h)
    bt_letters.place(x=res_w/5-70,y=res_h/6+100+cat_h,width=cat_w,height=cat_h)
    bt_fashion.place(x=(res_w/5*3)+70,y=res_h/6+100+cat_h,width=cat_w,height=cat_h)

    actives.append(bt_numbers)
    actives.append(bt_letters)
    actives.append(bt_fashion)
    
def paint(event):
    global cv
    size = 15
    x1, y1 = (event.x - size), (event.y - size)
    x2, y2 = (event.x + size), (event.y + size)
    cv.create_oval(x1, y1, x2, y2, fill="black",width=20)
    draw.line([x1, y1, x2, y2],fill="white",width=20)

def open_file():
    global filename
    bt_save.config(state="disabled")
    #bt_import.config(state="disabled")
    #bt_import.config(text=filename, state="disabled")

    filename = filedialog.askopenfilename(initialdir = "/Pictures",title = "Select file",filetypes = (("png files","*.png"),("all files","*.*")))
    if filename!='':
        bt_results.config(state='active')
        imported_img = ImageTk.PhotoImage(Image.open(filename))
        lb_img.config(image= imported_img , anchor='center')
        lb_img.image = imported_img 
        lb_img.place(x=200,y=170 , width = cv_w , height = cv_h)
        cv.place_forget()
    else:
        bt_save.config(state="active")
def drawing():
    bt_save.config(state="disabled")
    bt_import.config(state="disabled")
    cv.unbind('<B1-Motion>')

    ent_name.delete(0,"end")
    ent_name.insert(0,"Εισάγετε όνομα (χωρίς όνομα επέκτασης)")
    ent_name.place(x = 200+cv_w+100 , y = 200+100, width = imp_w , height = imp_h)
    bt_name.place(x = 200+cv_w+100+50+420, y = 200+120, width = 50 , height = 50)

def inserted():
    global filename,cv, new_image, draw
    name.set(name.get().strip())
    ent_name.place_forget()
    bt_name.place_forget()
    check = True
    for p in name.get():
        if p in '\/;*?"<>|':
            check=False
            break
        
    if check:
        print(name.get())
        bt_import.config(text=name.get(), font=('arial',25))
        #new_image.save(name.get()+".png")
        inverted_image = ImageOps.invert(new_image)
        inverted_image.save(name.get()+'.png')
        bt_results.config(state="active")
        filename=name.get()+".png"
    else:
        drawing()

def result(mode):
    global filename
    scr_bar = tk.Scrollbar(root)
    actives.append(scr_bar)
    f = open("information.txt",'a+',encoding='utf-8')
    f.write(filename)
    f.close()
    
    tx_rel = tk.Text(root, font = ('arial', 25),yscrollcommand=scr_bar.set)
    actives.append(tx_rel)
    scr_bar.config(command=tx_rel.yview)
    tx_rel.place(x=200,y=170,width=800,height=500)
    scr_bar.place(x=1050, y=300,width=25,height=225)
    bt_main.place(x = 167, y = 50, width = cat_w , height = 100)
    
   
    
    
    actives.append(bt_main)
    actives.append(bt_reset)
    actives.append(bt_resetf)
   
    
    #bt_reset.place(x = 167 + cat_w + 100 , y = 50, width = cat_w , height = 100)
    
    if mode=="numbers":
        bt_reset.place(x = 167 + cat_w + 100 , y = 50, width = cat_w , height = 100)
        
        import usemodel_new
        winner = usemodel_new.predict(usemodel_new.vectorr(filename))
        
        tx_rel.insert("end", "Ο προβλεπόμενος αριθμός είναι το {}.\n".format(winner))
        for p in range(0, len(usemodel_new.predictions[0] )):
            print("Πιθανότητα αριθμού {} : {:04.3f}\n".format(p, usemodel_new.predictions[0][p]) )
            tx_rel.insert("end", "Πιθανότητα αριθμού {} : {:04.3f}\n".format(p, usemodel_new.predictions[0][p]) )

    elif mode=="letters":
        bt_reset.place(x = 167 + cat_w + 100 , y = 50, width = cat_w , height = 100)
        import usemodel_letters_new
        winner = usemodel_letters_new.predict(usemodel_letters_new.vectorr(filename))
        tx_rel.insert("end", "Το προβλεπόμενο γράμμα είναι το {}.\n".format(winner))
        i=ord('A')
        for p in range(0, len(usemodel_letters_new.predictions[0])-1):
            print("Πιθανότητα γράμματος {} : {:04.3f}\n".format(chr(i+p), usemodel_letters_new.predictions[0][p+1]) )
            print(p)
            tx_rel.insert("end", "Πιθανότητα γράμματος {} : {:04.3f}\n".format(chr(i+p), usemodel_letters_new.predictions[0][p+1]) )
    elif mode=="fashion":
       
        bt_resetf.place(x = 167 + cat_w + 100 , y = 50, width = cat_w , height = 100)
        import usemodel_fashion_new
        Fashion={0:"T-shirt/top",1:"Trouser",2:"Pullover",3:"Dress",4:"Coat",5:"Sandal",
             6:"Shirt",7:"Sneaker",8:"Bag",9:"Ankle boot"}

        winner = usemodel_fashion_new.predict(usemodel_fashion_new.vectorr(filename))
        
        tx_rel.insert("end", "Tο προβλεπόμενο ρούχο είναι το {}.\n".format(winner))
        for p in Fashion :
            print("Πιθανότητα ρούχου {} : {:04.3f}\n".format(Fashion[p], usemodel_fashion_new.predictions[0][p]) )
            print(p)
            tx_rel.insert("end", "Πιθανότητα ρούχου {} : {:04.3f}\n".format(Fashion[p], usemodel_fashion_new.predictions[0][p]) )
    else:
        print("OOOO!")
   

# ΣΕΛΙΔΑ ΓΙΑ ΓΡΑΜΜΑΤΑ 'Η ΑΡΙΘΜΟΥΣ (Ίδια widgets αλλά καλεί διαφορετικό πρόγραμμα)
def num_let():
    global cv, new_image, draw
    new_image = PIL.Image.new("RGB", (500, 500))
    draw = ImageDraw.Draw(new_image)
    cv = tk.Canvas(root, bg='white')
    actives.append(bt_main)
    actives.append(bt_reset)
    actives.append(cv)
    actives.append(bt_save)
    actives.append(bt_import)
    actives.append(lb_img)
    actives.append(bt_results)
    cv.delete("all")
    bt_save.config(state="active")
    bt_import.config(state="active",text='ΕΙΣΑΓΩΓΗ ΕΙΚΟΝΑΣ',font=('arial',24))
    ent_name.place_forget()
    bt_name.place_forget()
    
    bt_main.place(x = 167, y = 50, width = cat_w , height = 100)

    bt_reset.place(x = 167 + cat_w + 100 , y = 50, width = cat_w , height = 100)
    
    bt_save.place(x = 200+cv_w+100, y = 170+cv_h-relt_h, width = save_w , height = save_h)
    
    cv.place(x = 200, y = 170 , width = cv_w , height = cv_h)
    cv.bind("<B1-Motion>", paint)
   

    bt_import.place(x = 200+cv_w+100 , y = 200+100, width = imp_w , height = imp_h)
    #bt_import.config(state="disabled")
    bt_results.place(x = 200+cv_w+100+save_w+200 , y = 170+cv_h-relt_h, width = relt_w , height = relt_h)
    bt_results.config(state='disabled')

def fashion():
    global cv, new_image, draw
    new_image = PIL.Image.new("RGB", (500, 500))
    draw = ImageDraw.Draw(new_image)
    cv = tk.Canvas(root, bg='white')
    actives.append(bt_main)
    actives.append(bt_resetf)
    actives.append(cv)
    actives.append(bt_save)
    actives.append(bt_import)
    actives.append(lb_img)
    actives.append(bt_results)
    cv.delete("all")
  
    bt_import.config(state="active",text='ΕΙΣΑΓΩΓΗ ΕΙΚΟΝΑΣ',font=('arial',24))
   
    
    bt_main.place(x = 167, y = 50, width = cat_w , height = 100)

    bt_resetf.place(x = 167 + cat_w + 100 , y = 50, width = cat_w , height = 100)
    
    
    
    cv.place(x = 200, y = 170 , width = cv_w , height = cv_h)
    cv.unbind('<B1-Motion>')
    
   

    bt_import.place(x = 200+cv_w+100 , y = 200+100, width = imp_w , height = imp_h)
    #bt_import.config(state="disabled")
    bt_results.place(x = 200+cv_w+100+save_w+200 , y = 170+cv_h-relt_h, width = relt_w , height = relt_h)
    bt_results.config(state='disabled')
    
    

#cccncncjcnjcnkjdnvjvnvjn
# ΑΛΛΑΓΗ ΣΕΛΙΔΑΣ
def change(mode):
    global option
    for i in actives:
        i.place_forget()
    actives.clear()
    if mode=='numbers' or mode=='letters':
        option=mode
        num_let()
    elif mode=='fashion':
        option=mode
        fashion()
    elif mode=='reset':
        num_let() 
    elif mode=='resetf':
        fashion()
    elif mode=="result":
        result(option)
    elif mode=="main":
        modes()
    else: print("Oops!")

   
    
def blink():
    pass

def datez(st):
    grdays=['Δευτέρα','Τρίτη','Τετάρτη','Πέμπτη','Παρασκευή','Σάββατο','Κυριακή']
    grmonths=['Ιανουαρίου','Φεβρουαρίου','Μαρτίου','Απριλίου','Μαΐου','Ιουνίου','Ιουλίου','Αυγούστου','Σεπτεμβρίου','Οκτωβρίου','Νοεμβρίου','Δεκεμβρίου']
    endays=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    enmonths=['Januray','February','March','April','May','June','July','August','September','October','November','December']
    return grdays[endays.index( st.split()[0] )] +', '+ st.split()[1] +' '+ grmonths[enmonths.index( st.split()[2] )] +' '+ st.split()[3] +'\n'+ st.split()[4]


#=============================================== MAIN ===============================================#
if __name__ == "__main__":

    winsound.PlaySound('foolboymedia__new-york-jazz-loop.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
    
    res_h, res_w = 768, 1366
    f1h = 120
    f1w = res_w
    f2h = 90
    f2w = res_w
    f3h = res_h-f1h-f2h
    f3w = res_w
    h = 0
    cv_h,cv_w = res_h*500/768, res_h*500/768

    cat_h, cat_w = res_h/4, res_w/5


    save_h , save_w = res_h/10 , res_w/8 
    relt_h , relt_w =res_h/7 ,res_w/7
    imp_h,imp_w = save_h, res_w/3
    actives = [] #list of active yet not permanent widgets (what to destroy when changing page)


    root = tk.Tk('white')
    root.title("A.I.")
    root.geometry(str(res_w)+"x"+str(res_h))
    key = tk.StringVar()
    date = tk.StringVar()
    name = tk.StringVar()
    total = tk.DoubleVar()
    date.set( datez(time.strftime("%A %d %B %Y %H:%M")) )

    # ΕΙΣΑΓΩΓΗ ΕΙΚΟΝΩΝ
    img_back = tk.PhotoImage(file='neural_bg_edited_v3.png')
    #img_logo = tk.PhotoImage(file='logo_edited.png')
    #img_logo.config()
    img_numbers = tk.PhotoImage(file='numbers.png')
    
    img_letters = tk.PhotoImage(file='letters.png')
    
    img_games = tk.PhotoImage(file='jim.png')

    img_main=tk.PhotoImage(file="house.png")
    #new_image = PIL.Image.new("RGB", (500, 500))
    #draw = ImageDraw.Draw(new_image)
    
    # WIDGETS ΑΡΧΙΚΗΣ
    lb_back = tk.Label(root, image=img_back)
    lb_back.place(x=0, y=0, height=res_h
                  , width=res_w)
    lb_date = tk.Label(root,textvariable=date,font=('arial',24),fg='#e4e4e4',bg='#384052')
    lb_date.place(x=900,y=50,width=400,height=70)
    #lb_logo = tk.Label(root, image=img_logo)
    #lb_logo.place(x=10, y=0, height=300, width=300)

    bt_numbers = tk.Button(root, image=img_numbers, command=lambda mode="numbers": change(mode))
    bt_letters = tk.Button(root, image=img_letters, command=lambda mode="letters": change(mode))
    bt_fashion = tk.Button(root,image=img_games, command=lambda mode="fashion": change(mode))

    # WIDGETS ΑΡΙΘΜΩΝ/ΓΡΑΜΜΑΤΩΝ
    #cv = tk.Canvas(root, bg='white')

    bt_results = tk.Button(root, text='RESULTS',font=('arial',24),bg='blue', command=lambda mode="result": change(mode))


    bt_main = tk.Button(root ,text="ΑΡΧΙΚΗ",font=("arial",24),bg="blue", command=lambda mode="main": change(mode))

    bt_reset = tk.Button(root,text="RESET",font=('arial',24), bg='red', command=lambda mode="reset": change(mode))
    
    bt_resetf=tk.Button(root,text="RESET",font=('arial',24), bg='red', command=lambda mode="resetf": change(mode))

    bt_save = tk.Button(root,bg='green', text='SAVE',font=('arial',24), command=drawing)

    bt_import = tk.Button(root, bg='#bbbbbb', command=open_file)

    lb_img = tk.Label(root)
    root.wm_attributes('-transparentcolor','grey')

    # temporary
    ent_name = tk.Entry(root,textvariable=name,font=('arial',24),bd=3,width=3,justify='center')
    bt_name = tk.Button(root, text="OK",font=("arial",24),bg='green', command=inserted)
    

    modes()
    
    root.mainloop()
    
    
