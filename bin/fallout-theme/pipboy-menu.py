#!/usr/bin/env python3
"""
Pip-Boy Theme Selection Menu (Curses version with transparency)
Fallout-style TUI for choosing terminal themes
"""

import curses
import subprocess
import os

THEMES = {
    "green": {"name": "Classic Green", "desc": "Original Pip-Boy phosphor green"},
    "blue": {"name": "Light Blue", "desc": "Vault-Tec cool blue tone"},
    "cyan": {"name": "Cyan", "desc": "Bright cyan terminal look"},
    "amber": {"name": "Amber", "desc": "Warm orange, easy on eyes"},
    "white": {"name": "White", "desc": "High contrast, bright"},
    "red": {"name": "Red", "desc": "Danger alert vibes"},
    "purple": {"name": "Purple", "desc": "Custom mystical theme"},
    "pink": {"name": "Pink", "desc": "Sweet bubblegum vibes"},
}

VAULT_BOY = r"""
______     _     __  __      _        ___  
|__  /    / \    \ \/ /     / |      / _ \ 
  / /    / _ \    \  /      | |     | | | |
 / /_   / ___ \   /  \      | |  _  | |_| |
/____| /_/   \_\ /_/\_\     |_| (_)  \___/ 
"""

def get_current_theme():
    """Read the current theme from file"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        theme_file = os.path.join(script_dir, ".current_theme")
        if os.path.exists(theme_file):
            with open(theme_file, 'r') as f:
                return f.read().strip()
    except:
        pass
    return "green"

def draw_box(stdscr, y, x, height, width, title=""):
    """Draw a rounded box with optional title"""
    try:
        # Top border with rounded corners
        stdscr.addstr(y, x, "╭" + "─" * (width - 2) + "╮")
        # Sides
        for i in range(1, height - 1):
            stdscr.addstr(y + i, x, "│" + " " * (width - 2) + "│")
        # Bottom border with rounded corners
        stdscr.addstr(y + height - 1, x, "╰" + "─" * (width - 2) + "╯")
        # Title
        if title:
            stdscr.addstr(y, x + 2, f" {title} ", curses.A_BOLD)
    except:
        pass

def draw_button(stdscr, y, x, width, text, selected=False):
    """Draw a rounded button with highlight box"""
    try:
        # Draw highlight box around entire button if selected
        if selected:
            # Outer highlight box
            stdscr.addstr(y - 1, x - 1, "┌" + "─" * width + "┐", curses.A_BOLD)
            stdscr.addstr(y, x - 1, "│", curses.A_BOLD)
            stdscr.addstr(y, x + width, "│", curses.A_BOLD)
            stdscr.addstr(y + 1, x - 1, "│", curses.A_BOLD)
            stdscr.addstr(y + 1, x + width, "│", curses.A_BOLD)
            stdscr.addstr(y + 2, x - 1, "│", curses.A_BOLD)
            stdscr.addstr(y + 2, x + width, "│", curses.A_BOLD)
            stdscr.addstr(y + 3, x - 1, "└" + "─" * width + "┘", curses.A_BOLD)
        
        # Button itself
        attr = curses.A_BOLD if selected else curses.A_NORMAL
        padding = (width - len(text)) // 2
        button_text = " " * padding + text + " " * (width - len(text) - padding)
        # Rounded corners for buttons
        stdscr.addstr(y, x, "╭" + "─" * (width - 2) + "╮", attr)
        stdscr.addstr(y + 1, x, "│" + button_text[1:-1] + "│", attr)
        stdscr.addstr(y + 2, x, "╰" + "─" * (width - 2) + "╯", attr)
    except:
        pass

def apply_theme(theme_key):
    """Apply a theme using the fallout-theme script"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, "fallout-theme")
        
        subprocess.run(
            [script_path, theme_key],
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except:
        return False

def draw_menu(stdscr, selected_idx, status_msg=""):
    """Draw the main menu"""
    stdscr.erase()
    h, w = stdscr.getmaxyx()
    
    # Title
    title = "VAULT-TEC TERMINAL CONFIGURATION SYSTEM v1.0"
    try:
        stdscr.addstr(1, (w - len(title)) // 2, title, curses.A_BOLD)
    except:
        pass
    
    # Vault Boy ASCII art
    vault_lines = VAULT_BOY.strip().split('\n')
    max_line_len = max(len(line) for line in vault_lines)
    vault_y = 3
    for i, line in enumerate(vault_lines):
        try:
            # Center based on longest line so all lines align
            x_pos = (w - max_line_len) // 2
            stdscr.addstr(vault_y + i, x_pos, line)
        except:
            pass

    # Menu box
    menu_y = vault_y + len(vault_lines) + 2
    menu_title = ">>> SELECT COLOR PROFILE <<<"
    try:
        stdscr.addstr(menu_y, (w - len(menu_title)) // 2, menu_title, curses.A_BOLD)
    except:
        pass
    
    # Theme buttons
    button_width = 30
    button_y = menu_y + 2
    theme_keys = list(THEMES.keys())
    
    for idx, theme_key in enumerate(theme_keys):
        theme_name = THEMES[theme_key]["name"].upper()
        button_x = (w - button_width) // 2
        draw_button(stdscr, button_y + (idx * 4), button_x, button_width, 
                   theme_name, selected=idx == selected_idx)
    
    # Status message
    if status_msg:
        try:
            stdscr.addstr(h - 4, (w - len(status_msg)) // 2, status_msg, curses.A_BOLD)
        except:
            pass
    
    # Footer
    footer = "[↑↓] Navigate  [ENTER] Select  [ESC/Q] Exit"
    try:
        stdscr.addstr(h - 2, (w - len(footer)) // 2, footer, curses.A_DIM)
    except:
        pass
    
    stdscr.refresh()

def main(stdscr):
    # Setup curses with transparency
    curses.curs_set(0)
    curses.use_default_colors()
    stdscr.bkgd(' ', curses.color_pair(0))
    curses.init_pair(1, -1, -1)
    stdscr.nodelay(0)
    stdscr.timeout(100)
    curses.mousemask(curses.BUTTON1_PRESSED | curses.BUTTON1_RELEASED | curses.REPORT_MOUSE_POSITION)
    
    current_theme = get_current_theme()
    theme_keys = list(THEMES.keys())
    selected_idx = theme_keys.index(current_theme) if current_theme in theme_keys else 0
    status_msg = ""
    last_hovered_idx = -1
    
    try:
        while True:
            draw_menu(stdscr, selected_idx, status_msg)
            
            key = stdscr.getch()
            
            if key == curses.KEY_DOWN:
                selected_idx = (selected_idx + 1) % len(theme_keys)
                # Apply theme on arrow key navigation too
                theme_key = theme_keys[selected_idx]
                theme_name = THEMES[theme_key]["name"].upper()
                apply_theme(theme_key)
                #status_msg = f"PREVIEWING: {theme_name}"
                last_hovered_idx = selected_idx
            elif key == curses.KEY_UP:
                selected_idx = (selected_idx - 1) % len(theme_keys)
                # Apply theme on arrow key navigation too
                theme_key = theme_keys[selected_idx]
                theme_name = THEMES[theme_key]["name"].upper()
                apply_theme(theme_key)
                #status_msg = f"PREVIEWING: {theme_name}"
                last_hovered_idx = selected_idx
            elif key == ord('\n') or key == curses.KEY_ENTER or key == 10:
                theme_key = theme_keys[selected_idx]
                theme_name = THEMES[theme_key]["name"].upper()
                if apply_theme(theme_key):
                    status_msg = f"✓ {theme_name} ACTIVATED"
                else:
                    status_msg = f"✗ FAILED TO APPLY {theme_name}"
            elif key == curses.KEY_MOUSE:
                try:
                    _, mx, my, _, bstate = curses.getmouse()
                    h, w = stdscr.getmaxyx()
                    
                    # Calculate button positions
                    vault_lines = VAULT_BOY.strip().split('\n')
                    vault_y = 3
                    menu_y = vault_y + len(vault_lines) + 2
                    button_y = menu_y + 2
                    button_width = 30
                    button_x = (w - button_width) // 2
                    
                    # Check which button the mouse is over
                    for idx in range(len(theme_keys)):
                        btn_y_start = button_y + (idx * 4) - 1  # Include highlight box
                        btn_y_end = btn_y_start + 4  # Button height + highlight
                        btn_x_start = button_x - 1  # Include highlight box
                        btn_x_end = button_x + button_width + 1
                        
                        if btn_y_start <= my <= btn_y_end and btn_x_start <= mx <= btn_x_end:
                            if idx != last_hovered_idx:
                                # Mouse hovering over new button
                                selected_idx = idx
                                theme_key = theme_keys[idx]
                                theme_name = THEMES[theme_key]["name"].upper()
                                apply_theme(theme_key)
                                #status_msg = f"PREVIEWING: {theme_name}"
                                last_hovered_idx = idx
                            break
                except curses.error:
                    pass
            elif key == 27 or key == ord('q'):  # ESC or Q
                break
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    curses.wrapper(main)
