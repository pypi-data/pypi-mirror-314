import numpy as np

from miv.mea import mea_map, rhd_32, rhs_32

rhd = mea_map["64_intanRHD"]
rhs = np.zeros_like(rhd) - 1

for rhd_ch, rhs_ch in zip(rhd_32.ravel(), rhs_32.ravel()):
    if rhd_ch == -1 and rhs_ch == -1:
        continue
    print(f"RHD: {rhd_ch} -> RHS: {rhs_ch}")
    print(f"RHD: {rhd_ch+32} -> RHS: {rhs_ch+32}")

    rhs[rhd == rhd_ch] = rhs_ch
    rhs[rhd == rhd_ch + 32] = rhs_ch + 32

print("RHD:")
print(repr(rhd))
print("RHS:")
print(repr(rhs))

xs = []
ys = []
for c in range(64):
    y, x = np.where(rhd[::-1, :] == c)
    if len(x) == 0:
        xs.append(None)
        ys.append(None)
    else:
        xs.append(x[0] * 200)
        ys.append(y[0] * 200)
    print(f"- [{xs[-1]}, {ys[-1]}]")
# print(xs)
# print(ys)
