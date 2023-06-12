import colour
from colour.plotting import plot_single_colour_swatch, ColourSwatch

XYZ = [0.4676, 0.42332, 0.10908]
illuminant_XYZ = [0.34570, 0.35850]
illuminant_RGB = [0.31270, 0.32900]
chromatic_adaptation_transform = "Bradford"
matrix_XYZ_to_RGB = [
    [3.24062548, -1.53720797, -0.49862860],
    [-0.96893071, 1.87575606, 0.04151752],
    [0.05571012, -0.20402105, 1.05699594],
]
a = colour.XYZ_to_RGB(
    XYZ,
    illuminant_XYZ,
    illuminant_RGB,
    matrix_XYZ_to_RGB,
    chromatic_adaptation_transform,
)
b = colour.RGB_to_HSL(a)
print (b[0])


plot_single_colour_swatch(
    ColourSwatch(a, 'Sample'),
    text_parameters={'size': 'x-large'});