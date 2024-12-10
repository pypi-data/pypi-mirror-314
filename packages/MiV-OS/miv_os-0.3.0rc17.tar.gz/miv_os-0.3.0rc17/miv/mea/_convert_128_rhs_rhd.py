from channel_mapping import MEA128

from miv.mea import mea_map

print(mea_map["128_dual_connector_two_64_rhd"])
print(mea_map["128_longMEA_rhd"])


print(repr(MEA128(map_key="128_longMEA_rhd").mea_intan))
print(repr(mea_map["128_longMEA_rhs"]))

print(repr(MEA128(map_key="128_dual_connector_two_64_rhd").mea_intan))
