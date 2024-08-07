import wx


class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title)

        panel = MyPanel(self)

class MyPanel(wx.Panel):
    def __init__(self,parent):
        super(MyPanel, self).__init__(parent)

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(parent=None, title="Hello")
        frame.Show()

        return True
