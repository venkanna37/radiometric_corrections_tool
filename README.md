# radiometric_corrections_tool

Radiometric correction tool, it can be used to correct the all radiometric corrections ( simply
editing the pixel values of raster image). as a module project in masters, I just completed only
some corrections ( those corrections need to be customize). It is a GUI based tool, It can be used as CLI.
below I mentioned the list of corrections I targeted.

### 1. Atmospheric corrections
- [x] Skyradiance/Haze/Dark Object Subtraction
- [x] Sun Angle Correction
### 2. Imperfection of sensor
- [ ] Line Drop
- [ ] Pixel Drop
- [ ] Line Strip
### 3. Image Enhancement
- [x] Average filter
- [x] Weighted Average filter
- [ ] X-Gradient filter
- [ ] Y-Gradient filter
- [ ] All-Gradient filter
- [ ] Edge enhancing filter

### Limitations
- In dark object subtraction, the minimum pixel value is subtracting from every pixel. It can extent,
that we can give minimum pixel value of each band and it can subtract respective value from each band.
- In Weighted average method, the constants weights multiplying in kernel, there we can choose weights.



### Installation && Running

#### Clone repository with git
`git clone https://github.com/venkanna37/radiometric_corrections_tool.git`
`cd radiometric_corrections_tool`

#### Install dependencies
`python3 -m pip install -r requirements.txt`

#### Running GUI
`python3 window.py`



