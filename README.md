# radiometric_corrections_tool

Radiometric correction tool is a tool for atmosperic corrections and image enhancement that simply modifies the pixel values of an image.

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


### Installation && Running

#### Clone repository with git
```
git clone https://github.com/venkanna37/radiometric_corrections_tool.git
cd radiometric_corrections_tool
```

#### Install dependencies
`python3 -m pip install -r requirements.txt`

#### Running GUI
`python3 window.py`



