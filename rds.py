import sys
import zmq
import pmt
import traceback

import argparse

class RBDSData(object):
	
	def __init__(self):
		self.program_info = ''
		self.station_name = ''
		self.program_type = ''
		self.traffic_program = False
		self.traffic_alert = False
		self.music = False
		self.mono = 0
		self.artificial_head = False
		self.compressed = False
		self.dynamic_pty = False
		self.radio_text = ''
		self.clock_time = 0
		self.alt_freq = 0
		self.frequency = 0
	
	def set_flags(self, flags):
		self.traffic_program = bool(int(flags[0]))
		self.traffic_alert = bool(int(flags[1]))
		self.music = bool(int(flags[2]))
		self.mono = bool(int(flags[3]))
		self.artificial_head = bool(int(flags[4]))
		self.compressed = bool(int(flags[5]))
		self.dynamic_pty = bool(int(flags[6]))
	
	def update(self, msg_type, msg):
		if msg_type == 0:
			self.program_info = msg
		elif msg_type == 1:
			self.station_name = unicode(msg, errors='replace')
		elif msg_type == 2:
			self.program_type = msg
		elif msg_type == 3:
			self.set_flags(msg)
		elif msg_type == 4:
			self.radio_text = unicode(msg, errors='ignore')
		elif msg_type == 5:
			self.clock_time = msg
		elif msg_type == 6:
			self.alg_freq = msg
		elif mg_type == 7:
			self.frequency = msg
	
	def __repr__(self):
		rtn_str = ''
		rtn_str += 'Program Info: {:>4} - Program Type: {}\n'.format(self.program_info, self.program_type)
		flag_str = ['_', '_', 'S', 'S', '_', '_', '_']
		if self.traffic_program:
			flag_str[0] = '*'
		if self.traffic_alert:
			flag_str[1] = '*'
		if self.music:
			flag_str[2] = 'M'
		if self.mono:
			flag_str[3] = 'M'
		if self.artificial_head:
			flag_str[4] = '*'
		if self.compressed:
			flag_Str[5] = '*'
		if self.dynamic_pty:
			flag_str[6] = '*'
		
		rtn_str += 'Traffic Program: ({}) Traffic Alert: ({}) Music/Speech: ({}) Mono/Stereo: ({})\n'.format(flag_str[0], flag_str[1], flag_str[2], flag_str[3])
		rtn_str += '{}\n{}\n'.format(self.station_name, self.radio_text)
		return rtn_str
			
		 

# Flags
# 0 - TP Flag (Station Has Traffic Information)
# 1 - TA Flag (Station broadcasting a traffic announcement)
# 2 - Music/Speech Flag
# 3 - Mono/Stereo Flag
# 4 - Artificial Head Flag (???)
# 5 - Compressed/Uncompressed Flag
# 6 - Static/Dynamic PTY Flag

packet_types = ['Program Info',
                'Station Name',
                'Program Type',
                'Flags',
                'Radio Text',
                'Clock Time',
                'Alt Freq',
                'Frequency']

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', '-s', default='127.0.0.1', help='remote server')
    parser.add_argument('--port', '-p', default=6000, type=int, help='remote port')
    args = parser.parse_args()
    
    # Socket to talk to server
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    print 'Collecting updates from radio server at {} port {}...'.format(args.server, args.port)
    socket.connect('tcp://{}:{}'.format(args.server, args.port))

    socket.setsockopt(zmq.SUBSCRIBE, '')
    data = RBDSData()
    try:
        while True:
            gnr_message_pmt = pmt.deserialize_str(socket.recv())
            if pmt.is_tuple(gnr_message_pmt):
                msg_type = pmt.to_long(pmt.tuple_ref(gnr_message_pmt, 0))
                msg = pmt.symbol_to_string(pmt.tuple_ref(gnr_message_pmt, 1))
                data.update(msg_type, msg)
                print repr(data)
            else:
			    print 'Encountered Data I Did Not Understand'
			    
    except KeyboardInterrupt:
        print "Shutdown requested...exiting"
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)
