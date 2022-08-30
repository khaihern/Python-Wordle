import pygame
import random

# SETUP DISPLAY
pygame.init()
WIDTH, HEIGHT = 900, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle")

# SYSTEM VARIABLES
FPS = 60
clock = pygame.time.Clock()

# GAME VARIABLES
def set_game_variables():
  global cursor, guesses
  cursor = 0
  guesses = 0

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (211, 214, 218)
DARK_GRAY = (120, 124, 126)
GREEN = (106, 170, 100)
YELLOW = (201, 180, 88)

# FONTS
TITLE_FONT = pygame.font.SysFont("bahnschrift", 30)
LETTER_FONT = pygame.font.SysFont("bahnschrift", 16)
BOX_FONT = pygame.font.SysFont("bahnschrift", 30)
MSG_BOX_FONT = pygame.font.SysFont("bahnschrift", 20)

# LOAD TEXT
def load_text():
  global wordleWords, allWords # allWords contain all 5 letter English words; wordleWords contain only the most "common" words
  with open("wordleWords.txt", "r") as f:
    wordleWords = f.read().split(",")

  with open("allWords.txt", "r") as f:
    allWords = f.read().split(",")

# PICK A RANDOM WORD 
def pick_word():
  global word
  word = random.choice(wordleWords).upper()

# WORDLE BOXES CALCULATION
BOX_WIDTH = 55
BOX_GAP = 5
box_startx = round((WIDTH - (BOX_WIDTH + BOX_GAP) * 5) / 2) # Calculate where on the x-axis to start drawing the boxes
box_starty = 110

