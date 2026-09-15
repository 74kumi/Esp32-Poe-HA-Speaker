from pathlib import Path
f=Path('engineering/prune_c11_old_spur.py');s=f.read_text().replace('power-trial','ethernet-trial').replace("['AMP_GVDD','GND']","['ETH_RX_P','ETH_RX_N']").replace('c11-spur-removal.json','rx-termination-spur-removal.json').replace('C11 trial','RX termination trial').replace('AMP_GVDD/GND','RX signal');Path('engineering/prune_rx_termination_spurs.py').write_text(s)
