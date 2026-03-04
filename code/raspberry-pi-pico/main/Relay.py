from machine import Pin

class Relay:
    """
    Relay control class with configurable active-LOW or active-HIGH logic.
    
    Active LOW (active_low=True, default):
    - Pin value 0 (LOW) = Relay ON (connected)
    - Pin value 1 (HIGH) = Relay OFF (disconnected)
    
    Active HIGH (active_low=False):
    - Pin value 1 (HIGH) = Relay ON (connected)
    - Pin value 0 (LOW) = Relay OFF (disconnected)
    """
    
    def __init__(self, pinNumber, name="RELAY", active_low=False):
        self.pinNumber = pinNumber
        self.name = name
        self.active_low = active_low
        self.pin = Pin(pinNumber, Pin.OUT)
        
        # Determine on/off pin values based on active_low setting
        self._on_value = 0 if active_low else 1
        self._off_value = 1 if active_low else 0
        
        # Initialize to OFF state
        self.pin.value(self._off_value)
        self._isOn = False
        
        mode = "Active LOW" if active_low else "Active HIGH"
        print(f"[{self.name}] Initialized on GP{pinNumber} ({mode}) - Initial state: OFF (pin={self._off_value})")
    
    def turnOn(self):
        """Turn relay ON"""
        self.pin.value(self._on_value)
        self._isOn = True
        actualValue = self.pin.value()
        print(f"[{self.name}] turnOn() called - pin set to {self._on_value}, actual pin value: {actualValue}")
    
    def turnOff(self):
        """Turn relay OFF"""
        self.pin.value(self._off_value)
        self._isOn = False
        actualValue = self.pin.value()
        print(f"[{self.name}] turnOff() called - pin set to {self._off_value}, actual pin value: {actualValue}")
    
    def isOn(self):
        """Return current relay state"""
        return self._isOn
    
    def getStatus(self):
        """Get relay status as string"""
        pinValue = self.pin.value()
        mode = "Active LOW" if self.active_low else "Active HIGH"
        return f"GP{self.pinNumber}: isOn={self._isOn}, pinValue={pinValue}, mode={mode}"