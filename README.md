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
        self.placeholder = TKPlaceHolder(self.test)
        # or
        self.placeholder.source_entries = self.test

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
