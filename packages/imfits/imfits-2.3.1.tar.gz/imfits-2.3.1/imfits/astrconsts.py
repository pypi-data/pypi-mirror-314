### Often Use Constants
import numpy as np
from astropy import constants, units

### constants

Ggrav  = constants.G.cgs.value        # Gravitational constant
Msun   = constants.M_sun.cgs.value    # Solar mass (g)
Lsun   = constants.L_sun.cgs.value    # Solar luminosity (erg s^-1)
Rsun   = constants.R_sun.cgs.value    # Solar radius (cm)
clight = constants.c.cgs.value        # light speed (cm s^-1)
kb     = constants.k_B.cgs.value      # Boltzman coefficient
sigsb  = constants.sigma_sb.cgs.value # Stefan-Boltzmann constant (erg s^-1 cm^-2 K^-4)
mH     = constants.m_p.cgs.value      # Proton mass (g)
hp     = constants.h.cgs.value # Planck constant [erg s]
NA     = constants.N_A.cgs.value  # mol^-1
Mearth = constants.M_earth.cgs.value  # Earth mass [g]
Mjup   = constants.M_jup.cgs.value  # Jupiter mass [g]

# distance
auTOcm = units.au.to('cm') # 1 au (cm)
pcTOcm = units.pc.to('cm') # 1 pc (cm)
auTOpc = units.au.to('pc') # au --> pc
pcTOau = units.pc.to('au') # pc --> au

# units
# J = 1e7 erg
