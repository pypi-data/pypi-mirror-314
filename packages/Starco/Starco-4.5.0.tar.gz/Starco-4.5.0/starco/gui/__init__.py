from tkinter import ttk
from tkinter import *
from functools import partial
from .utils import *
from starco.pkl import Pkl

class GUI:
    def __init__(
            self, title: str,
              tabs={'start': {'rows': 5}},
                tabs_padding=15,
                width=350,
                height=500
                ,full_screen=False,
                bg_color ='#000',
                fg_color ='#fff',
                **kargs
                ) -> None:
        '''
            pkl_path
        '''
        self.vars = {}
        self.root = Tk()
        self.root.geometry(f"{width}x{height}")
        if full_screen:
            FullScreenApp(self.root)
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.root.update()
        self.root.title(title)
        self.x_y_info = {}
        self.pkl = Pkl(kargs.get('pkl_path','setting'))
        self.tabs_padding = tabs_padding
        self.tabs = tabs
        self.init_tabs()
        self.set_styles()

    def set_styles(self):
        style = ttk.Style(self.root)
        style.theme_use('alt')
        styles = {}
        styles['frame'] = ttk.Style()
        styles['frame'].configure('new.TFrame', background=self.bg_color,foreground=self.fg_color)
        styles['checkbutton'] = ttk.Style()
        styles['checkbutton'].configure('new.TCheckbutton', background=self.bg_color,foreground=self.fg_color)
        styles['label'] = ttk.Style()
        styles['label'].configure("new.TLabel", background=self.bg_color,foreground=self.fg_color)
        styles['treeview'] = ttk.Style()
        styles['treeview'].configure('Treeview', rowheight=40)

        # ('aqua', 'step', 'clam', 'alt', 'default', 'classic')
    
    def init_tabs(self):

        tabControl = ttk.Notebook(self.root, padding=self.tabs_padding)
        for tab in self.tabs.keys():
            self.vars[tab] = ttk.Frame(tabControl, padding=self.tabs_padding, style='new.TFrame')
            tabControl.add(self.vars[tab], text=tab.title())

        tabControl.pack(expand=1, fill="both")

    def callback(self, sv, *args):
        self.pkl.pkl(str(sv), sv.get())

    def label_txt(self, str_in):
        return str_in.replace("_", " ").title()+" : "

    def get_row(self, name: str):
        row = self.x_y_info.get(name, 0)
        self.x_y_info[name] = row+1
        return row

    def get_rely(self, name: str):
        row = self.get_row(name)
        step = 1/self.tabs[name]['rows']
        return row*(step)

    def add_label_input(self, tab, name: str, label_to_input_ratio=0.5, end_label: str = None, label: str = None, savable: bool = True, empty_return: str = '', margin: float = 0, input_justify=LEFT):
        root = self.vars[tab]
        rely = self.get_rely(tab)
        if not label:
            label = self.label_txt(name)
        item_w = label_to_input_ratio * (1-2*margin)
        self.vars[name] = StringVar(value=self.pkl.pkl(
            name, empty_return=empty_return), name=name)

        a = ttk.Label(root, text=label, style='new.TLabel')
        indent = margin
        a.place(relx=indent, rely=rely, relwidth=item_w)

        if savable:
            self.vars[name].trace("w", lambda name, index,
                                  mode, sv=self.vars[name]: self.callback(sv))
        relwidth = (1-label_to_input_ratio) * (1-2*margin)
        if end_label != None:
            relwidth = (1-2*label_to_input_ratio) * (1-2*margin)

        b = ttk.Entry(
            root, textvariable=self.vars[name], justify=input_justify)
        indent += item_w
        b.place(relx=indent, rely=rely, relwidth=relwidth)

        if end_label != None:
            indent += relwidth+0.01
            c = ttk.Label(root, text=end_label, style='new.TLabel')
            c.place(relx=indent, rely=rely, relwidth=item_w)

    def add_label(self, tab, name: str, label: str = None, margin: float = 0, input_justify=CENTER):
        root = self.vars[tab]
        rely = self.get_rely(tab)
        if not label:
            label = name
        item_w = (1-2*margin)

        a = ttk.Label(root, text=label, style='new.TLabel',justify=input_justify)
        indent = margin
        a.place(relx=indent, rely=rely, relwidth=item_w)

    def add_combobox(self, tab, name: str, values: list, label_to_input_ratio=0.5, end_label: str = None, label: str = None, savable: bool = True, empty_return: str = '', margin: float = 0):
        root = self.vars[tab]
        rely = self.get_rely(tab)
        if not label:
            label = self.label_txt(name)
        item_w = label_to_input_ratio * (1-2*margin)
        self.vars[name] = StringVar(value=self.pkl.pkl(
            name, empty_return=empty_return), name=name)

        a = ttk.Label(root, text=label, style='new.TLabel')
        indent = margin
        a.place(relx=indent, rely=rely, relwidth=item_w)

        relwidth = (1-label_to_input_ratio) * (1-2*margin)
        if end_label != None:
            relwidth = (1-2*label_to_input_ratio) * (1-2*margin)

        b = ttk.Combobox(
            root, justify=CENTER, textvariable=self.vars[name], values=values, state='readonly')
        if savable:
            b.bind("<<ComboboxSelected>>", partial(
                self.callback, self.vars[name]))
        indent += item_w
        b.place(relx=indent, rely=rely, relwidth=relwidth)

        if end_label != None:
            indent += relwidth+0.01
            c = ttk.Label(root, text=end_label, style='new.TLabel')
            c.place(relx=indent, rely=rely, relwidth=item_w)

    def add_chekbox(self, tab, name: str, label_to_input_ratio=0.5, label: str = None, empty_return: str = '', margin: float = 0):
        root = self.vars[tab]
        rely = self.get_rely(tab)
        if not label:
            label = self.label_txt(name)
        item_w = label_to_input_ratio * (1-2*margin)
        self.vars[name] = StringVar(value=self.pkl.pkl(
            name, empty_return=empty_return), name=name)

        a = ttk.Label(root, text=label, style='new.TLabel')
        indent = margin
        a.place(relx=indent, rely=rely, relwidth=item_w)
        relwidth = (1-label_to_input_ratio) * (1-2*margin)
        b = Checkbutton(root, command=partial(self.callback, self.vars[name]), background=self.bg_color, activebackground=self.bg_color,
                        highlightcolor=self.bg_color, highlightbackground=self.bg_color, borderwidth=None, variable=self.vars[name], onvalue=1, offvalue=0)
        indent += item_w
        b.place(relx=indent, rely=rely, relwidth=relwidth)

    def add_button(self, tab, name: str, label: str = None, bg: str = 'green', command=None, margin: float = 0):
        root = self.vars[tab]
        rely = self.get_rely(tab)
        indent = margin
        relwidth = 1-2*indent
        # self.vars[name] = StringVar(value=self.pkl.pkl(name,empty_return=empty_return),name=name)
        btn =  Button(root, text=label, bg=bg)
        if type(command)!=type(None):
            btn.config(command=partial(command,self.vars))
        self.vars[name] =btn
        self.vars[name].place(relx=indent, rely=rely, relwidth=relwidth)

    def add_frame(self,tab, name: str,fill_raw=1,relwidth=1,relx=0):
        root = self.vars[tab]
        rely = self.get_rely(tab)
        for _ in range(fill_raw-1):
            self.get_row(tab)
        rely2= self.get_rely(tab)
        
        self.vars[name] = Frame(root)
        self.vars[name].place(relx=relx,rely=rely,relwidth=relwidth,relheight=abs(rely2-rely))
      
    def add_label_text(self, tab, name: str, label_to_input_ratio=0.5, label: str = None, savable: bool = True, empty_return: str = '', margin: float = 0,height=2,state=DISABLED):
        root = self.vars[tab]
        rely = self.get_rely(tab)
        if not label:
            label = self.label_txt(name)
        item_w = label_to_input_ratio * (1-2*margin)
        a = ttk.Label(root, text=label, style='new.TLabel')
        indent = margin
        a.place(relx=indent, rely=rely, relwidth=item_w)

        relwidth = (1-label_to_input_ratio) * (1-2*margin)
        

        self.vars[name] = Text(root ,height= height)
        self.vars[name].config(state=state)
        indent += item_w
        self.vars[name].place(relx=indent, rely=rely, relwidth=relwidth)
        
    def add_tabel(self, tab, name: str,columns_dict:dict,inputs_show='v',remoev_duplicate=None):
        '''
        columns_dict:
        w : columns width
        justify':RIGHT
        filter : list of finction
        options: auto complete options
        defulte_text: string
        action : function
        is_timestamp: bool or str format filter_column=sum , selection
        
        '''
        root = self.vars[tab]
        if remoev_duplicate!=None:
            remoev_duplicate=name+remoev_duplicate
        table =Custom_Table(name, root, self.vars, self.pkl.pkl,columns_dict,inputs_show=inputs_show,remoev_duplicate=remoev_duplicate)
        table.show_data()

    def close(self,func=None,*args,**fun_kargs):
        if type(func)!=type(None):
            func(**fun_kargs)
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    pass