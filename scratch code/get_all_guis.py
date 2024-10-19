import psutil
import win32gui
import win32process




def callback(hwnd, lParam):
  if win32gui.IsWindowVisible(hwnd) == False:
     return
  
  _, pid = win32process.GetWindowThreadProcessId(hwnd)
  lParam[pid] = win32gui.GetWindowText(hwnd)

allWindows = {}
win32gui.EnumWindows(callback, allWindows)

for process in psutil.process_iter():
    if process.pid in allWindows:
       print(process)
       print(allWindows[process.pid])

