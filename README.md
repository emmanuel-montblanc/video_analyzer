#Video analyzer

This project has as objective to allow you to download instagram clips, analyze them frame by frame, draw on it, and record your analysis, all in one program.

## Install
Clone the repository:  
`git clone https://github.com/emmanuel-montblanc/video_analyzer.git`  

Install the requirements:  
`pip install -r requirements.txt`

Install pyaudio:  
Using it is the only way I found so far to record the voice with python, but installing it sucks, you can't directly install it by doing "pip install pyaudio" if you re using python3.
If you're using python3, go to https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio and download the version corresponding to your python version. Go to the folder where it was downloaded, open a console, and install it with the file, for example:  
`pip install PyAudio-0.2.11-cp37-cp37m-win_amd64.whl`

Install ffmpeg:  
To merge the audio and the video of the recording, I'm using ffmpeg, you also have to install it. To do so, go to https://github.com/BtbN/FFmpeg-Builds/releases and download the version corresponding to your system, and simply extract it to somewhere on your computer.
Then add the path to the binaries of ffmpeg to your system PATH. To check it is correctly installed, you can simply type `ffmpeg` in a console and see if the version of ffmpeg is printed.

I'm realising that the recording is really annoying to install, and maybe not the most useful, I will probably make a version without the recorder later to make it easier to install.

## Usage
To execute the program, you just have to go in the video_analyzer folder, then in the script folder, and execute the python script "select_vid":  
`python select_vid.py`

You can then either analyze a local video by clicking on "analyze local vid" and then selecting the video you want to analyze in the dialog, or an instagram video by clicking on "analyze instagram vid" and then entering the url of the post and clicking on "ok".

The video will then be downloaded to the folder "insta_videos" (if you chose an instagram video), and then all the frames of the videos will be extracted to the folder "videos"/<name_of_the_video>.  

The analysis window will open, and you will be able to play the video with different speed or play it using your mouse, to zoom on it and to draw on it and to record your analysis. If you want more info on the buttons of this window, you can click on the "help" button.

Finally once you finished your analysis, if you want you can analyze another video and return to the starting window by clicking on "change video", or you can simply close the window if you're done.

## Contact
If you encounter any problems or bug while using or installing the program, report it to me via mail or insta, it always helps.
Same, if you have any suggestion of what to implement/improve next, feel free to contact me to suggest it.

mail: emmanuel.montblanc@insa-lyon.fr  
insta: emmanuelmontblanc
