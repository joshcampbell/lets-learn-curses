#!/usr/bin/env python

import json
import curses

game_state = json.loads(open("./fixture.json").read())

def main(screen):
  assert curses.has_colors(), "This game requires a color terminal."
  show_title(screen)
  game_loop(screen)

def show_title(screen):
  screen.clear()
  title = """

  """

def game_loop(screen):
  while True:
    # wait for user input
    key_pressed = screen.getch()
    
    

if __name__ == '__main__':
  curses.wrapper(main)
