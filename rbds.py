import sys
import zmq
import pmt
import traceback

import argparse
from string import maketrans
import rbds_const


ansi_esc_char = '\x1b['
def ansi_erase_display(n = 0):
	return ansi_esc_char + str(n) + 'J'

def ansi_move_to(n = 1, m = 1):
	return ansi_esc_char + str(n) + ';' + str(m) + 'H'

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

	@property
	def program_info(self):
		return self._program_info
	@program_info.setter
	def program_info(self, value):
		self._program_info = value.upper()

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

	def callsign(self):
		pi = self.program_info
		if pi[0:2] == 'AF':
			picode = pi[2:] + '00'

		if pi[0] == 'A':
			picode = pi[1] + '0' + pi[2:]

		picode = int(pi, 16)
		cs = ['','','','']
		if picode > 4095 and picode < 39247:
			if picode > 21671:
				cs[0] = 'W'
				picode = picode - 21672
			else:
				cs[0] = 'K'
				picode = picode - 4096

			cs[1] = picode // 676
			picode = picode - (676 * cs[1])
			cs[2] = picode // 26
			cs[3] = picode - (26 * cs[2])
			cs[1] = chr(cs[1] + ord('A'))
			cs[2] = chr(cs[2] + ord('A'))
			cs[3] = chr(cs[3] + ord('A'))
			cs = ''.join(cs)
		elif picode in rbds_const.three_letter.keys():
				cs = rbds_const.three_letter[picode]
		else:
			cs = 'ERR'

		return cs

	def __repr__(self):
		rtn_str = '[' + ('-' * 85) + ']'
		pi_pt_str = 'Program Info: {:>4} - Program Type: {}'.format(self.callsign(), self.program_type)
		rtn_str += '\n[ {:<84}]\n'.format(pi_pt_str)
		flag_str = [' ', ' ', 'S', 'S', ' ', ' ', ' ']
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

		rt = self.radio_text.strip()
		rtn_str += '[ Traffic Program: ({}) ][ Traffic Alert: ({}) ][ Music/Speech: ({}) ][ Mono/Stereo: ({}) ]\n'.format(flag_str[0], flag_str[1], flag_str[2], flag_str[3])
		rtn_str += '[ Artificial Head: ({}) ][ Compressed:    ({}) ][ Dynamic PTY:  ({}) ][                  ]\n'.format(flag_str[4], flag_str[5], flag_str[6])
		rtn_str += '[ {:<84}]\n[ {:<84}]\n'.format(self.station_name, rt)
		rtn_str += '[' + ('-' * 85) + ']'
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
                print ansi_erase_display(2) + repr(data) + ansi_move_to(1,1)
            else:
			    print 'Encountered Data I Did Not Understand'

    except KeyboardInterrupt:
        print ansi_erase_display(2) + ansi_move_to(1,1) + "Shutdown requested...exiting"
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)
