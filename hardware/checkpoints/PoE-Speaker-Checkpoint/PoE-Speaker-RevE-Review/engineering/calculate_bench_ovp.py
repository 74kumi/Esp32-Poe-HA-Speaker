"""OVP tolerance/temperature corners and illustrative ramp sensitivity.
Not a circuit simulation or surge qualification. Run from the project root.
"""
import itertools,json
from pathlib import Path
rt,rb,tol=200000,10000,0.001

def corners(tcr_ppm=0,temperature_span_c=100):
    result=[]
    drift=tcr_ppm*1e-6*temperature_span_c
    for vt,st,sb,dt,db,ileak in itertools.product([1.176,1.224],[-1,1],[-1,1],[-1,1],[-1,1],[-150e-9,150e-9]):
        a=rt*(1+st*tol)*(1+dt*drift)
        b=rb*(1+sb*tol)*(1+db*drift)
        result.append(vt*(1+a/b)+ileak*a)
    return min(result),max(result)

base=corners()
rows=[]
for ppm in [10,25,50,100]:
    lo,hi=corners(ppm)
    rows.append({'tcr_each_ppm_per_c':ppm,'min_trip_v':lo,'max_trip_v':hi,
                 'margin_above_supply_max_v':lo-24.48,'margin_below_26v':26-hi,
                 'passes_static_window':lo>24.48 and hi<26})
# Deliberately simple upper-rail ramp exposure, not a transfer model.
# 14 us applies only under the specified datasheet overdrive test conditions.
hi25=next(x['max_trip_v'] for x in rows if x['tcr_each_ppm_per_c']==25)
ramps=[{'assumed_rail_ramp_v_per_ms':slew,'additional_voltage_in_14us_v':slew*.014,
        'illustrative_rail_after_14us_v':hi25+slew*.014} for slew in [1,5,10,20,100]]
r={'status':'Proposal not implemented; temperature and transient margin review',
   'candidate':'TPS26630 adjustable OVP','divider_top_ohm':rt,'divider_bottom_ohm':rb,
   'resistor_initial_tolerance':tol,'nominal_cutoff_v':25.2,
   'initial_only_corner_v':list(base),'resistor_temperature_assumption_c':[-40,125],
   'reference_temperature_c':25,'max_temperature_distance_c':100,
   'temperature_corners':rows,'illustrative_ramp_exposure':ramps,
   'assumed_supply_v':[23.52,24.48],
   'decision':'Do not implement yet: static margin is small and dynamic protection is unproven.',
   'limits':['Opposite worst-case resistor TCRs assumed; comparator and leakage bounds already include their datasheet temperature range.',
             'Resistor aging, voltage coefficient, self heating and supplier-specific tolerance definitions still need review.',
             'Ramp table assumes the protected rail tracks the input during a 14 us delay; it is neither a guaranteed bound nor a circuit simulation.',
             'Datasheet delay test overdrive, FET turnoff, cable energy, output capacitance and backfeed require actual circuit analysis.']}
assert base[0]>24.48 and base[1]<26
assert rows[-1]['passes_static_window'] is False
out=Path(__file__).resolve().parent/'bench-ovp-calculation.json'
out.write_text(json.dumps(r,indent=2))
for x in rows:print(x)
print('Saved',out)
