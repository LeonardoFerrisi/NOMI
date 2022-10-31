import time
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets, LogLevels

class Comms:

    def __init__(self, board_id, serial_port=None):
        params = BrainFlowInputParams()

        if board_id != -1: 
            assert serial_port != None
            params.serial_port = serial_port

        self.board_id = board_id
        self.params = params
        self.board = BoardShim(board_id, params)
        self.sampling_rate = self.board.get_sampling_rate(board_id)
        self.live = False

    def start(self, inf=False, runtime=10):
        self.board.prepare_session()
        self.board.start_stream()
        self.live = True
        BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
        if not inf:
            time.sleep(runtime)
            self.stop()

    def stop(self):
        self.board.stop_stream()

    def release(self):

        # data = board.get_current_board_data (256) # get latest 256 packages or less, doesnt remove them from internal buffer
        self.data = self.board.get_board_data()  # get all data and remove it from internal buffer
        self.board.release_session()

        # print(self.data)

    def get_data(self):
        if self.live: return self.board.get_board_data()
        else: return None

    def get_current_data(self, window_size, preset=BrainFlowPresets.DEFAULT_PRESET):
        sample_size = self.sampling_rate * window_size
        if self.live: return self.board.get_current_board_data(sample_size, preset)
        else: return None