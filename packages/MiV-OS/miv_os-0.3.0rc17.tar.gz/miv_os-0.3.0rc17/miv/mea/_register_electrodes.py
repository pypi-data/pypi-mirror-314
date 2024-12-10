from miv_os_contrib.mea.utils import create_yaml
from channel_mapping import MEA128

from miv.mea import mea_map

create_yaml(
    "electrodes/128_rhs",
    MEA128(map_key="128_dual_connector_two_64_rhd").mea_intan,
    pitch=[200, 200],
    size=30,
    description="128 MEA with RHS chips",
)
# create_yaml(
#     "electrodes/128_dual_connector_two_64_rhd",
#     mea_map["128_dual_connector_two_64_rhd"],
#     pitch=[200, 200],
#     size=30,
#     description="128 MEA with two dual connector. Intan RHD chip",
# )
# create_yaml(
#     "electrodes/64_intanRHS",
#     mea_map["64_intanRHS"],
#     pitch=[200, 200],
#     size=30,
#     description="64 MEA commercial from MCS, standard. Intan RHS chip",
# )
# create_yaml(
#     "electrodes/64_intanRHD",
#     mea_map["64_intanRHD"],
#     pitch=[200, 200],
#     size=30,
#     description="64 MEA commercial from MCS, standard. Intan RHD chip",
# )
#
# create_yaml(
#     "electrodes/128_longMEA_rhd",
#     mea_map["128_longMEA_rhd"],
#     pitch=[60, 60],
#     size=15,
#     description="128 Long-MEA. Intan RHD chip",
# )
# create_yaml(
#     "electrodes/128_longMEA_rhs",
#     mea_map["128_longMEA_rhs"],
#     pitch=[60, 60],
#     size=15,
#     description="128 Long-MEA. Intan RHS chip",
# )
#
# create_yaml(
#     "electrodes/512_rhd",
#     mea_map["512_rhd"],
#     pitch=[150, 150],
#     size=30,
#     description="512 standard MEA. Four Intan RHD 128 chip",
# )
