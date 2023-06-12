from colour.plotting import plot_sds_in_chromaticity_diagram_CIE1931
from colour import SDS_ILLUMINANTS

A = SDS_ILLUMINANTS["A"]
D65 = SDS_ILLUMINANTS["D65"]
D75 = SDS_ILLUMINANTS["D75"]
D55 = SDS_ILLUMINANTS["D55"]
D50 = SDS_ILLUMINANTS["D50"]
a = plot_sds_in_chromaticity_diagram_CIE1931([A, D65, D50, D55, D75 ])
print(a)
print(a)
