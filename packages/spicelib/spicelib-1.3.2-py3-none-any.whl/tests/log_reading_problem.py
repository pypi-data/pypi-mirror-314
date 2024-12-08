from spicelib.log.ltsteps import LTSpiceLogReader


log = LTSpiceLogReader("2_NJF_Bias_dB.log")
print(log.fourier)
print(log.stepset)
print(log.dataset)
print(log.step_count)
log.export_data("2_NJF_Bias_dB.tlog")