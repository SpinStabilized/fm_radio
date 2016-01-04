#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: FM Radio
# Author: Brian McLaughlin (bjmclaughlin@gmail.com)
# Generated: Mon Jan  4 17:31:33 2016
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import osmosdr
import sip
import sys
import time


class fm_radio(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "FM Radio")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("FM Radio")
        try:
             self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
             pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "fm_radio")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2.048e6
        self.baseband_decimation = baseband_decimation = 10
        self.rds_dec = rds_dec = 10
        self.baseband_rate = baseband_rate = samp_rate // baseband_decimation
        self.slider_volume = slider_volume = 0
        self.rds_subcarrier = rds_subcarrier = 57e3
        self.rds_samp_rate = rds_samp_rate = baseband_rate / rds_dec
        self.rds_bitrate = rds_bitrate = 1.1875e3
        self.fm_station = fm_station = 102.7
        self.fm_broadcast_seperation = fm_broadcast_seperation = 0.2
        self.fm_broadcast_low = fm_broadcast_low = 87.1
        self.fm_broadcast_high = fm_broadcast_high = 107.9
        self.audio_rate = audio_rate = 48e3

        ##################################################
        # Blocks
        ##################################################
        self.notebook_top = Qt.QTabWidget()
        self.notebook_top_widget_0 = Qt.QWidget()
        self.notebook_top_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.notebook_top_widget_0)
        self.notebook_top_grid_layout_0 = Qt.QGridLayout()
        self.notebook_top_layout_0.addLayout(self.notebook_top_grid_layout_0)
        self.notebook_top.addTab(self.notebook_top_widget_0, "RF Receive")
        self.notebook_top_widget_1 = Qt.QWidget()
        self.notebook_top_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.notebook_top_widget_1)
        self.notebook_top_grid_layout_1 = Qt.QGridLayout()
        self.notebook_top_layout_1.addLayout(self.notebook_top_grid_layout_1)
        self.notebook_top.addTab(self.notebook_top_widget_1, "Baseband")
        self.notebook_top_widget_2 = Qt.QWidget()
        self.notebook_top_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.notebook_top_widget_2)
        self.notebook_top_grid_layout_2 = Qt.QGridLayout()
        self.notebook_top_layout_2.addLayout(self.notebook_top_grid_layout_2)
        self.notebook_top.addTab(self.notebook_top_widget_2, "Mono Audio")
        self.notebook_top_widget_3 = Qt.QWidget()
        self.notebook_top_layout_3 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.notebook_top_widget_3)
        self.notebook_top_grid_layout_3 = Qt.QGridLayout()
        self.notebook_top_layout_3.addLayout(self.notebook_top_grid_layout_3)
        self.notebook_top.addTab(self.notebook_top_widget_3, "Pilot")
        self.notebook_top_widget_4 = Qt.QWidget()
        self.notebook_top_layout_4 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.notebook_top_widget_4)
        self.notebook_top_grid_layout_4 = Qt.QGridLayout()
        self.notebook_top_layout_4.addLayout(self.notebook_top_grid_layout_4)
        self.notebook_top.addTab(self.notebook_top_widget_4, "Stereo")
        self.notebook_top_widget_5 = Qt.QWidget()
        self.notebook_top_layout_5 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.notebook_top_widget_5)
        self.notebook_top_grid_layout_5 = Qt.QGridLayout()
        self.notebook_top_layout_5.addLayout(self.notebook_top_grid_layout_5)
        self.notebook_top.addTab(self.notebook_top_widget_5, "RDS")
        self.top_grid_layout.addWidget(self.notebook_top, 1, 0, 1, 1)
        self._slider_volume_range = Range(0, 5, 0.1, 0, 200)
        self._slider_volume_win = RangeWidget(self._slider_volume_range, self.set_slider_volume, "Volume", "dial", float)
        self.notebook_top_grid_layout_2.addWidget(self._slider_volume_win, 0, 0, 1, 1)
        self._fm_station_range = Range(fm_broadcast_low, fm_broadcast_high, fm_broadcast_seperation, 102.7, 200)
        self._fm_station_win = RangeWidget(self._fm_station_range, self.set_fm_station, "FM Station", "counter_slider", float)
        self.top_grid_layout.addWidget(self._fm_station_win, 0, 0, 1, 1)
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(fm_station * 1e6, 0)
        self.rtlsdr_source_0.set_freq_corr(9, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(2, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(2, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(49.6, 0)
        self.rtlsdr_source_0.set_if_gain(1, 0)
        self.rtlsdr_source_0.set_bb_gain(1, 0)
        self.rtlsdr_source_0.set_antenna("", 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
          
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=int(audio_rate),
                decimation=int(baseband_rate),
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	1024, #size
        	baseband_rate, #samp_rate
        	"19 KHz Pilot Signal", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-0.004, 0.004)
        
        self.qtgui_time_sink_x_0.set_y_label("Amplitude", "counts")
        
        self.qtgui_time_sink_x_0.enable_tags(-1, False)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        
        if not False:
          self.qtgui_time_sink_x_0.disable_legend()
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.notebook_top_grid_layout_3.addWidget(self._qtgui_time_sink_x_0_win, 0, 1, 1, 1)
        self.qtgui_freq_sink_x_0_1_0 = qtgui.freq_sink_f(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	baseband_rate, #bw
        	"RF Frequency", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0_1_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_1_0.set_y_axis(-100, -70)
        self.qtgui_freq_sink_x_0_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_1_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_1_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_1_0.set_fft_average(0.1)
        self.qtgui_freq_sink_x_0_1_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_freq_sink_x_0_1_0.disable_legend()
        
        if float == type(float()):
          self.qtgui_freq_sink_x_0_1_0.set_plot_pos_half(not False)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_1_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_1_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_1_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_1_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_1_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_1_0.pyqwidget(), Qt.QWidget)
        self.notebook_top_grid_layout_4.addWidget(self._qtgui_freq_sink_x_0_1_0_win, 0, 1, 1, 1)
        self.qtgui_freq_sink_x_0_1 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	rds_subcarrier, #fc
        	baseband_rate / 10, #bw
        	"RF Frequency", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_1.set_y_axis(-80, -40)
        self.qtgui_freq_sink_x_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_1.enable_grid(False)
        self.qtgui_freq_sink_x_0_1.set_fft_average(0.1)
        self.qtgui_freq_sink_x_0_1.enable_control_panel(False)
        
        if not True:
          self.qtgui_freq_sink_x_0_1.disable_legend()
        
        if complex == type(float()):
          self.qtgui_freq_sink_x_0_1.set_plot_pos_half(not True)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_1.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_1.pyqwidget(), Qt.QWidget)
        self.notebook_top_grid_layout_5.addWidget(self._qtgui_freq_sink_x_0_1_win, 0, 1, 1, 1)
        self.qtgui_freq_sink_x_0_0_0 = qtgui.freq_sink_f(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	audio_rate, #bw
        	"Mono Audio", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0_0.set_y_axis(-100, -30)
        self.qtgui_freq_sink_x_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0_0.set_fft_average(0.2)
        self.qtgui_freq_sink_x_0_0_0.enable_control_panel(False)
        
        if not False:
          self.qtgui_freq_sink_x_0_0_0.disable_legend()
        
        if float == type(float()):
          self.qtgui_freq_sink_x_0_0_0.set_plot_pos_half(not False)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0_0.pyqwidget(), Qt.QWidget)
        self.notebook_top_grid_layout_2.addWidget(self._qtgui_freq_sink_x_0_0_0_win, 1, 0, 1, 5)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_f(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	baseband_rate, #bw
        	"FM Baseband", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0.set_y_axis(-100, -30)
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0.set_fft_average(0.1)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)
        
        if not False:
          self.qtgui_freq_sink_x_0_0.disable_legend()
        
        if float == type(float()):
          self.qtgui_freq_sink_x_0_0.set_plot_pos_half(not False)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.notebook_top_grid_layout_1.addWidget(self._qtgui_freq_sink_x_0_0_win, 0, 1, 1, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	fm_station * 1e6, #fc
        	samp_rate, #bw
        	"RF Frequency", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-80, -40)
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(0.1)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()
        
        if complex == type(float()):
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.notebook_top_grid_layout_0.addWidget(self._qtgui_freq_sink_x_0_win, 0, 1, 1, 1)
        self.low_pass_filter_1 = filter.fir_filter_fff(1, firdes.low_pass(
        	10, baseband_rate, 15e3, 3e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(baseband_decimation, firdes.low_pass(
        	1, samp_rate, 60e3, 1e3, firdes.WIN_HAMMING, 6.76))
        self.hilbert_fc_0 = filter.hilbert_fc(255, firdes.WIN_HAMMING, 6.76)
        self.freq_xlating_fft_filter_ccc_0 = filter.freq_xlating_fft_filter_ccc(rds_dec, (firdes.low_pass(10, baseband_rate, 2e3, 0.5e3)), rds_subcarrier, baseband_rate)
        self.freq_xlating_fft_filter_ccc_0.set_nthreads(1)
        self.freq_xlating_fft_filter_ccc_0.declare_sample_delay(0)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((slider_volume, ))
        self.band_pass_filter_0_0 = filter.fir_filter_fff(1, firdes.band_pass(
        	1, baseband_rate, 23e3, 53e3, 1e3, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0 = filter.fir_filter_fff(1, firdes.band_pass(
        	1, baseband_rate, 18.5e3, 19.5e3, 1e3, firdes.WIN_HAMMING, 6.76))
        self.audio_sink_0 = audio.sink(48000, "", True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=baseband_rate,
        	audio_decimation=1,
        )
        self.analog_fm_deemph_0 = analog.fm_deemph(fs=audio_rate, tau=75e-6)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fm_deemph_0, 0), (self.blocks_multiply_const_vxx_1, 0))    
        self.connect((self.analog_fm_deemph_0, 0), (self.qtgui_freq_sink_x_0_0_0, 0))    
        self.connect((self.analog_wfm_rcv_0, 0), (self.band_pass_filter_0, 0))    
        self.connect((self.analog_wfm_rcv_0, 0), (self.band_pass_filter_0_0, 0))    
        self.connect((self.analog_wfm_rcv_0, 0), (self.hilbert_fc_0, 0))    
        self.connect((self.analog_wfm_rcv_0, 0), (self.low_pass_filter_1, 0))    
        self.connect((self.analog_wfm_rcv_0, 0), (self.qtgui_freq_sink_x_0_0, 0))    
        self.connect((self.band_pass_filter_0, 0), (self.qtgui_time_sink_x_0, 0))    
        self.connect((self.band_pass_filter_0_0, 0), (self.qtgui_freq_sink_x_0_1_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.audio_sink_0, 0))    
        self.connect((self.freq_xlating_fft_filter_ccc_0, 0), (self.qtgui_freq_sink_x_0_1, 0))    
        self.connect((self.hilbert_fc_0, 0), (self.freq_xlating_fft_filter_ccc_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.analog_wfm_rcv_0, 0))    
        self.connect((self.low_pass_filter_1, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.analog_fm_deemph_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.qtgui_freq_sink_x_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "fm_radio")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_baseband_rate(self.samp_rate // self.baseband_decimation)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 60e3, 1e3, firdes.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0.set_frequency_range(self.fm_station * 1e6, self.samp_rate)
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_baseband_decimation(self):
        return self.baseband_decimation

    def set_baseband_decimation(self, baseband_decimation):
        self.baseband_decimation = baseband_decimation
        self.set_baseband_rate(self.samp_rate // self.baseband_decimation)

    def get_rds_dec(self):
        return self.rds_dec

    def set_rds_dec(self, rds_dec):
        self.rds_dec = rds_dec
        self.set_rds_samp_rate(self.baseband_rate / self.rds_dec)

    def get_baseband_rate(self):
        return self.baseband_rate

    def set_baseband_rate(self, baseband_rate):
        self.baseband_rate = baseband_rate
        self.set_rds_samp_rate(self.baseband_rate / self.rds_dec)
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.baseband_rate, 18.5e3, 19.5e3, 1e3, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(1, self.baseband_rate, 23e3, 53e3, 1e3, firdes.WIN_HAMMING, 6.76))
        self.freq_xlating_fft_filter_ccc_0.set_taps((firdes.low_pass(10, self.baseband_rate, 2e3, 0.5e3)))
        self.low_pass_filter_1.set_taps(firdes.low_pass(10, self.baseband_rate, 15e3, 3e3, firdes.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0_0.set_frequency_range(0, self.baseband_rate)
        self.qtgui_freq_sink_x_0_1.set_frequency_range(self.rds_subcarrier, self.baseband_rate / 10)
        self.qtgui_freq_sink_x_0_1_0.set_frequency_range(0, self.baseband_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.baseband_rate)

    def get_slider_volume(self):
        return self.slider_volume

    def set_slider_volume(self, slider_volume):
        self.slider_volume = slider_volume
        self.blocks_multiply_const_vxx_1.set_k((self.slider_volume, ))

    def get_rds_subcarrier(self):
        return self.rds_subcarrier

    def set_rds_subcarrier(self, rds_subcarrier):
        self.rds_subcarrier = rds_subcarrier
        self.freq_xlating_fft_filter_ccc_0.set_center_freq(self.rds_subcarrier)
        self.qtgui_freq_sink_x_0_1.set_frequency_range(self.rds_subcarrier, self.baseband_rate / 10)

    def get_rds_samp_rate(self):
        return self.rds_samp_rate

    def set_rds_samp_rate(self, rds_samp_rate):
        self.rds_samp_rate = rds_samp_rate

    def get_rds_bitrate(self):
        return self.rds_bitrate

    def set_rds_bitrate(self, rds_bitrate):
        self.rds_bitrate = rds_bitrate

    def get_fm_station(self):
        return self.fm_station

    def set_fm_station(self, fm_station):
        self.fm_station = fm_station
        self.qtgui_freq_sink_x_0.set_frequency_range(self.fm_station * 1e6, self.samp_rate)
        self.rtlsdr_source_0.set_center_freq(self.fm_station * 1e6, 0)

    def get_fm_broadcast_seperation(self):
        return self.fm_broadcast_seperation

    def set_fm_broadcast_seperation(self, fm_broadcast_seperation):
        self.fm_broadcast_seperation = fm_broadcast_seperation

    def get_fm_broadcast_low(self):
        return self.fm_broadcast_low

    def set_fm_broadcast_low(self, fm_broadcast_low):
        self.fm_broadcast_low = fm_broadcast_low

    def get_fm_broadcast_high(self):
        return self.fm_broadcast_high

    def set_fm_broadcast_high(self, fm_broadcast_high):
        self.fm_broadcast_high = fm_broadcast_high

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate
        self.qtgui_freq_sink_x_0_0_0.set_frequency_range(0, self.audio_rate)


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)
    tb = fm_radio()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None  # to clean up Qt widgets
