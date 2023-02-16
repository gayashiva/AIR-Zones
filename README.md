# AIR-Zones
Quantifying suitability of regions to achieve winter water storage using artificial ice reservoirs (AIRs)

1. Extract water tower units (WTUs) from [Immerzeel et. al.](https://www.nature.com/articles/s41586-019-1822-y)
2. Download high resolution DEM from 
  - a. Downscale it to the WTUs
3. Download long-term monthly mean temperature dataset from 
  - a. Downscale it to WTUs
  - b. Perform altitude correction of the temperature dataset

## Notebooks
- [test_W5E5_quality.ipynb](docs/test_W5E5_quality.ipynb): 
    - extract temperature data for Leh Glacier (4572 m a.s.l.) from W5E5 and ERA5 (monthly varying lapse rates),
    - extract temperature data from Gangles AWS (4009 m a.s.l.)
    - Apply lapse correction for AWS temperature and compare
