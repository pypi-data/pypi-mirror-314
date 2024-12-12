from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

# this is the popup class for settings
class SettingsPopup(Popup):
    def send_info(self, caller):
        self.caller = caller
        self.ids.gridSize.text = str(caller.grid_size)
        self.ids.winCount.text = str(caller.win_count)
    def apply_settings(self):
        if self.ids.gridSize.text != '' and int(self.ids.gridSize.text) > 0 and self.ids.winCount.text != '' and int(self.ids.winCount.text) > 0 and int(self.ids.winCount.text) <= int(self.ids.gridSize.text):
            self.caller.grid_size = int(self.ids.gridSize.text)
            self.caller.fill_grid()
            self.caller.win_count = int(self.ids.winCount.text)
            self.dismiss()

# this is the grid button class used in the main grid
class GridButton(Button):
    def send_info(self, caller, row, col):
        self.caller = caller
        self.row = row
        self.col = col
    def click(self):
        if self.text == '':
            self.text = self.caller.current_player
            self.caller.current_player = 'X' if self.caller.current_player == 'O' else 'O'
            self.caller.check_winner(self)

# this is the main grid class of the app
class MainGrid(GridLayout):
    def settings(self):
        popup = SettingsPopup()
        popup.send_info(self)
        popup.open()
    def reset(self):
        self.current_player = 'X'
        self.fill_grid()
    def fill_grid(self):
        self.current_player = 'X'
        game_grid = self.ids.gameGrid
        game_grid.clear_widgets()
        self.grid = []
        for i in range(self.grid_size):
            self.grid.append([])
            for j in range(self.grid_size):
                grid_button = GridButton()
                grid_button.send_info(self, i, j)
                game_grid.add_widget(grid_button)
                self.grid[i].append(grid_button)
        # its a bit weird to set the cols, and then return it as well, but it is necessary and it works
        game_grid.cols = self.grid_size
        return self.grid_size
    def check_winner(self, button_clicked):
        buttons_of_player = 0
        winner_buttons = []
        # checking both horizontal options
        checked = 0
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if self.grid[button_clicked.row][button_clicked.col + checked].text == button_clicked.text:
                    buttons_of_player += 1
                    winner_buttons.append(self.grid[button_clicked.row][button_clicked.col + checked])
            except:
                break
            checked += 1
        checked = 0
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if self.grid[button_clicked.row][button_clicked.col - checked].text == button_clicked.text:
                    buttons_of_player += 1
                    winner_buttons.append(self.grid[button_clicked.row][button_clicked.col - checked])
            except:
                break
            checked += 1
        if buttons_of_player >= self.win_count + 1: # the plus one is there because the button that was clicked last is counted twice
            self.winner(button_clicked.text, winner_buttons)
        # checking both vertical options
        buttons_of_player = 0
        checked = 0
        winner_buttons = []
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if self.grid[button_clicked.row + checked][button_clicked.col].text == button_clicked.text:
                    buttons_of_player += 1
                    winner_buttons.append(self.grid[button_clicked.row + checked][button_clicked.col])
            except:
                break
            checked += 1
        checked = 0
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if self.grid[button_clicked.row - checked][button_clicked.col].text == button_clicked.text:
                    buttons_of_player += 1
                    winner_buttons.append(self.grid[button_clicked.row - checked][button_clicked.col])
            except:
                break
            checked += 1
        if buttons_of_player >= self.win_count + 1:
            self.winner(button_clicked.text, winner_buttons)
        # checking the first pair of diagonal options
        buttons_of_player = 0
        checked = 0
        winner_buttons = []
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if self.grid[button_clicked.row + checked][button_clicked.col + checked].text == button_clicked.text:
                    buttons_of_player += 1
                    winner_buttons.append(self.grid[button_clicked.row + checked][button_clicked.col + checked])
            except:
                break
            checked += 1
        checked = 0
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if self.grid[button_clicked.row - checked][button_clicked.col - checked].text == button_clicked.text:
                    buttons_of_player += 1
                    winner_buttons.append(self.grid[button_clicked.row - checked][button_clicked.col - checked])
            except:
                break
            checked += 1
        if buttons_of_player >= self.win_count + 1:
            self.winner(button_clicked.text, winner_buttons)
        # checking the second pair of diagonal options
        buttons_of_player = 0
        checked = 0
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if self.grid[button_clicked.row - checked][button_clicked.col + checked].text == button_clicked.text:
                    buttons_of_player += 1
                    winner_buttons.append(self.grid[button_clicked.row - checked][button_clicked.col + checked])
            except:
                break
            checked += 1
        checked = 0
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if self.grid[button_clicked.row + checked][button_clicked.col - checked].text == button_clicked.text:
                    buttons_of_player += 1
                    winner_buttons.append(self.grid[button_clicked.row + checked][button_clicked.col - checked])
            except:
                break
            checked += 1
        if buttons_of_player >= self.win_count + 1:
            self.winner(button_clicked.text, winner_buttons)
    def winner(self, winner, winner_buttons):
        self.ids.currentPlayer.text = 'Winner is: ' + winner
        for button in self.ids.gameGrid.children:
            button.disabled = True
        for button in winner_buttons:
            button.background_color = (0, 1, 0, 1)

# app class
class TicTacToeApp(App):
    def build(self):
        return MainGrid()

# running the app
if __name__ == '__main__':
    TicTacToeApp().run()