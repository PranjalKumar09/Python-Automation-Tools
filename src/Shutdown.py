import os
from tkinter import Tk, Button ,RAISED 

def restart():
    os.system("sudo shutdown -r now")

def restart_timer():
    os.system("sleep 60 && gnome-screensaver-command -l && sudo shutdown -r now")

def logout():
    os.system("gnome-session-quit --logout --no-prompt")

def poweroff():
    os.system("sudo shutdown -P +10")

st = Tk()
st.title("Shutdown App")
st.geometry("500x500")
st.config(bg="blue")

r_button = Button(st, text="Restart", font=("Times New Roman", 20, "bold"), relief= RAISED, cursor="plus", command=restart)
r_button.place(x=150, y=60, height=50, width=200)

r_button = Button(st, text="Restart Time", font=("Times New Roman", 20, "bold"), relief= RAISED, cursor="plus", command=restart_timer)
r_button.place(x=150, y=170, height=50, width=200)

r_button = Button(st, text="Logout", font=("Times New Roman", 20, "bold"), relief = RAISED, cursor="plus", command=logout)
r_button.place(x=150, y=270, height=50, width=200)

r_button = Button(st, text="Shut down", font=("Times New Roman", 20, "bold"), relief= RAISED, cursor="plus", command=poweroff)
r_button.place(x=150, y=370, height=50, width=200)

st.mainloop()
