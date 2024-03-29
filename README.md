# Broadcast Latency Tester
![Block Diagram](doc/read.png)

## Purpose

The "Broadcast Latency Tester" (BLT) solves two problems

1. Having a source available with a frame counter, allowing latency comparisons
2. Having a source available with GLITS on to measure audio sync

Without having to have expensive proprietary equipment. This will run on any machine with a blackmagic card.

## Installation

To install blt, use Ubuntu 20.04 and install the blt package. Also install the Blackmagic drivers - 12.2 is a good year. Update the firmware and reboot. 

Visit the Setting page: http://server.ip/blt/settings.cgi. Ensure the configuration options are correct and hit save. 

Then proceed to the calibration settings section. Recommended process is first calibrate the generator

1. Ensure NTP is correctly synced at the top of the settings page

2. Ensure your own desktop machine is synced by checking at https://time.is

3. Put the setting clock (driven from your internal clock) next to a monitor showing the output of BLT

4. Take a photo, and make sure the displayed times are accurate

Then you calibrate the reader. Push the otuput of the BLT into the input, and return to the reader, where it says something like
    Video latency calculated at 4, with a built in calibration of 3 frames meaning latency = 1 frames, but this relies on various factors. 

5. Adjust the number on the setting page so the video latency = 0 frames. This is always plus-or-minus a frame, so aiming for a latency of 1 may be a better (area for future discussion)

It's plausbile the delay through a given model of blackmagic card is always the same, so using the recommended setting may do the job

## Usage
Once installed the BLT generator should run by itself. To use the reader, simply visit the BLT webpage and see the display.


### Measuring audio sync

Take the output of the BLT and route into a video encoder. Point the encoder at a decoder, and route the decoder back to the BLT. See the webpage to ensure the signal is looping through and the reported audio latency is correct. Leave to run for a few hours.

![Block Diagram](doc/bd1.png)

The BLT can test other SDI signal chain, but it's main purpose is for measuring IP encode/decode latency and drift

### Measuring video latency (method 1)

Set up the system as for measuring audio sync, but tee off to two separate monitors

![Block Diagram](doc/bd2.png)

Take a picture of the two identical monitors or multiviewer inputs, subtract the frame count, and that's your latency. To ensure your monitors are introducing different delays, it's worth swapping the inputs round just con confirm

### Measuring video latency (method 2)
This **requires** a calibrated encoder and decoder, but can be used when you don't have two monitors in the same room/continent

![Block Diagram](doc/bd3.png)

### Measuring change over time
BLT will log data over time, just look at the graph on the website.

## Details
### Generator
![Testcard](doc/tc.png)

Using FFMPEG and a blackmagic card we can create a fairly useful test card

It has the following features

#### Left/Right GLITS
![Left Indicator](doc/glits-left.png) ![Right Indicator](doc/glits-right.png)

In the top left corner, every 4 seconds, audio vanishes on the left leg and a red square, 100px * 100px, appears. Shortly after audio vanishes on the right leg and a green square appears offset from the left square by 100px. 

(The audio isn't neccersarilly 1kHz / 0dB)

#### Moving frame-rate box
![Frame movement](doc/framerate.png)

The top box moves rightwards every frame, crossing the screen once per second, showing a codec hasn't frozen

#### Moving field-rate box

![Field movement](doc/fieldrate.png)

The top box moves rightwards every field, crossing the screen once per second, showing if fields are reversed or something else is "off" with them, it should appear smoother than the frame-rate box above

#### Field indicator
![Field Indicator](doc/fieldind.png)

Field 1 or Field 2 is printed on each field, showing if just one field is shown

#### Frame counter
A number since the start increments, one per frame, allowing easy comparison between two different sources with different latencies

![Frame indicator](doc/framecounter.png)

#### Time of day
![TimeOfDay](doc/tod.png)

The time of day of the generating computer. This is based on NTP from the generating machine, however needs calibrating to cope with different cards. The end-to-end latency for an encode+decode process is typically 6 frames, but the output needs calibrating by comparing with a correct time of day source.

The date is encoded in binary underneath (the < and > characters), allowing a reader application to easily decode and calculate end to end delay between different sites without using an excessive amount of CPU OCRing each frame. The time is based on the start time plus the number of displayed frames. This does seem to drift about 1 frame an hour, as such BLT by default automatically restarts the output process every 30 minutes.

### READER
![Reader webpage](doc/read.png)

A program can be used to decode the testcard, this outputs as a webpage showing the current input picture, and decoding it



#### Audio Offset
This records the time between the audio supposed to be vanishing (at the start of the first frame when solid red is shown in the top left corner), and the audio actually vanishing. This is graphed in blue over the last few hours on the right of the screen and displayed in milliseconds. 


#### Latency
This decodes the time of day, there are caveat. The time of day is measured by counting the number of frames from when the decoder changes second to when the received decoder changes second. Latency could be a frame out either way even when calibrated due to clock drift, and assumes both encoder and decoder are synced with NTP



## License

This program is licensed under GPL, do whatever you want with it (laugh etc), just give back your changes. The C++ code for the Capture program is based on the blackmagic sample code from the decklink drivers, with the license in the header of the files. The modifications to ffmpeg are in [github](https://github.com/isostatic/FFmpeg) (because the code is awful and far to embarrasing to mention to geniuses behind ffmpeg). The binaries provided in this repo are built under x64/ubuntu 20.04 with desktopvideo 12.2.2a6

The "1-20" count on channel 2 is from https://freesound.org/people/EnjoyPA/sounds/203066/, user "EnjoyPA", released under CC0

---

# TODOs

## Installation
* detect first time installation and apply recommended settings (including correct card detection)
* Calibration for audio samples? Currently a few samples off, less than 1ms

## Time based
* Expose timezone selection in settings.cgi
* check an NTP daemon is running as well as checking in sync

## Displays
* Manage older log/capture files
* Expose older log/capture files
* Make the graph javascript based slippygraph
* detected decoder code seems to be a bit haywire in recent versions
* overlay changes in detected decoder
* Cope better with invalid sources when it comes to the graph (and the detector)

## Core functions
* Allow authentication on webpage (based on http header perhaps?)
* Support more than just 1080i25 - UHD for example
* Record - detect it's working or failed rather than just waiting and hoping

