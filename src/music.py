import musicalbeeps as msb

pl = msb.Player(volume = 0.5, mute_output = False)
p2 = msb.Player(volume = 0.5, mute_output = False)
p2.play_note("C",2)
pl.play_note("E1",0.5)
pl.play_note("E1",0.5)
pl.play_note("F1",0.5)
pl.play_note("G1",0.5)
p2.play_note("G",2)
pl.play_note("G",0.5)
pl.play_note("F",0.5)
pl.play_note("E",0.5)
pl.play_note("D",0.5)
p2.play_note("A",2)
pl.play_note("C",0.5)
pl.play_note("C",0.5)
pl.play_note("D",0.5)
pl.play_note("E",0.5)
pl.play_note("E",0.5)
pl.play_note("D",0.5)
pl.play_note("D",0.5)
pl.play_note("D",0.5)
pl.play_note("D",0.5)