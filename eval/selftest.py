from .aggregate import tail
assert tail([1.0]) == 1.0
assert tail([]) == 0.0
assert abs(tail([0.0, 1.0]) - (0.55*0.5 + 0.30*0.0 + 0.15*0.0)) < 1e-9
print("aggregate selftest ok")
