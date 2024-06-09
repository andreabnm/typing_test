import tkinter
from tkinter import *
from tkinter import font, messagebox
import threading
import datetime
from timer import Typing_Timer
import time
import sqlite3

window = Tk()
window.title("Typing Speed Test")
window.minsize(width=500, height=300)
timer = Typing_Timer()
db_con = sqlite3.connect("data.db")
db_cur = db_con.cursor()


def fetch_sample_from_db():
    res = db_cur.execute("SELECT txt FROM data ORDER BY RANDOM() LIMIT 1")
    sample = res.fetchone()
    return sample[0]


arial_font24 = font.Font(family='Arial', size=24, weight=font.BOLD)
arial_font18 = font.Font(family='Arial', size=18, weight=font.NORMAL)

label_image = Label(text="Press start and copy the phrase that appear as fast as you can.", font=arial_font24)
label_image.grid(row=0, column=0, columnspan=3, pady=(30, 30))

sample_text_entry = Text(width=70, height=10)
sample_text_entry.grid(row=2, column=0, columnspan=3)


def insert_text_to_copy(text):
    # Insert text sample
    sample_text_entry.config(state=NORMAL)
    sample_text_entry.delete(index1=1.0, index2=END)
    sample_text_entry.insert(tkinter.END, chars=text)
    sample_text_entry.config(state=DISABLED)


insert_text_to_copy('')

write_text_entry = Text(width=70, height=10)
write_text_entry.grid(row=3, column=0, columnspan=3)

label_seconds = Label(text="", font=arial_font18)
label_seconds.grid(row=1, column=2, columnspan=1, sticky="E")


def show_timer():
    while timer.started:
        timer.increase_counter()
        label_seconds.config(text=f'{str(datetime.timedelta(seconds=timer.counter))}')
        time.sleep(1)


def start_timer():
    if not timer.started:
        sample_text = fetch_sample_from_db()
        insert_text_to_copy(sample_text)
        timer.start(sample_text)
        t = threading.Thread(target=show_timer)
        t.start()
        write_text_entry.focus_set()


def stop_timer():
    if timer.started:
        insert_text_to_copy('')
        timer.end()
        calculate_typing_speed()
        write_text_entry.delete(index1=1.0, index2=END)


def calculate_typing_speed():
    sample_string = timer.text
    input_string = write_text_entry.get('1.0', 'end-1c')

    typing_speed = len(input_string) / (timer.end_time - timer.start_time)

    # Calculate accuracy
    accuracy = 0
    for i in range(len(sample_string)):
        if (len(input_string) - 1) >= i:
            if sample_string[i] == input_string[i]:
                accuracy += 1
    accuracy = accuracy / len(sample_string) * 100

    result = 'Typing speed: {:.2f} characters per second.'.format(typing_speed) + " Accuracy: {:.2f}%".format(accuracy)

    new_message = messagebox.Message(type='ok', title='Result', message=result, icon='info')
    new_message.show()


start_btn = Button(text="Start", command=start_timer, font=arial_font24, width=20)
start_btn.grid(row=4, column=0, columnspan=1, pady=(30, 10))

stop_btn = Button(text="Stop", command=stop_timer, font=arial_font24, width=10)
stop_btn.grid(row=4, column=1, columnspan=2, pady=(30, 10))

t = threading.Thread(target=show_timer)
t.start()
window.mainloop()
