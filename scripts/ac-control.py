#!/usr/bin/env python3
import curses
import asyncio
import aiohttp
from gehomesdk import GeWebsocketClient, ErdCode, ErdAcFanSetting, ErdAcOperationMode, ErdOnOff

USERNAME = "amii.brunk@gmail.com"
PASSWORD = "TheSeededEarth#2"
REGION = "US"
APPLIANCE_ID = "020000245A73"

class ACController:
    def __init__(self):
        self.client = None
        self.appliance = None
        self.session = None
        self.client_task = None
        self.current_temp = "N/A"
        self.target_temp = "N/A"
        self.mode = "N/A"
        self.fan = "N/A"
        self.power = "N/A"
        
    async def connect(self):
        self.session = aiohttp.ClientSession()
        self.client = GeWebsocketClient(USERNAME, PASSWORD, REGION)
        self.client_task = asyncio.create_task(
            self.client.async_get_credentials_and_run(self.session)
        )
        await asyncio.sleep(10)
        if APPLIANCE_ID in self.client.appliances:
            self.appliance = self.client.appliances[APPLIANCE_ID]
            self.update_status()
            return True
        return False
        
    async def disconnect(self):
        if self.client_task and not self.client_task.done():
            self.client_task.cancel()
            try:
                await asyncio.wait_for(self.client_task, timeout=0.5)
            except (asyncio.CancelledError, asyncio.TimeoutError, Exception):
                pass
        if self.session and not self.session.closed:
            await self.session.close()
        
    def update_status(self):
        if self.appliance:
            try:
                self.current_temp = str(self.appliance.get_erd_value(ErdCode.AC_AMBIENT_TEMPERATURE) or "N/A")
                self.target_temp = str(self.appliance.get_erd_value(ErdCode.AC_TARGET_TEMPERATURE) or "N/A")
                mode = self.appliance.get_erd_value(ErdCode.AC_OPERATION_MODE)
                mode_str = str(mode).split('.')[-1] if mode else "N/A"
                # Convert ENERGY_SAVER to ECO and FAN_ONLY to FAN for display
                if mode_str == "ENERGY_SAVER":
                    self.mode = "ECO"
                elif mode_str == "FAN_ONLY":
                    self.mode = "FAN"
                else:
                    self.mode = mode_str
                fan = self.appliance.get_erd_value(ErdCode.AC_FAN_SETTING)
                self.fan = str(fan).split('.')[-1] if fan else "N/A"
                power = self.appliance.get_erd_value(ErdCode.AC_POWER_STATUS)
                self.power = "ON" if power == ErdOnOff.ON else "OFF"
            except:
                pass
    
    async def set_power(self, on):
        val = ErdOnOff.ON if on else ErdOnOff.OFF
        await self.appliance.async_set_erd_value(ErdCode.AC_POWER_STATUS, val)
        await asyncio.sleep(2)
        self.update_status()
        
    async def set_temp(self, temp):
        await self.appliance.async_set_erd_value(ErdCode.AC_TARGET_TEMPERATURE, temp)
        await asyncio.sleep(1)
        self.update_status()
        
    async def set_mode(self, mode):
        await self.appliance.async_set_erd_value(ErdCode.AC_OPERATION_MODE, mode)
        await asyncio.sleep(1)
        self.update_status()
        
    async def set_fan(self, fan):
        await self.appliance.async_set_erd_value(ErdCode.AC_FAN_SETTING, fan)
        await asyncio.sleep(1)
        self.update_status()

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
    """Draw a rounded button"""
    try:
        attr = curses.A_REVERSE if selected else curses.A_NORMAL
        padding = (width - len(text)) // 2
        button_text = " " * padding + text + " " * (width - len(text) - padding)
        # Rounded corners for buttons
        stdscr.addstr(y, x, "╭" + "─" * (width - 2) + "╮")
        stdscr.addstr(y + 1, x, "│" + button_text[1:-1] + "│", attr)
        stdscr.addstr(y + 2, x, "╰" + "─" * (width - 2) + "╯")
    except:
        pass

