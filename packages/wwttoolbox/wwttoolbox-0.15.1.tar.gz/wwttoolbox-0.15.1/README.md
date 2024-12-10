# wwt-toolbox

# Sub-packages

## nc - work with NetCDF files

An module with NetCDF files. The module should be used in conjunction with:

- [netcdf4](https://unidata.github.io/netcdf4-python/)
- [NetCDF CF Conventions](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.11/cf-conventions.html)

**No support for coordinates which are function of multiple dimensions**

E.g.:

Dimensions:

- time
- depth

Variables:

- time (time)
- depth (time, depth)

## conversion - convert between different units

### unit conversion

### time conversion

## transformers - transform data to different formats

### WET

### SWAT

## yaml - edit yaml files

## QAQC

To use qaqc modules, the 'qaqc' optional dependency must be installed with `pip install wwtttoolbox[qaqc]`.

To use the qaqa validation module following must also be installed: `pip install wwtttoolbox[qaqc-validation]`.
