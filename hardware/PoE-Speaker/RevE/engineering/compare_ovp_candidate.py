import itertools,json
from pathlib import Path
rows=[]
for ppm in [10,25]:
 vals=[]
 for vt,at,ab,dt,db,leak in itertools.product([.4925,.5075],[-1,1],[-1,1],[-1,1],[-1,1],[-10e-9,10e-9]):
  top=198000*(1+at*.001)*(1+dt*ppm*1e-6*100)
  bottom=4020*(1+ab*.001)*(1+db*ppm*1e-6*100)
  vals.append(vt*(1+top/bottom)+leak*top)
 rows.append({'tcr_ppm_per_c':ppm,'min_trip_v':min(vals),'max_trip_v':max(vals),'margin_below_26v':26-max(vals),'margin_above_24_48v':min(vals)-24.48})
r={'candidate':'LTC4365','status':'Preferred candidate for next schematic prototype; not implemented or surge qualified','top_ohm':198000,'bottom_ohm':4020,'initial_tolerance':.001,'nominal_trip_v':.5*(1+198000/4020),'resistor_temperature_c':[-40,125],'results':rows,'source':'https://www.analog.com/media/en/technical-documentation/data-sheets/ltc4365.pdf','limits':['External MOSFET switching, inrush, SOA and inductive energy not modeled.','2 us datasheet fault delay is specified at 50 mV comparator overdrive and 12 V; it is not a universal 24 V cutoff guarantee.','No current limiter is provided by this candidate; fuse alone does not establish semiconductor SOA protection.']}
assert rows[0]['min_trip_v']>24.48 and rows[0]['max_trip_v']<26
Path('engineering/ltc4365-ovp-calculation.json').write_text(json.dumps(r,indent=2))
print(json.dumps(r,indent=2))

