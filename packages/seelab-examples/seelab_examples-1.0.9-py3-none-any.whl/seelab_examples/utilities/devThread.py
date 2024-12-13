import time
from PyQt5 import QtCore
from queue import Queue
from dataclasses import dataclass
from enum import Enum, auto


@dataclass
class Command:
    type: str
    args: dict

class SCOPESTATES(Enum):
    FREE = 1
    CAPTURING = 2
    COMPLETED = 3
    FETCHING = 4
    CAPTURING_FULLSPEED = 5

class DeviceThread(QtCore.QThread):
    data_ready = QtCore.pyqtSignal(object, object)
    voltage_ready = QtCore.pyqtSignal(str, float)
    resistance_ready = QtCore.pyqtSignal(float)
    capacitance_ready = QtCore.pyqtSignal(float)
    frequency_ready = QtCore.pyqtSignal(str, float, float)
    progress_ready = QtCore.pyqtSignal(bool, bool, float)
    trace_ready = QtCore.pyqtSignal(int)
    finished = QtCore.pyqtSignal()
    execute_function_signal = QtCore.pyqtSignal(str, object, dict)
    
    def __init__(self, device):
        super().__init__()
        self.device = device
        self.timeData = {}
        self.voltData = {}
        self.running = True
        self.fetchTime = 0
        self.paused = False
        self.enabled_channels = [True] * 4  # All channels enabled by default
        self.trigger_enabled = True
        self.command_queue = Queue()
        self.scope_conflict_command_queue = Queue()
        self.timebase_value = 2  # Initialize timebase_value with a default value
        self.NP = 1000
        self.state = SCOPESTATES.FREE

    def updateDevice(self, device):
        self.device = device
        self.state = SCOPESTATES.FREE

    def run(self):
        while self.running:
            if self.device is None:
                time.sleep(0.1)
                continue

            if not self.device.H.connected:
                time.sleep(0.1)
                continue
            try:
                if self.state != SCOPESTATES.CAPTURING:
                    self.process_noscope_commands()
                self.process_commands()
            except Exception as e:
                pass
            time.sleep(0.001)
            #print('alive',time.time())
        print('thread is finished!!!!!!!!!!!!!!!!!!!!!!', self.running)

    def add_command(self, cmd: Command):
        if cmd.type in ['get_voltage','get_resistance','get_capacitance','get_freq']:
            self.scope_conflict_command_queue.put(cmd)
        else:
            self.command_queue.put(cmd)

    def process_commands(self):
        """Process all pending commands in the queue"""
        while not self.command_queue.empty():
            try:
                cmd = self.command_queue.get_nowait()
                self.execute_command(cmd)
                self.command_queue.task_done()
            except Exception as e:
                print(f'Error processing command: {e}')
                break
    
    def process_noscope_commands(self):
        """Process all pending commands in the queue"""
        while not self.scope_conflict_command_queue.empty():
            try:
                cmd = self.scope_conflict_command_queue.get_nowait()
                self.execute_command(cmd)
                self.scope_conflict_command_queue.task_done()
            except Exception as e:
                print(f'Error processing command: {e}')
                break

    def isQueueEmpty(self):
        return self.command_queue.empty() and self.scope_conflict_command_queue.empty()
    
    def clearQueue(self):
        self.command_queue.queue.clear()
        self.scope_conflict_command_queue.queue.clear()

    def execute_command(self, cmd: Command):
        """Execute a single command"""
        resp = None
        if cmd.type == 'configure_trigger':
            resp=   self.device.configure_trigger(
                cmd.args['channel'],
                cmd.args['source'],
                cmd.args['level'],
                resolution = cmd.args.get('resolution', 10),
                prescaler = cmd.args.get('prescaler', 5)
            )
        elif cmd.type == 'capture_traces':
            self.state = SCOPESTATES.CAPTURING
            self.device.achans[0].resolution = 10
            resp= self.device.capture_traces(
                cmd.args['num_channels'],
                cmd.args['samples'],
                cmd.args['timebase'],
                cmd.args['channel_input'],
                trigger=cmd.args['trigger']
            )
        elif cmd.type == 'capture_hr':
            self.state = SCOPESTATES.CAPTURING
            resp= self.device.capture_highres_traces(
                cmd.args['channel_input'],
                cmd.args['samples'],
                cmd.args['timebase'],
                trigger=cmd.args['trigger']
            )
        elif cmd.type == 'capture_action':
            print('capture_action',cmd.args['channel_input'],
                cmd.args['samples'],
                cmd.args['timebase'],
                cmd.args['action'])
            resp= self.device.__capture_fullspeed_hr__(
                cmd.args['channel_input'],
                cmd.args['samples'],
                cmd.args['timebase'],
                cmd.args['action']
            )
            self.state = SCOPESTATES.CAPTURING_FULLSPEED
            self.fetchTime = time.time() + 1e-6 * cmd.args['samples'] * cmd.args['timebase'] + .01

        elif cmd.type == 'oscilloscope_progress':
            status, trigwait, resp = self.device.oscilloscope_progress()
            if status: #conversion complete
                self.state = SCOPESTATES.COMPLETED
            self.progress_ready.emit(status, trigwait,  resp)

        elif cmd.type == 'fetch_trace':
            ch = cmd.args['channel_num']
            print(f'######### Fetching trace {cmd.args["channel_num"]}')
            self.device.__fetch_channel__(ch)
            self.trace_ready.emit(cmd.args['channel_num'])

        elif cmd.type == 'fetch_partial_trace':
            ch = cmd.args['channel_num']
            self.device.__fetch_incremental_channel__(int(ch),int(cmd.args["progress"]))

            self.trace_ready.emit(cmd.args['channel_num'])

        elif cmd.type == 'enable_trigger':
            resp= self.trigger_enabled = cmd.args['enabled']
        elif cmd.type == 'set_sine':
            resp= self.device.set_sine(cmd.args['frequency'])
        elif cmd.type == 'set_sine_amp':
            resp= self.device.set_sine_amp(cmd.args['index'])
        elif cmd.type == 'set_sqr1':
            resp= self.device.set_sqr1(cmd.args['frequency'],cmd.args['duty_cycle'])
        elif cmd.type == 'set_sqr2':
            resp= self.device.set_sqr2(cmd.args['frequency'],cmd.args['duty_cycle'])
        elif cmd.type == 'set_pv1':
            resp= self.device.set_pv1(cmd.args['voltage'])
        elif cmd.type == 'set_pv2':
            resp= self.device.set_pv2(cmd.args['voltage'])
        elif cmd.type == 'set_multiplexer':
            resp= self.device.set_multiplexer(cmd.args['pos'])
        elif cmd.type == 'set_pv2':
            resp= self.device.set_pv2(cmd.args['voltage'])
        elif cmd.type == 'select_range':
            resp= self.device.select_range(cmd.args['channel'],cmd.args['value'])
        elif cmd.type == 'set_state':
            resp= self.device.set_state(**cmd.args)
        elif cmd.type == 'get_voltage':
            resp= self.device.get_voltage(cmd.args['channel'])
            self.voltage_ready.emit(cmd.args['channel'], resp)
        elif cmd.type == 'get_resistance':
            resp= self.device.get_resistance()
            self.resistance_ready.emit(resp)
        elif cmd.type == 'get_capacitance':
            resp= self.device.get_capacitance()
            self.capacitance_ready.emit(resp)
        elif cmd.type == 'get_freq':
            resp= self.device.get_freq(cmd.args['channel'])
            hi= self.device.r2ftime(cmd.args['channel'], cmd.args['channel'])
            self.frequency_ready.emit(cmd.args['channel'], resp, hi)
        # Add more command handlers as needed
        if 'callback' in cmd.args and cmd.args['callback'] is not None:
            cmd.args['callback'](resp)
    
    def pause(self):
        """Pause data acquisition"""
        self.paused = True
    
    def resume(self):
        """Resume data acquisition"""
        self.paused = False
    
    def stop(self):
        """Stop the thread"""
        self.running = False
        self.wait()
    
    def update_channels(self, enabled_list):
        """Update which channels are enabled"""
        self.enabled_channels = enabled_list
