import pathlib
import sys

import numpy as np
from miv_os_contrib.mea.andrew import wells as andrew_wells
from miv_os_contrib.mea.kimia import wells as kimia_wells

from miv.mea import mea_map

parent = pathlib.Path("/Users/skim0119/Results/mea_map")

tasks = [
    # (mea_map["128_longMEA_rhd"], "longMEA_128.json", 128),
    # (mea_map["128_dual_connector_two_64_rhd"], "regular_128.json", 128),
    # (mea_map["128_dual_connector_two_64_rhd"].T, "regular_128_T.json", 128),
    (
        np.concatenate([kimia_wells[i].grid for i in range(4)], axis=0),
        "longMEA_512_4well.json",
        512,
    ),
    (kimia_wells[0].grid, "longMEA_512_chipside.json", 512),
    (kimia_wells[1].grid, "longMEA_512_leftAB.json", 512),
    (kimia_wells[2].grid, "longMEA_512_latchside.json", 512),
    (kimia_wells[3].grid, "longMEA_512_rightCD.json", 512),
    (
        np.concatenate([andrew_wells[i].grid for i in range(4)], axis=0),
        "regular_512_4well.json",
        512,
    ),
    (andrew_wells[0].grid, "regular_512_chipside.json", 512),
    (andrew_wells[1].grid, "regular_512_leftAB.json", 512),
    (andrew_wells[2].grid, "regular_512_latchside.json", 512),
    (andrew_wells[3].grid, "regular_512_rightCD.json", 512),
    (
        np.concatenate([andrew_wells[i].grid.T for i in range(4)], axis=0),
        "regular_512_4well_T.json",
        512,
    ),
    (andrew_wells[0].grid.T, "regular_512_chipside_T.json", 512),
    (andrew_wells[1].grid.T, "regular_512_leftAB_T.json", 512),
    (andrew_wells[2].grid.T, "regular_512_latchside_T.json", 512),
    (andrew_wells[3].grid.T, "regular_512_rightCD_T.json", 512),
]

for mea, filen, num_electrodes in tasks:
    print(mea)
    print(mea.shape, num_electrodes)
    print(filen)

    mea_list = mea.ravel().tolist()
    enabled_str = "true, " * (len(mea_list) - 1) + "true"

    if len(mea_list) < num_electrodes:
        remaining_mea = set(range(num_electrodes)) - set(mea_list)
        mea_list = mea_list + list(remaining_mea)
        enabled_str = (
            enabled_str + ", " + "false, " * (len(remaining_mea) - 1) + "false"
        )

    if num_electrodes == 512:
        # Map to v2 device
        filen = filen.replace("512", "512v2")
        map_path = "mea_map_512_to_512v2.csv"
        # Read CSV. make a map: column 1 to colume 2
        mea_map_512_to_512v2 = np.genfromtxt(map_path, delimiter=",", dtype=int)
        v2_map = {f[0]: f[1] for f in mea_map_512_to_512v2}
        mea_list = [v2_map[f + 1] for f in mea_list]

    filename = parent / filen

    with open(filename, "w") as f:
        f.write("{\n")
        f.write('    "0": {\n')
        f.write(f'        "mapping": {mea_list},\n')
        f.write(f'        "enabled": [{enabled_str}]\n')
        f.write("    }\n")
        f.write("}\n")
