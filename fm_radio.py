#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: FM Radio
# Author: Brian McLaughlin (bjmclaughlin@gmail.com)
# Generated: Sat Jan  2 13:10:37 2016
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

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import time
import wx


class fm_radio(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="FM Radio")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2.048e6
        self.baseband_decimation = baseband_decimation = 10
        self.rds_dec = rds_dec = 10
        self.frequency_list = frequency_list = range(87100000, 107900000, 200000)
        self.baseband_rate = baseband_rate = samp_rate // baseband_decimation
        self.slider_audio_gain = slider_audio_gain = 1
        self.rds_subcarrier = rds_subcarrier = 57e3
        self.rds_samp_rate = rds_samp_rate = baseband_rate / rds_dec
        self.rds_bitrate = rds_bitrate = 1.1875e3
        self.frequency_labels = frequency_labels = ['{:5.1f}'.format(i / 1e6) for i in frequency_list]
        self.fm_station = fm_station = 102700000

        ##################################################
        # Blocks
        ##################################################
        self.notebook_top = self.notebook_top = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.notebook_top.AddPage(grc_wxgui.Panel(self.notebook_top), "RF Receiver")
        self.notebook_top.AddPage(grc_wxgui.Panel(self.notebook_top), "Filtered")
        self.notebook_top.AddPage(grc_wxgui.Panel(self.notebook_top), "Baseband")
        self.notebook_top.AddPage(grc_wxgui.Panel(self.notebook_top), "Mono-Audio")
        self.notebook_top.AddPage(grc_wxgui.Panel(self.notebook_top), "Pilot")
        self.notebook_top.AddPage(grc_wxgui.Panel(self.notebook_top), "RDS")
        self.GridAdd(self.notebook_top, 1, 0, 2, 2)
        _slider_audio_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._slider_audio_gain_text_box = forms.text_box(
        	parent=self.notebook_top.GetPage(3).GetWin(),
        	sizer=_slider_audio_gain_sizer,
        	value=self.slider_audio_gain,
        	callback=self.set_slider_audio_gain,
        	label="Volume",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._slider_audio_gain_slider = forms.slider(
        	parent=self.notebook_top.GetPage(3).GetWin(),
        	sizer=_slider_audio_gain_sizer,
        	value=self.slider_audio_gain,
        	callback=self.set_slider_audio_gain,
        	minimum=0,
        	maximum=4,
        	num_steps=100,
        	style=wx.SL_VERTICAL,
        	cast=float,
        	proportion=1,
        )
        self.notebook_top.GetPage(3).GridAdd(_slider_audio_gain_sizer, 0, 1, 1, 1)
        self.notebook_rds = self.notebook_rds = wx.Notebook(self.notebook_top.GetPage(5).GetWin(), style=wx.NB_TOP)
        self.notebook_rds.AddPage(grc_wxgui.Panel(self.notebook_rds), "RDS Spectrum")
        self.notebook_top.GetPage(5).Add(self.notebook_rds)
        self._fm_station_chooser = forms.drop_down(
        	parent=self.GetWin(),
        	value=self.fm_station,
        	callback=self.set_fm_station,
        	label="FM Station",
        	choices=frequency_list,
        	labels=frequency_labels,
        )
        self.GridAdd(self._fm_station_chooser, 0, 0, 1, 1)
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_f(
        	self.notebook_top.GetPage(4).GetWin(),
        	title="19 KHz Pilot Carrier",
        	sample_rate=baseband_rate,
        	v_scale=0,
        	v_offset=0,
        	t_scale=0,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Counts",
        )
        self.notebook_top.GetPage(4).Add(self.wxgui_scopesink2_0.win)
        self.wxgui_fftsink2_0_0_1 = fftsink2.fft_sink_c(
        	self.notebook_rds.GetPage(0).GetWin(),
        	baseband_freq=rds_subcarrier,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=baseband_rate / 10,
        	fft_size=1024,
        	fft_rate=15,
        	average=True,
        	avg_alpha=0.1333,
        	title="RDS Spectrum",
        	peak_hold=True,
        )
        self.notebook_rds.GetPage(0).Add(self.wxgui_fftsink2_0_0_1.win)
        self.wxgui_fftsink2_0_0_0_0 = fftsink2.fft_sink_f(
        	self.notebook_top.GetPage(3).GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=48e3,
        	fft_size=1024,
        	fft_rate=15,
        	average=True,
        	avg_alpha=0.1333,
        	title="RF Spectrum",
        	peak_hold=True,
        	win=window.flattop,
        )
        self.notebook_top.GetPage(3).GridAdd(self.wxgui_fftsink2_0_0_0_0.win, 0, 0, 1, 1)
        self.wxgui_fftsink2_0_0_0 = fftsink2.fft_sink_f(
        	self.notebook_top.GetPage(2).GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=baseband_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=True,
        	avg_alpha=0.1333,
        	title="Baseband Spectrum",
        	peak_hold=True,
        	win=window.flattop,
        )
        self.notebook_top.GetPage(2).Add(self.wxgui_fftsink2_0_0_0.win)
        self.wxgui_fftsink2_0_0 = fftsink2.fft_sink_c(
        	self.notebook_top.GetPage(1).GetWin(),
        	baseband_freq=fm_station,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=baseband_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=True,
        	avg_alpha=0.1333,
        	title="RF Spectrum",
        	peak_hold=True,
        )
        self.notebook_top.GetPage(1).Add(self.wxgui_fftsink2_0_0.win)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.notebook_top.GetPage(0).GetWin(),
        	baseband_freq=fm_station,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=True,
        	avg_alpha=0.1333,
        	title="RF Spectrum",
        	peak_hold=True,
        )
        self.notebook_top.GetPage(0).Add(self.wxgui_fftsink2_0.win)
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(fm_station, 0)
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
                interpolation=int(48e3),
                decimation=int(baseband_rate),
                taps=None,
                fractional_bw=None,
        )
        self.low_pass_filter_1 = filter.fir_filter_fff(1, firdes.low_pass(
        	10, baseband_rate, 15e3, 3e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(baseband_decimation, firdes.low_pass(
        	1, samp_rate, 100e3, 1e3, firdes.WIN_HAMMING, 6.76))
        self.hilbert_fc_0 = filter.hilbert_fc(255, firdes.WIN_HAMMING, 6.76)
        self.freq_xlating_fft_filter_ccc_0 = filter.freq_xlating_fft_filter_ccc(rds_dec, (firdes.low_pass(10, baseband_rate, 2e3, 0.5e3)), rds_subcarrier, baseband_rate)
        self.freq_xlating_fft_filter_ccc_0.set_nthreads(1)
        self.freq_xlating_fft_filter_ccc_0.declare_sample_delay(0)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((slider_audio_gain, ))
        self.band_pass_filter_0 = filter.fir_filter_fff(1, firdes.band_pass(
        	1, baseband_rate, 18.5e3, 19.5e3, 1e3, firdes.WIN_HAMMING, 6.76))
        self.audio_sink_0 = audio.sink(48000, "", True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=baseband_rate,
        	audio_decimation=1,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.band_pass_filter_0, 0))    
        self.connect((self.analog_wfm_rcv_0, 0), (self.hilbert_fc_0, 0))    
        self.connect((self.analog_wfm_rcv_0, 0), (self.low_pass_filter_1, 0))    
        self.connect((self.analog_wfm_rcv_0, 0), (self.wxgui_fftsink2_0_0_0, 0))    
        self.connect((self.band_pass_filter_0, 0), (self.wxgui_scopesink2_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.audio_sink_0, 0))    
        self.connect((self.freq_xlating_fft_filter_ccc_0, 0), (self.wxgui_fftsink2_0_0_1, 0))    
        self.connect((self.hilbert_fc_0, 0), (self.freq_xlating_fft_filter_ccc_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.analog_wfm_rcv_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.wxgui_fftsink2_0_0, 0))    
        self.connect((self.low_pass_filter_1, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_multiply_const_vxx_1, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.wxgui_fftsink2_0_0_0_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.wxgui_fftsink2_0, 0))    


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_baseband_rate(self.samp_rate // self.baseband_decimation)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 100e3, 1e3, firdes.WIN_HAMMING, 6.76))
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)

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

    def get_frequency_list(self):
        return self.frequency_list

    def set_frequency_list(self, frequency_list):
        self.frequency_list = frequency_list
        self.set_frequency_labels(['{:5.1f}'.format(i / 1e6) for i in self.frequency_list])

    def get_baseband_rate(self):
        return self.baseband_rate

    def set_baseband_rate(self, baseband_rate):
        self.baseband_rate = baseband_rate
        self.set_rds_samp_rate(self.baseband_rate / self.rds_dec)
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.baseband_rate, 18.5e3, 19.5e3, 1e3, firdes.WIN_HAMMING, 6.76))
        self.freq_xlating_fft_filter_ccc_0.set_taps((firdes.low_pass(10, self.baseband_rate, 2e3, 0.5e3)))
        self.low_pass_filter_1.set_taps(firdes.low_pass(10, self.baseband_rate, 15e3, 3e3, firdes.WIN_HAMMING, 6.76))
        self.wxgui_fftsink2_0_0.set_sample_rate(self.baseband_rate)
        self.wxgui_fftsink2_0_0_0.set_sample_rate(self.baseband_rate)
        self.wxgui_fftsink2_0_0_1.set_sample_rate(self.baseband_rate / 10)
        self.wxgui_scopesink2_0.set_sample_rate(self.baseband_rate)

    def get_slider_audio_gain(self):
        return self.slider_audio_gain

    def set_slider_audio_gain(self, slider_audio_gain):
        self.slider_audio_gain = slider_audio_gain
        self._slider_audio_gain_slider.set_value(self.slider_audio_gain)
        self._slider_audio_gain_text_box.set_value(self.slider_audio_gain)
        self.blocks_multiply_const_vxx_1.set_k((self.slider_audio_gain, ))

    def get_rds_subcarrier(self):
        return self.rds_subcarrier

    def set_rds_subcarrier(self, rds_subcarrier):
        self.rds_subcarrier = rds_subcarrier
        self.freq_xlating_fft_filter_ccc_0.set_center_freq(self.rds_subcarrier)
        self.wxgui_fftsink2_0_0_1.set_baseband_freq(self.rds_subcarrier)

    def get_rds_samp_rate(self):
        return self.rds_samp_rate

    def set_rds_samp_rate(self, rds_samp_rate):
        self.rds_samp_rate = rds_samp_rate

    def get_rds_bitrate(self):
        return self.rds_bitrate

    def set_rds_bitrate(self, rds_bitrate):
        self.rds_bitrate = rds_bitrate

    def get_frequency_labels(self):
        return self.frequency_labels

    def set_frequency_labels(self, frequency_labels):
        self.frequency_labels = frequency_labels

    def get_fm_station(self):
        return self.fm_station

    def set_fm_station(self, fm_station):
        self.fm_station = fm_station
        self._fm_station_chooser.set_value(self.fm_station)
        self.rtlsdr_source_0.set_center_freq(self.fm_station, 0)
        self.wxgui_fftsink2_0.set_baseband_freq(self.fm_station)
        self.wxgui_fftsink2_0_0.set_baseband_freq(self.fm_station)


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = fm_radio()
    tb.Start(True)
    tb.Wait()
