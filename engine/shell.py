import textengine
import getch

textengine.init()
textengine.player.model.load('player')
getch_moves = {
    b'w': [0, -1],
    b'a': [-1, 0],
    b's': [0, 1],
    b'd': [1, 0],
}
textengine.area.draw()
while True:
    letter = getch.getch()
    if letter == b'\t':
        textengine.close()
    textengine.player.move(getch_moves[letter])
    textengine.area.draw(text_under=f'x: {textengine.player.get_coords()[0]}; y: {textengine.player.get_coords()[1]}', timer=0)
