# Gesture-Based Programming Tutorials

Team BSc coursework, written with Jacob: a Python and OpenCV application that teaches basic programming through hand gestures and voice commands.

## The task

> This coursework aims to implement a visual programming language and accompanying environment in which end users can create simple programs using gestures.

> All the gestures should allow the user to implement basic programming concepts using a programming language that has been developed specifically for this task.

## Method

- **Gesture input:** OpenCV reads the camera and a Haar cascade detects the user's hand, which is drawn on screen as a cursor.
- **Voice input:** the `speech_recognition` library listens on the microphone and `recognize_google` converts the audio to text. A command is the activation phrase "ok program" plus a keyword such as `select`, `drop`, `run` or `help`.
- **Interface:** each screen is drawn with OpenCV. `Menu.py`, `Options.py` and `TaskScreen.py` are the menu screens, and `Tutorial1.py` to `Tutorial3.py` are the tutorials.
- **Concurrency:** each screen runs its speech and display routines on separate threads, so listening for speech does not freeze the display.
- **Navigation:** screens open one another with `exec(open("<file>.py").read())`.
- **Saved state:** the colour setting is kept in `Colour.txt` and tutorial progress in `Tutorial1.txt` to `Tutorial3.txt`.

Limitations stated in the write-up:

> The main issue with the program is the fact that it cannot be used from start to finish instead all different screens need to be accessed separately to avoid a crash.

> Although the program meets nearly all the requirements outlined in the requirements section some are missing in the current version of the program as the program does not show the user how to utilise data structures or modules these were not included due to time constraints and the scope of the program created.

## Results

The write-up records this testing plan. It has not been re-run for this repository. The write-up also records a navigation bug that the table does not show:

> During the testing phase, it was discovered that the menus would not work correctly when navigating from one screen to another, the problem occurs because the threads continue to run after the initial screen is closed and therefore the program attempts to pass button values for the first screen opened this would lead to the program not accepting the current screen button values.

| Test No | Description | Expected Result | Actual Result | Comments/ Changes Made |
| --- | --- | --- | --- | --- |
| 1 | Gesture Recognition | The program recognises the user’s hand and follows it  hand in real-time | As expected. | No changes made |
| 2 | Voice Recognition | The program will record and recognise users’ voice commands | As expected. | No changes made |
| 3 | Main menu: All buttons | Do all buttons work as expected on this screen? | As expected. | No changes made |
| 4 | Options: All buttons | Do all buttons work as expected on this screen? | As expected. | No changes made |
| 5 | Task Selection: All buttons | Do all buttons work as expected on this screen? | As expected. | No changes made |
| 6 | Tutorial Pages: All buttons | Do all buttons work as expected on this screen? | As expected. | No changes made |
| 7 | Tutorial 1: Task Steps | Do the tasks update with the task steps? | As expected. | No changes made |
| 8 | Tutorial 2: Task Steps | Do the tasks update with the task steps? | As expected. | No changes made |
| 9 | Tutorial 3: Task Steps | Do the tasks update with the task steps? | As expected. | No changes made |
| 10 | Voice Command – Start: All applicable pages | Does the start command take the user to the task selection screen? | As expected. (Menu Only) | No changes made |
| 11 | Voice Command – Options: All applicable  pages | Does the command take the user to the options screen? | As expected. (Menu Only) | No changes made |
| 12 | Voice Command – Quit: All applicable pages | Does the command quit the program? | As expected. (All Pages) | No changes made |
| 13 | Voice Command – Back: All applicable pages | Does the menu go back to the main options? | As expected. (Tutorial Only ) | No changes made |
| 14 | Voice Command – Help: All applicable pages | Does the help command display the help pop-up window? | As expected. (All Pages) | No changes made |
| 15 | Voice Command – Close: All applicable pages | Does the close command close the help pop-up window? | As expected. (All pages) | No changes made |
| 16 | Voice Command – Exit: All applicable pages | Does this send the user to the previous screen? | As expected. (All Pages, except Menu) | No changes made |
| 17 | Voice Command – Save: All applicable pages | Does this command save the users place in the tutorial? | As expected. (Tutorial Only ) | No changes made |
| 18 | Voice Command – Reset: All applicable pages | Does this command reset the tutorial to the beginning? | As expected. (Tutorial Only ) | No changes made |
| 19 | Voice Command – Run: All applicable pages | Does this command run the users code | As expected. (Tutorial Only ) | No changes made |
| 20 | Voice Command – Colour: All applicable pages | Does this command change the colour setting of the application | As expected. (Options Only ) | No changes made |
| 21 | Voice Command – Select: All applicable pages | Does this activate the button the user is hovering over? | As expected. (All Pages) | No changes made |
| 22 | Voice Command – Drop: All applicable pages | Does this command allow the user to drop a function into the code? | As expected. (Tutorial Only ) | No changes made |
| 23 | Voice Command – Input: All applicable pages | Does this command allow the user to input a var name? | As expected. (Tutorial Only ) | No changes made |
| 24 | Menu Navigation | Can the user navigate through the different menus? | As expected. (Menu Only) | No changes made |
| 25 | Options Changes | Do the options change the program on all screens? | As expected. (All Screens ) | No changes made |
| 26 | Tutorial Pages: Load Saved File | Do the tutorials continue where the user left off? | As expected. (Tutorial Only ) | No changes made |

## Data

Excluded from this repository:

- `Code/haarcascades/`: eight trained cascade XML files, including the `Hand.Cascade.1.xml` file the code loads.
- `Code/Colour.txt`: a one-byte saved setting.
- Four demonstration and tutorial videos (`.mp4`).
- The coursework write-up.

## How to run

**Not verified.** This copy has not been run.

Requirements taken from the code:

- A camera and a microphone. The camera is opened with `cv2.CAP_DSHOW`, a Windows capture backend.
- An internet connection, because the code calls `recognize_google`.
- The Python modules the code imports: `numpy`, `cv2`, `threading` and `speech_recognition`.
- A cascade file at `Code/haarcascades/Hand.Cascade.1.xml`. It is not in this repository, so it must be supplied first.

To start:

```
cd Code
python Menu.py
```

Run it from inside `Code`, because the code opens the other screens, the cascade file and its saved-state files by relative path.
