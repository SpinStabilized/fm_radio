#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: FM Radio
# Author: Brian McLaughlin (bjmclaughlin@gmail.com)
# Generated: Sun Mar  6 13:27:58 2016
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
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import digital
from gnuradio import digital;import cmath
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import cmath
import osmosdr
import rds
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
        self.valid_gains = valid_gains = [0.0, 0.9, 1.4, 2.7, 3.7, 7.7, 8.7, 12.5, 14.4, 15.7, 16.6, 19.7, 20.7, 22.9, 25.4, 28.0, 29.7, 32.8, 33.8, 36.4, 37.2, 38.6, 40.2, 42.1, 43.4, 43.9, 44.5, 48.0, 49.6]
        self.samp_rate = samp_rate = 2.048e6
        self.baseband_decimation = baseband_decimation = 10
        self.rf_gain = rf_gain = len(valid_gains)-1
        self.rds_dec = rds_dec = 10
        self.pilot_tone = pilot_tone = 19e3
        self.baseband_rate = baseband_rate = samp_rate // baseband_decimation
        self.stereo_subcarrier = stereo_subcarrier = pilot_tone * 2
        self.stereo_button = stereo_button = 0
        self.slider_volume = slider_volume = 0
        self.sdr_gain = sdr_gain = valid_gains[rf_gain]
        self.rds_symbols_per_bit = rds_symbols_per_bit = 2
        self.rds_subcarrier = rds_subcarrier = pilot_tone * 3
        self.rds_samp_rate = rds_samp_rate = baseband_rate / rds_dec
        self.rds_bitrate = rds_bitrate = 1.1875e3
        self.rds_bandwidth = rds_bandwidth = 2.83e3
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
        self.notebook_top.addTab(self.notebook_top_widget_3, "Sub-Carrier Generation")
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
        self.top_grid_layout.addWidget(self.notebook_top, 3, 0, 1, 8)
        self._slider_volume_range = Range(0, 11.1, 0.1, 0, 100)
        self._slider_volume_win = RangeWidget(self._slider_volume_range, self.set_slider_volume, 'Volume', "counter_slider", float)
        self.top_grid_layout.addWidget(self._slider_volume_win, 1, 1, 1, 1)
        self.notebook_subcarriers = Qt.QTabWidget()
        self.notebook_subcarriers_widget_0 = Qt.QWidget()
        self.notebook_subcarriers_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.notebook_subcarriers_widget_0)
        self.notebook_subcarriers_grid_layout_0 = Qt.QGridLayout()
        self.notebook_subcarriers_layout_0.addLayout(self.notebook_subcarriers_grid_layout_0)
        self.notebook_subcarriers.addTab(self.notebook_subcarriers_widget_0, "Pilot Signal")
        self.notebook_subcarriers_widget_1 = Qt.QWidget()
        self.notebook_subcarriers_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.notebook_subcarriers_widget_1)
        self.notebook_subcarriers_grid_layout_1 = Qt.QGridLayout()
        self.notebook_subcarriers_layout_1.addLayout(self.notebook_subcarriers_grid_layout_1)
        self.notebook_subcarriers.addTab(self.notebook_subcarriers_widget_1, "Spectrum")
        self.notebook_top_grid_layout_3.addWidget(self.notebook_subcarriers, 0, 0, 1, 1)
        self.notebook_rds = Qt.QTabWidget()
        self.notebook_rds_widget_0 = Qt.QWidget()
        self.notebook_rds_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.notebook_rds_widget_0)
        self.notebook_rds_grid_layout_0 = Qt.QGridLayout()
        self.notebook_rds_layout_0.addLayout(self.notebook_rds_grid_layout_0)
        self.notebook_rds.addTab(self.notebook_rds_widget_0, "RDS Signal")
        self.notebook_rds_widget_1 = Qt.QWidget()
        self.notebook_rds_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.notebook_rds_widget_1)
        self.notebook_rds_grid_layout_1 = Qt.QGridLayout()
        self.notebook_rds_layout_1.addLayout(self.notebook_rds_grid_layout_1)
        self.notebook_rds.addTab(self.notebook_rds_widget_1, "RDS Bitstream")
        self.notebook_top_grid_layout_5.addWidget(self.notebook_rds, 0, 0, 1, 1)
        self._fm_station_range = Range(fm_broadcast_low, fm_broadcast_high, fm_broadcast_seperation, 102.7, 200)
        self._fm_station_win = RangeWidget(self._fm_station_range, self.set_fm_station, "FM Station", "counter_slider", float)
        self.top_grid_layout.addWidget(self._fm_station_win, 0, 0, 1, 8)
        self._stereo_button_options = (0, 1, )
        self._stereo_button_labels = ("Mono", "Stereo", )
        self._stereo_button_tool_bar = Qt.QToolBar(self)
        self._stereo_button_tool_bar.addWidget(Qt.QLabel("Audio Output"+": "))
        self._stereo_button_combo_box = Qt.QComboBox()
        self._stereo_button_tool_bar.addWidget(self._stereo_button_combo_box)
        for label in self._stereo_button_labels: self._stereo_button_combo_box.addItem(label)
        self._stereo_button_callback = lambda i: Qt.QMetaObject.invokeMethod(self._stereo_button_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._stereo_button_options.index(i)))
        self._stereo_button_callback(self.stereo_button)
        self._stereo_button_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_stereo_button(self._stereo_button_options[i]))
        self.top_grid_layout.addWidget(self._stereo_button_tool_bar, 1, 2, 1, 1)
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(fm_station * 1e6, 0)
        self.rtlsdr_source_0.set_freq_corr(14, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(2, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(sdr_gain, 0)
        self.rtlsdr_source_0.set_if_gain(0, 0)
        self.rtlsdr_source_0.set_bb_gain(0, 0)
        self.rtlsdr_source_0.set_antenna("", 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
          
        self.root_raised_cosine_filter_0 = filter.fir_filter_ccf(1, firdes.root_raised_cosine(
        	2, rds_samp_rate, rds_bitrate * rds_symbols_per_bit, 0.275, 16))
        self._rf_gain_range = Range(0, len(valid_gains)-1, 1, len(valid_gains)-1, 200)
        self._rf_gain_win = RangeWidget(self._rf_gain_range, self.set_rf_gain, "RF Gain", "counter_slider", int)
        self.top_grid_layout.addWidget(self._rf_gain_win, 1, 0, 1, 1)
        self.rds_qt_panel_0 = self.rds_qt_panel_0 = rds.qt_panel()
        self.notebook_top_layout_5.addWidget(self.rds_qt_panel_0)
          
        self.rational_resampler_xxx_0_0_0_1 = filter.rational_resampler_fff(
                interpolation=int(audio_rate),
                decimation=int(baseband_rate),
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0_0_0_0 = filter.rational_resampler_fff(
                interpolation=int(audio_rate),
                decimation=int(baseband_rate),
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0_0_0 = filter.rational_resampler_fff(
                interpolation=int(audio_rate),
                decimation=int(baseband_rate),
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_time_sink_x_1 = qtgui.time_sink_f(
        	1024, #size
        	samp_rate, #samp_rate
        	"RBDS Bit Stream", #name
        	2 #number of inputs
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1.7, 1.7)
        
        self.qtgui_time_sink_x_1.set_y_label("Amplitude", "")
        
        self.qtgui_time_sink_x_1.enable_tags(-1, False)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1.enable_grid(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_1.disable_legend()
        
        labels = ["Raw Bit Stream", "Differential Decoded", "", "", "",
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
        
        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.pyqwidget(), Qt.QWidget)
        self.notebook_rds_layout_1.addWidget(self._qtgui_time_sink_x_1_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	1024, #size
        	baseband_rate, #samp_rate
        	"19 KHz Pilot Signal", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1.5, 1.5)
        
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
        self.notebook_subcarriers_grid_layout_0.addWidget(self._qtgui_time_sink_x_0_win, 0, 1, 1, 1)
        self.qtgui_freq_sink_x_1 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	rds_samp_rate, #bw
        	"RDS Subcarrier Signal (DSB-SSC)", #name
        	2 #number of inputs
        )
        self.qtgui_freq_sink_x_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_1.set_y_axis(-100, 0)
        self.qtgui_freq_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1.enable_grid(False)
        self.qtgui_freq_sink_x_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1.enable_control_panel(False)
        
        if not False:
          self.qtgui_freq_sink_x_1.disable_legend()
        
        if complex == type(float()):
          self.qtgui_freq_sink_x_1.set_plot_pos_half(not True)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1.pyqwidget(), Qt.QWidget)
        self.notebook_rds_grid_layout_0 .addWidget(self._qtgui_freq_sink_x_1_win,  0, 0, 1, 1)
        self.qtgui_freq_sink_x_0_1_0_1_0 = qtgui.freq_sink_f(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	audio_rate, #bw
        	"Stereo Audio Left", #name
        	2 #number of inputs
        )
        self.qtgui_freq_sink_x_0_1_0_1_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_1_0_1_0.set_y_axis(-100, -30)
        self.qtgui_freq_sink_x_0_1_0_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_1_0_1_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_1_0_1_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_1_0_1_0.set_fft_average(0.1)
        self.qtgui_freq_sink_x_0_1_0_1_0.enable_control_panel(False)
        
        if not False:
          self.qtgui_freq_sink_x_0_1_0_1_0.disable_legend()
        
        if float == type(float()):
          self.qtgui_freq_sink_x_0_1_0_1_0.set_plot_pos_half(not False)
        
        labels = ["Stereo Left", "Stereo Right", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_1_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_1_0_1_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_1_0_1_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_1_0_1_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_1_0_1_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_1_0_1_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_1_0_1_0.pyqwidget(), Qt.QWidget)
        self.notebook_top_grid_layout_4.addWidget(self._qtgui_freq_sink_x_0_1_0_1_0_win, 0, 0, 1, 1)
        self.qtgui_freq_sink_x_0_1_0_1 = qtgui.freq_sink_f(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	audio_rate, #bw
        	"Stereo Audio Right", #name
        	2 #number of inputs
        )
        self.qtgui_freq_sink_x_0_1_0_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_1_0_1.set_y_axis(-100, -30)
        self.qtgui_freq_sink_x_0_1_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_1_0_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_1_0_1.enable_grid(False)
        self.qtgui_freq_sink_x_0_1_0_1.set_fft_average(0.1)
        self.qtgui_freq_sink_x_0_1_0_1.enable_control_panel(False)
        
        if not False:
          self.qtgui_freq_sink_x_0_1_0_1.disable_legend()
        
        if float == type(float()):
          self.qtgui_freq_sink_x_0_1_0_1.set_plot_pos_half(not False)
        
        labels = ["Stereo Right", "Stereo Right", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_1_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_1_0_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_1_0_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_1_0_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_1_0_1.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_1_0_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_1_0_1.pyqwidget(), Qt.QWidget)
        self.notebook_top_grid_layout_4.addWidget(self._qtgui_freq_sink_x_0_1_0_1_win, 0, 1, 1, 1)
        self.qtgui_freq_sink_x_0_1_0_0 = qtgui.freq_sink_f(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	baseband_rate, #bw
        	"Pilot & Stereo Carrier", #name
        	2 #number of inputs
        )
        self.qtgui_freq_sink_x_0_1_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_1_0_0.set_y_axis(-80, 0)
        self.qtgui_freq_sink_x_0_1_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_1_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_1_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_1_0_0.set_fft_average(0.1)
        self.qtgui_freq_sink_x_0_1_0_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_freq_sink_x_0_1_0_0.disable_legend()
        
        if float == type(float()):
          self.qtgui_freq_sink_x_0_1_0_0.set_plot_pos_half(not False)
        
        labels = ["Pilot Tone", "Stereo Carrier", "RDS Carrier", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_1_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_1_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_1_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_1_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_1_0_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_1_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_1_0_0.pyqwidget(), Qt.QWidget)
        self.notebook_subcarriers_grid_layout_1.addWidget(self._qtgui_freq_sink_x_0_1_0_0_win, 0, 0, 1, 1)
        self.qtgui_freq_sink_x_0_0_0 = qtgui.freq_sink_f(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	audio_rate, #bw
        	"Mono Audio (L+R)", #name
        	2 #number of inputs
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
        for i in xrange(2):
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
        self.qtgui_freq_sink_x_0.set_y_axis(-90, 0)
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(0.1)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        
        if not False:
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
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
        	1024, #size
        	"RDS BPSK Constellation", #name
        	1 #number of inputs
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis(-1.6, 1.6)
        self.qtgui_const_sink_x_0.set_x_axis(-1.6, 1.6)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(True)
        
        if not False:
          self.qtgui_const_sink_x_0.disable_legend()
        
        labels = ["RBDS BPSK", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
                  "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.pyqwidget(), Qt.QWidget)
        self.notebook_rds_grid_layout_0.addWidget(self._qtgui_const_sink_x_0_win, 0, 1, 1, 1)
        self.low_pass_filter_4 = filter.fir_filter_fff(1, firdes.low_pass(
        	1, baseband_rate, 60e3, 1e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_2 = filter.fir_filter_fff(1, firdes.low_pass(
        	1, baseband_rate, 16e3, 1e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_1 = filter.fir_filter_fff(1, firdes.low_pass(
        	10, baseband_rate, 15e3, 3e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(baseband_decimation, firdes.low_pass(
        	1, samp_rate, 75e3, 1e3, firdes.WIN_HAMMING, 6.76))
        self.gr_rds_parser_0 = rds.parser(False, False, 1)
        self.gr_rds_decoder_0 = rds.decoder(False, False)
        self.freq_xlating_fir_filter_xxx_1 = filter.freq_xlating_fir_filter_fcc(rds_dec, (firdes.low_pass(2500,baseband_rate,rds_bandwidth,1e3,firdes.WIN_HAMMING)), rds_subcarrier, baseband_rate)
        self.digital_mpsk_receiver_cc_0 = digital.mpsk_receiver_cc(2, 0, (2 * cmath.pi) / 100, -0.00006, 0.00006, 0.5, 0.05, rds_samp_rate / (rds_bitrate * 2), ((rds_samp_rate / (rds_bitrate * 2)) ** 2)/ 4, 0.005)
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(2)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_uchar_to_float_0_0 = blocks.uchar_to_float()
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_multiply_xx_1 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_multiply_const_vxx_1_0_1_0_1 = blocks.multiply_const_vff((11, ))
        self.blocks_multiply_const_vxx_1_0_1_0_0 = blocks.multiply_const_vff((11, ))
        self.blocks_multiply_const_vxx_1_0_1_0 = blocks.multiply_const_vff((11, ))
        self.blocks_multiply_const_vxx_1_0_1 = blocks.multiply_const_vff((slider_volume, ))
        self.blocks_multiply_const_vxx_1_0_0 = blocks.multiply_const_vff((slider_volume, ))
        self.blocks_multiply_const_vxx_1_0 = blocks.multiply_const_vff((slider_volume, ))
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_char*1, 2)
        self.blocks_complex_to_real_1 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.blocks_add_const_vxx_0_0 = blocks.add_const_vff((0.5, ))
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((-1.5, ))
        self.blks2_selector_0_0 = grc_blks2.selector(
        	item_size=gr.sizeof_float*1,
        	num_inputs=2,
        	num_outputs=1,
        	input_index=0,
        	output_index=0,
        )
        self.blks2_selector_0 = grc_blks2.selector(
        	item_size=gr.sizeof_float*1,
        	num_inputs=2,
        	num_outputs=1,
        	input_index=0,
        	output_index=0,
        )
        self.band_pass_filter_1 = filter.fir_filter_fff(1, firdes.band_pass(
        	1, baseband_rate, stereo_subcarrier - 0.5e3, stereo_subcarrier + 0.5e3, 0.5e3, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_0 = filter.fir_filter_fff(1, firdes.band_pass(
        	1, baseband_rate, 23e3, 53e3, 1e3, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0 = filter.fir_filter_fcc(1, firdes.complex_band_pass(
        	1, baseband_rate, pilot_tone - 0.5e3, pilot_tone+0.5e3, 1e3, firdes.WIN_HAMMING, 6.76))
        self.audio_sink_0 = audio.sink(48000, "", True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=baseband_rate,
        	audio_decimation=1,
        )
        self.analog_pll_refout_cc_0 = analog.pll_refout_cc(1e-3, 2 * cmath.pi * (19000+200) / baseband_rate, 2 * cmath.pi * (19000-200) / baseband_rate)
        self.analog_fm_deemph_0_0_0_1 = analog.fm_deemph(fs=baseband_rate, tau=75e-6)
        self.analog_fm_deemph_0_0_0_0 = analog.fm_deemph(fs=baseband_rate, tau=75e-6)
        self.analog_fm_deemph_0_0_0 = analog.fm_deemph(fs=baseband_rate, tau=75e-6)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.gr_rds_decoder_0, 'out'), (self.gr_rds_parser_0, 'in'))    
        self.msg_connect((self.gr_rds_parser_0, 'out'), (self.rds_qt_panel_0, 'in'))    
        self.connect((self.analog_fm_deemph_0_0_0, 0), (self.rational_resampler_xxx_0_0_0, 0))    
        self.connect((self.analog_fm_deemph_0_0_0_0, 0), (self.rational_resampler_xxx_0_0_0_0, 0))    
        self.connect((self.analog_fm_deemph_0_0_0_1, 0), (self.rational_resampler_xxx_0_0_0_1, 0))    
        self.connect((self.analog_pll_refout_cc_0, 0), (self.blocks_complex_to_real_1, 0))    
        self.connect((self.analog_wfm_rcv_0, 0), (self.low_pass_filter_4, 0))    
        self.connect((self.band_pass_filter_0, 0), (self.analog_pll_refout_cc_0, 0))    
        self.connect((self.band_pass_filter_0_0, 0), (self.blocks_multiply_xx_1, 1))    
        self.connect((self.band_pass_filter_1, 0), (self.blocks_multiply_xx_1, 0))    
        self.connect((self.band_pass_filter_1, 0), (self.qtgui_freq_sink_x_0_1_0_0, 1))    
        self.connect((self.blks2_selector_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.blks2_selector_0_0, 0), (self.audio_sink_0, 1))    
        self.connect((self.blocks_add_const_vxx_0, 0), (self.qtgui_time_sink_x_1, 1))    
        self.connect((self.blocks_add_const_vxx_0_0, 0), (self.qtgui_time_sink_x_1, 0))    
        self.connect((self.blocks_add_xx_0, 0), (self.analog_fm_deemph_0_0_0_0, 0))    
        self.connect((self.blocks_complex_to_real_0, 0), (self.digital_binary_slicer_fb_0, 0))    
        self.connect((self.blocks_complex_to_real_1, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self.blocks_complex_to_real_1, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.blocks_complex_to_real_1, 0), (self.qtgui_freq_sink_x_0_1_0_0, 0))    
        self.connect((self.blocks_complex_to_real_1, 0), (self.qtgui_time_sink_x_0, 0))    
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.blocks_uchar_to_float_0, 0))    
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.digital_diff_decoder_bb_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1_0, 0), (self.blks2_selector_0, 1))    
        self.connect((self.blocks_multiply_const_vxx_1_0, 0), (self.qtgui_freq_sink_x_0_1_0_1, 1))    
        self.connect((self.blocks_multiply_const_vxx_1_0_0, 0), (self.blks2_selector_0_0, 1))    
        self.connect((self.blocks_multiply_const_vxx_1_0_0, 0), (self.qtgui_freq_sink_x_0_1_0_1_0, 1))    
        self.connect((self.blocks_multiply_const_vxx_1_0_1, 0), (self.blks2_selector_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1_0_1, 0), (self.blks2_selector_0_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1_0_1, 0), (self.qtgui_freq_sink_x_0_0_0, 1))    
        self.connect((self.blocks_multiply_const_vxx_1_0_1_0, 0), (self.qtgui_freq_sink_x_0_0_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1_0_1_0_0, 0), (self.qtgui_freq_sink_x_0_1_0_1, 0))    
        self.connect((self.blocks_multiply_const_vxx_1_0_1_0_1, 0), (self.qtgui_freq_sink_x_0_1_0_1_0, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.band_pass_filter_1, 0))    
        self.connect((self.blocks_multiply_xx_1, 0), (self.low_pass_filter_2, 0))    
        self.connect((self.blocks_sub_xx_0, 0), (self.analog_fm_deemph_0_0_0, 0))    
        self.connect((self.blocks_uchar_to_float_0, 0), (self.blocks_add_const_vxx_0_0, 0))    
        self.connect((self.blocks_uchar_to_float_0_0, 0), (self.blocks_add_const_vxx_0, 0))    
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_keep_one_in_n_0, 0))    
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.blocks_uchar_to_float_0_0, 0))    
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.gr_rds_decoder_0, 0))    
        self.connect((self.digital_mpsk_receiver_cc_0, 0), (self.blocks_complex_to_real_0, 0))    
        self.connect((self.digital_mpsk_receiver_cc_0, 0), (self.qtgui_const_sink_x_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_1, 0), (self.qtgui_freq_sink_x_1, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_1, 0), (self.root_raised_cosine_filter_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.analog_wfm_rcv_0, 0))    
        self.connect((self.low_pass_filter_1, 0), (self.analog_fm_deemph_0_0_0_1, 0))    
        self.connect((self.low_pass_filter_1, 0), (self.blocks_add_xx_0, 0))    
        self.connect((self.low_pass_filter_1, 0), (self.blocks_sub_xx_0, 0))    
        self.connect((self.low_pass_filter_2, 0), (self.blocks_add_xx_0, 1))    
        self.connect((self.low_pass_filter_2, 0), (self.blocks_sub_xx_0, 1))    
        self.connect((self.low_pass_filter_4, 0), (self.band_pass_filter_0, 0))    
        self.connect((self.low_pass_filter_4, 0), (self.band_pass_filter_0_0, 0))    
        self.connect((self.low_pass_filter_4, 0), (self.freq_xlating_fir_filter_xxx_1, 0))    
        self.connect((self.low_pass_filter_4, 0), (self.low_pass_filter_1, 0))    
        self.connect((self.low_pass_filter_4, 0), (self.qtgui_freq_sink_x_0_0, 0))    
        self.connect((self.rational_resampler_xxx_0_0_0, 0), (self.blocks_multiply_const_vxx_1_0, 0))    
        self.connect((self.rational_resampler_xxx_0_0_0, 0), (self.blocks_multiply_const_vxx_1_0_1_0_0, 0))    
        self.connect((self.rational_resampler_xxx_0_0_0_0, 0), (self.blocks_multiply_const_vxx_1_0_0, 0))    
        self.connect((self.rational_resampler_xxx_0_0_0_0, 0), (self.blocks_multiply_const_vxx_1_0_1_0_1, 0))    
        self.connect((self.rational_resampler_xxx_0_0_0_1, 0), (self.blocks_multiply_const_vxx_1_0_1, 0))    
        self.connect((self.rational_resampler_xxx_0_0_0_1, 0), (self.blocks_multiply_const_vxx_1_0_1_0, 0))    
        self.connect((self.root_raised_cosine_filter_0, 0), (self.digital_mpsk_receiver_cc_0, 0))    
        self.connect((self.root_raised_cosine_filter_0, 0), (self.qtgui_freq_sink_x_1, 1))    
        self.connect((self.rtlsdr_source_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.qtgui_freq_sink_x_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "fm_radio")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_valid_gains(self):
        return self.valid_gains

    def set_valid_gains(self, valid_gains):
        self.valid_gains = valid_gains
        self.set_rf_gain(len(self.valid_gains)-1)
        self.set_sdr_gain(self.valid_gains[self.rf_gain])

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_baseband_rate(self.samp_rate // self.baseband_decimation)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 75e3, 1e3, firdes.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0.set_frequency_range(self.fm_station * 1e6, self.samp_rate)
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate)
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_baseband_decimation(self):
        return self.baseband_decimation

    def set_baseband_decimation(self, baseband_decimation):
        self.baseband_decimation = baseband_decimation
        self.set_baseband_rate(self.samp_rate // self.baseband_decimation)

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.set_sdr_gain(self.valid_gains[self.rf_gain])

    def get_rds_dec(self):
        return self.rds_dec

    def set_rds_dec(self, rds_dec):
        self.rds_dec = rds_dec
        self.set_rds_samp_rate(self.baseband_rate / self.rds_dec)

    def get_pilot_tone(self):
        return self.pilot_tone

    def set_pilot_tone(self, pilot_tone):
        self.pilot_tone = pilot_tone
        self.set_rds_subcarrier(self.pilot_tone * 3)
        self.set_stereo_subcarrier(self.pilot_tone * 2)
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.baseband_rate, self.pilot_tone - 0.5e3, self.pilot_tone+0.5e3, 1e3, firdes.WIN_HAMMING, 6.76))

    def get_baseband_rate(self):
        return self.baseband_rate

    def set_baseband_rate(self, baseband_rate):
        self.baseband_rate = baseband_rate
        self.set_rds_samp_rate(self.baseband_rate / self.rds_dec)
        self.analog_pll_refout_cc_0.set_max_freq(2 * cmath.pi * (19000+200) / self.baseband_rate)
        self.analog_pll_refout_cc_0.set_min_freq(2 * cmath.pi * (19000-200) / self.baseband_rate)
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.baseband_rate, self.pilot_tone - 0.5e3, self.pilot_tone+0.5e3, 1e3, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(1, self.baseband_rate, 23e3, 53e3, 1e3, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_1.set_taps(firdes.band_pass(1, self.baseband_rate, self.stereo_subcarrier - 0.5e3, self.stereo_subcarrier + 0.5e3, 0.5e3, firdes.WIN_HAMMING, 6.76))
        self.freq_xlating_fir_filter_xxx_1.set_taps((firdes.low_pass(2500,self.baseband_rate,self.rds_bandwidth,1e3,firdes.WIN_HAMMING)))
        self.low_pass_filter_1.set_taps(firdes.low_pass(10, self.baseband_rate, 15e3, 3e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_2.set_taps(firdes.low_pass(1, self.baseband_rate, 16e3, 1e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_4.set_taps(firdes.low_pass(1, self.baseband_rate, 60e3, 1e3, firdes.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0_0.set_frequency_range(0, self.baseband_rate)
        self.qtgui_freq_sink_x_0_1_0_0.set_frequency_range(0, self.baseband_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.baseband_rate)

    def get_stereo_subcarrier(self):
        return self.stereo_subcarrier

    def set_stereo_subcarrier(self, stereo_subcarrier):
        self.stereo_subcarrier = stereo_subcarrier
        self.band_pass_filter_1.set_taps(firdes.band_pass(1, self.baseband_rate, self.stereo_subcarrier - 0.5e3, self.stereo_subcarrier + 0.5e3, 0.5e3, firdes.WIN_HAMMING, 6.76))

    def get_stereo_button(self):
        return self.stereo_button

    def set_stereo_button(self, stereo_button):
        self.stereo_button = stereo_button
        self._stereo_button_callback(self.stereo_button)

    def get_slider_volume(self):
        return self.slider_volume

    def set_slider_volume(self, slider_volume):
        self.slider_volume = slider_volume
        self.blocks_multiply_const_vxx_1_0.set_k((self.slider_volume, ))
        self.blocks_multiply_const_vxx_1_0_0.set_k((self.slider_volume, ))
        self.blocks_multiply_const_vxx_1_0_1.set_k((self.slider_volume, ))

    def get_sdr_gain(self):
        return self.sdr_gain

    def set_sdr_gain(self, sdr_gain):
        self.sdr_gain = sdr_gain
        self.rtlsdr_source_0.set_gain(self.sdr_gain, 0)

    def get_rds_symbols_per_bit(self):
        return self.rds_symbols_per_bit

    def set_rds_symbols_per_bit(self, rds_symbols_per_bit):
        self.rds_symbols_per_bit = rds_symbols_per_bit
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(2, self.rds_samp_rate, self.rds_bitrate * self.rds_symbols_per_bit, 0.275, 16))

    def get_rds_subcarrier(self):
        return self.rds_subcarrier

    def set_rds_subcarrier(self, rds_subcarrier):
        self.rds_subcarrier = rds_subcarrier
        self.freq_xlating_fir_filter_xxx_1.set_center_freq(self.rds_subcarrier)

    def get_rds_samp_rate(self):
        return self.rds_samp_rate

    def set_rds_samp_rate(self, rds_samp_rate):
        self.rds_samp_rate = rds_samp_rate
        self.digital_mpsk_receiver_cc_0.set_omega(self.rds_samp_rate / (self.rds_bitrate * 2))
        self.digital_mpsk_receiver_cc_0.set_gain_omega(((self.rds_samp_rate / (self.rds_bitrate * 2)) ** 2)/ 4)
        self.qtgui_freq_sink_x_1.set_frequency_range(0, self.rds_samp_rate)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(2, self.rds_samp_rate, self.rds_bitrate * self.rds_symbols_per_bit, 0.275, 16))

    def get_rds_bitrate(self):
        return self.rds_bitrate

    def set_rds_bitrate(self, rds_bitrate):
        self.rds_bitrate = rds_bitrate
        self.digital_mpsk_receiver_cc_0.set_omega(self.rds_samp_rate / (self.rds_bitrate * 2))
        self.digital_mpsk_receiver_cc_0.set_gain_omega(((self.rds_samp_rate / (self.rds_bitrate * 2)) ** 2)/ 4)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(2, self.rds_samp_rate, self.rds_bitrate * self.rds_symbols_per_bit, 0.275, 16))

    def get_rds_bandwidth(self):
        return self.rds_bandwidth

    def set_rds_bandwidth(self, rds_bandwidth):
        self.rds_bandwidth = rds_bandwidth
        self.freq_xlating_fir_filter_xxx_1.set_taps((firdes.low_pass(2500,self.baseband_rate,self.rds_bandwidth,1e3,firdes.WIN_HAMMING)))

    def get_fm_station(self):
        return self.fm_station

    def set_fm_station(self, fm_station):
        self.fm_station = fm_station
        self.qtgui_freq_sink_x_0.set_frequency_range(self.fm_station * 1e6, self.samp_rate)
        self.rds_qt_panel_0.set_frequency(float(self.fm_station))
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
        self.qtgui_freq_sink_x_0_1_0_1.set_frequency_range(0, self.audio_rate)
        self.qtgui_freq_sink_x_0_1_0_1_0.set_frequency_range(0, self.audio_rate)


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