def setup_boxes():
  global boxes
  boxes = []
  for i in range(30):
    x = box_startx + BOX_GAP * 6 + ((BOX_WIDTH + BOX_GAP) * (i % 5)) # i%5 because there are 5 boxes in a row
    y = box_starty + ((i // 5) * (BOX_GAP + BOX_WIDTH))
    boxes.append([x, y, '', WHITE])

# KEYBOARD KEYS CALCULATION
KEY_WIDTH = 45
KEY_GAP = 10
LKEY_WIDTH = KEY_WIDTH*2 + KEY_GAP # width for the Enter key
key_startx = round((WIDTH - (KEY_WIDTH + KEY_GAP) * 9.5) / 2) # Calculate where on the x-axis to start drawing the keys
key_starty = 480
KEY_CHARS = ["Q","W","E","R","T","Y","U","I","O","P","A","S","D","F","G","H","J","K","L","Z","X","C","V","B","N","M","<<","Enter"]

def setup_keys():
  global letters
  letters = []
  for i in range(28):
    if i == 27:
      x = letters[26][0] + KEY_WIDTH/2 + KEY_GAP + LKEY_WIDTH/2
    else:
      x = key_startx + KEY_GAP + ((KEY_WIDTH + KEY_GAP) * (i % 9.5)) # i%9.5 is used to create desired keyboard layout (10 keys on top, 9 keys in middle, 7 letter keys and a backspace and 2 size enter key on the bottom)
    y = key_starty + ((i // 9.5) * (KEY_GAP + KEY_WIDTH))
    letters.append([x, y, KEY_CHARS[i], LIGHT_GRAY])

# SHOW POPUP MESSAGE
MSG_BOX_Y = 80
MSG_BOX_MARGIN = 12
def display_message(status):
  msg = ""
  if status == "won":
    match guesses:
      case 0:
        msg = "Genius"
      case 1:
        msg = "Magnificent"
      case 2:
        msg = "Impressive"
      case 3:
        msg = "Splendid"
      case 4: 
        msg = "Great"
      case 5:
        msg = "Phew" 
  elif status == "lost":
    msg = word 
  elif status == "not_in_list":
    msg = "Not in word list"

  msg_box_text = MSG_BOX_FONT.render(msg, 1, WHITE)
  msg_box = pygame.Rect(WIDTH/2 - msg_box_text.get_width()/2 - MSG_BOX_MARGIN, MSG_BOX_Y - msg_box_text.get_height()/2 - MSG_BOX_MARGIN/2, msg_box_text.get_width() + MSG_BOX_MARGIN*2, msg_box_text.get_height() + MSG_BOX_MARGIN/2*2) # The box width and height scale dynamically with the size of the text inside (msg_box_text)
  pygame.draw.rect(WIN, BLACK, msg_box, border_radius=3)
  WIN.blit(msg_box_text, (WIDTH/2 - msg_box_text.get_width()/2, MSG_BOX_Y - msg_box_text.get_height()/2))

  pygame.display.update()
  
  if status == "not_in_list":
    pygame.time.delay(1000) # Show message for 1 second
  else:
    pygame.time.delay(3000)

# CHECK GUESS
def check_guess():
  correct = 0
  word_letters = [*word] # Split character of string into array "ant" => ["a", "n", "t"]
  not_green = []
  for i in range(5):
    if boxes[5*guesses+i][2] == word_letters[i]: # letter in the box matches in the correct position with target word 
      boxes[5*guesses+i][3] = GREEN
      word_letters[i] = ""
      correct += 1
      
      for letter in letters:
        x, y, ltr, color = letter
        if ltr == boxes[5*guesses+i][2]:
          letter[3] = GREEN
    else:
      not_green.append(i) # store all the letters that are not green 

  for j in not_green:
    if boxes[5*guesses+j][2] in word_letters: 
      boxes[5*guesses+j][3] = YELLOW
      word_letters.remove(boxes[5*guesses+j][2]) # remove letter so that we won't have two "a" light up yellow for one "a" in a different position
      for letter in letters:
        x, y, ltr, color = letter
        if ltr == boxes[5*guesses+j][2] and color == LIGHT_GRAY: # don't change keyboard letter color if it's green "only upgrade colors"
          letter[3] = YELLOW
    else:
      boxes[5*guesses+j][3] = DARK_GRAY
      for letter in letters:
        x, y, ltr, color = letter
        if ltr == boxes[5*guesses+j][2] and color == LIGHT_GRAY:
          letter[3] = DARK_GRAY

  if correct == 5:
    return True # won the game
  return False

# DRAW
def draw():
  WIN.fill(WHITE)

  # draw title
  title_text = TITLE_FONT.render("Wordle", 1, BLACK)
  WIN.blit(title_text, (WIDTH/2 - title_text.get_width()/2, box_starty - 90))

  # draw keyboard
  for i, letter in enumerate(letters):
    x, y, ltr, color = letter
    key_width = LKEY_WIDTH if i == 27 else KEY_WIDTH # draw enter key with larger width
    key = pygame.Rect(x - key_width/2, y - KEY_WIDTH/2, key_width, KEY_WIDTH)
    pygame.draw.rect(WIN, color, key, border_radius=4)
    letter_text = LETTER_FONT.render(ltr, 1, (BLACK if color == LIGHT_GRAY else WHITE)) # draw black text on LIGHT_GRAY background else white text
    WIN.blit(letter_text, (x - letter_text.get_width()/2, y - letter_text.get_height()/2))

  # draw wordle input boxes
  for box in boxes:
    x, y, chr, color = box
    box_rect = pygame.Rect(x - BOX_WIDTH/2, y - BOX_WIDTH/2, BOX_WIDTH, BOX_WIDTH)
    if box[3] == WHITE:
      pygame.draw.rect(WIN, LIGHT_GRAY, box_rect, 2) # box with LIGHT_GRAY color size 2 outline and no fill
      box_text = BOX_FONT.render(chr, 1, BLACK)
    else:
      pygame.draw.rect(WIN, box[3], box_rect) # box with designated color and fill
      box_text = BOX_FONT.render(chr, 1, WHITE)

    WIN.blit(box_text, (x - box_text.get_width()/2, y - box_text.get_height()/2))
  
  pygame.display.update()

# SETUP GAME
def setup_game():
  global run
  run = True
  set_game_variables()
  load_text()
  pick_word()
  print(word)
  setup_keys()
  setup_boxes()

# GAME LOOP
def main():
  global run, cursor, guesses
  setup_game()

  while run:
    clock.tick(FPS) # runs the game at the same frame rate on all devices

    for event in pygame.event.get():
      if event.type == pygame.QUIT: # close the window if user "x" out
        run = False
        pygame.quit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        m_x, m_y = pygame.mouse.get_pos()
        for i, letter in enumerate(letters):
          x, y, ltr, color = letter
          if m_x > x - (LKEY_WIDTH if i == 27 else KEY_WIDTH)/2 and m_x < x + (LKEY_WIDTH if i == 27 else KEY_WIDTH)/2 and m_y > y - KEY_WIDTH/2 and m_y < y + KEY_WIDTH/2: # check if mouse position is inside the key
            if ltr == "<<": # backspace button hit
              if cursor != 0:
                cursor -= 1
                boxes[5*guesses+cursor][2] = ""
            elif ltr == "Enter":
              if cursor == 5:
                # check if the word entered is an actual word by seeing if it exist in the allWords list
                entered_word = ""
                for i in range(5):
                  entered_word = entered_word + boxes[5*guesses+i][2]
                if entered_word.lower() not in allWords:
                  display_message("not_in_list")
                  continue # if the word is nonexistent, skip all commands down and go to top of loop

                won = check_guess() # returns True if won, False if haven't won
                draw()
                if won:
                  print("You Won!")
                  display_message("won")
                  run = False
                elif guesses == 5: # all the guesses used up
                  print("You Lost!")
                  display_message("lost")
                  run = False
                else: # guess is incorrect, move to next guess
                  guesses += 1
                  cursor = 0
            elif cursor < 5:
              boxes[5*guesses+cursor][2] = ltr # type a letter
              cursor += 1

    draw()

  main() # start a new wordle game after the previous one is completed

if __name__ == "__main__": # Only run the game if the file is run directly, not if it's imported
  main()