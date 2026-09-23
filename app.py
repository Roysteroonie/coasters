import queue
import threading
import traceback
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from coaster_core import generate, read_players_xlsx

APP_TITLE = 'RLO Player Coaster Generator'

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry('760x610')
        self.minsize(720, 560)
        self.queue = queue.Queue()
        self.xlsx_path = tk.StringVar()
        self.output_dir = tk.StringVar(value=str(Path.home() / 'Documents' / 'RLO Coaster Output'))
        self.name_var = tk.StringVar(value='JAMES')
        self.number_var = tk.StringVar(value='7')
        self._build()
        self.after(100, self._poll)

    def _build(self):
        pad = {'padx': 12, 'pady': 7}
        top = ttk.Frame(self)
        top.pack(fill='x', padx=18, pady=(18, 8))
        ttk.Label(top, text='RLO PLAYER COASTER GENERATOR', font=('Segoe UI', 18, 'bold')).pack(anchor='w')
        ttk.Label(top, text='Locked V4 design • 100 × 100 × 4 mm • face-down production 3MF').pack(anchor='w', pady=(2, 0))

        one = ttk.LabelFrame(self, text='Generate one player')
        one.pack(fill='x', padx=18, pady=8)
        ttk.Label(one, text='Player name').grid(row=0, column=0, sticky='w', **pad)
        ttk.Entry(one, textvariable=self.name_var, width=28).grid(row=0, column=1, sticky='ew', **pad)
        ttk.Label(one, text='Number').grid(row=0, column=2, sticky='w', **pad)
        ttk.Entry(one, textvariable=self.number_var, width=10).grid(row=0, column=3, sticky='w', **pad)
        ttk.Button(one, text='Generate Player', command=self.generate_one).grid(row=0, column=4, **pad)
        one.columnconfigure(1, weight=1)

        batch = ttk.LabelFrame(self, text='Generate entire XLSX squad')
        batch.pack(fill='x', padx=18, pady=8)
        ttk.Label(batch, text='Spreadsheet').grid(row=0, column=0, sticky='w', **pad)
        ttk.Entry(batch, textvariable=self.xlsx_path).grid(row=0, column=1, sticky='ew', **pad)
        ttk.Button(batch, text='Browse…', command=self.pick_xlsx).grid(row=0, column=2, **pad)
        ttk.Button(batch, text='Generate XLSX', command=self.generate_xlsx).grid(row=1, column=2, **pad)
        ttk.Label(batch, text='Expected columns: Name | Position | Number').grid(row=1, column=1, sticky='w', **pad)
        batch.columnconfigure(1, weight=1)

        out = ttk.LabelFrame(self, text='Output')
        out.pack(fill='x', padx=18, pady=8)
        ttk.Entry(out, textvariable=self.output_dir).grid(row=0, column=0, sticky='ew', **pad)
        ttk.Button(out, text='Choose Folder…', command=self.pick_output).grid(row=0, column=1, **pad)
        out.columnconfigure(0, weight=1)

        self.progress = ttk.Progressbar(self, mode='determinate')
        self.progress.pack(fill='x', padx=30, pady=(8, 2))
        self.status = ttk.Label(self, text='Ready')
        self.status.pack(anchor='w', padx=30, pady=(0, 8))

        logframe = ttk.LabelFrame(self, text='Log')
        logframe.pack(fill='both', expand=True, padx=18, pady=(0, 18))
        self.log = tk.Text(logframe, height=14, wrap='word', state='disabled', font=('Consolas', 9))
        self.log.pack(fill='both', expand=True, padx=8, pady=8)

    def pick_xlsx(self):
        p = filedialog.askopenfilename(title='Choose squad spreadsheet', filetypes=[('Excel workbook', '*.xlsx')])
        if p:
            self.xlsx_path.set(p)

    def pick_output(self):
        p = filedialog.askdirectory(title='Choose output folder')
        if p:
            self.output_dir.set(p)

    def _append(self, text):
        self.log.config(state='normal')
        self.log.insert('end', text.rstrip() + '\n')
        self.log.see('end')
        self.log.config(state='disabled')

    def _worker(self, fn):
        try:
            fn()
        except Exception:
            self.queue.put(('error', traceback.format_exc()))
        finally:
            self.queue.put(('done', None))

    def _start(self, fn):
        self.progress['value'] = 0
        self.status.config(text='Working…')
        threading.Thread(target=self._worker, args=(fn,), daemon=True).start()

    def generate_one(self):
        name = self.name_var.get().strip()
        number = self.number_var.get().strip()
        if not name or not number:
            messagebox.showwarning(APP_TITLE, 'Enter both player name and number.')
            return
        out = self.output_dir.get().strip()
        def work():
            self.queue.put(('log', f'Generating {name.upper()} {number}…'))
            p, _, prev = generate(name, number, out, face_down=True)
            self.queue.put(('log', f'Created: {p}'))
            if prev:
                self.queue.put(('log', f'Preview: {prev}'))
            self.queue.put(('progress', 100))
            self.queue.put(('success', f'Finished {name.upper()} {number}'))
        self._start(work)

    def generate_xlsx(self):
        xlsx = self.xlsx_path.get().strip()
        if not xlsx or not Path(xlsx).exists():
            messagebox.showwarning(APP_TITLE, 'Choose a valid .xlsx file first.')
            return
        out = self.output_dir.get().strip()
        def work():
            players = read_players_xlsx(xlsx)
            if not players:
                raise RuntimeError('No valid player rows found in the spreadsheet.')
            self.queue.put(('log', f'Loaded {len(players)} player rows.'))
            for i, player in enumerate(players, start=1):
                name, number = player['name'], player['number']
                self.queue.put(('log', f'[{i}/{len(players)}] {name.upper()} {number}'))
                generate(name, number, out, face_down=True)
                self.queue.put(('progress', int(i * 100 / len(players))))
            self.queue.put(('success', f'Finished generating {len(players)} coasters.'))
        self._start(work)

    def _poll(self):
        try:
            while True:
                kind, payload = self.queue.get_nowait()
                if kind == 'log':
                    self._append(payload)
                elif kind == 'progress':
                    self.progress['value'] = payload
                elif kind == 'error':
                    self._append(payload)
                    messagebox.showerror(APP_TITLE, 'Generation failed. See the log for details.')
                elif kind == 'success':
                    self._append(payload)
                    messagebox.showinfo(APP_TITLE, payload)
                elif kind == 'done':
                    self.status.config(text='Ready')
        except queue.Empty:
            pass
        self.after(100, self._poll)

if __name__ == '__main__':
    App().mainloop()
