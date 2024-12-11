from pathlib import Path
import pandas as pd
import numpy as np
import lime
# fadress = '/home/vital/Downloads/Final_Wavelength_Table_with_Angstrom_Units.csv'
#
# df = lime.load_frame(fadress)
# df.rename(columns={"First Column": "label", "Second Column": "wavelength"}, inplace=True)
# df['wave_vac'] = df['wavelength']
# df['w1'] = df['wavelength'] - 0.03 *10000
# df['w2'] = df['wavelength'] - 0.02 *10000
# df['w3'] = df['wavelength'] - 0.01 *10000
# df['w4'] = df['wavelength'] + 0.01 *10000
# df['w5'] = df['wavelength'] + 0.02 *10000
# df['w6'] = df['wavelength'] + 0.03 *10000
# for label in df.index:
#     line = lime.Line(label)
#     print(line)
#     df.loc[label, 'latex_label'] = line.latex_label[0]
#     df.loc[label, 'units_wave'] = line.units_wave[0]
#     df.loc[label, 'particle'] = line.particle[0]
#     df.loc[label, 'transition'] = line.transition_comp[0]
#     df.loc[label, 'rel_int'] = 0
#
#
# # latex_label units_wave particle transition  rel_int
# # # df[:, ['w1', 'w2']] = [df['wavelength'] - 0.1 *10000,  df['wavelength'] + 0.1 *10000]
# lime.save_frame('miri_lines.txt', df)
# print(df)

bands_df = lime.line_bands()
# bands_df.drop(columns=['latex_label'], inplace=True)
# bands_df['latex_label'] = None
for i, label in enumerate(bands_df.index):
    line = lime.Line(label, band=bands_df)
    print(i, label, bands_df.loc[label, 'latex_label'], line.latex_label[0])

# lime.save_frame('test_df.txt', bands_df)