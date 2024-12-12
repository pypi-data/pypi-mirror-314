import json
import os
import random
import string
import time
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import webbrowser
import uuid
from datetime import datetime
from tkinter import ttk
from tkinter import *


class DataEntryForm(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.file_path_list = []
        hdr_txt = "A Real-time Strain Submission Platform"
        hdr = tk.Label(master, text=hdr_txt, font=("Arial", 16, "bold"), bg='white')
        hdr.pack(pady=20)

        slframe = tk.Frame(master, pady=10, bg='white')
        slframe.pack()
        sltb = tk.Label(slframe, text="Select fastq files", font=("Arial", 10, "bold"), width=32, fg='black',
                        bg="lightgreen", relief=FLAT)
        sltb.pack(side=tk.LEFT)
        sltb.bind('<Button-1>', self.select_file)

        ctb = tk.Label(slframe, text="Clear", width=5, fg='black', font=("Arial", 10, "bold"), bg="red",
                       relief=FLAT)
        ctb.pack(side=tk.RIGHT, padx=10)
        ctb.bind('<Button-1>', self.clear)

        self.file_list_frame = tk.Frame(master)
        self.file_list_frame.pack(pady=5)
        self.file_list_label = tk.Label(self.file_list_frame, wraplength=300, bg='white', fg='black',
                                        font=("Arial", 10, "bold"), relief=FLAT)
        self.file_list_label.pack()

        Departmentframe = tk.Frame(master, pady=10, bg='white')
        Departmentframe.pack()
        Departmentlabel = tk.Label(Departmentframe, text='Department:', bg='white', fg='black',
                                   font=("Arial", 10, "bold"), relief=FLAT)
        Departmentlabel.pack(side=tk.LEFT)

        self.department = tk.Entry(Departmentframe, highlightthickness=1, fg='black', font=("Arial", 10, "bold"),
                                   width=33, relief=FLAT)
        self.department.pack(side=tk.RIGHT, padx=8)

        scframe = tk.Frame(master, pady=10, bg='white')
        scframe.pack()
        cantb = tk.Label(scframe, text="Cancel", width=18, fg='black', bg="red", highlightthickness=1,
                         font=("Arial", 10, "bold"), relief=FLAT)
        cantb.pack(side=tk.LEFT)
        cantb.bind('<Button-1>', self.cancel)

        subtb = tk.Label(scframe, text="Submit", width=18, fg='black', bg="lightgreen", highlightthickness=1,
                         font=("Arial", 10, "bold"), relief=FLAT)
        subtb.pack(side=tk.RIGHT, padx=20)
        subtb.bind('<Button-1>', self.submit)

        self.index = 0
        self.uid = uuid.UUID(int=uuid.getnode()).hex[-12:]
        # self.uid = '72c94ee169f5'
        url = f"http://www.metakssdcoabundance.link/kssdtree/v2/personal?uid={self.uid}"
        r = requests.get(url)
        result = json.loads(r.text)
        self.ids = []
        self.samples = []
        self.speciess = []
        self.views = []
        self.departments = []
        self.dates = []
        self.ps = []
        self.first = False
        if result['code'] == 200:
            data = result['result']
            if len(data) > 0:
                self.first = True
                for x in data:
                    self.ids.append(x['id'])
                    self.samples.append(x['sample'])
                    self.speciess.append(x['species'])
                    self.departments.append(x['department'])
                    self.dates.append(x['date'])
                    self.views.append(x['view'])
                    self.ps.append(x['p'])
        if len(self.ids) > 0:
            line = tk.Label(self.master,
                            text="------------------------------------------------------------------------------------------------------------------------------------",
                            fg='lightgray', bg='white')
            line.pack(pady=2)
            my = tk.Label(master, text="My Submission", font=("Arial", 14, "bold"), bg='white')
            my.pack(pady=2)

            vdframe = tk.Frame(master, pady=5, bg='white')
            vdframe.pack(pady=10, side=tk.RIGHT, padx=5)

            vtb = tk.Label(vdframe, text="View", width=5, fg='black', bg="lightgreen", highlightthickness=1,
                           font=("Arial", 10, "bold"), relief=FLAT)
            vtb.pack(side=tk.LEFT)
            vtb.bind('<Button-1>', self.view)

            dtb = tk.Label(vdframe, text="Delete", width=5, fg='black', bg="red", highlightthickness=1,
                           font=("Arial", 10, "bold"), relief=FLAT)
            dtb.pack(side=tk.RIGHT, padx=5)
            dtb.bind('<Button-1>', self.delete)

            f = ttk.Frame(master)
            s = ttk.Scrollbar(f)
            self.t = ttk.Treeview(f, columns=('c1', 'c2', 'c3', 'c4', 'c5'), show="headings",
                                  yscrollcommand=s.set)
            s.config(command=self.t.yview)
            f.pack(pady=5)
            s.pack(side='right', fill='y')
            self.t.pack(side='left', fill='y')

            self.t.pack(pady=5)
            self.t.column('c1', width=80, anchor='center')
            self.t.column('c2', width=220, anchor='center')
            self.t.column('c3', width=220, anchor='center')
            self.t.column('c4', width=150, anchor='center')
            self.t.column('c5', width=150, anchor='center')

            self.t.heading('c1', text='No')
            self.t.heading('c2', text='Sample')
            self.t.heading('c3', text='Species')
            self.t.heading('c4', text='Placement position')
            self.t.heading('c5', text='Submission date')

            for i in range(len(self.ids)):
                self.t.insert('', i + 1,
                              values=[i + 1, self.samples[i], self.speciess[i], self.ps[i], self.dates[i]])
            self.t.bind("<<TreeviewSelect>>", self.on_item_selected)

    def on_item_selected(self, event):
        ss = self.t.selection()
        if len(ss) > 1:
            self.index = -1
        else:
            selected_item = self.t.selection()[0]
            item_value = self.t.item(selected_item)
            self.index = int(item_value['values'][0]) - 1
            print(self.index)

    def view(self, event):
        print('view: ', self.index)
        if self.index != -1:
            webbrowser.open(self.views[self.index])
        else:
            messagebox.showwarning("Warning", f"Don't support multiple view", default="ok",
                                   icon="warning")

    def delete(self, event):
        print('delete: ', self.index)
        if self.index != -1:
            ok = messagebox.askyesno("Warning", f"Delete this submission?",
                                     icon="warning")
            if ok:
                id = self.ids[self.index]
                url = f"http://www.metakssdcoabundance.link/kssdtree/v2/personal_del?id={id}"
                r = requests.get(url)
                result = json.loads(r.text)
                if result['code'] == 200:
                    ID = self.t.get_children()[self.index]
                    self.t.delete(ID)
                    print('delete success')
                    self.clear_treeview()
                    url = f"http://www.metakssdcoabundance.link/kssdtree/v2/personal?uid={self.uid}"
                    r = requests.get(url)
                    result = json.loads(r.text)
                    self.ids = []
                    self.samples = []
                    self.speciess = []
                    self.views = []
                    self.departments = []
                    self.dates = []
                    self.ps = []
                    if result['code'] == 200:
                        data = result['result']
                        if len(data) > 0:
                            self.first = True
                            for x in data:
                                self.ids.append(x['id'])
                                self.samples.append(x['sample'])
                                self.speciess.append(x['species'])
                                self.departments.append(x['department'])
                                self.dates.append(x['date'])
                                self.views.append(x['view'])
                                self.ps.append(x['p'])
                    if len(self.ids) > 0:
                        for i in range(len(self.ids)):
                            self.t.insert('', i + 1,
                                          values=[i + 1, self.samples[i], self.speciess[i], self.ps[i], self.dates[i]])
                        self.t.bind("<<TreeviewSelect>>", self.on_item_selected)
        else:
            messagebox.showwarning("Warning", f"Don't support multiple delete", default="ok",
                                   icon="warning")

    def clear_treeview(self):
        for item in self.t.get_children():
            self.t.delete(item)

    def select_file(self, event):
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            valid_files = []
            for file_path in file_paths:
                if file_path.endswith('.fq') or file_path.endswith('.fq.gz') or file_path.endswith(
                        '.fastq') or file_path.endswith('.fastq.gz'):
                    valid_files.append(file_path)
                else:
                    messagebox.showwarning("Warning", f"{file_path} is not a fastq file !!!", default="ok",
                                           icon="warning")
            if valid_files:
                for path in valid_files:
                    self.file_path_list.append(path)
                file_list_str = '\n'.join([path.split('/')[-1] for path in self.file_path_list])
                self.file_list_label.config(text=f"{file_list_str}")

    def clear(self, event):
        if len(self.file_path_list) > 0:
            self.file_path_list = []
            self.file_list_label.config(text='')

    def get_parent_dir(self, file_paths):
        if not file_paths:
            return None
        common_dir = os.path.dirname(file_paths[0])
        for path in file_paths[1:]:
            while not path.startswith(common_dir):
                common_dir = os.path.dirname(common_dir)
        return common_dir

    def get_city(self):
        response = requests.get("http://httpbin.org/ip")
        ip_address = response.json()['origin']
        api_key = 'bc804966ff0fe2'
        url = f'https://ipinfo.io/{ip_address}/json?token={api_key}'
        response = requests.get(url)
        data = response.json()
        city = data.get('city')
        country = data.get('country')
        lat, lon = data.get('loc', '0,0').split(',')
        location = f'{city}, {country}'
        return location, lon, lat

    def upload_file(self, file_path_list, city, lon, lat, department, date):
        print('file_path_list: ', file_path_list)
        species_list = []
        common_dir = self.get_parent_dir(file_path_list)
        shuf_file = os.path.join(common_dir, 'L3K10.shuf')
        if not os.path.exists(shuf_file):
            print('Downloading...', shuf_file)
            start_time = time.time()
            url = 'http://www.metakssdcoabundance.link/kssdtree/shuf/L3K10.shuf'
            headers = {'Accept-Encoding': 'gzip, deflate'}
            response = requests.get(url, headers=headers, stream=True)
            with open(shuf_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            end_time = time.time()
            if end_time - start_time > 200:
                print(
                    "Network timeout, please manually download from https://zenodo.org/records/12699159")
                return False
            print('Finished')
        for x in file_path_list:
            timeStamp = int(time.mktime(time.localtime(time.time())))
            letters = string.ascii_lowercase
            numbers = string.digits
            random_letters = ''.join(random.choice(letters) for i in range(6))
            random_numbers = ''.join(random.choice(numbers) for i in range(3))
            ln = 'sspp' + random_letters + random_numbers
            qry_sketch = ln + '_sketch_' + str(timeStamp)
            genome_files = x
            import kssdutils
            print('shuf_file: ', shuf_file)
            print('genome_files: ', genome_files)
            kssdutils.sketch(shuf_file=shuf_file, genome_files=genome_files, output=qry_sketch, set_opt=True)
            zip_file = qry_sketch + '.zip'
            zip = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED)
            for item in os.listdir(qry_sketch):
                zip.write(qry_sketch + os.sep + item)
            zip.close()

            url = "http://www.metakssdcoabundance.link/kssdtree/v2/upload"
            header = {
                "kssdtreev2": 'uploadl'
            }

            sample = x.split('/')[-1]
            data = {
                'uid': self.uid,
                'sample': sample,
                'city': city,
                "lon": lon,
                'lat': lat,
                's_depart': department,
                "s_date": date
            }
            print(data)
            current_path = os.getcwd()
            files = {'file': open(os.path.join(current_path, zip_file), "rb")}
            res = requests.post(url=url, headers=header, data=data, files=files)
            print(res.status_code)
            if res.status_code == 200:
                response = res.text
                json_data = json.loads(response)
                species = json_data['species']
                species_list.append(species)
            else:
                pass

        if len(species_list) == len(file_path_list):
            self.file_path_list = []
            self.file_list_label.config(text='')
            if self.first:
                self.clear_treeview()
                url = f"http://www.metakssdcoabundance.link/kssdtree/v2/personal?uid={self.uid}"
                r = requests.get(url)
                result = json.loads(r.text)
                self.ids = []
                self.samples = []
                self.speciess = []
                self.views = []
                self.departments = []
                self.dates = []
                self.ps = []
                if result['code'] == 200:
                    data = result['result']
                    if len(data) > 0:
                        self.first = True
                        for x in data:
                            self.ids.append(x['id'])
                            self.samples.append(x['sample'])
                            self.speciess.append(x['species'])
                            self.departments.append(x['department'])
                            self.dates.append(x['date'])
                            self.views.append(x['view'])
                            self.ps.append(x['p'])
                if len(self.ids) > 0:
                    for i in range(len(self.ids)):
                        self.t.insert('', i + 1,
                                      values=[i + 1, self.samples[i], self.speciess[i], self.ps[i], self.dates[i]])
                    self.t.bind("<<TreeviewSelect>>", self.on_item_selected)
            else:
                url = f"http://www.metakssdcoabundance.link/kssdtree/v2/personal?uid={self.uid}"
                r = requests.get(url)
                result = json.loads(r.text)
                self.ids = []
                self.samples = []
                self.speciess = []
                self.views = []
                self.departments = []
                self.dates = []
                self.ps = []
                if result['code'] == 200:
                    data = result['result']
                    if len(data) > 0:
                        for x in data:
                            self.ids.append(x['id'])
                            self.samples.append(x['sample'])
                            self.speciess.append(x['species'])
                            self.departments.append(x['department'])
                            self.dates.append(x['date'])
                            self.views.append(x['view'])
                            self.ps.append(x['p'])
                if len(self.ids) > 0:
                    line = tk.Label(self.master,
                                    text="------------------------------------------------------------------------------------------------------------------------------------",
                                    fg='lightgray', bg='white')
                    line.pack(pady=2)
                    my = tk.Label(self.master, text="My Submission", font=("Arial", 14, "bold"), bg='white')
                    my.pack(pady=2)

                    vdframe = tk.Frame(self.master, pady=5, bg='white')
                    vdframe.pack(pady=10)
                    vtb = tk.Label(vdframe, text="View", width=5, fg='black', bg="lightgreen", highlightthickness=1,
                                   font=("Arial", 10, "bold"), relief=FLAT)
                    vtb.pack(side=tk.LEFT)
                    vtb.bind('<Button-1>', self.view)

                    dtb = tk.Label(vdframe, text="Delete", width=5, fg='black', bg="red", highlightthickness=1,
                                   font=("Arial", 10, "bold"), relief=FLAT)
                    dtb.pack(side=tk.RIGHT, padx=5)
                    dtb.bind('<Button-1>', self.delete)

                    f = ttk.Frame(self.master)
                    s = ttk.Scrollbar(f)
                    self.t = ttk.Treeview(f, columns=('c1', 'c2', 'c3', 'c4', 'c5'), show="headings",
                                          yscrollcommand=s.set)
                    s.config(command=self.t.yview)
                    f.pack(pady=5)
                    s.pack(side='right', fill='y')
                    self.t.pack(side='left', fill='y')

                    self.t.pack(pady=5)
                    self.t.column('c1', width=80, anchor='center')
                    self.t.column('c2', width=220, anchor='center')
                    self.t.column('c3', width=220, anchor='center')
                    self.t.column('c4', width=150, anchor='center')
                    self.t.column('c5', width=150, anchor='center')

                    self.t.heading('c1', text='No')
                    self.t.heading('c2', text='Sample')
                    self.t.heading('c3', text='Species')
                    self.t.heading('c4', text='Placement position')
                    self.t.heading('c5', text='Submission date')

                    for i in range(len(self.ids)):
                        self.t.insert('', i + 1,
                                      values=[i + 1, self.samples[i], self.speciess[i], self.ps[i], self.dates[i]])
                    self.t.bind("<<TreeviewSelect>>", self.on_item_selected)
        else:
            messagebox.showwarning("Warning", f"Upload failed !!!", default="ok",
                                   icon="warning")

    def submit(self, event):
        if len(self.file_path_list) == 0:
            messagebox.showwarning("Warning", f" Please select a fastq file or multiple fastq files !!!",
                                   default="ok",
                                   icon="warning")
        else:
            if self.department.get() == '':
                messagebox.showwarning("Warning", f"Department can not be empty !!!",
                                       default="ok",
                                       icon="warning")
            else:
                department = self.department.get()
                city, lon, lat = self.get_city()
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(date)
                self.upload_file(self.file_path_list, city, lon, lat, department, date)

    def cancel(self, event):
        self.quit()


def isConnected():
    try:
        html = requests.get("https://www.baidu.com", timeout=5)
        print("Network available")
        return 1
    except:
        print("Network connection exception")
        return 0


def show():
    root = tk.Tk()

    window_width = 1000
    window_height = 500

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    root.geometry(f'{window_width}x{window_height}+{x}+{y}')
    # if isConnected():
    #     DataEntryForm(root)
    # else:
    #     messagebox.showwarning("Warning", f"Network connection exception", default="ok",
    #                            icon="warning")
    root.config(bg="#ffffff")
    root.title("SSBPP")
    root.resizable(height=False, width=False)
    DataEntryForm(root)
    root.mainloop()
