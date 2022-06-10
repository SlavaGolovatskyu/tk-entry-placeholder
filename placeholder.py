import tkinter as tk

from typing import List, Dict

__author__ = 'Yaroslav Holovatskyu'

# TODO change self._entries from list to queue with O(1)
class TKPlaceHolder:
    ADD = 'add'
    DELETE = 'delete'
    INSERT = 'insert'
    TEXT = 'placeholder'
    ENTRY = 'entry'
    BIND = 'bind'
    UNBIND = 'unbind'
    MOUSE_CLICK = '<Button-1>'
    ARROW_TOP = '<Up>'
    ARROW_DOWN = '<Down>'

    # @example
    # list = [{'placeholder': 'test', 'entry': tkinter.Entry}] with one entry
    # many [{'placeholder': 'test', 'entry': tkinter.Entry}, { ... }, { ... }]
    # ** insert argument call function which insert text which is located in placeholder key as default
    def __init__(
        self,
        entries: List[Dict[str, str or tk.Entry]] = None,
        with_arrows: bool = True,
        insert: bool = True,
    ) -> None:
        self._entries = entries
        self._last_entry: Dict[str, str or bool or tk.Entry] or None = None
        self._with_arrows = with_arrows

        if entries is None: return
        
        self._check_entries_on_correct(entries)

        if insert:
            self._entries_actions(self._entries, TKPlaceHolder.INSERT)

        self._entries_actions(self._entries, TKPlaceHolder.BIND)

    @property
    def source_entries(self) -> List[Dict[str, str or bool or tk.Entry]]:
        return self._entries

    @property
    def last_entry(self) -> Dict[str, str or bool or tk.Entry] or None:
        return self._last_entry
    
    # Setter if user doesnt give an entries by constructor
    # First checked on correctness of list and objects with entries
    # Second step unbind all older entries and delete all
    # Third set new entries
    # Four insert text in all entries
    # Five bind all entries
    @source_entries.setter
    def source_entries(self, entries: List[Dict[str, str or bool or tk.Entry]]):
        self._check_entries_on_correct(entries)
        self.clear_all()

        self._entries = entries

        self._entries_actions(self._entries, TKPlaceHolder.INSERT)
        self._entries_actions(self._entries, TKPlaceHolder.BIND)

    @last_entry.setter
    def last_entry(self, entry: Dict[str, str or bool or tk.Entry]):
        self._check_entries_on_correct([entry])
        e = [e for e in self._entries if e[TKPlaceHolder.ENTRY] == entry[TKPlaceHolder.ENTRY]]

        if not e: return False

        self._last_entry = e[0]


    # @example
    # First arg your dict with placeholder and entry
    # ** action: bool 2 regimes 'add' or 'delete' which save entry to others or delete
    # ** withText: bool = True as default
    # added text to placeholder or delete
    def entry_action(
        self,
        entry: Dict[str, str or tk.Entry],
        action: str = 'add',
        withText: bool = True
    ) -> None:
        self._check_entries_on_correct([entry])

        if action == TKPlaceHolder.ADD:
            self._entries.append(entry)
            entry[TKPlaceHolder.ENTRY].bind(TKPlaceHolder.MOUSE_CLICK, self._on_click)

            if withText:
                self._entries_actions([entry], TKPlaceHolder.INSERT)

        elif action == TKPlaceHolder.DELETE:
            self._entries = list(filter(lambda e: e[TKPlaceHolder.ENTRY] != entry[TKPlaceHolder.ENTRY], self._entries))
            entry[TKPlaceHolder.ENTRY].unbind(TKPlaceHolder.MOUSE_CLICK)

            if withText:
                self._entries_actions([entry], TKPlaceHolder.DELETE)

    # function for bind or unbind availiable entry
    # ** Entry -> tk.Entry
    # ** action -> 'bind' or 'unbind'
    def bind_action(self, entry: Dict[str, str or tk.Entry], action: str = 'bind'):
        self._check_entries_on_correct([entry])
        e = [e for e in self._entries if e[TKPlaceHolder.ENTRY] == entry[TKPlaceHolder.ENTRY]]

        if not e: return

        if action == TKPlaceHolder.BIND:
            e[0][TKPlaceHolder.ENTRY].bind(TKPlaceHolder.MOUSE_CLICK, self._on_click)

        elif action == TKPlaceHolder.UNBIND:
            e[0][TKPlaceHolder.ENTRY].unbind(TKPlaceHolder.MOUSE_CLICK)

    def unbind_all(self):
        if not isinstance(self._entries, list): return

        self._entries_actions(self._entries, TKPlaceHolder.UNBIND)
    
    # unbind all entries, and delete all which is saved
    def clear_all(self):
        self.unbind_all()
        self._entries = None
        self._last_entry = None

    def _on_up(self, event):
        self._on_arrow_keys(event, 'up')

    def _on_down(self, event):
        self._on_arrow_keys(event, 'down')

    # if user tapped on binded entry
    def _on_click(self, event) -> None:
        # Find entry widget on which user was a clicked
        on_clicked_entry = self._find_entry_by_event(event, TKPlaceHolder.ENTRY)

        # if we have prev entry and he was empty, inserting placeholder's text
        self._insert_in_last_entry(on_clicked_entry)

        # set a last entry Current clicked entry
        self._last_entry = on_clicked_entry
        # Delete placeholder on the onclick
        self._last_entry[TKPlaceHolder.ENTRY].delete(0, tk.END)
    
    # For bind entries on arrow keys up & down
    # event -> tkinter event
    # action: str = 'up' or 'down'
    def _on_arrow_keys(self, event, action: str = 'up'):
        last_ent_idx = self._find_entry_by_event(event, 'idx')

        if last_ent_idx is None: return

        self._insert_in_last_entry(self._entries[last_ent_idx])

        down_or_up_entry = last_ent_idx - 1 if action == 'up' else last_ent_idx + 1
        down_or_up_entry = 0 if down_or_up_entry == len(self._entries) else down_or_up_entry

        self._last_entry = self._entries[down_or_up_entry]

        self.last_entry[TKPlaceHolder.ENTRY].delete(0, tk.END)
        self.last_entry[TKPlaceHolder.ENTRY].focus()
    
    # event -> tkinter event
    # idx_or_entry: str -> entry || idx
    def _find_entry_by_event(self, event, idx_or_entry: str = 'entry'):
        entry = [
            [index, entry] for index, entry in enumerate(self._entries)
            if entry[TKPlaceHolder.ENTRY] == event.widget
        ]

        if not entry: return

        if idx_or_entry == TKPlaceHolder.ENTRY:
            return entry[0][1]
        return entry[0][0]
    
    def _insert_in_last_entry(self, entry):
        if (
            self._last_entry and
            entry != self._last_entry[TKPlaceHolder.ENTRY] and not
            self._last_entry[TKPlaceHolder.ENTRY].get()
        ):
            self._last_entry[TKPlaceHolder.ENTRY].insert(0, self._last_entry[TKPlaceHolder.TEXT])
    
    def _entries_actions(self, entries: List[Dict[str, str or bool or tk.Entry]], action: str = 'bind'):
        ENTRY = TKPlaceHolder.ENTRY
        MOUSE_CLICK = TKPlaceHolder.MOUSE_CLICK
        ARROW_TOP = TKPlaceHolder.ARROW_TOP
        ARROW_DOWN = TKPlaceHolder.ARROW_DOWN

        for entry in entries:
            if action == TKPlaceHolder.BIND:
                if self._with_arrows:
                    entry[ENTRY].bind(ARROW_TOP, self._on_up)
                    entry[ENTRY].bind(ARROW_DOWN, self._on_down)
                entry[ENTRY].bind(MOUSE_CLICK, self._on_click)

            elif action == TKPlaceHolder.UNBIND:
                if self._with_arrows:
                    entry[ENTRY].unbind(ARROW_TOP)
                    entry[ENTRY].unbind(ARROW_DOWN)
                entry[ENTRY].unbind(MOUSE_CLICK)

            elif action == TKPlaceHolder.INSERT:
                entry[ENTRY].insert(0, entry[TKPlaceHolder.TEXT])
            
            elif action == TKPlaceHolder.DELETE:
                entry[ENTRY].delete(0, tk.END)

    @staticmethod
    def _check_entries_on_correct(entries) -> None:
        errors = []

        if not isinstance(entries, list):
            raise TypeError('Entries should located in a list')

        for index, entry in enumerate(entries):
            if not isinstance(entry, dict):
                errors.append(f'Value must be a dict, but you entry is a {type(entry)}\nProblem value {entries[index]}')
                continue
            
            entry_keys = entry.keys()

            if not TKPlaceHolder.TEXT in entry_keys or not TKPlaceHolder.ENTRY in entry_keys:
                errors.append(f'Your object doesn\'t have key placeholder or entry, obj with problem {entries[index]}')
                continue

            if (
                not isinstance(entry[TKPlaceHolder.TEXT], str) or
                not isinstance(entry[TKPlaceHolder.ENTRY], tk.Entry)
            ):
                errors.append(
                    'Wrong type of placeholder or entry, placeholder must be a string, entry object of tkinter.Entry' \
                    f'\nobj with problem {entries[index]}'
                )

        if errors:
            for index, error in enumerate(errors):
                print(f'\n\nError #{index+1} : \n', error, '\n\n')
            raise TypeError('Validation Error')