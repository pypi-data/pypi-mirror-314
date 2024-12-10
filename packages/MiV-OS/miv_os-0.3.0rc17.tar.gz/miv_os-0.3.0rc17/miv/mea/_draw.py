import matplotlib.pyplot as plt
import numpy as np

from miv.mea import mea_map
from miv.mea.channel_mapping import MEA128

MEA128(map_key="128_longMEA_rhd").plot_network(
    list(range(128)), save_path="long_mea_intan_map.png"
)
