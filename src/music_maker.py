#########################################
# NOMI Version 0.5                      #
# Neurally Operated Musical Instrument  #
#########################################

import time

import pygame
from threading import Thread
import os
import numpy as np
from src.signal_converter_relay import DataThread
from src.board_communicator import Comms as boardComm
from numpy_ringbuffer import RingBuffer


class MUSICMAKER:
    """
    A Neurally Operated Musical Instrument using the brainflow API to let you play music with your mind
    Documentation
    
    Can be run to test entire NOMI software
    """

    def __init__(self, boardID: int = -1, serialPort: str = '', brainStateVal: int = 1):
        self.board_id = boardID
        self.serial = serialPort
        self.newBoard = boardComm(self.board_id, self.serial)
        self.brainStateVal = brainStateVal  # either concentration or relaxation
        self.prediction = None
        self.nMusicChannels = None
        # self.multiplayer = myMultiPlayer()

        print('Welcome to NOMI: The Neurally Operated Musical Instrument \n ')

    def playWav(self, filename, channelNum):
        print(filename)
        # pygame.mixer.load(filename)
        pygame.mixer.Channel(channelNum).play(pygame.mixer.Sound(filename), -1)

    def increaseVolume(self, channelNum):
        '''
        "Max Volume" on a channel
        '''
        chan = pygame.mixer.Channel(channelNum)
        chan.set_volume(0.75)

    def decreaseVolume(self, channelNum):
        '''
        Turn off Volume on a channel
        '''
        chan = pygame.mixer.Channel(channelNum)
        chan.set_volume(0)

    def loadWav(self):
        """
        Loads all the wave files (actually plays them but sets the volumes to 0)
        While waiting for neural data, plays bolero's drum beat
        Each wav file is played on a different audio channel
        Returns nMusicChannels (number of audio channels)
        Note: the audio channel number is an index into the wav file
        """
        pygame.mixer.init()
        musicFolder = f"lib{os.path.sep}music{os.path.sep}"

        # NEEDS TO LOAD WAV FILES
        if self.brainStateVal == 0:  # Relaxation Files
            # filenames dict are chanNumber : wav file pairs
            filenames = {0: 'first_layer_r.wav', 1: 'second_layer_r.wav', 2: 'third_layer_r.wav',
                         3: 'fourth_layer_r.wav', 4: 'fifth_layer_r.wav'}
        elif self.brainStateVal == 1:  # Concentration Files
            filenames = {0: 'first_layer_c.wav', 1: 'second_layer_c.wav', 2: 'third_layer_c.wav',
                         3: 'fourth_layer_c.wav'}
        # number of music channels
        self.nMusicChannels = len(filenames)
        # play drumbeat while waiting for data to arrive
        self.playWav(f"{musicFolder}bolero_snare_drum.wav", self.nMusicChannels)
        self.increaseVolume(self.nMusicChannels)
        # play the wav files but set volume to 0

        for chan in range(self.nMusicChannels):
            # self.multiplayer.loop(filename=f"{musicFolder}{filenames[chan]}", channel=chan,loopTimes=100)

            self.playWav(f"{musicFolder}{filenames[chan]}", chan)

            self.decreaseVolume(chan)
            # dont need to do it in a loop... but dont forget to...
            # put the wavfiles on different channels and then an extra channel for drum beat while waiting for data to arrive
            # set the volume of all chans except for the drum beat to 0 while waiting for data to arrive
            # Note here that n_chans will also be an index for the drum beat

    def predToWavFeats(self, avg_prediction):
        """
        Gets prediction in MusicMaker (avg of the last 5 predictions output by brainAnalyzer)
        and gets nMusicChannels from loadWav
        For each prediction, adjusts the volume of the music channels
        Right now, the layering is fixed (First Layer, Second Layer...)
        With increasing concentration (or relaxation), more layers have volume on

        :param prediction: classifier prediction float 0-1
        :param nMusicChannels: Number of music channels integer
        :return: doesnt return anything, just adjusts volume
        """
        # if avg_prediction is not None:
        if str(avg_prediction) != 'nan': # couldnt check for nan so just looked for if the string version of it is nan
            # turn off the drum beat
            self.decreaseVolume(self.nMusicChannels)
            # takes the prediction of brain state and maps it to changes in the way that wav files are being played
            # thresholds = np.linspace(0.5, 0, self.nMusicChannels)
            if self.nMusicChannels == 5: # Basically these channels all have different thresholds so different files play in different ways
                thresholds = [.93, .87, .70, .2, .00]
            elif self.nMusicChannels == 4:
                thresholds = [.9, .5, .3, .00]

            for chan in range(self.nMusicChannels):
                if avg_prediction > thresholds[chan]:
                    # print("PREDICTION IS ABOVE THRESHOLD")
                    self.increaseVolume(chan)
                else:
                    self.decreaseVolume(chan)
        else:
            print('gathering data.... please hold')

    def musicMaker(self):
        # def listener(self, threshold):
        """
        # listens to brain state predictions and uses it to decide how to change the music
        # listens to prediction and then averages the last 5 predictions
        # calls predToWave to adjust volumes

        :return: average prediction
        """
        # imported DataThread from signal_converter_relayOld.py
        bciThread = DataThread(self.newBoard, self.brainStateVal)
        state = self.brainStateVal
        # if state == 0:
        # elif
        # if
        bciThread.start()  # starts the thread
        # self.bciThread.run()
        pHolder = RingBuffer(2) # prediction holder
        startTime = time.time()
        critval = 0.99
        counter = 0
        while True:

            # print('is running musicMaker')
            self.prediction = bciThread.prediction
            # print(f"Brain analyzer says prediction: {self.prediction} for brainstate {self.brainStateVal}")
            # Here it should update not every sample, but setting it to self.prediction
            pHolder.appendleft(self.prediction)

            avg_prediction = np.mean(pHolder)
            if avg_prediction > critval:
                counter+=1
            else:
                counter=0
            # print('Counter', counter)
            # if str(avg_prediction)!= 'nan':
                # print('Average prediction: ' + str(avg_prediction) + " || Time since start: " + str(time.time() - startTime) + " seconds")
            myDiff = np.diff(pHolder)
            self.predToWavFeats(avg_prediction)

    def start(self):
        self.initBoard()

    def initBoard(self):
        """
        Initiates board ... do we need this or does boardCommunicator take care of it?
        :param boardID: By default synthetic, can be set to the ID number of any board we want
        :param serial_port: By default nothing, can be set to the serial port taking data from your board
        """
        # run bc and scr
        # self.newBoard = boardComm(boardID, serial_port)
        self.newBoard.startStream()
        print('Now Streaming')
        # while True:
        #     pass

    def brainAnalyzer(self):
        """
        Sets up board and sends out brain state prediction
        :return:
        """
        # a = Thread(target=self.runBCIThread)
        b = Thread(target=self.musicMaker)
        # a.start()
        b.start()

    def initializeBoard(self):
        """
        Prepares the board for streaming and starts a stream
        :return:
        """
        self.newBoard.startStream()

    def update(self):
        """
        Updates the data stream from a board that is streaming
        :return:
        """


if __name__ == '__main__':
    # boardId = int(0)
    # serialPort = 'COM3'
    # #
    boardId = -1
    serialPort = ''

    instrument = MUSICMAKER(boardId, serialPort, brainStateVal=1)
    instrument.start()
    # loads the wav files and outputs
    # number of music channels
    instrument.loadWav()
    # HERE GOES NOTHING

    # threadA = Thread(target=instrument.brainAnalyzer())
    # threadA.start()
    instrument.brainAnalyzer()
    # threadB.run()
    # instrument.brainAnalyzer()
    # instrument.musicMaker()

