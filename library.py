from audioop import add
from tkinter import *
from tkinter import ttk
from db import Database
db = Database("my_library.db")





#global vars
pad_input_x = 390
pad_label = [155,72]
font_name_size = ('Ariel',15)
input_font_name_size = ('Roman classic', 14)
background_color = ['lightgreen','lightblue','lightgrey','#004953','silver','red']
width_height = [1250,600]
input_width = [30]
themes = ["alt","clam","classic","default","xpnative","winnative"]
global count 

class Root(Tk):
    def __init__(self):
        super().__init__()
        self.title('Find book')
        self.iconbitmap('book.ico')
        self.geometry("1250x600")
        self.maxsize(width_height[0],width_height[1])
        self.style = ttk.Style()
        self.style.theme_use(themes[3])
        self.my_book = ttk.Notebook(self,width=width_height[0],height=width_height[1])
        self.my_book.pack()
        self.list_books()
        self.search_books()
        

    def add_to_treeview(self):
        if len(self.title_input.get()) == 0:
            self.message_label_title.config(text='*Please,Enter Title !')
        elif len(self.author_input.get()) == 0:
            self.message_label_author.config(text='*Please,Enter Author !')
        elif len(self.year_input.get()) == 0:
            self.message_label_year.config(text='*Please,Enter Year !')
        elif len(self.isbn_input.get()) == 0:
            self.message_label_isbn.config(text='*Please,Enter ISBN ! ')    
        else:
            db.insert(self.title_input.get() , self.author_input.get(), self.year_input.get(), self.isbn_input.get())
            # Clear entry
            self.clear_entries()
            #add new treeview data
            self.treeview_display()
        
        
    def treeview_display(self,records=None):
        self.my_tree.delete(*self.my_tree.get_children())
        if records==None:
            records=db.fetch()
        count = 0
        for record in records:
            if count % 2 == 0:
                self.my_tree.insert(parent='', index='end' ,text='',iid=count, values=(record[0],record[1],record[2],record[3],record[4]),tags=('evenrow',))
            else:
                self.my_tree.insert(parent='', index='end' ,text='',iid=count, values=(record[0],record[1],record[2],record[3],record[4]),tags=('oddrow',))
            count+=1
    
    def selected_item_treeview(self,e):
        #Get record number
        selected =self.my_tree.focus()
        #Get record values from treeview
        self.values = self.my_tree.item(selected,'values')
        self.clear_entries()
        try:
        #place the items in there entries
            self.title_input.insert(0,self.values[1])
            self.author_input.insert(0,self.values[2])
            self.year_input.insert(0,self.values[3])
            self.isbn_input.insert(0,self.values[4])
        except IndexError:
            pass
    
    def update_item_treeview(self):
        if len(self.title_input.get()) == 0:
            self.message_label_title.config(text='*Please,Enter Title !')
        elif len(self.author_input.get()) == 0:
            self.message_label_author.config(text='*Please,Enter Author !')
        elif len(self.year_input.get()) == 0:
            self.message_label_year.config(text='*Please,Enter Year !')
        elif len(self.isbn_input.get()) == 0:
            self.message_label_isbn.config(text='*Please,Enter ISBN ! ')    
        else:
            db.update(self.values[0],
                  self.title_input.get() ,
                  self.author_input.get(),
                  self.year_input.get(),
                  self.isbn_input.get())
            self.treeview_display()

    def delete_item_treeview(self):
        db.remove(self.values[0])
        self.clear_entries()
        self.treeview_display()
    
    def search_item_treeview(self):
        records = db.search(self.search_input.get(),
                            self.search_input.get(),
                            self.search_input.get(),
                            self.search_input.get())
        self.treeview_display(records)
        
    def clear_entries(self):
        self.title_input.delete(0,END)
        self.author_input.delete(0,END)
        self.year_input.delete(0,END)
        self.isbn_input.delete(0,END)
        self.message_label_title.config(text=' ')
        self.message_label_author.config(text=' ')
        self.message_label_year.config(text=' ')
        self.message_label_isbn.config(text=' ')
        
         
         
    
    def list_books(self):
        #main frame
        add_frame = Frame(self.my_book,width=width_height[0],height=width_height[1], bg=background_color[2])
        add_frame.pack(fill='both', expand=1)
        
        #frame around treeview
        outline_frame = LabelFrame(add_frame, text="List", width=1100,height=800,font=input_font_name_size,bg=background_color[2])
        outline_frame.grid(row=0, column=1, padx=50 ,pady=20)
        outline_frame.grid_propagate(0)
        
        #frame around form 
        outline_frame_form = LabelFrame(add_frame, text="Form", width=1100,height=800,font=input_font_name_size,bg=background_color[2])
        outline_frame_form.grid(row=0, column=2, padx=150)
        outline_frame_form.grid_propagate(0)

        self.my_book.add(add_frame, text="View List")
        
        
        # Create title input Entry and Label
        self.title_input=Entry(outline_frame_form, width=input_width)
        title_input_label = Label(outline_frame_form, text='Title      :',bg=background_color[4])
        self.message_label_title = Label(add_frame, text=' ',bg=background_color[2])
        # Create author input Entry and Label
        self.author_input=Entry(outline_frame_form, width=input_width)
        author_input_label = Label(outline_frame_form, text='Author :',bg=background_color[4])
        self.message_label_author = Label(add_frame, text=' ',bg=background_color[2])
        # Create year input Entry and Label
        self.year_input=Entry(outline_frame_form, width=input_width)
        year_input_label = Label(outline_frame_form, text='Date      :',bg=background_color[4])
        self.message_label_year = Label(add_frame, text=' ',bg=background_color[2])
        
        
        #Create ISBN input Entry and Label
        self.isbn_input=Entry(outline_frame_form, width=input_width)
        isbn_input_label = Label(outline_frame_form, text='ISBN     :',bg=background_color[4])
        self.message_label_isbn = Label(add_frame, text=' ',bg=background_color[2])
        
        # search entry
        self.search_input=Entry(add_frame, width=input_width,font=('Roman classic', 15))
        
        # Error message 
        self.message_label_title.place(x=865,y=135)
        self.message_label_author.place(x=865,y=195)
        self.message_label_year.place(x=865,y=255)
        self.message_label_isbn.place(x=865,y=315)
   

        #Add Created label and input to the page
        self.search_input.place(x=610,y=20)
        self.title_input.pack(padx=100,pady=20)
        title_input_label.grid(row=0,column=0,padx=50,pady=19)
        self.author_input.pack(padx=100,pady=20)
        author_input_label.grid(row=1,column=0,padx=50,pady=19)
        self.year_input.pack(padx=100,pady=20)
        year_input_label.grid(row=2,column=0,padx=50,pady=19)
        self.isbn_input.pack(padx=100,pady=20)
        isbn_input_label.grid(row=3,column=0,padx=50,pady=19)
        
        
        #Create Add button    
        submit_button = ttk.Button(add_frame, text='Add',width=25, command=self.add_to_treeview)
        submit_button.place(x=580,y=140)
        
        # Create Update button 
        update_button = ttk.Button(add_frame, text='Update',width=25, command=self.update_item_treeview)
        update_button.place(x=580,y=170) 
        #delete button
        delete_button = ttk.Button(add_frame, text='Delete',width=25, command=self.delete_item_treeview)
        delete_button.place(x=580,y=200) 

        # dispaly all entries button
        display_all = ttk.Button(add_frame, text='Display all',width=25, command=self.treeview_display)
        display_all.place(x=580,y=230) 

        # Search button
        search_button = ttk.Button(add_frame, text='Search',width=20,command=self.search_item_treeview)
        search_button.place(x=960,y=20.4) 
        
        
        # Clear button
        clear_button = ttk.Button(add_frame, text='Clear Entires',width=25,command=self.clear_entries)
        clear_button.place(x=880,y=400) 
        
           
        
        #Create Scrollbar for treeview
        tree_scroll = Scrollbar(outline_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)
        self.my_tree = ttk.Treeview(outline_frame,height=15,yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=self.my_tree.yview)
        
        #Create Columns for Treeview    
        self.my_tree['columns'] = ('ID','Title','Author','Date','ISBN')
        #Add style
        self.style = ttk.Style()
        
        
        #pick a theme
        self.style.configure("Treeview", 
                        rowheight=25,
                        font=(None,11)
                        )

      
        #format our columns
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("ID", width=10, anchor=CENTER)
        self.my_tree.column("Title", width=130, anchor=W)
        self.my_tree.column("Author", width=130,anchor=W)
        self.my_tree.column("Date",width=100, anchor=CENTER)
        self.my_tree.column("ISBN",width=100, anchor=CENTER)
        
        #Create heading and format heading 
        self.my_tree.heading("#0",text="", anchor=W)
        self.my_tree.heading("ID", text="ID", anchor=CENTER)
        self.my_tree.heading("Title", text="Title", anchor=W)
        self.my_tree.heading("Author", text="Author", anchor=W)
        self.my_tree.heading("Date", text="Date", anchor=CENTER)
        self.my_tree.heading("ISBN", text="ISBN", anchor=CENTER)
        
        #Create striped row tags
        self.my_tree.tag_configure('oddrow',background="white")
        self.my_tree.tag_configure('evenrow',background="lightblue")
        self.my_tree.pack(pady=15, padx=10)
        self.my_tree.bind('<<TreeviewSelect>>', self.selected_item_treeview)
        self.treeview_display()
    # add last tab 
    def search_books(self):    
        add_frame = Frame(self.my_book,width=width_height[0],height=width_height[1], bg=background_color[2])
        add_frame.pack(fill='both', expand=1)
        outline_frame = LabelFrame(add_frame,text="", width=500,height=500,font=('Roman classic',30),bg=background_color[2])
        outline_frame.grid(row=0, column=1, padx=350 ,pady=20)
        outline_frame.grid_propagate(0)   
            
        self.my_book.add(add_frame, text=":)")
        last_part=Label(outline_frame, text="I hope you enjoy it", font=('Roman classic',40),bg=background_color[2])
        last_part.place(x=30, y=100)
        

window = Root() 
window.mainloop()       
    