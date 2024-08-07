import random
import wx

deck_cent  = [10] * 8 + [0] * 12
deck_left  = [10] * 8 + [0] * 12
deck_right = [10] * 8 + [0] * 12

my_decks = [deck_cent, deck_left, deck_right]


class Player:
    def __init__(self):
        self.data = [0] * 13
        self.inv = [0] * 15
        self.cat = False


def generate_card(deck):
    rand_int = random.randint(0, 13)
    while deck[rand_int] == 0:
        rand_int = random.randint(0, 13)

    return rand_int



class MyFrame(wx.Frame):

    def draw_card(self, which_deck):
        if which_deck == 'left':
            self.deck_left[self.card_left] -= 1
            self.card_left = generate_card(self.deck_left)
            self.button_left.SetBitmap(self.cards.GetSubBitmap((100*self.card_left,  148, 100, 148)))
        elif which_deck == 'right':
            self.deck_right[self.card_right] -= 1
            self.card_right = generate_card(self.deck_right)
            self.button_right.SetBitmap(self.cards.GetSubBitmap((100*self.card_right,  148, 100, 148)))
        else:
            self.deck_cent[self.card_cent] -= 1
            self.card_cent = generate_card(self.deck_cent)


    def __init__(self, parent, title, decks):
        super(MyFrame, self).__init__(parent, title=title, style=wx.MAXIMIZE)

        frame_size = self.GetSize()
        # [0] - WIDTH - 1538
        # [1] - HEIGHT - 866

        #INIT DECKS
        self.deck_cent  = decks[0]
        self.deck_left  = decks[1]
        self.deck_right = decks[2]

        #INIT TOP CARDS
        self.card_cent  = generate_card(self.deck_cent)
        self.card_left  = generate_card(self.deck_left)
        self.card_right = generate_card(self.deck_right)

        #INIT IMAGE SOURCE for CARDS
        self.cards = wx.Bitmap("Assets/cards.png", wx.BITMAP_TYPE_PNG)

        #INIT IMAGE for TOP CARDS
        self.card_cent_image  = self.cards.GetSubBitmap((0, 0, 100, 148))
        self.card_left_image  = self.cards.GetSubBitmap((100*self.card_left,  148, 100, 148))
        self.card_right_image = self.cards.GetSubBitmap((100*self.card_right, 148, 100, 148))

        panel = MyPanel(self)

        #INIT DECK-BUTTONS
        self.button_cent  = wx.BitmapButton(panel, bitmap=self.card_cent_image,  style=wx.NO_BORDER, pos=((frame_size[0]//2)-50, 50))
        self.button_left  = wx.BitmapButton(panel, bitmap=self.card_left_image,  style=wx.NO_BORDER, pos=(100, 300))
        self.button_right = wx.BitmapButton(panel, bitmap=self.card_right_image, style=wx.NO_BORDER, pos=(frame_size[0]-200, 300))

        #BIND DECK-BUTTONS to FUNCTIONALITY
        self.button_cent.Bind(wx.EVT_BUTTON,  lambda event: self.draw_card('cent' ))
        self.button_left.Bind(wx.EVT_BUTTON,  lambda event: self.draw_card('left' ))
        self.button_right.Bind(wx.EVT_BUTTON, lambda event: self.draw_card('right'))

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
