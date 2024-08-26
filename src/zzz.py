"""
This script is hard-coded for the most part,
from the ascii art to the lyrics.
No external libraries required for this to run, enjoy.
"""


import time
import os

# Screen size
width = 60
height = 12

# Road frames
road_frames = [
    "===   ===   ===   ===   ===   ===   ===   ===   ===   ===   ===   ===",    # 70 chars > width   ==> OK
    "==   ===   ===   ===   ===   ===   ===   ===   ===   ===   ===   === ",
    "=   ===   ===   ===   ===   ===   ===   ===   ===   ===   ===   ===  ",
    "   ===   ===   ===   ===   ===   ===   ===   ===   ===   ===   ===   ",
    "  ===   ===   ===   ===   ===   ===   ===   ===   ===   ===   ===   =",
    " ===   ===   ===   ===   ===   ===   ===   ===   ===   ===   ===   =="
]

seek = 70   # skip first 70s of the song
end = 104   # timestamp when will the car goes out of the screen (end animation)

# song: Kam Prada - Angel
lyrics = {
    71 : "You look like an angel",
    73 : "but you gave me hell",
    76 : "I picked that bottle right up from that shelf",
    80 : "From lovers to strangers,",
    82 : "I broke from your spell",
    84 : "I need sum stronger,",
    86 : "these tall ones won't help",
    88 : "I know now I see it,",
    90 : "I know all your secrets",
    92 : "You look like an angel",
    94 : "but got me fighting demons",
    97 : "You look like an angel",
    99 : "but you gave me hell",
    103 : "hell",
    105 : "hell..."
}

# Read file -> get art
def read_ascii_art(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

# Get the car art
script_dir = os.path.dirname(os.path.abspath(__file__))
car_file_path = os.path.join(script_dir, 'arts/car.txt')
car_file_path2 = os.path.join(script_dir, 'arts/car2.txt')
car_frames = [
    read_ascii_art(car_file_path),
    read_ascii_art(car_file_path2)
]

# Format seconds -> timer
def get_formatted_time(seconds) -> str:
    mins, secs = divmod(seconds, 60)
    return f"{mins:02}:{secs:02}"


# Update the Screen
def update_screen(sentence, car_art, car_pos, road, current_time):
    # Clear the screen array
    # for y in range(height):
    #     for x in range(width):
    #         screen[y][x] = ' '

    # Place the timer at top left corner of the screen
    ft = get_formatted_time(current_time)
    for x, char in enumerate(ft):
        if 0 <= x < width:
            screen[0][x] = char

    # Place the road first, then the car will override it
    for x, char in enumerate(road):
        if 0 <= x < width:
            screen[-1][x] = char
    
    # Place the car art in the bottom part of the screen
    car_height = len(car_art)
    for y, line in enumerate(car_art):
        if height - car_height + y < height:  # Ensure within vertical bounds
            line = line.rstrip()  # Remove trailing newline characters
            for x, char in enumerate(line):
                if 0 <= car_pos + x < width:
                    screen[height - car_height + y][car_pos + x] = char
            
            # clear junk character on the left side of car_pos
            if 0 <= car_pos-1 < width:
                screen[height - car_height + y][car_pos-1] = ' '
    
    # Place the sentence above the car
    if sentence is not None:
        sentence_y = height - len(car_art) - 3
        for x, char in enumerate(sentence):
            if 0 <= x < width:
                screen[sentence_y][x] = char

        # clear junk characters on the right side of the sentence
        for i in range(len(sentence), width):
            screen[sentence_y][i] = ' '

# Render the screen
def render_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("┏", end="")
    print("━" * (width + 1), end="")
    print("┓")
    for row in screen:
        print("┃ "+''.join(row)+"┃")
    print("┗", end="")
    print("━" * (width + 1), end="")
    print("┛")

# init array
screen = [[' ' for _ in range(width)] for _ in range(height)]

# main func
def animate():
    
    start_time = time.time()
    road_frame_index = 0
    car_frame_index = 0
    car_pos = 0

    while True:
        # get road frame based on current index
        if road_frame_index >= len(road_frames):
            road_frame_index = 0
        
        if road_frame_index == 0 or road_frame_index == 3:
            car_frame_index = 0 if car_frame_index == 1 else 1

        # get lyric based on timestamp
        lyric = None
        second = int(time.time() - start_time) + seek
        if lyrics.get(second, None) is not None:
            lyric = lyrics.get(second)
        
        if second > end:
            car_pos += 1

        update_screen(lyric, car_frames[car_frame_index], car_pos, road_frames[road_frame_index], second)
        render_screen()
        road_frame_index += 1
        time.sleep(0.03)


if __name__ == "__main__":
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        input("Press Enter to start ...")
        animate()
    except KeyboardInterrupt:
        pass
    else:
        raise
