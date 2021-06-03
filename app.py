import os
import shutil
from tkinter import *
import win32evtlog
import winshell


class MainWindow:
    def __init__(self, master):
        self.lbl_title = Label(root, text="Basic Cleaner", fg="#4d4d4d", font=(None, 20)).grid(row=0, column=0,
                                                                                               columnspan=2,
                                                                                               pady=(20, 0))
        cb_frame = Frame(master).grid(row=1, column=0)

        self.cb_temp_files_value = BooleanVar()
        self.cb_temp_files = Checkbutton(cb_frame, text="Archivos Temporales", onvalue=True, offvalue=False,
                                         variable=self.cb_temp_files_value, command=self.check_uncheck_children)
        self.cb_temp_files.grid(row=1, column=0, sticky="w", padx=20)

        self.cb_temp_value = BooleanVar()
        self.cb_temp = Checkbutton(cb_frame, text="Temp", onvalue=True, offvalue=False, variable=self.cb_temp_value,
                                   command=self.check_uncheck_parent)
        self.cb_temp.grid(row=2, column=0, sticky="w", padx=30)

        self.cb_temp2_value = BooleanVar()
        self.cb_temp2 = Checkbutton(cb_frame, text="%Temp%", onvalue=True, offvalue=False,
                                    variable=self.cb_temp2_value, command=self.check_uncheck_parent)
        self.cb_temp2.grid(row=3, column=0, sticky="w", padx=30)

        self.cb_prefetch_value = BooleanVar()
        self.cb_prefetch = Checkbutton(cb_frame, text="Prefetch", onvalue=True, offvalue=False,
                                       variable=self.cb_prefetch_value, command=self.check_uncheck_parent)
        self.cb_prefetch.grid(row=4, column=0, sticky="w", padx=30)

        self.cb_temp_files_children = [self.cb_temp, self.cb_temp2, self.cb_prefetch]

        self.cb_event_log = BooleanVar()
        Checkbutton(cb_frame, text="Registro Visor Eventos", onvalue=True, offvalue=False,
                    variable=self.cb_event_log).grid(row=5, column=0, sticky="w",
                                                     padx=20)

        self.cb_recycle_bin = BooleanVar()
        Checkbutton(cb_frame, text="Papelera de Reciclaje", onvalue=True, offvalue=False,
                    variable=self.cb_recycle_bin).grid(row=6, column=0, sticky="w",
                                                       padx=20)

        self.cb_downloads = BooleanVar()
        Checkbutton(cb_frame, text="Descargas", onvalue=True, offvalue=False,
                    variable=self.cb_downloads).grid(row=7, column=0, sticky="w", padx=20)

        self.btn_clean = Button(root, text="Limpiar", bg="#3f74d4", fg="#eeeeee", pady=10, padx=10, borderwidth=0,
                                font=(None, 10), command=self.clean).grid(row=9, column=1, padx=20,
                                                                          pady=(0, 20), sticky="e")

        self.lst = Listbox(root, borderwidth=0, highlightthickness=0, font=(None, 12), activestyle=NONE)
        self.lst.grid(row=8, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

    def deleteFiles(self, paths):
        for path in paths:
            with os.scandir(path) as entries:
                for entry in entries:
                    if entry.is_file():
                        try:
                            os.remove(entry)
                            self.lst.insert(END, f'{entry.name} Eliminado con éxito')
                            self.lst.itemconfig(END, {'fg': 'green'})
                        except Exception as e:
                            self.lst.insert(END, f'{e} al eliminar el archivo {entry.name}')
                            self.lst.itemconfig(END, {'fg': 'red'})
                    elif entry.is_dir():
                        try:
                            shutil.rmtree(entry)
                            self.lst.insert(END, f'Carpeta {entry.name} Eliminada con éxito')
                            self.lst.itemconfig(END, {'fg': 'green'})
                        except Exception as e:
                            self.lst.insert(END, f'{e} al eliminar la carpeta {entry.name}')
                            self.lst.itemconfig(END, {'fg': 'red'})

    def clearAllEventLog(self):
        log_types = ['Application', 'Security', 'Setup', 'System', 'Forwarded Events']
        for logtype in log_types:
            try:
                handle = win32evtlog.OpenEventLog(None, logtype)
                win32evtlog.ClearEventLog(handle, None)
                self.lst.insert(END, f'Registo {logtype} limpiado con éxito')
                self.lst.itemconfig(END, {'fg': 'green'})
            except Exception as e:
                self.lst.insert(END, f'{e} al eliminar el registro {logtype}')
                self.lst.itemconfig(END, {'fg': 'red'})

    def emptyRecycleBin(self):
        r = list(winshell.recycle_bin())
        if len(r) > 0:
            winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
            self.lst.insert(END, 'Papelera de reciclaje vaciada con éxito')
            self.lst.itemconfig(END, {'fg': 'green'})
        else:
            self.lst.insert(END, 'Papelera de reciclaje sin elementos')
            self.lst.itemconfig(END, {'fg': 'red'})

    def clean(self):

        if self.lst.size() > 0:
            self.lst.delete(0, END)

        if self.cb_temp_files_value.get():
            if self.cb_temp_value.get():
                self.deleteFiles(['C:/Windows/Temp'])
            if self.cb_temp2_value.get():
                self.deleteFiles([os.environ['TMP']])
            if self.cb_prefetch_value.get():
                self.deleteFiles(['C:/Windows/Prefetch'])

        if self.cb_event_log.get():
            self.clearAllEventLog()

        if self.cb_downloads.get():
            self.deleteFiles([os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads')])

        if self.cb_recycle_bin.get():
            self.emptyRecycleBin()

    def check_uncheck_children(self):
        for cb in self.cb_temp_files_children:
            if self.cb_temp_files_value.get():
                cb.select()
            else:
                cb.deselect()

    def check_uncheck_parent(self):
        if self.cb_temp_value.get() or self.cb_temp2_value.get() or self.cb_prefetch_value.get():
            self.cb_temp_files.select()
        else:
            self.cb_temp_files.deselect()


def centerWindow(master, width, height):
    position_right = int(master.winfo_screenwidth() / 2 - width / 2)
    position_down = int(master.winfo_screenheight() / 3 - height / 2)
    master.geometry("+{}+{}".format(position_right, position_down))


root = Tk()
root.title("Basic Cleaner")
root.minsize(width=600, height=400)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(8, weight=1)
centerWindow(root, 600, 400)
app = MainWindow(root)
root.mainloop()
