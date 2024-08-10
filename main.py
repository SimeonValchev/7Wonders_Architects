import random
import wx

deck_cent = [0] + [10] * 14
deck_left = [0] + [10] * 14
deck_right = [0] + [10] * 14

my_decks = [deck_cent, deck_left, deck_right]
inventions = [1] * 15


class Player:
    def __init__(self):
        self.data = [0] * 13
        self.inv = [0] * 15
        self.cat = False


def generate_card(deck):
    rand_int = random.randint(1, 14)
    while deck[rand_int] == 0:
        rand_int = random.randint(1, 14)

    return rand_int


class MyFrame(wx.Frame):

    def draw_card(self, which_deck):
        if which_deck == 'left':
            self.deck_left[self.card_left] -= 1
            self.card_left = generate_card(self.deck_left)
            self.button_left.SetBitmap(self.cards.GetSubBitmap((100 * self.card_left, 0, 100, 148)))
        elif which_deck == 'right':
            self.deck_right[self.card_right] -= 1
            self.card_right = generate_card(self.deck_right)
            self.button_right.SetBitmap(self.cards.GetSubBitmap((100 * self.card_right, 0, 100, 148)))
        else:
            self.deck_cent[self.card_cent] -= 1
            self.card_cent = generate_card(self.deck_cent)

    def hover_cent_deck(self, cat, hover):
        if cat:
            if hover:
                self.button_cent.SetBitmap(self.cards.GetSubBitmap((100 * self.card_cent, 0, 100, 148)))
            else:
                self.button_cent.SetBitmap(self.cards.GetSubBitmap((0, 0, 100, 148)))

    def OnPaint(self, event):

        wonder_leftside = wx.Bitmap('Assets/wonder_babylon.png', wx.BITMAP_TYPE_PNG).GetSubBitmap((0, 0, 350, 318))
        wonder_rightside = wx.Bitmap('Assets/wonder_alexandria.png', wx.BITMAP_TYPE_PNG).GetSubBitmap((0, 0, 350, 472))
        icons = wx.Bitmap('Assets/main_icons.png', wx.BITMAP_TYPE_PNG)
        peace_icons = wx.Bitmap('Assets/war_icons.png', wx.BITMAP_TYPE_PNG).GetSubBitmap((75, 0, 75, 75))
        invent_icons = wx.Bitmap('Assets/progress - Copy.png', wx.BITMAP_TYPE_PNG).GetSubBitmap((0, 0, 100, 100))

        # BACKGROUND
        bg_image = wx.Bitmap('Assets/background.png', wx.BITMAP_TYPE_PNG)
        dc = wx.PaintDC(self.panel)
        panel_size = self.panel.GetSize()

        img_width = bg_image.GetWidth()
        img_height = bg_image.GetHeight()

        # Tile the image across the panel
        for x in range(0, panel_size.width, img_width):
            for y in range(0, panel_size.height, img_height):
                dc.DrawBitmap(bg_image, x, y)

        # TRANSPARENT PNGs
        dc.SetBackground(wx.Brush("WHITE"))
        dc.DrawBitmap(wonder_leftside, 100, self.GetSize()[1]-200 - wonder_leftside.GetSize()[1], True)
        dc.DrawBitmap(icons, 50, self.GetSize()[1]-200, True)
        dc.DrawBitmap(peace_icons, 50+93, 63, True)
        dc.DrawBitmap(peace_icons, 135+93, 63, True)
        dc.DrawBitmap(peace_icons, 220+93, 63, True)
        dc.DrawBitmap(invent_icons, self.GetSize()[0] - 480, 50, True)
        dc.DrawBitmap(invent_icons, self.GetSize()[0] - 370, 50, True)
        dc.DrawBitmap(invent_icons, self.GetSize()[0] - 260, 50, True)
        dc.DrawBitmap(invent_icons, self.GetSize()[0] - 150, 50, True)
        dc.DrawBitmap(wonder_rightside, self.GetSize()[0]-450, self.GetSize()[1]-200 - wonder_rightside.GetSize()[1], True)

    def __init__(self, parent, title, decks):
        super(MyFrame, self).__init__(parent, title=title, style=wx.MAXIMIZE)

        frame_size = self.GetSize()
        # [0] - WIDTH - 1538
        # [1] - HEIGHT - 864

        # INIT DECKS
        self.deck_cent = decks[0]
        self.deck_left = decks[1]
        self.deck_right = decks[2]

        # INIT TOP CARDS
        #   these represent indexes, each index is associated with a card
        self.card_cent = generate_card(self.deck_cent)
        self.card_left = generate_card(self.deck_left)
        self.card_right = generate_card(self.deck_right)

        # INIT IMAGE SOURCE for CARDS
        self.cards = wx.Bitmap("Assets/cards_regular.png", wx.BITMAP_TYPE_PNG)

        # INIT IMAGE for TOP CARDS
        card_cent_image = self.cards.GetSubBitmap((0, 0, 100, 148))
        card_left_image = self.cards.GetSubBitmap((100 * self.card_left, 0, 100, 148))
        card_right_image = self.cards.GetSubBitmap((100 * self.card_right, 0, 100, 148))

        # INIT IMAGE for INVENTIONS

        self.panel = MyPanel(self)
        #INVENTIONS CLICK
        #self.panel.Bind(wx.EVT_LEFT_DOWN, lambda event: self.draw_card('left'))

        # BACKGROUND
        self.panel.Bind(wx.EVT_PAINT, self.OnPaint)

        # QUIT BUTTON
        quit_image = wx.Bitmap('Assets/ex.png', wx.BITMAP_TYPE_PNG)
        quit_image_hover = wx.Bitmap('Assets/exq.png', wx.BITMAP_TYPE_PNG)
        button_quit = wx.BitmapButton(self.panel, bitmap=quit_image, style=wx.NO_BORDER, pos=(frame_size[0] - 30, 0))

        button_quit.Bind(wx.EVT_BUTTON, lambda event: self.Close())
        button_quit.Bind(wx.EVT_ENTER_WINDOW, lambda event: button_quit.SetBitmap(quit_image_hover))
        button_quit.Bind(wx.EVT_LEAVE_WINDOW, lambda event: button_quit.SetBitmap(quit_image))

        # INIT DECK-BUTTONS
        self.button_cent = wx.BitmapButton(self.panel, bitmap=card_cent_image, style=wx.NO_BORDER,
                                           pos=((frame_size[0] // 2) - 50, 50))
        self.button_left = wx.BitmapButton(self.panel, bitmap=card_left_image, style=wx.NO_BORDER,
                                           pos=((frame_size[0] // 2)-200, (frame_size[1] // 2)-25))
        self.button_right = wx.BitmapButton(self.panel, bitmap=card_right_image, style=wx.NO_BORDER,
                                            pos=((frame_size[0] // 2)+100, (frame_size[1] // 2)-25))

        # BIND DECK-BUTTONS to FUNCTIONALITY
        self.button_cent.Bind(wx.EVT_BUTTON, lambda event: self.draw_card('cent'))
        self.button_left.Bind(wx.EVT_BUTTON, lambda event: self.draw_card('left'))
        self.button_right.Bind(wx.EVT_BUTTON, lambda event: self.draw_card('right'))

        # BIND HOVERING CENT-DECK for CAT TOTEM FUNCTIONALITY
        self.button_cent.Bind(wx.EVT_ENTER_WINDOW, lambda event: self.hover_cent_deck(True, True))
        self.button_cent.Bind(wx.EVT_LEAVE_WINDOW, lambda event: self.hover_cent_deck(True, False))


class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(parent=None, title="Hello", decks=my_decks)
        frame.ShowFullScreen(True)

        return True


app = MyApp()
app.MainLoop()
