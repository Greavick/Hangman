import numpy as np
import arcade
import string
import csv

# Number of rows and columns of the grid
ROW_COUNT = 15
COLUMN_COUNT = 11

# GRID and LINE WIDTH of squared paper sheet
GRID_WIDTH = 50
LINE_WIDTH = 1
GL_WIDTH = GRID_WIDTH + LINE_WIDTH

# Calculations of necessary screen width and height
SCREEN_WIDTH = (GRID_WIDTH + LINE_WIDTH) * COLUMN_COUNT + LINE_WIDTH
SCREEN_HEIGHT = (GRID_WIDTH + LINE_WIDTH) * ROW_COUNT + LINE_WIDTH
SCREEN_TITLE = "Hangman"


class Hangman(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.LIGHT_STEEL_BLUE)
        self.playing = True
        self.grid_list = None

        # Holding count of the misses and hits of our guesses
        self.misses = 0
        self.hits = 0

        # Holds respective grid color code
        self.grid_color = np.zeros((ROW_COUNT, COLUMN_COUNT))
        self.recreate_grid()

        # Letter (Alphabet) Generator - upper case
        letter = self.get_letter()

        # Load randomly selected word from dictionary
        self.final_word = self.get_random_word()

        # Store currently discovered letters
        self.current_word = [' '] * len(self.final_word)

        # Mapping used for application keyboard (character input)
        self.letter_mapping = {}

        for row in range(3, 0, -1):
            for column in range(1, 10):
                if not (row == 1 and column == 9):
                    self.letter_mapping[column * 9 + row] = next(letter)

    # Resets game
    def reset(self):
        arcade.set_background_color(arcade.color.LIGHT_STEEL_BLUE)
        self.playing = True
        self.grid_list = None
        self.misses = 0
        self.hits = 0
        self.grid_color = np.zeros((ROW_COUNT, COLUMN_COUNT))
        self.recreate_grid()
        self.final_word = self.get_random_word()
        self.current_word = ['_'] * len(self.final_word)
        # print(self.final_word)

    # Returns random word from dictionary file
    def get_random_word(self):
        with open('dictionary', 'r') as f:
            reader = csv.DictReader(f)
            word_list = list(reader)
        r = np.random.randint(0, len(word_list)-1)
        return word_list[r]['Words'].upper()

    # Updating grid elements colors
    def recreate_grid(self):
        colors = {0: arcade.color.WHITE,
                  1: arcade.color.GREEN,
                  2: arcade.color.RED}

        self.grid_list = arcade.ShapeElementList()

        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):

                color = colors[self.grid_color[row][column]]

                x = GL_WIDTH * column + LINE_WIDTH + GRID_WIDTH // 2
                y = GL_WIDTH * row + LINE_WIDTH + GRID_WIDTH // 2

                current_rect = arcade.create_rectangle_filled(x, y, GRID_WIDTH, GRID_WIDTH, color)
                self.grid_list.append(current_rect)

    # Draws virtual keyboard and currently known part of the word
    def draw_letters(self):
        letter = self.get_letter()
        for row in range(3, 0, -1):
            for column in range(1, 10):
                x = GL_WIDTH * column + LINE_WIDTH + GRID_WIDTH // 2
                y = GL_WIDTH * row + LINE_WIDTH + GRID_WIDTH // 2
                if not (row == 1 and column == 9):
                    arcade.draw_text(next(letter), x, y, arcade.color.BLACK, 20,
                                     align="center", anchor_x="center", anchor_y="center")

        for column in range(1, len(self.final_word) + 1):
            x = GL_WIDTH * column + LINE_WIDTH + GRID_WIDTH // 2
            y = GL_WIDTH * 5 + LINE_WIDTH + GRID_WIDTH // 2
            arcade.draw_text(self.current_word[column - 1], x, y, arcade.color.BLACK, 20,
                             align="center", anchor_x="center", anchor_y="center")
            x = GL_WIDTH * column
            y = GL_WIDTH * 5 + GRID_WIDTH // 4
            arcade.draw_line(x + GRID_WIDTH // 6, y, x + GRID_WIDTH - GRID_WIDTH // 6, y, arcade.color.BLACK, 3)

    # Consecutive alphabet letter generator
    def get_letter(self):
        alphabet = string.ascii_uppercase
        for l in alphabet:
            yield l

    # Drawing 'Win' notification
    def draw_win(self):
        x = GL_WIDTH * 3 + LINE_WIDTH + GRID_WIDTH // 2
        y = GL_WIDTH * 10 + LINE_WIDTH + GRID_WIDTH // 2
        arcade.draw_text("YOU WON!", x, y, arcade.color.BLUE, 50)

        if not self.playing:
            x = GL_WIDTH * 7 + LINE_WIDTH + GRID_WIDTH // 2
            y = GL_WIDTH * 7 + LINE_WIDTH + GRID_WIDTH // 2
            arcade.draw_text("Try Again", x, y, arcade.color.BLACK, 20,
                             align="center", anchor_x="center", anchor_y="center")

    # Drawing 'Lose' notification
    def draw_lose(self):
        x = GL_WIDTH * 3 + LINE_WIDTH + GRID_WIDTH // 2
        y = GL_WIDTH * 10 + LINE_WIDTH + GRID_WIDTH // 2
        arcade.draw_text("YOU LOST!", x, y, arcade.color.BLUE, 50)

        if not self.playing:
            x = GL_WIDTH * 7 + LINE_WIDTH + GRID_WIDTH // 2
            y = GL_WIDTH * 7 + LINE_WIDTH + GRID_WIDTH // 2
            arcade.draw_text("Try Again", x, y, arcade.color.BLACK, 20,
                             align="center", anchor_x="center", anchor_y="center")

    # Drawing the hangman, depending on current number of misses
    def draw_hangman(self):
        # Gallows
        x1 = x2 = GL_WIDTH * 2 + LINE_WIDTH + GRID_WIDTH // 2
        y1 = GL_WIDTH * 7.5 + LINE_WIDTH
        y2 = GL_WIDTH * 12.5 + LINE_WIDTH + GRID_WIDTH
        arcade.draw_line(x1, y1, x2, y2, arcade.color.BROWN, 10)
        x3 = GL_WIDTH * 4 + LINE_WIDTH + GRID_WIDTH // 2
        arcade.draw_line(x2 - 5, y2, x3 + 5, y2, arcade.color.BROWN, 10)
        y3 = GL_WIDTH * 11.5 + LINE_WIDTH + GRID_WIDTH
        arcade.draw_line(x3, y2, x3, y3, arcade.color.BROWN, 10)

        # Right leg
        if self.misses > 5:
            x6 = GL_WIDTH * 4.5 + LINE_WIDTH + GRID_WIDTH // 2
            y5 = GL_WIDTH * 9 + LINE_WIDTH + GRID_WIDTH
            arcade.draw_line(x3, y3 - GRID_WIDTH * 2, x6, y5, arcade.color.BLACK, 10)
        # Left leg
        if self.misses > 4:
            x5 = GL_WIDTH * 3.5 + LINE_WIDTH + GRID_WIDTH // 2
            y5 = GL_WIDTH * 9 + LINE_WIDTH + GRID_WIDTH
            arcade.draw_line(x3, y3 - GRID_WIDTH * 2, x5, y5, arcade.color.BLACK, 10)
        # Right arm
        if self.misses > 3:
            x6 = GL_WIDTH * 4.5 + LINE_WIDTH + GRID_WIDTH // 2
            y5 = GL_WIDTH * 10 + LINE_WIDTH + GRID_WIDTH
            arcade.draw_line(x3, y3 - GRID_WIDTH, x6, y5, arcade.color.BLACK, 10)
        # Left arm
        if self.misses > 2:
            x5 = GL_WIDTH * 3.5 + LINE_WIDTH + GRID_WIDTH // 2
            y5 = GL_WIDTH * 10 + LINE_WIDTH + GRID_WIDTH
            arcade.draw_line(x3, y3 - GRID_WIDTH, x5, y5, arcade.color.BLACK, 10)
        # Body
        if self.misses > 1:
            arcade.draw_line(x3, y3 - GRID_WIDTH, x3, y3 - GRID_WIDTH * 2, arcade.color.BLACK, 10)
        # Head
        if self.misses > 0:
            y4 = y3 - GRID_WIDTH // 2
            arcade.draw_circle_outline(x3, y4, GRID_WIDTH // 2, arcade.color.BLACK, 5)

    # Draw functions calls
    def on_draw(self):
        # Checking if player won ...
        if self.hits == len(self.final_word):
            arcade.start_render()
            self.grid_list.draw()
            self.draw_letters()
            self.draw_hangman()
            self.draw_win()
            self.playing = False
        # ... or still misses available ...
        elif self.misses < 6:
            arcade.start_render()
            self.grid_list.draw()
            self.draw_letters()
            self.draw_hangman()
        # ... else end the game.
        else:
            arcade.start_render()
            self.current_word = self.final_word
            self.grid_list.draw()
            self.draw_hangman()
            self.draw_letters()
            self.draw_lose()
            self.playing = False

    # Control of the mouse input
    def on_mouse_press(self, x, y, button, modifiers):

        # Row and column numbers of a grid that had been pressed on.
        column = int(x // GL_WIDTH)
        row = int(y // GL_WIDTH)

        if row < ROW_COUNT and column < COLUMN_COUNT and self.playing:
            if self.grid_color[row][column] == 0 and row + 9 * column in self.letter_mapping:
                # If input letter is a good guess, mark it and update currently known letters and hits count.
                if self.letter_mapping[row + 9 * column] in self.final_word:
                    self.grid_color[row][column] = 1
                    for i, l in enumerate(self.final_word):
                        if l == self.letter_mapping[row + 9 * column]:
                            self.current_word[i] = l
                            self.hits += 1
                # If input is a wrong guess, mark it appropriately and increment misses count.
                else:
                    self.grid_color[row][column] = 2
                    self.misses += 1

        # Update colors of the grid according to new hit/miss.
        self.recreate_grid()

        # In case game had been finished, pressing on displayed 'Try Again' area will result in reset.
        if row == 7 and 5 < column < 8 and not self.playing:
            self.reset()


def main():
    Hangman(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
