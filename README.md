# NOMI

![logo](https://github.com/LeonardoFerrisi/NOMI/logo_icon.png)

### Neurally Operated Musical Instrument Version 2.0

The Neurally Operated Musical Instrument (NOMI) is a program which allows users to create or rather, modulate music by altering and learning to control their brain state. NOMI comes with a GUI designed with QT designer and can be interfaced with a variety of headsets compatible with the Brainflow python package. The Brainflow python package also allows for simple implementations of sophisticated methods. NOMI consists of three core parts: a board communicator, a real-time EEG stream analyzer and a music generator. In order to ensure timely updates, the EEG stream is run on a separate thread than the music generation via python’s threading library. 

NOMI utilizes real-time EEG data to estimate the brain state of the user. NOMI currently supports two modes of operation: relaxation and concentration, each with their own assigned group of music channels. The user can also introduce their own .wav files for customized layering. The level of relaxation or concentration is currently determined using a pre-trained linear regression classifier, though other classifiers are also available via Brainflow. The prediction of the classifier is then mapped to thresholds of multiple music channels, where each channel has a different threshold. With increasing concentration (or relaxation), more channels are mixed and in a fully concentrated (or relaxed) state, all channels are mixed together. Pygame is used to mix and adjust the volume of the channels. 

### Running NOMI

In order to run NOMI, right now there is a demo script, `NOMI.py` available in src.

#### Setting up a virtual environment

To run NOMI under the desired conditions, in a terminal create a python virtual environment using:

`python -m venv .<your virual environment name>`

Then, once the environment has been setup, if you are on Windows activate using:

`.<your virtual environment name>\Scripts\activate`

and if you are on MacOS or Linux us

`source <your virtual environment name>\bin\activate`

#### Installing dependencies

Now that you are in your virtual environment (*Your console should have a `(<your virtual environment name>)` flag at the start of each new line*),
you can install the dependencies using:

`pip install -r requirements.txt`

Let the process finish and you should be all set to run without errors

#### Running

Run using:

`python NOMI.py`

#### Whats next?

**Coming soon:** 

- An improved more colorful UI for playing with this thing!
- Better audio files!

# 

###### NOMI v0.1 was initially built as a collabrative hackathon project for the NATHACKS 2021 Hackathon
