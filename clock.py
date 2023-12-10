import tkinter as tk
import time
import math
import datetime as dt

root = tk.Tk()
root.title("Часы")

# создание холста
canvas = tk.Canvas(root, width=600, height=600, bg="rosybrown")
canvas.pack()

phases = {
    0: "new (totally dark)",
    1: "waxing crescent (increasing to full)",
    2: "in its first quarter (increasing to full)",
    3: "waxing gibbous (increasing to full)",
    4: "full (full light)",
    5: "waning gibbous (decreasing from full)",
    6: "in its last quarter (decreasing from full)",
    7: "waning crescent (decreasing from full)",
}


def moon_phase(month, day, year):
    ages = [18, 0, 11, 22, 3, 14, 25, 6, 17, 28, 9, 20, 1, 12, 23, 4, 15, 26, 7]
    offsets = [-1, 1, 0, 1, 2, 3, 4, 5, 7, 7, 9, 9]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    if day == 31:
        day = 1
    days_into_phase = ((ages[(year + 1) % 19] +
                        ((day + offsets[month - 1]) % 30) +
                        (year < 1900)) % 30)
    index = int((days_into_phase + 2) * 16 / 59.0)
    if index > 7:
        index = 7
    status = phases[index]
    return index, status


# отрисовка фазы луны
def draw_moonphase(month, day, year):
    canvas.create_text(540, 480, text='Фаза луны:', font='Arial', fill='black')

    phase, descr = moon_phase(month, day, year)
    if phase == 0:
        canvas.create_oval(500, 500, 600, 600, fill="gray", outline='gray')  # good
    elif phase == 1:
        canvas.create_arc(500, 500, 600, 600, start=90, extent=180, fill="gray", outline='gray')
        canvas.create_arc(500, 500, 600, 600, start=-90, extent=180, fill='yellow', outline='yellow')
        canvas.create_arc(510, 500, 590, 600, start=-90, extent=180, fill="gray", outline='gray')
    elif phase == 2:
        canvas.create_arc(500, 500, 600, 600, start=90, extent=180, fill='gray', outline='gray')  # good
        canvas.create_arc(500, 500, 600, 600, start=-90, extent=180, fill='yellow', outline='gray')  # good
    elif phase == 3:
        canvas.create_arc(500, 500, 600, 600, start=-90, extent=180, fill="yellow", outline='yellow')
        canvas.create_arc(500, 500, 600, 600, start=90, extent=180, fill='gray', outline='gray')
        canvas.create_arc(510, 500, 590, 600, start=90, extent=180, fill="yellow", outline='yellow')
    elif phase == 4:
        canvas.create_oval(500, 500, 600, 600, fill="yellow", outline='yellow')  # good
    elif phase == 5:
        canvas.create_arc(500, 500, 600, 600, start=90, extent=180, fill="yellow", outline='yellow')
        canvas.create_arc(500, 500, 600, 600, start=-90, extent=180, fill='gray', outline='gray')
        canvas.create_arc(510, 500, 590, 600, start=-90, extent=180, fill="yellow", outline='yellow')
    elif phase == 6:
        canvas.create_arc(500, 500, 600, 600, start=-90, extent=180, fill='gray', outline='gray')  # good
    elif phase == 7:
        canvas.create_arc(500, 500, 600, 600, start=-90, extent=180, fill="gray", outline='gray')
        canvas.create_arc(500, 500, 600, 600, start=90, extent=180, fill='yellow', outline='yellow')
        canvas.create_arc(510, 500, 590, 600, start=90, extent=180, fill="gray", outline='gray')


# обновление часов
def clock():
    canvas.delete("all")
    now = time.localtime()
    hour = now.tm_hour % 12
    minute = now.tm_min
    second = now.tm_sec
    date = dt.datetime.now()
    format_date = (f"{date:%a, %b %d %Y}")
    label = tk.Label(root, text=format_date, font=("Arial", 18), bg="silver")
    label.pack()
    canvas.create_window(110, 20, window=label, width=216, height=40)

    x = 300
    y = 300

    hour_angle = (hour + minute / 60) * math.pi / 6 - math.pi / 2
    hour_x = 300 + 0.5 * 220 * math.cos(hour_angle)
    hour_y = 300 + 0.5 * 220 * math.sin(hour_angle)

    canvas.create_line(300, 300, hour_x, hour_y, fill="black", width=10, arrowshape=(8, 10, 3), capstyle=tk.ROUND)

    minute_angle = (minute + second / 60) * math.pi / 30 - math.pi / 2
    minute_x = 300 + 0.7 * 220 * math.cos(minute_angle)
    minute_y = 300 + 0.7 * 220 * math.sin(minute_angle)
    canvas.create_line(300, 300, minute_x, minute_y, fill="black", width=7, capstyle=tk.ROUND)

    second_angle = second * math.pi / 30 - math.pi / 2
    second_x = 300 + 0.6 * 220 * math.cos(second_angle)
    second_y = 300 + 0.6 * 220 * math.sin(second_angle)
    canvas.create_line(300, 300, second_x, second_y, fill="silver", width=4, capstyle=tk.ROUND)

    center = canvas.create_oval(x - 7, y - 7, x + 7, y + 7, outline="silver", fill="silver")

    # фаза луны
    draw_moonphase(date.month, date.day, date.year)

    canvas.after(1000, clock)


clock()

if __name__ == "__main__":
    root.mainloop()