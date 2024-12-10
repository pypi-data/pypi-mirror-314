# badger2040-pystub
Python stub file for the badger2040 module. Contains some documentation and ports from the CPP/C headers

Documentation from [here](https://github.com/pimoroni/pimoroni-pico/tree/main/micropython/modules/badger2040)

To install:  
`pip install badger2040-pystub`  
or  
`pip install git+https://github.com/V3ntus/badger2040-pystub`  

To use:
```py
from badger2040 import Badger2040

badger = Badger2040()

# your own code here
```  
Then ideally, this would be copied onto your badger2040 as `main.py` (or `boot.py`) with micropython installed. The real `badger2040` module will be resolved on the device.  

**Note**: this is only a stub file, it has no functionality. It is only used for documentation and proper typehinting
