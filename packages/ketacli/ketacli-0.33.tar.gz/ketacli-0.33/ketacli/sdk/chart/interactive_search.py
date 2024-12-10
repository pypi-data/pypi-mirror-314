import time
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from ketacli.sdk.base.getch import get_key_thread
from pynput.keyboard import Controller
from rich.live import Live
import re
from pynput import keyboard
import sys
import pyperclip
from ketacli.sdk.chart.table import KTable
from ketacli.sdk.base.getch import is_current_process_in_foreground
import pygetwindow as gw

SPECIAL_CHAR = ["\n", "\r", "\x08", "\x7f", "\x1b", '\x1b\x1b', '\x03', '\x1b[A', '\x1b[B', '\x1b[C', '\x1b[D',
                '\x1b\x1b[C', '\x1b\x1b[D', '\x1b\x7f', '\x08', '\x1b\x62', '\x1b\x66']
YELLOW_HIGH_LIGHT_WORDS = ['search2', 'search', 'mstats', 'stats', 'eval', 'limit', 'sort', 'top', 'start',
                           'end', 'addinfo', 'streamstats', 'accum', 'compare', 'chart', 'movingavg', 'rare',
                           'sparkline', 'timechart', 'eventstats', 'append', 'dedup', 'export', 'where', 'fields']
GREEN_HIGH_LIGHT_WORDS = ['by', 'as', 'AND', 'OR', 'and', 'or', 'NOT', 'not']

REGEX_HIGH_KEY = r"('\w+')|(\w+)"
REGEX_HIGH_VALUE = r"=(\"\w+\")|=('''\w+''')|=(\"\"\"\w+\"\"\")"
REGEX_FUNCTION = r"(\w+\(.*\))"


