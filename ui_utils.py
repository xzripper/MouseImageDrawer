from tkinter import Tk, Label, Button

from tkinter.filedialog import askopenfilename

from threading import Thread


Tk().withdraw()

_area = [None]

def ask_image() -> str:
    return askopenfilename(filetypes=[('Image', '*.png *.jpg *.jpeg')], title='Select image.')

def ask_area(previous_area: tuple=None) -> None:
    def _ask():
        if previous_area:
            geometry = f'{previous_area[0]}x{previous_area[1]}+{previous_area[2]}+{previous_area[3]}'

        else:
            geometry = '250x250+100+100'

        window = Tk(); (
            window.title('Area selection.'),
            window.geometry(geometry),

            window.attributes('-alpha', 0.8),

            window.configure(bg='black'))

        area_label = Label(window,
                        text=geometry,

                        fg='white', bg='black',

                        font=('Arial', 16)
        )

        area_label.pack()

        def confirm() -> None:
            window.destroy()

            exit(0)

        confirm_button = Button(window,
                                text='Confirm.',

                                fg='white', bg='black',

                                font=('Arial', 16),

                                borderwidth=0,

                                command=confirm
        )

        confirm_button.pack()

        def area_change(_) -> None:
            _area[0] = (
                window.winfo_width(),
                window.winfo_height(),

                window.winfo_x(),
                window.winfo_y()
            )

            area_label['text'] = f'{_area[0][0]}x{_area[0][1]}x{_area[0][2]}x{_area[0][3]}'

        window.bind('<Configure>', area_change)

        window.mainloop()

    thread = Thread(target=_ask); thread.start()

    while thread.is_alive(): ...

    return _area[0]
