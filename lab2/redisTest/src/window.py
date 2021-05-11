import win32gui
import ctypes
def getNameOfActiveWindow():
    w=win32gui
    return w.GetWindowText(w.GetForegroundWindow())
def changeTheNameTitle(login):
    ctypes.windll.kernel32.SetConsoleTitleW(login)
    return True



