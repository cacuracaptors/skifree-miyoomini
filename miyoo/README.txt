SkiFree - Miyoo Mini Plus / OnionOS Port
========================================

An unofficial port of the classic Windows game SkiFree (Chris Pirih,
1991) to run as a standalone OnionOS Port on the Miyoo Mini Plus, based
on the open-source decompilation of the original game
(https://github.com/yuv422/skifree_decomp) and its SDL2 source port
(https://github.com/Slayer366/skifree_sdl).

READY TO RUN
------------
Nothing else to download: the game's graphics are built into the
program, as in the PortMaster version of this same source port. SkiFree
has always been given away for free by its author, on its official site
(https://ski.ihoc.net/).

FEATURES
--------
- 60 frames per second, with the game running at exactly the original
  speed. Menu+Start switches back to the original 25 frames per second
  (see FRAME RATE below)
- Light on the battery: the program sleeps until the next frame
- Pixel-perfect 640x480 picture
- The status box in the original Windows "Terminal" font
- High Scores, as in the original (the 10 best results of each course),
  now with your name, typed with the buttons (see HIGH SCORES below)
- The signs on the title screen name the Miyoo buttons
- Silent, like the original game
- The Menu key quits when released, and only if no other button was
  pressed while it was held, so Menu+Start, Menu+Select and the OnionOS
  Menu+Power screenshot combo don't quit the game

INSTALLATION
------------
1. Extract this zip's contents to the root of your OnionOS SD card.
2. On the device, open the "Ports" menu - "SkiFree" should appear in the
   list. If not, use "refresh roms" at the bottom of the list.

CONTROLS
--------
  Button               Action
  -----------------------------------------------------
  D-pad                Move (as with the keyboard arrows)
  A                    Immediate down-right
  Y                    Immediate down-left
  L2                   Immediate left-face
  R2                   Immediate right-face
  B / R1               Jump
  X                    Slight jump
  L1                   Speed boost (on / off)
  Start                Pause / Resume
  Select               New game
  Menu key (Function)  Exit the game
  Menu + Start         Frame rate: 60 fps / original (25 fps)
  Menu + Select        High Scores

HIGH SCORES
-----------
The original game keeps the 10 best results of each of its three
courses (the time for Slalom and Tree Slalom, the style points for
Freestyle) and shows them when you reach the finish line: your result is
marked "<-- that's you", or shown below the list with "<-- try again!".
This port does the same, and adds your name to each result.

- When a run makes the top 10, the box opens by itself so you can type
  your name:
    D-pad Up/Down   choose the letter (shown inverted)
    D-pad Left      switch between upper and lower case
    D-pad Right     add a space
    A               keep the letter and move to the next one
    B               erase
    Start           save
- Saving an empty name uses the last name you typed ("Skier" at first).
- Press Menu+Select at any time to see the tables. D-pad Left/Right
  switches between the courses, Select asks whether to clear the table on
  the screen (A: yes, B: no), and A, B, Start or Y close the box.
- The game is paused while the box is open, and the Menu key does
  nothing, so the OnionOS Menu+Power screenshot combo works on it.
- Your scores are saved as soon as you save a name, in
  Roms/PORTS/Games/SkiFree/highscores.txt
  Keep that file when you update or reinstall the port. Extracting a new
  version's zip over the old one keeps it.

FRAME RATE
----------
The original game updates and draws the slope 25 times a second. This
port keeps the game running at that same rate, so speed, physics and the
timer are exactly the original's, but draws the picture 60 times a
second: between two updates, everything on screen is drawn part of the
way from where it was to where it is now.

Menu+Start switches between this (the default) and the original 25
frames per second, which uses a little less battery. The choice is saved
in Roms/PORTS/Games/SkiFree/framerate.cfg

KNOWN ISSUES
------------
- The decompilation's conversion to C is not byte-exact, so small
  differences from the Windows game may remain.
- Where the original showed an "Assertion Failed" box, this port writes
  it to Roms/PORTS/Games/SkiFree/log.txt and pauses the game, as pressing
  OK did in the original; press Start to carry on.

CHANGELOG
---------
- v1.0.0 - Initial release.

BUILDING FROM SOURCE
--------------------
Full source code, build instructions, and a list of every change made to
the upstream project are available in this port's GitHub repository:
https://github.com/cacuracaptors/skifree-miyoomini

CREDITS
-------
- Chris Pirih - the original SkiFree (1991)
- Eric Fry (yuv422) - the SkiFree decompilation
- jeff-1amstudios, brooksytech and Slayer366 - the SDL2 source port
- steward-fu - SDL2 for the Miyoo Mini (Plus)
- shauninman - union-miyoomini-toolchain