def draw_menu(stdscr, controller, selected_col, selected_row):
    try:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        
        # Title with decorative borders
        title = "═══ AC CONTROL ═══"
        stdscr.addstr(1, w//2 - len(title)//2, title, curses.A_BOLD)
        
        # Status display
        status_y = 3
        stdscr.addstr(status_y, 4, f"Current Temperature: {controller.current_temp}°F", curses.A_BOLD)
        
        # Column positions
        col_width = 18
        col_spacing = 2
        start_x = 4
        
        cols = [
            start_x,
            start_x + col_width + col_spacing,
            start_x + 2 * (col_width + col_spacing),
            start_x + 3 * (col_width + col_spacing)
        ]
        
        box_y = 6
        
        # Column 1: Power
        draw_box(stdscr, box_y, cols[0], 10, col_width, "POWER")
        is_on = controller.power == "ON"
        draw_button(stdscr, box_y + 2, cols[0] + 2, col_width - 4, "ON", 
                   selected_col == 0 and selected_row == 0)
        if is_on:
            stdscr.addstr(box_y + 3, cols[0] + col_width - 5, "●", curses.A_BOLD)
        draw_button(stdscr, box_y + 5, cols[0] + 2, col_width - 4, "OFF",
                   selected_col == 0 and selected_row == 1)
        if not is_on:
            stdscr.addstr(box_y + 6, cols[0] + col_width - 5, "●", curses.A_BOLD)
        
        # Column 2: Temperature
        draw_box(stdscr, box_y, cols[1], 10, col_width, "TEMPERATURE")
        temp_text = f"{controller.target_temp}°F"
        draw_button(stdscr, box_y + 2, cols[1] + 2, col_width - 4, "▲ UP",
                   selected_col == 1 and selected_row == 0)
        stdscr.addstr(box_y + 5, cols[1] + (col_width - len(temp_text))//2, temp_text, curses.A_BOLD)
        draw_button(stdscr, box_y + 6, cols[1] + 2, col_width - 4, "▼ DOWN",
                   selected_col == 1 and selected_row == 1)
        
        # Column 3: Mode
        draw_box(stdscr, box_y, cols[2], 13, col_width, "MODE")
        modes = ["COOL", "FAN", "ECO"]
        for i, mode in enumerate(modes):
            is_active = controller.mode == mode
            draw_button(stdscr, box_y + 2 + (i * 3), cols[2] + 2, col_width - 4, mode,
                       selected_col == 2 and selected_row == i)
            if is_active:
                stdscr.addstr(box_y + 3 + (i * 3), cols[2] + col_width - 5, "●", curses.A_BOLD)
        
        # Column 4: Fan Speed
        draw_box(stdscr, box_y, cols[3], 16, col_width, "FAN SPEED")
        fans = ["AUTO", "LOW", "MED", "HIGH"]
        for i, fan in enumerate(fans):
            is_active = controller.fan == fan
            draw_button(stdscr, box_y + 2 + (i * 3), cols[3] + 2, col_width - 4, fan,
                       selected_col == 3 and selected_row == i)
            if is_active:
                stdscr.addstr(box_y + 3 + (i * 3), cols[3] + col_width - 5, "●", curses.A_BOLD)
        
        # Instructions
        stdscr.addstr(h-3, 2, "Navigation: Arrow Keys / Tab | Select: Enter | Refresh: r", curses.A_DIM)
        stdscr.addstr(h-2, 2, "Mouse: Click buttons | Quit: Press Ctrl+C", curses.A_DIM)
        
        stdscr.refresh()
    except Exception as e:
        pass

async def run_tui(stdscr):
    curses.curs_set(0)
    curses.use_default_colors()  # use terminals background
    curses.init_pair(1, -1, -1)  # foreground -1, background -1 = terminal defaults
    stdscr.nodelay(1)
    stdscr.timeout(100)
    curses.mousemask(curses.ALL_MOUSE_EVENTS)
    
    controller = ACController()
    
    # Animated connecting message
    connect_task = asyncio.create_task(controller.connect())
    dots = 0
    while not connect_task.done():
        stdscr.clear()
        dot_string = "." * (dots % 4)
        stdscr.addstr(0, 0, f"Connecting to AC{dot_string}   ")
        stdscr.addstr(1, 0, "(10 seconds, Ctrl+C to cancel)")
        stdscr.refresh()
        dots += 1
        await asyncio.sleep(0.3)
    
    connected = await connect_task
    
    if not connected:
        stdscr.clear()
        stdscr.addstr(0, 0, "Failed to connect. Press any key to exit.")
        stdscr.refresh()
        stdscr.nodelay(0)
        stdscr.getch()
        await controller.disconnect()
        return
    
    selected_col = 0
    selected_row = 0
    max_rows = [2, 2, 3, 4]  # Max rows per column
    
    try:
        last_refresh = 0
        while True:
            # Auto-refresh every second
            current_time = asyncio.get_event_loop().time()
            if current_time - last_refresh > 1.0:
                controller.update_status()
                last_refresh = current_time
            
            draw_menu(stdscr, controller, selected_col, selected_row)
            
            try:
                key = stdscr.getch()
                
                if key == ord('r'):
                    controller.update_status()
                elif key == curses.KEY_RIGHT or key == ord('\t'):
                    selected_col = (selected_col + 1) % 4
                    selected_row = 0  # Reset to first item in new column
                elif key == curses.KEY_LEFT:
                    selected_col = (selected_col - 1) % 4
                    selected_row = 0  # Reset to first item in new column
                elif key == curses.KEY_DOWN:
                    selected_row = min(selected_row + 1, max_rows[selected_col] - 1)
                elif key == curses.KEY_UP:
                    selected_row = max(selected_row - 1, 0)
                elif key == ord('\n') or key == curses.KEY_ENTER or key == 10:
                    # Execute action based on selected column/row
                    if selected_col == 0:  # Power
                        await controller.set_power(selected_row == 0)
                    elif selected_col == 1:  # Temperature
                        temp = int(controller.target_temp)
                        if selected_row == 0:  # Up
                            await controller.set_temp(temp + 1)
                        else:  # Down
                            await controller.set_temp(temp - 1)
                    elif selected_col == 2:  # Mode
                        modes = [ErdAcOperationMode.COOL, ErdAcOperationMode.FAN_ONLY, ErdAcOperationMode.ENERGY_SAVER]
                        await controller.set_mode(modes[selected_row])
                    elif selected_col == 3:  # Fan
                        fans = [ErdAcFanSetting.AUTO, ErdAcFanSetting.LOW, ErdAcFanSetting.MED, ErdAcFanSetting.HIGH]
                        await controller.set_fan(fans[selected_row])
                elif key == curses.KEY_MOUSE:
                    _, mx, my, _, _ = curses.getmouse()
                    # Calculate which button was clicked based on mouse position
                    col_width = 18
                    col_spacing = 2
                    start_x = 4
                    box_y = 6
                    
                    # Check each column
                    for col in range(4):
                        col_x = start_x + col * (col_width + col_spacing)
                        if col_x + 2 <= mx <= col_x + col_width - 2:
                            # Check which row
                            if col == 0:  # Power
                                if box_y + 2 <= my <= box_y + 4:
                                    await controller.set_power(True)
                                elif box_y + 5 <= my <= box_y + 7:
                                    await controller.set_power(False)
                            elif col == 1:  # Temp
                                if box_y + 2 <= my <= box_y + 4:
                                    temp = int(controller.target_temp)
                                    await controller.set_temp(temp + 1)
                                elif box_y + 6 <= my <= box_y + 8:
                                    temp = int(controller.target_temp)
                                    await controller.set_temp(temp - 1)
                            elif col == 2:  # Mode
                                modes = [ErdAcOperationMode.COOL, ErdAcOperationMode.FAN_ONLY, ErdAcOperationMode.ENERGY_SAVER]
                                for i in range(3):
                                    if box_y + 2 + (i * 3) <= my <= box_y + 4 + (i * 3):
                                        await controller.set_mode(modes[i])
                            elif col == 3:  # Fan
                                fans = [ErdAcFanSetting.AUTO, ErdAcFanSetting.LOW, ErdAcFanSetting.MED, ErdAcFanSetting.HIGH]
                                for i in range(4):
                                    if box_y + 2 + (i * 3) <= my <= box_y + 4 + (i * 3):
                                        await controller.set_fan(fans[i])
                    
            except curses.error:
                pass
            
            await asyncio.sleep(0.1)
    finally:
        await controller.disconnect()

def main(stdscr):
    try:
        asyncio.run(run_tui(stdscr))
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "on":
            async def quick_on():
                session = aiohttp.ClientSession()
                client = GeWebsocketClient(USERNAME, PASSWORD, REGION)
                task = asyncio.create_task(client.async_get_credentials_and_run(session))
                await asyncio.sleep(10)
                appliance = client.appliances.get(APPLIANCE_ID)
                if appliance:
                    await appliance.async_set_erd_value(ErdCode.AC_POWER_STATUS, ErdOnOff.ON)
                    await asyncio.sleep(1)
                    await appliance.async_set_erd_value(ErdCode.AC_OPERATION_MODE, ErdAcOperationMode.COOL)
                    await asyncio.sleep(2)
                    power = appliance.get_erd_value(ErdCode.AC_POWER_STATUS)
                    mode = appliance.get_erd_value(ErdCode.AC_OPERATION_MODE)
                    if power == ErdOnOff.ON and mode == ErdAcOperationMode.COOL:
                        print('✓ AC successfully turned ON (COOL mode)')
                    else:
                        print('✗ Failed to turn AC ON')
                else:
                    print('✗ Failed to connect to AC')
                
                if task and not task.done():
                    task.cancel()
                    try:
                        await asyncio.wait_for(task, timeout=0.5)
                    except (asyncio.CancelledError, asyncio.TimeoutError, Exception):
                        pass
                if session and not session.closed:
                    await session.close()
            
            asyncio.run(quick_on())
        
        elif sys.argv[1] == "off":
            async def quick_off():
                session = aiohttp.ClientSession()
                client = GeWebsocketClient(USERNAME, PASSWORD, REGION)
                task = asyncio.create_task(client.async_get_credentials_and_run(session))
                await asyncio.sleep(10)
                appliance = client.appliances.get(APPLIANCE_ID)
                if appliance:
                    await appliance.async_set_erd_value(ErdCode.AC_POWER_STATUS, ErdOnOff.OFF)
                    await asyncio.sleep(2)
                    power = appliance.get_erd_value(ErdCode.AC_POWER_STATUS)
                    if power == ErdOnOff.OFF:
                        print('✓ AC successfully turned OFF')
                    else:
                        print('✗ Failed to turn AC OFF')
                else:
                    print('✗ Failed to connect to AC')
                
                if task and not task.done():
                    task.cancel()
                    try:
                        await asyncio.wait_for(task, timeout=0.5)
                    except (asyncio.CancelledError, asyncio.TimeoutError, Exception):
                        pass
                if session and not session.closed:
                    await session.close()
            
            asyncio.run(quick_off())
    else:
        curses.wrapper(main)
