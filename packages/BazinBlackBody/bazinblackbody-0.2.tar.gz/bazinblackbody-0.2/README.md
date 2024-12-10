# The BazinBlackBody package (BBB)

  

Time-Wavelength fit to find fast rising transients. BazinBlackBody or ExponentialBlackBody

The algorithm is motivated and defined [here](https://roywilliams.github.io/papers/Bazin_Exp_Blackbody.pdf)

The input is either a ZTF or LSST alert structure, and the output is the temperature `T` and rise rate `kr` or `k`, and perhaps the fall rate `kf`.
The `k` and `kr` are rise rate in mags per day, and `T` is black body temperature in kiloKelvin.
How to use the package:

- Copy the settings_bbb_template.py into your own settings.py.
    Most of this is intended for using the 'annotate' feature of BBB, which pulls filtered alerts from Lasair, runs BBB, then pushes them back to Lasair as annotations.

- Decide which survey you will use: LSST or ZTF.
    This decides the schema that BBB will use to get its inputs from the alert packet. What is wanted are in the first column, and the idiosyncratic survey name in other columns.

| name | ZTF | LSST |
|--------|-------------|---------|
| MJD | mjd | midpointMjdTai |
| Object |  | `diaObject` |
| Sources | `diaSourceList` | `candidates` |
| Forced | `forcedphot` | `diaForcedSourcesList` |
| Band index | `fid` | `band` |
| Flux | converted from `magpsf` | `psfFlux` |
| Flux error | converted from `sigmapsf` | `psfFluxError` |
| Forced Flux | `forcediffimflux` | `psfFlux` |
| Forced Flux error | `forcediffimfluxunc` | `psfFluxErr` |

Now the code can be called as follows:
```
import BBBEngine
BE = BBBEngine.BBB('ZTF', verbose=True)
(dicte, dictb) =  BE.make_fit(alert)
if dicte:
    BE.plot(alert, dicte, 'image/%s.png'%objectId)
if dictb:
    BE.plot(alert, dictb, 'image/%s.png'%objectId)
```
In addition to the survey names (mandatory), and the verbose flag, the class instantiation can have other parameters for the initial conditions of the fitting process:

`nforced=4, A=10000, T=8, t0=-6, kr=1, kf=0.1`

Where 
- `nforced` is the number of forced phot points utilised before discovery
- `A` is the overall scale (in nanoJanskies for LSST and microJanskies for ZTF)
- and `T` is the initial guess for the temparature in kiloKelvins
- and `kr` and `kf` are initial guesses for the rise rate per day and the fall rate per day.

The return from make_fit may contain two dictionaries, one for the Exponential-Blackbody fit to the lightcurve (linear in magnitude), and the other the result of the Bazin-Blackbody fit.