class InteractiveSearch:
    def __init__(self, page_size=10, limit=500, overflow="ellipsis"):
        self.root = Layout(name="root")
        self.spl_input = list("search2 repo=\"_internal\"\n|fields _raw")
        self.spl_input_cursor = len(self.spl_input)
        self.search_layout = Layout(name="search", size=4)
        self.detail_layout = Layout(name="detail", ratio=5)
        self.history_layout_visible = False
        self.history_layout = Layout(name="history", ratio=3, visible=self.history_layout_visible)
        column_layout = Layout(name="column", ratio=5)
        column_layout.split_column(self.search_layout, self.detail_layout)
        self.root.split_row(self.history_layout, column_layout)
        self.start = None
        self.end = None
        self.limit = limit
        self.page_size = page_size
        self.page_num = 1
        self.overflow = overflow
        self.key = None
        self.live = None
        self.search_panel = Panel(f"{self.get_str_spl()}",
                                  title=f"请输入 [green bold]SPL[/green bold]，回车键查询 "
                                        f"| [green bold]CMD+/[/green bold] 可打开/关闭筛选功能 "
                                        f"| [green bold]CTRL+H[/green bold] 可打开/关闭搜索历史页面",
                                  expand=True,
                                  padding=(0, 2),
                                  border_style="")
        self.search_layout.update(self.search_panel)
        self.detail_panel = None
        self.details_dialog = KTable(
            chart_config={
                "title": "".join(self.spl_input), "spl": "".join(self.spl_input), "start": self.start,
                "end": self.end, "limit": self.limit, "overflow": self.overflow, "page_size": self.page_size
            }
        )

        self.history_details = ""
        self.keys = []
        self.need_exit = False
        self.search_visible = True
        self.keyboard_controller = Controller()
        self.self_window_name = gw.getActiveWindow()

    def refresh_spl(self):
        self.search_panel.renderable = self.get_str_spl()

    def refresh_details(self):
        self.detail_layout.update(self.details_dialog)

    def refresh_history_panel(self):
        if self.history_layout_visible:
            self.history_details = KTable(chart_config={
                "title": "搜索历史",
                "spl": """
                search2 start="-12h" repo="_internal" AND 'action.name'="search" 
                | stats latest(_time) as _time by action.details
                | sort by _time
                |fields -_time""",
                "page_size": 20,
                "columns": {
                    "action.details": {
                        "alias": "搜索语句",
                        "style": "green",
                        "justify": "left"
                    }
                }

            })
            self.history_details.search()
            self.history_layout.update(self.history_details)
        self.history_layout.visible = self.history_layout_visible

    def clean_input(self):
        if not is_current_process_in_foreground(self.self_window_name):
            return
        self.spl_input = [" "]
        self.spl_input_cursor = len(self.spl_input)
        self.refresh_spl()

    def enter(self):
        if not is_current_process_in_foreground(self.self_window_name):
            return
        if self.history_layout_visible:
            spl = self.history_details.get_current_raw_data()[0]
            self.spl_input = list(spl)
            self.spl_input_cursor = len(self.spl_input)
            self.search_layout.size = spl.count('\n') + 3
            self.refresh_spl()
        self.search()

    def cmd_enter(self):
        if not is_current_process_in_foreground(self.self_window_name):
            return
        self.spl_input.append("\n")
        self.spl_input_cursor += 1
        self.search_layout.size += 1
        self.refresh_spl()

    def show_history(self):
        if not is_current_process_in_foreground(self.self_window_name):
            return
        if self.history_layout_visible:
            self.history_layout_visible = False
        else:
            self.history_layout_visible = True
        self.refresh_history_panel()

    def exit(self):
        if not is_current_process_in_foreground(self.self_window_name):
            return
        self.live.stop()
        sys.exit()

    def cursor_right(self):
        if self.spl_input_cursor <= len(self.spl_input):
            if len(self.spl_input) == self.spl_input_cursor and self.spl_input[-1] != ' ':
                self.spl_input.append(' ')
            self.spl_input_cursor += 1
        self.refresh_spl()

    def cursor_left(self):
        if self.spl_input_cursor > 0:
            if len(self.spl_input) == self.spl_input_cursor and self.spl_input[-1] == ' ':
                self.spl_input = self.spl_input[:-1]
            self.spl_input_cursor -= 1
        self.refresh_spl()

    def _need_exit(self):
        self.need_exit = True

    def filter_switch(self):
        if not is_current_process_in_foreground(self.self_window_name):
            return
        self.search_visible = not self.search_visible
        self.details_dialog.filter_switch()

    def up(self):
        if self.history_layout_visible:
            self.history_details.row_sub()
        else:
            self.details_dialog.row_sub()

    def down(self):
        if self.history_layout_visible:
            self.history_details.row_add()
        else:
            self.details_dialog.row_add()

    def page_up(self):
        if self.history_layout_visible:
            self.history_details.page_sub()
        else:
            self.details_dialog.page_sub()

    def page_down(self):
        if self.history_layout_visible:
            self.history_details.page_add()
        else:
            self.details_dialog.page_add()

    def keyboard_press(self, key):
        if not is_current_process_in_foreground(self.self_window_name):
            return
        if key == keyboard.Key.enter:
            self.enter()
        elif key == keyboard.Key.backspace:
            self.backspace()
        elif key == keyboard.Key.right:
            self.cursor_right()
        elif key == keyboard.Key.left:
            self.cursor_left()
        elif key == keyboard.Key.up:
            self.up()
        elif key == keyboard.Key.down:
            self.down()
        elif key == keyboard.Key.page_up:
            self.page_up()
        elif key == keyboard.Key.page_down:
            self.page_down()
        else:
            return

    def ctrl_v(self):
        if not is_current_process_in_foreground(self.self_window_name):
            return
        for i in range(len(pyperclip.paste())):
            with self.keyboard_controller.pressed(keyboard.Key.space):
                pass
                time.sleep(0.05)

    def loop(self):
        # 组合键监听
        hotkey = keyboard.GlobalHotKeys({
            "<cmd>+<backspace>": self.clean_input,
            "<ctrl>+h": self.show_history,
            "<ctrl>+c": self._need_exit,
            "<cmd>+/": self.filter_switch,
            "<ctrl>+v": self.ctrl_v,
            "<cmd>+v": self.ctrl_v,
            "<cmd>+<right>": self.page_down,
            "<cmd>+<left>": self.page_up,
            "<cmd>+<enter>": self.cmd_enter

        })
        hotkey.start()
        time.sleep(0.5)

        listener = keyboard.Listener(on_press=self.keyboard_press)
        listener.start()

        # 输入内容监听
        key = get_key_thread(callback=self.input_spl_char)
        key.start()
        self.search()
        with Live(self.root, auto_refresh=True, screen=True, refresh_per_second=5) as self.live:
            self.refresh_spl()
            self.refresh_details()

            while True:
                if self.need_exit:
                    self.exit()
                time.sleep(1)

    @staticmethod
    def check_char(key):
        allowed_pattern = r'^[\u4e00-\u9fa5A-Za-z0-9\w .,;!?()\'"\-\|_/\*=:<>\{\}\[\]\$#%@!&\*\^+~`;\\]+$'

        # 检查key是否符合允许的字符范围
        if re.match(allowed_pattern, key):
            return key

    def input_spl_char(self, key):
        if not is_current_process_in_foreground(self.self_window_name):
            return

        if not self.check_char(key):
            return
        if key == "|":
            key = "\n| "
            self.search_layout.size += 1
        if self.search_visible:
            # 当 search 输入框处于激活状态时
            self.spl_input = [*self.spl_input[:self.spl_input_cursor - 1], key,
                              *self.spl_input[self.spl_input_cursor - 1:]]
            self.spl_input_cursor += 1
        elif self.details_dialog.search_visible:
            # 当详情搜索框处于激活状态时
            self.details_dialog.search_input(key)
        self.refresh_spl()

    def calculate_enter(self):
        enter_cnt = str(self.get_str_spl()).count("\n")
        if enter_cnt > 10:
            enter_cnt = 10
        self.search_layout.size = enter_cnt + 3

    def backspace(self):
        if self.search_visible:
            if len(self.spl_input) > 0:
                self.spl_input = [*self.spl_input[:self.spl_input_cursor - 2],
                                  *self.spl_input[self.spl_input_cursor - 1:]]
                self.spl_input_cursor -= 1
        else:
            self.details_dialog.backspace()
        self.refresh_spl()
        self.calculate_enter()

    def get_str_spl(self):

        text = Text()
        if self.spl_input_cursor == 0:
            self.spl_input_cursor = 1
        elif self.spl_input_cursor > len(self.spl_input):
            self.spl_input_cursor = len(self.spl_input)

        if not self.spl_input:
            return ""
        text.append("".join(self.spl_input[:self.spl_input_cursor - 1]), )
        text.append(f"{self.spl_input[self.spl_input_cursor - 1]}", style="bold u")
        text.append("".join(self.spl_input[self.spl_input_cursor:]), )

        text.highlight_regex(REGEX_HIGH_KEY, 'magenta')
        text.highlight_regex(REGEX_HIGH_VALUE, '#5c90cd')
        text.highlight_regex(REGEX_FUNCTION, 'green')
        text.highlight_words(YELLOW_HIGH_LIGHT_WORDS, 'yellow')
        text.highlight_words(GREEN_HIGH_LIGHT_WORDS, 'green')
        return text

    def search(self):
        self.detail_layout.update(Text('Searching...', justify="center"))
        try:
            spl = self.get_str_spl()
            self.details_dialog.search(spl.plain)
            self.detail_layout.update(self.details_dialog)
        except Exception as e:
            self.detail_layout.update(Text(f"Error: {e}", justify="center"))
            self.exit()
