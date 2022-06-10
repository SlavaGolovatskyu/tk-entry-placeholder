# TKPlaceHolder

# Requirement python version >= 3.5 because library use type hints for describe variables and other things

Example
```py
import tkinter as tk

# import our class library
from placeholder import TKPlaceHolder

class App:
    def __init__(self):
        self.width, self.height = 300, 300
        self.marginTop, self.marginLeft = 300, 150
        self.root = tk.Tk()
        self.root.geometry(f'{self.width}x{self.height}+{self.marginTop}+{self.marginLeft}')

        self.ent = tk.Entry(
            self.root, bg = '#0f0505', fg = '#ffffff',
            width = 20, font = 'Consolas 12', justify = 'center'
        )

        self.ent2 = tk.Entry(
            self.root, bg = '#0f0505', fg = '#ffffff',
            width = 20, font = 'Consolas 12', justify = 'center'
        )

        self.ent3 = tk.Entry(
            self.root, bg = '#0f0505', fg = '#ffffff',
            width = 20, font = 'Consolas 12', justify = 'center'
        )

        # You should created a same object with same keys as placeholder and entry
        # Just using you text for placeholder and your entries names
        # After this you should just give this array to TKPlaceHolder constructor or use setter for this
        self.test = [
            {
                'placeholder': 'test1',
                'entry': self.ent,
            },
            {
                'placeholder': 'test2',
                'entry': self.ent2,
            },
            {
                'placeholder': 'test3',
                'entry': self.ent3,
            },
        ]

        # You can also give this to constructor
        # TKPlaceHolder also have 2 other args
        # First with_arrows: bool as default True Response for the bind entries to arrows keys (up, down)
        # Second insert: bool = as default True Response for the insert placeholder into entries when call constructor
        # Also this class have some methods which you can find in him, and check what they was doing
        self.placeholder = TKPlaceHolder(self.test, with_arrows=True, insert=True)
        # or
        self.placeholder.source_entries = self.test

        # Unbind all entries and clear all which saved in object of this class
        # self.placeholder.clear_all()

        # unbind all entries from binds which made an our library
        # self.placeholder.unbind_all()

    def run(self):
        self._draw_window()
        self.root.mainloop()
    
    def _draw_window(self):
        self.ent.place(x=100, y=100)
        self.ent2.place(x=100, y=150)
        self.ent3.place(x=100, y=200)

if __name__ == '__main__':
    App().run()
```

# Video work example 
## https://www.youtube.com/watch?v=jAvPWXkMVHQ
