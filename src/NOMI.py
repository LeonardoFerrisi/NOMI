from button import Button
import os
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter
from brainflow.ml_model import MLModel, BrainFlowMetrics, BrainFlowClassifiers, BrainFlowModelParams
from brainflow.exit_codes import *
import numpy as np
from pygame import mixer
import time
DIRNAME = os.path.dirname(__file__)

class NOMI:

    def __init__(self, boardID=-1, serial_port='', window_size=5, debug=False):
        
        # self.load_audio()

        self.debug = debug
        self.window_size = window_size

        # board values
        self.boardID = boardID
        self.serial_port = serial_port

    def play(self):
        self.perform_preflight(self.boardID, self.serial_port)
        time.sleep(3)
        while True:
            self.get_focus_val()


    def load_audio(self):
        """
        Loads all the wave files (actually plays them but sets the volumes to 0)
        While waiting for neural data, plays bolero's drum beat
        Each wav file is played on a different audio channel
        Returns nMusicChannels (number of audio channels)
        Note: the audio channel number is an index into the wav file
        """
        mixer.init()

        audioset = []

        for channel, audiofile in enumerate(audioset):
            audiopath = os.path.join(DIRNAME, audiofile)
            if self.debug: print(f"\nLoading {audiopath}\n")
            mixer.Channel(channel).play(mixer.Sound(audiopath), -1)  

    def set_vol(self, channel, value):
        """
        Set channel volume to `value`
        """
        mixer.Channel(channel).set_volume(value)

    def increase_vol(self, channel):
        '''
        increase vol on a channel
        '''
        self.set_vol(channel, 0.75)
    
    def mute(self, channel):
        """
        Mute a channel
        """
        self.set_vol(channel, 0.0)

    # ==========================================
    # Brainflow methods

    def perform_preflight(self, board, serial_port=''):

        self.prep_brainflow()
        print("Brainflow prepped")

        if board==38:
            self.connect_muse()
        elif board==0:
            if serial_port != '':
                self.connect_cyton(serial_port=serial_port)
            else:
                raise TypeError("Expected Serial Port, but got '' ")
        else:
            self.connect_synth()

        print(f"Board {board} connected")

        self.prep_ml()
        print("ML Prep completed")
        self.start_stream()
        print("Successfully streaming")

    def prep_brainflow(self):
        BoardShim.enable_board_logger()
        DataFilter.enable_data_logger()
        MLModel.enable_ml_logger()

    def connect_synth(self):
        params = BrainFlowInputParams ()
        self.board = BoardShim(BoardIds.SYNTHETIC_BOARD.value, params)
        self.master_board_id = self.board.get_board_id ()
        self.sampling_rate = BoardShim.get_sampling_rate (self.master_board_id)
        self.board.prepare_session ()
        self.connected = True

    def connect_muse(self):
        params = BrainFlowInputParams ()
        self.board = BoardShim(BoardIds.MUSE_2_BOARD.value, params)
        self.master_board_id = self.board.get_board_id ()
        self.sampling_rate = BoardShim.get_sampling_rate (self.master_board_id)
        self.board.prepare_session ()
        self.connected = True

    def connect_cyton(self, serial_port="COM4"):
        params = BrainFlowInputParams ()
        params.serial_port = serial_port # get some way to specify this
        self.board = BoardShim(BoardIds.CYTON_BOARD.value, params)
        self.master_board_id = self.board.get_board_id ()
        self.sampling_rate = BoardShim.get_sampling_rate (self.master_board_id)
        self.board.prepare_session()
        self.connected = True

    def prep_ml(self):
        print("\nPrepping ML...\n")
        # calc concentration
        concentration_params = BrainFlowModelParams (BrainFlowMetrics.CONCENTRATION.value, BrainFlowClassifiers.KNN.value)
        self.concentration = MLModel(concentration_params)
        self.concentration.prepare()
        self.ml_prepped = True
        print("\nML Prepped\n")
    
    def start_stream(self, nsamples=45000):
        self.board.start_stream(nsamples, '')
        self.streaming = True
        BoardShim.log_message (LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
        if not self.ml_prepped:
            self.prep_ml()

    def board_connected(self):
        return self.connected
    
    def get_current_data(self, seconds):
        data = self.board.get_current_board_data(self.sampling_rate*seconds)
        return data

    def get_focus_val(self):
        assert self.ml_prepped
        current_data = self.get_current_data(self.window_size)
        eeg_channels = BoardShim.get_eeg_channels (int (self.master_board_id))
        bands = DataFilter.get_avg_band_powers (current_data, eeg_channels, self.sampling_rate, True)
        feature_vector = np.concatenate ((bands[0], bands[1]))

        prediction = self.concentration.predict (feature_vector)
        print ('Concentration: %f' % prediction)
        return prediction

    # ========================================================================================================

if __name__ == "__main__":
    n = NOMI(boardID=-1, serial_port='')
    n.play()
    