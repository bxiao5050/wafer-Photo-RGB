
import tkinter
from tkinter import *
from tkinter import ttk
import threading
import time
from tkinter import filedialog, messagebox
from imageProcess import ImageProcess
import os

class Batch():
    def __init__(self, master, treeview, save_path, dirname):
        self.save_path = save_path
        self.dirname = dirname
        self.treeview = treeview
        self.w = Toplevel(master)
        self.w.grab_set()
        self.w.title('batch process')
        # self.w.pack()
        Button(self.w, text = 'choose a folder to save results', command = self._on_path).grid(row = 0, column = 0, sticky = 'w', padx = (5,5), pady = (5,2))
        self.dirPath = Entry(self.w, width = 120)
        self.dirPath.insert(0, self.save_path)
        self.dirPath.grid(row = 1, column = 0, columnspan = 2,sticky = 'w', padx = (5,5))

        self.var_wafer = IntVar(value = 1)
        self.var_rgb_data = IntVar(value = 1)

        check_f = LabelFrame(self.w, text = 'choose which files to save', fg = 'blue')
        check_f.grid(row = 2, column = 0, sticky = 'w', pady = (5,5), padx = (5,5))
        Checkbutton(check_f, text = 'wafer image', variable = self.var_wafer, fg= 'blue',onvalue = 1, offvalue = 0, command = self._on_wafer).pack(side = 'left', padx = (5,5))
        Checkbutton(check_f, text = 'RGB .cvs', variable = self.var_rgb_data,  fg= 'blue',onvalue = 1, offvalue = 0,command = self._on_rgb_data).pack(side = 'left', padx = (5,5))
        Button(self.w, text = 'run', width = 8, fg = 'red', command=self._on_run).grid(row = 3, column =1, sticky = 'e', padx = (5,5), pady = (5,5))

    def _on_run(self):
        self.run(self.treeview)

        self.w.destroy()



    def _on_wafer(self):
        self.var_wafer.set(0) if self.var_wafer.get() ==0 else self.var_wafer.set(1)

    def _on_rgb_data(self):
        self.var_rgb_data.set(0) if self.var_rgb_data.get() ==0 else self.var_rgb_data.set(1)

    def _on_path(self):
        self.save_path = filedialog.askdirectory()
        self.dirPath.delete(0, 'end')
        self.dirPath.insert(0, self.save_path)


    def run(self, treeview):
        threading.Thread(target = lambda treeview = treeview:self.go(treeview)).start()


    def go(self, treeview):
        succeed = 0
        fail = 0
        for index in treeview.get_children():
            treeview.focus(index)
            treeview.selection_set(index)
            treeview.item(index, tags = index)
            imageName = self.treeview.item(index, 'text')

            try:
                imageProcess = ImageProcess(os.path.join(self.dirname,imageName))
                image_path = os.path.join(self.save_path,imageName[:-4])
                if self.var_rgb_data.get() ==1:
                    imageProcess.save_rgb_data(image_path)
                if self.var_wafer.get() ==1:
                    imageProcess.save_wafer_image(image_path)
                treeview.tag_configure(index, background='lightgreen')
                succeed += 1
            except:
                treeview.tag_configure(index, background='tomato')
                fail +=1
                pass

            time.sleep(0.2)
        messagebox.showinfo(message =f'{succeed} succeeded and {fail} failed')





def main():
    # print(version('tkinter'))
    # import pkg_resources
    # print(pkg_resources.get_distribution('tkinter').version)
    root = Tk()
    # treeview = ttk.Treeview(root)

    # treeview.pack()
    # for i in range(8):
    #     treeview.insert("", 'end', text = i)

    #     ttk.Style().theme_use('clam')
    Batch(root)
    # app = Batch().run(treeview)

    root.mainloop()

if __name__ == '__main__':
    main()
