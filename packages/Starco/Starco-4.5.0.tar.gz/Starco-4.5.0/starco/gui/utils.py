from threading import Thread
from functools import partial
from time import sleep
from tkinter import *
from tkinter import ttk
import tkinter
from datetime import datetime
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import mplfinance as mpf
import pandas as pd
from datetime import datetime
from time import sleep
# import matplotlib.pyplot as plt
# import numpy as np
# from scipy.stats import linregress
from starco.debug import Debug

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)            
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        # print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom


class Custom_Table:
    def __init__(self, pfx_name, root, var, pkl, columns_dict, **args) -> None:
        '''
            columns_dict:
                    w : columns width
                    justify':RIGHT
                    filter : list of finction
                    options: auto complete options
                    defulte_text: string
                    action : function
                    is_timestamp: bool or str format
                    filter_column=sum , selection
            
            inputs_show='h'
            frame_width=0
            frame_height=0
            updatable = False
            add_id=True
            add_rmv=True
            update_widget_data =[]
            tag_red_green=column name
            self.remoev_duplicate!=None


        '''
        self.remoev_duplicate=args.get('remoev_duplicate')
        self.debug = Debug().debug
        self.pfx_name = pfx_name
        self.var = var
        self.pkl = pkl
        add_id=args.get('add_id',True)
        self.add_id = add_id
        add_rmv = args.get('add_rmv',True)
        self.add_rmv = add_rmv

        self.base_columns = columns_dict
        self.columns = self.base_columns
        self.action_columns=[]
        self.updatable = args.get('updatable',False)
        self.filterable_culumns={}
        if add_id:
            self.columns = {**{'id': {'w': 20}}, **self.columns}
        if add_rmv:
            self.columns = {**self.columns, **{'rmv': {'w': 20}}}
        self.inputs_show = args.get('inputs_show','h')
        self.root = root
        frame_height = args.get('frame_height',0)
        self.height = frame_height
        if frame_height == 0:
            self.height = root.winfo_height()
        frame_width = args.get('frame_width',0)
        self.width = frame_width
        if frame_width == 0:
            self.width = root.winfo_width()
        self.update_widget_data=args.get('update_widget_data',[])
        self.tag_red_green = args.get('tag_red_green','None')
        self.filters_var={}
        self.last_data=[]
        self.init_action_columns()
        self.init_filter_column()
        self.create()
    
    def init_action_columns(self):

        for i in self.base_columns:
            item = self.base_columns[i]
            if 'action' in item:
                self.action_columns+=[i]

    def init_filter_column(self):
        for k,v in self.columns.items():
            if v.get('filter_column')!=None:
                self.filterable_culumns[k]=v['filter_column']
    
    def apply_columns_filters(self,data):
        colsk = list(self.columns.keys())
        for k,v in self.filterable_culumns.items():
            idx = colsk.index(k)
            if v=='sum':
                sum_amounts=0
                for item in self.Tree.get_children():
                    sum_amounts += float(self.Tree.item(item)['values'][idx])
                self.filters_var[k]['text']=round(sum_amounts,2)
            elif len(data)>0 and v=='selection':
                combo_values=[]
                for item in data:
                    combo_values += [item[k]]
                self.filters_var[k+'combo']['values']=['']+list(set(combo_values))

    def setup_columns_filter(self,width_list,relheight):
        col_keys = list(self.columns.keys())
        relwidth= 1/len(self.columns)
        for k,v in self.filterable_culumns.items():
            col_idx = col_keys.index(k)
            
            if v=='sum':
                self.filters_var[k] = Label(self.root , justify=CENTER)

            elif v=='selection':
                self.filters_var[k] = StringVar(self.root,value='',name=k)
                self.filters_var[k+'combo'] = ttk.Combobox(self.root,textvariable=self.filters_var[k],state='readonly')
                k+='combo'
                self.filters_var[k].bind("<<ComboboxSelected>>",self.show_data)
            relx = col_idx * relwidth
    
            self.filters_var[k].place(relheight=relheight,relx=relx,relwidth = relwidth,rely=0)

    def create(self):
        tree_wlist = len(self.columns)*[100]
        for i, k in enumerate(self.columns):
            item = self.columns[k]
            if 'w' in item:
                tree_wlist[i] = item['w']
        relheight = .1
        self.setup_columns_filter(tree_wlist,relheight)

        def tcellw(x): return int(self.width*(tree_wlist[x]/sum(tree_wlist)))

        tree = ttk.Treeview(self.root, column=[self.tree_header_name(i) for i in self.columns], show='headings')
        self.Tree =tree
        if self.tag_red_green!='None':
            self.Tree.tag_configure(tagname='red', foreground='red')
            self.Tree.tag_configure(tagname='green', foreground='green')

        for i, k in enumerate(self.columns):
            tree.column(self.tree_header_name(k), anchor=CENTER, width=int(tcellw(i)))
            tree.heading(self.tree_header_name(k), text=k)
        self.var[self.pfx_name+'tree'] = tree
        if self.filterable_culumns:
            tree.bind("<Button-1>",
                  partial(self.disable_resizing))
        tree.bind("<ButtonRelease-1>",
                  partial(self.edite_delete_node))
        
        ################################################
        if self.inputs_show == 'h':
            rel_height_tree = .85
            rely = .9
            relwidth = (1/(len(self.base_columns)))-.02
        elif self.inputs_show == 'v':
            rel_height_tree = 1-(len(self.base_columns)+1)*.05
            rely = rel_height_tree+.05
            relwidth = .5
        else:
            rel_height_tree = 1

        relx = 0
        if self.filterable_culumns:
            rel_height_tree-=relheight
            tree.place(rely=relheight,relx=0, relheight=rel_height_tree, relwidth=1)
        else:tree.place(relx=0, relheight=rel_height_tree, relwidth=1)
        if self.inputs_show in ['h', 'v']:
            for k, v in self.base_columns.items():
                label = k
                if 'label' in v:
                    label = k['label']
                lbl = Label(self.root, anchor=CENTER, text=self.label_txt(
                    label))
                lbl.place(relx=relx, rely=rely, relwidth=relwidth)
                name = self.pfx_name+k
                self.var[name] = StringVar(value='', name=name)
                if self.inputs_show == 'h':
                    rely += .05

                if self.inputs_show != 'h':
                    relx = .5
                if 'options' in v:
                    inputs = AutocompleteCombobox(self.root,textvariable=self.var[name])
                    inputs.set_completion_list(v['options'])
                    inputs.focus_set()
                else:
                    inputs = Entry(self.root, justify=v.get(
                        'justify', CENTER), textvariable=self.var[name])
                if 'filter' in v:
                    if isinstance(v['filter'], list):
                        for i in v['filter']:
                            i(inputs)
                inputs.place(relx=relx, rely=rely, relwidth=relwidth)
                if self.inputs_show == 'h':
                    rely -= .05
                    relx += relwidth+.02
                else:
                    rely += .05
                    relx = 0
                inputs.bind('<Return>', partial(self.add_node))

    def label_txt(self, str_in):
        return str_in.replace("_", " ").title()+" : "

    def tree_header_name(self,item):
        return item.replace(' ','_')
    
    def disable_resizing(self, event, *args):
        try:
            
            tree = self.var[self.pfx_name+'tree']
            region = tree.identify("region", event.x, event.y)
            item = tree.selection()
            if region == "separator":
                return "break"
        except:pass

    def edite_delete_node(self, event, *args):
        try:
            tree = self.var[self.pfx_name+'tree']
            region = tree.identify("region", event.x, event.y)
            item = tree.selection()
            if region == "cell":
                item0 = tree.item(item[0])['values']
                id = int(item0[0] - 1)
                column_name = list(self.columns.keys())[int(tree.identify_column(event.x)[1:])-1]
                if column_name == 'rmv' and self.add_rmv:
                    # remove
                    data = self.pkl(
                        self.pfx_name, empty_return=[])
                    try:
                        data.pop(id)
                        self.pkl(self.pfx_name, data)
                        self.show_data()
                    except:
                        pass
                elif self.inputs_show != None and self.updatable:
                    data = self.pkl(
                        self.pfx_name, empty_return=[])
                    try:
                        item = data[id]
                        for k in item:
                            self.var[k].set(item[k])
                        data.pop(id)
                        self.pkl(self.pfx_name, data)
                        self.show_data()
                    except:
                        pass
                elif column_name in self.action_columns:
                    self.base_columns[column_name]['action'](tree.item(item[0]) , self.columns)
        except Exception as e:
            self.debug(e)

    def add_node(self, *arg):
        data = self.pkl(self.pfx_name, empty_return=[])
        cols = self.base_columns
        fs = {}
        for k in cols:
            fs[self.pfx_name+k] = self.var[self.pfx_name+k].get()
            self.var[self.pfx_name+k].set('')
        data += [fs]
        if self.remoev_duplicate!=None:
            try:
                data = pd.DataFrame(data).drop_duplicates(subset=self.remoev_duplicate, keep="first").to_dict('records')
            except Exception as e:self.debug(e)
        self.pkl(self.pfx_name, data)
        self.show_data()

    def do_update_widget(self ,data):

        if isinstance(self.update_widget_data,list):
            for i in self.update_widget_data:
                data = [j[i['target']] for j in data]
                obj = i['object']
                if isinstance(obj,AutocompleteCombobox):
                    obj.set_completion_list(data)
        else:
            i = self.update_widget_data
            data = [j[i['target']] for j in data]
            obj = i['object']
            if isinstance(obj,AutocompleteCombobox):

                obj.set_completion_list(data)

    def show_data(self ,data =[]):
        tree = self.var[self.pfx_name+'tree']
        try:
            tree.delete(*tree.get_children())
        except:
            pass
        if not isinstance(data,list):data=self.last_data
        if len(data)==0:
            saved_data = self.pkl(self.pfx_name, empty_return=[])
            data=[]
            for item in saved_data:
                data+=[dict(zip(self.base_columns.keys(),item.values()))]
        self.last_data=data
        self.do_update_widget(data)
        I=0
        for i, item in enumerate(data):
            values = []
            if self.add_id :values += [str(I+1)]
            tag=[]
            do_continue=False
            for key,base_column in self.base_columns.items():
                value = item.get(key,0)
                if 'defulte_text' in base_column:
                    value=base_column['defulte_text']
                elif 'is_timestamp' in base_column:
                    _format=base_column['is_timestamp']
                    if isinstance(_format,str):
                        value= convert_timestamp_to_strtime(value,_format)
                    else :
                        value= convert_timestamp_to_strtime(value)
                if key in self.filterable_culumns:
                    if self.filterable_culumns[key]=='selection':
                        selected = self.filters_var[key].get()
                        if selected!='' and value!=selected:
                            do_continue=True
                            break
                if self.tag_red_green == key:
                    if float(value)>=0:tag='green'
                    else:tag='red'
                values += [value]
            

            if do_continue:continue
            
            if self.add_rmv: values += ['X']
            tree.insert('', 'end', values=values,tag=tag)
            I+=1
        self.apply_columns_filters(data)

    def realtime_update(self,func):
        '''
        function(tree , item ,columns)
        '''
        try:
            tree = self.var[self.pfx_name+'tree']
            func(tree ,self)
            self.apply_columns_filters([])
        except Exception as e:self.debug(e)

