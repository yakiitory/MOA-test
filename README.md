# MOA-test
A method of adjustment listening test software used for preference headphone studies.

## Setup
The MOA-test requires installing Python 3.11.x.
First, you must install the tkinter module and the openpyxl module, so in Command Prompt, type:
```
pip install tk openpyxl
```
Afterwards, run the main python file (main.py)
## Instructions of usage:
1) Import DF-equalized headphone file onto EqualizerAPO.
2) Create a file "Preference.txt" on config folder.
3) Use this format for Preference.txt
```
Preamp: -10 dB
Filter 1: ON LSC Fc 112 Hz Gain 0 dB Q 0.350
Filter 2: ON HSC Fc 3550 Hz Gain 0 dB Q 0.350
Filter 3: ON LSC Fc 105 Hz Gain 0.00 dB Q 0.770
Filter 4: ON HSC Fc 2500 Hz Gain 0 dB Q 0.350
Filter 5: ON PK Fc 2800 Hz Gain 0 dB Q 1.800
Filter 6: ON LSC Fc 50 Hz Gain 0.00 dB Q 0.500
```
4) If additional music files are needed, it has to be placed inside the "music" folder. Feel free to add numbers in the music name for a custom order
