# STRANGLER-IPU reproducibility package

The warehouse memory model is the canonical, zero-dependency regression for the
STRANGLER-IPU research slice. It uses a fixed random seed (`42`) and reports
the baseline, v+1 coalescer, and isolated v+2 near-memory reduction.

```powershell
python sim\warehouse_mem_sim.py --json-output sim\results\latest.json
python -m unittest sim.test_warehouse_mem_sim sim.test_reproducibility
```

`sim/results/latest.json` is generated output, not a manually transcribed
claim. The v+1 speedup is measured on the modeled workload. The v+2
`99.976%` figure is **boundary traffic reduction for the isolated reduction
channel**; it is not a whole-pipeline attention result or a hardware
measurement.