# 
class AutocompleteCombobox(tkinter.ttk.Combobox):

    def set_completion_list(self, completion_list):
        """Use our completion list as our drop down selection menu, arrows move through menu."""
        self._completion_list = sorted(
            completion_list, key=str.lower)  # Work with a sorted list
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self['values'] = self._completion_list  # Setup our popup menu

    def autocomplete(self, delta=0):
        """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
        if delta:  # need to delete selection otherwise we would fix the current position
            self.delete(self.position, tkinter.END)
        else:  # set position to end so selection starts where textentry ended
            self.position = len(self.get())
        # collect hits
        _hits = []
        for element in self._completion_list:
            if element.lower().startswith(self.get().lower()):  # Match case insensitively
                _hits.append(element)
        # if we have a new hit list, keep this in mind
        if _hits != self._hits:
            self._hit_index = 0
            self._hits = _hits
        # only allow cycling if we are in a known hit list
        if _hits == self._hits and self._hits:
            self._hit_index = (self._hit_index + delta) % len(self._hits)
        # now finally perform the auto completion
        if self._hits:
            self.delete(0, tkinter.END)
            self.insert(0, self._hits[self._hit_index])
            self.select_range(self.position, tkinter.END)


    def handle_keyrelease(self, event):
        """event handler for the keyrelease event on this widget"""
        if event.keysym == "BackSpace":
            self.delete(self.index(tkinter.INSERT), tkinter.END)
            self.position = self.index(tkinter.END)
        if event.keysym == "Left":
            if self.position < self.index(tkinter.END):  # delete the selection
                self.delete(self.position, tkinter.END)
            else:
                self.position = self.position-1  # delete one character
                self.delete(self.position, tkinter.END)
        if event.keysym == "Right":
            self.position = self.index(tkinter.END)  # go to end (no selection)
        if len(event.keysym) == 1:
            self.autocomplete()
        # No need for up/down, we'll jump to the popup
        # list at the position of the autocompletion

def convert_timestamp_to_strtime(ts,format='%Y-%m-%d %H:%M:%S'):
    try:
        return datetime.utcfromtimestamp(int(ts)).strftime(format)
    except:pass
    return '0'

def find_neighbours(value, df, colname,lower_neighber=True):
    exactmatch = df[df[colname] == value]
    if not exactmatch.empty:
        return exactmatch.index
    else:
        lowerneighbour_ind = df[df[colname] < value][colname].idxmax()
        upperneighbour_ind = df[df[colname] >= value][colname].idxmin()
        if lower_neighber:
            return int(lowerneighbour_ind)
        else:return int(upperneighbour_ind)

# class Chart:
#     def __init__(self, name, root, pkl,var, **args) -> None:
#         '''
        
#         ploter='mpf',
#         type='candle'
#         scroll=False
#         limit=100
#         zoom_coffe=10
#         zoom_status:False
#         max_df_len=5000
#         fill_input_by_presskey_and_mouse_click=[{key:'t' , 'mouse_btn':1 ,target:'',filter:None}]
#         line_pkl_path=''
#         shapes_target_var=''
#         '''
#         self.var=var
#         self.name = name
#         self.root = root
#         self.pkl = pkl
#         self.ploter = args.get('ploter','mpf')
#         self.type = args.get('type','candle')
#         self.zoom_status = args.get('zoom_status',False)
#         self.scroll = args.get('scroll',False)
#         self.df =[]
#         self.base_limit = args.get('limit',100)
#         self.limit =  args.get('limit',100)
#         self.max_df_len =  args.get('max_df_len',5000)
#         self.status=None
#         self.pressed_key =None
#         self.zoom_coffe =args.get('zoom_coffe',10)
#         self.end_sequence=0
#         self.digits = 0
#         self.temp_lines=[]
#         self.busy=False
#         self.shapes=['trendLine','hLine','vLine']
#         self.line_pkl_path=args.get('line_pkl_path','')
#         self.shapes_target_var=args.get('shapes_target_var','')
#         self.fill_input_by_presskey_and_mouse_click=args.get('fill_input_by_presskey_and_mouse_click',[])
#         self.tp=-1
#         self.sl=-1
#         self.entry_points_list=[]
#         self.exit_points_list=[]
#         self.draw()

#     def draw(self):
#         if self.ploter=='mpf':
            
#             self.fig = mpf.figure(style=self.pkl(self.name+'style', empty_return='binance'))
#             self.ax = self.fig.add_subplot(1, 1, 1)
#             # frame1.axes.get_xaxis().set_visible(False)
#             self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
#             self.ax.axes.get_xaxis().set_visible(False)
#             self.fig.tight_layout()
#             # self.fig.use_sticky_edges = True
#             self.canvas.draw()
#             self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
#             self.canvas.mpl_connect('scroll_event', self._on_mousewheel)
#             self.canvas.mpl_connect('button_press_event', self._on_mousewheel)
#             self.canvas.mpl_connect('key_press_event', self._key_preesed)
#             self.canvas.mpl_connect('key_release_event', self._key_released)
#             self.canvas.mpl_connect('motion_notify_event', self._mouse_hover)
#             self.print_data = Label(self.root,anchor=CENTER)
#             self.print_data.place(rely=.95,relx=.93)
#             self.print_now_price = Label(self.root,anchor=CENTER)
#             self.print_now_price.place(rely=.01,relx=.93)
#         else:
#             self.fig = plt.figure()
#             self.ax = self.fig.add_subplot(1, 1, 1)
#             self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
#             self.canvas.draw()
#             self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    
#     def line_data_creator(self,lines_points):
#         result = []
#         if len(lines_points) > 0:
#             for i in lines_points:
#                 res = linregress(i[0], i[1])
#                 result += [[i[0][0], i[0][1], res.slope, res.intercept]]
#         return np.array(result)

#     def get_line_data(self, event , type_line):
#         # global temp_lines, lines
#         # start
#         try:
#             if event.button==1:
#                 y = float(event.ydata)
#                 x = int(round(event.xdata))

#                 self.temp_lines += [[x, y]]
#                 if type_line=='trendLine':
#                     try:
#                         if len(self.temp_lines) != 2:return
#                         temp_lines = self.temp_lines
#                         mn_id = np.argmin([temp_lines[0][0], temp_lines[1][0]])
#                         mx_id= np.argmax([temp_lines[0][0], temp_lines[1][0]])

#                         x1,x2 = temp_lines[mn_id][0], temp_lines[mx_id][0]
#                         x1 = int(self.show_df.iloc[x1].time)
#                         x2 = int(self.show_df.iloc[x2].time)
#                         y1,y2 = temp_lines[mn_id][1], temp_lines[mx_id][1]
#                         inputs = [[[x1,x2],[y1,y2]]]
#                         line = self.line_data_creator(inputs)[0]
#                         saved = self.pkl(self.shapes_target_var.get()+type_line,empty_return=[],path = self.line_pkl_path)
#                         saved += [line]
#                         self.pkl(self.shapes_target_var.get()+type_line,saved,path = self.line_pkl_path)
#                     except:pass
#                     self.temp_lines = []
#                 elif type_line=='hLine':
#                     try:
#                         temp_lines = self.temp_lines[0]
#                         y = temp_lines[1]
#                         saved = self.pkl(self.shapes_target_var.get()+type_line,empty_return=[],path = self.line_pkl_path)
#                         saved += [y]
#                         self.pkl(self.shapes_target_var.get()+type_line,saved,path = self.line_pkl_path)
#                     except:pass
#                     self.temp_lines = []
#                 elif type_line=='vLine':
#                     try:
#                         temp_lines = self.temp_lines[0]
#                         x = temp_lines[0]
#                         x = int(self.show_df.iloc[x].time)
#                         saved = self.pkl(self.shapes_target_var.get()+type_line,empty_return=[],path = self.line_pkl_path)
#                         saved += [x]
#                         self.pkl(self.shapes_target_var.get()+type_line,saved,path = self.line_pkl_path)
#                     except:pass
#                     self.temp_lines = []
#         except:
#             pass
   
#     def _mouse_hover(self,*args):
#         event = args[0]
#         data=event.ydata
#         if data!=None:
#             self.print_data['text'] = str(round(data,5))

#     def _key_preesed(self,*args):
#         event = args[0]
#         self.pressed_key = str(event.key)

#     def _key_released(self,*args):
#         self.pressed_key = None

#     def _on_mousewheel(self,*args):
#         if self.busy:return
#         self.busy=True
#         event = args[0]
#         btn = event.button
#         if btn in['down' , 'up' ,2] and self.pressed_key=='control' and self.zoom_status:
#             if btn == 'down':
#                 # deal with zoom in
#                 if self.limit <1000:
#                     self.limit+=self.zoom_coffe
#                 # scale_factor = 1/base_scale
#             elif btn == 'up':
#                 # deal with zoom out
#                 if self.limit>self.base_limit:
#                     self.limit -=self.zoom_coffe
#             elif btn==2:
#                 self.limit = self.base_limit
            
#             if len(self.df) > self.base_limit:
#                 if self.status=='pause':

#                     self._do_update()
#         elif  btn in['down' , 'up' ,2] and self.scroll:
#             if len(self.df)>0:
#                 if btn == 'down':
#                     # deal with zoom in
#                     if len(self.df) + self.end_sequence > self.base_limit:
#                         self.end_sequence -=1
#                     # scale_factor = 1/base_scale
#                 elif btn == 'up':
#                     # deal with zoom out
#                     if self.end_sequence<0:
#                         self.end_sequence +=1
#                 elif btn==2:
#                     self.end_sequence = 0
                
#                 if len(self.df) > self.base_limit:
#                     if self.status=='pause':
#                         self._do_update()
#         elif self.line_pkl_path!='' and btn==1 and  self.pressed_key=='d':
#             pass
#         elif self.line_pkl_path!='' and btn==3 and  self.pressed_key=='d':
#             for i in self.shapes:
#                 self.pkl(self.shapes_target_var.get()+i,[],path = self.line_pkl_path)
#         elif self.line_pkl_path!='' and btn==1 and self.line_box.get() in self.shapes:
#             self.get_line_data(event,self.line_box.get())
#         else:
#             event_to_do = self.fill_input_by_presskey_and_mouse_click
#             for i in event_to_do:
#                 if self.pressed_key==i.get('key') and btn==int(i.get('mouse_btn',-1)):
#                     try:
#                         data = round(event.ydata,self.digits)
#                         try:
#                             data = i.get('filter')(data)
#                         except:pass
#                         self.var[i.get('target')].set(data)
#                     except Exception as e:
#                         debug(e)
#         self.busy=False

#     def set_style_box(self,relx,rely,relwidth):
#         name = self.name+'style'
#         var = StringVar(value=self.pkl(
#             name, empty_return='binance'), name=name)
#         style_list = ['binance','blueskies','brasil','charles','checkers','classic','default','ibd','kenan','mike','nightclouds','sas','starsandstripes','yahoo']
#         combo = ttk.Combobox(self.root, justify=CENTER,
#                              textvariable=var, state='readonly', values=style_list)
#         combo.place(relx=relx, rely=rely, relwidth=relwidth)
#         combo.bind("<<ComboboxSelected>>", partial(self.style_changer,name,var))
    
#     def set_line_box(self,relx,rely,relwidth):
#         name = self.name+'line_box'
#         var = StringVar(value='None', name=name)
#         self.line_box=var
#         _list = ['None']+self.shapes
#         combo = ttk.Combobox(self.root, justify=CENTER,
#                              textvariable=var, state='readonly', values=_list)
#         combo.place(relx=relx, rely=rely, relwidth=relwidth)

#     def style_changer(self,name,var,*args):
#         self.pkl(name, var.get())
#         # self.canvas.get_tk_widget().delete('all')
#         # self.draw()

#     def _show_lines(self,time_frame):
#         tf_sec=time_frame*60
#         try:
#             start_seq = min(self.show_df.time)
#             end_seq = max(self.show_df.time)
#             min_price , max_price=min(self.show_df.low) , max(self.show_df.high)
#             vline=[]
#             temp_trendline=[]
#             try:
#                 temp_trendline=self.pkl(self.shapes_target_var.get()+'trendLine',empty_return =[],path = self.line_pkl_path)
#                 hline = self.pkl(self.shapes_target_var.get()+'hLine',empty_return =[],path = self.line_pkl_path)
#                 vline = self.pkl(self.shapes_target_var.get()+'vLine',empty_return =[],path = self.line_pkl_path)
                
#                 hline = dict(hlines=[i for i in hline if min_price<=i<=max_price])
#                 hline['colors'] = len(hline['hlines'])*['b']
#                 hline['linestyle'] = len(hline['hlines'])*['-']
#             except:
#                 hline = dict(hlines=[])
#                 hline['colors'] = []
#                 hline['linestyle'] = []
            
            
#             vline = [convert_timestamp_to_strtime(i) for i in vline if start_seq<=i<=end_seq]
#             step = int(abs(self.show_df.iloc[0].time - self.show_df.iloc[1].time))

#             if min_price<=self.tp<=max_price:
#                 hline['hlines']+=[self.tp]
#                 hline['colors']+=['g']
#                 hline['linestyle']+=['-.']
#             if min_price<=self.sl<=max_price:
#                 hline['hlines']+=[self.sl]
#                 hline['colors']+=['r']
#                 hline['linestyle']+=['-.']
                
#             add_plots=[]
#             if len(self.entry_points_list)>0:
#                 signal = np.array([np.nan]*len(self.show_df))
#                 idxs = list(self.show_df.time)
#                 for item in self.entry_points_list:

#                     item0=item[0]
#                     if tf_sec>0:
#                         item0-= (item0%tf_sec)
#                     if start_seq<=item0<=end_seq and min_price<=item[1]<=max_price:
#                         sel = find_neighbours(item0,self.show_df,'time')
#                         signal[sel] = item[1]

#                 add_plots+=[mpf.make_addplot(signal,ax=self.ax,type='scatter',markersize=50,marker='o',color='lime')]
            
#             if len(self.exit_points_list)>0:
#                 signal = np.array([np.nan]*len(self.show_df))
#                 idxs = list(self.show_df.time)
#                 item0=item[0]
#                 if tf_sec>0:
#                     item0-= (item0%tf_sec)

#                 for item in self.exit_points_list:
#                     if start_seq<=item0<=end_seq and min_price<=item[1]<=max_price:
#                         signal[idxs.index(item0)] = item[1]
#                 add_plots+=[mpf.make_addplot(signal,ax=self.ax,type='scatter',markersize=50,marker='x',color='red')]


            
#             trendline=[]
#             for i in temp_trendline:
#                 try:
#                     x= np.arange(int(i[0]),int(i[1]+step),step)
#                     sel = np.where(np.logical_and(x>=start_seq,x<=end_seq))[0]
#                     if len(sel)<=0:continue
#                     x= x[sel]
#                     y = x*i[2]+i[3]
#                     sel = np.where(np.logical_and(y>=min_price,y<=max_price))[0]
#                     if len(sel)<=0:continue
#                     y=y[sel]
#                     trendline+=[[
#                             (convert_timestamp_to_strtime(x[0]), y[0]),
#                             (convert_timestamp_to_strtime(x[-1]),y[-1])
#                         ]]
#                 except Exception as e:
#                     debug(e)
            
#             return hline , vline , trendline,add_plots
#         except Exception as e:debug(e)
#         return [],[],[] ,[]

#     def update(self, df,int_time_frame=0):
#         try:
#             if self.df.close.iloc[-1]==df.iloc[-1].close:return
#         except:pass
#         self.df = df
#         self.df = self.df.iloc[-1*(self.max_df_len):].reset_index(drop=True)
#         self._do_update(int_time_frame)

#     def _do_update(self,time_frame):
#         if self.status!='pause' and self.status!=None:self.end_sequence=0
#         if len(self.df) >= self.base_limit:
            
#             if self.end_sequence==0:
#                 self.show_df = self.df.iloc[-1*(self.limit):].copy()
#                 self.show_df.reset_index(drop=True,inplace=True)

#             else:
#                 start = -1*(self.limit) + self.end_sequence
#                 self.show_df = self.df.iloc[start:self.end_sequence].copy()
#             hline , vline , trendline,add_plots = self._show_lines(time_frame)
#             self.print_now_price['text']= self.show_df.close.iloc[-1]
#             self.ax.clear()
#             mpf.plot(
#                 self.df_ready(self.show_df.copy()),
#                 warn_too_much_data=1000, type=self.type,
#                  ax=self.ax,hlines=hline,vlines=vline,alines=trendline,addplot=add_plots)
#             self.canvas.draw_idle()

#     def df_ready(self, df):
#         if self.ploter == 'mpf':
#             df.columns = list(map(lambda x: x.capitalize(), list(df.columns)))
#             df['Date']=df['Time'].apply(convert_timestamp_to_second)
#             df['Date']=df['Time'].apply(convert_timestamp_to_strtime)
#             df['Date'] = pd.to_datetime(df['Date'])
#             df.set_index('Date', drop=True, inplace=True)
#             try:
#                 df.drop(columns=['Time'], inplace=True)
#             except:
#                 pass
#             try:
#                 df.drop(columns=['Volume'], inplace=True)
#             except:
#                 pass

#         return df
