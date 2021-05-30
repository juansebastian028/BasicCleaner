import os
from tkinter import *
import win32evtlog

root = Tk()
root.title("Basic Cleaner")
root.minsize(width=600, height=400)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

frame = Frame(root).grid(row=0, column=0, rowspan=3, columnspan=3, sticky='nsew')

lbl_title = Label(frame,
                  text="Basic Cleaner",
                  fg="#4d4d4d",
                  font=(None, 20)) \
    .grid(row=0, column=0, columnspan=2, pady=(20, 0))

listbox = Listbox(frame, borderwidth=0, highlightthickness=0, font=(None, 12), activestyle=NONE)
listbox.grid(row=1, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")

Button(frame,
       text="Archivos Temporales",
       bg="#3f74d4", fg="#eeeeee",
       pady=10,
       padx=10,
       borderwidth=0,
       font=(None, 10),
       command=lambda: deleteTempFiles()) \
    .grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")

Button(frame,
       text="Registro Visor Eventos",
       bg="#3f74d4", fg="#eeeeee",
       pady=10,
       padx=10,
       borderwidth=0,
       font=(None, 10),
       command=lambda: clearAllEventsLog()) \
    .grid(row=2, column=1, padx=20, pady=(0, 20), sticky="ew")


def deleteTempFiles():
    listbox.delete(0, END)
    paths = [os.environ['TMP'], 'C:/Windows/Temp', 'C:/Windows/Prefetch']
    for path in paths:
        with os.scandir(path) as entries:
            for entry in entries:
                try:
                    os.remove(entry)
                    listbox.insert(END, f'{entry.name} Eliminado con éxito')
                except:
                    pass
    if listbox.size() == 0:
        listbox.insert(END, 'No hay archivos temporales para borrar')


def clearAllEventsLog():
    listbox.delete(0, END)
    log_types = ['Application', 'Security', 'Setup', 'System', 'Forwarded Events']
    for logtype in log_types:
        handle = win32evtlog.OpenEventLog(None, logtype)
        win32evtlog.ClearEventLog(handle, None)
        listbox.insert(END, f'Registo {logtype} limpiado con éxito')


root.mainloop()

