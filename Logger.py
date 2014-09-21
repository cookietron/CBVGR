import pythoncom, pyHook, ctypes

#keyMonitor is used to not record repeat key down events when a key is held
keyMonitor = {}
recording = False
f = open('inputLog.tsv', 'w')
f.write('Program\tMessage\tTime\tDetails\n')
user32 = ctypes.windll.user32

def standardLog(event):
    f.write(str(event.WindowName)+'\t')
    f.write(str(event.MessageName)+'\t')
    f.write(str(event.Time)+'\t')

def OnMouseEvent(event):
    if event.MessageName in ('mouse left down','mouse left up','mouse right down','mouse right up'):
        standardLog(event)
        f.write(str(event.Position)+'\n')
    return True

def OnKeyboardEvent(event):
    if event.Key == 'Home' and event.MessageName == 'key down':
        hm.HookMouse()
        recording = True
        f.write('Resolution\t'+str(user32.GetSystemMetrics(0))+'\t'+str(user32.GetSystemMetrics(1))+'\n')
    elif event.Key == 'End':
        recording = False
        f.close()
        hm.UnhookMouse()
        hm.UnhookKeyboard()
    elif event.MessageName == 'key down':
        if keyMonitor.get(event.Key, False) == False:
            keyMonitor[event.Key] = True
            standardLog(event)
            f.write(str(event.Key)+'\n')
    elif event.MessageName == 'key up':
        keyMonitor[event.Key] = False
        standardLog(event)
        f.write(str(event.Key)+'\n')
    return True

hm = pyHook.HookManager()

hm.MouseAll = OnMouseEvent
hm.KeyAll = OnKeyboardEvent
hm.HookKeyboard()
hm.HookMouse()
pythoncom.PumpMessages()
