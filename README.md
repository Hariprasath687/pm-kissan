# FingerPrint

This is the driver (or interface) for the fingerprint sensor on my laptop (LG Gram 2018). This script should work on other laptops and even desktops with fingerprint sensors as well.

## Principles

Call Windows Biometric Framework API to interact with the sensor. Technically, you can use the API to 
access any WBF devices, including facial recognition and iris recognition.

## How to use

You can integrate this interface with other command line and GUI programs to serve as an authentication.

```python
myFP = FingerPrint()
try:
    myFP.open()
    print("Please touch the fingerprint sensor")
    if myFP.verify():
        print("Hello! Master")
    else:
        print("Sorry! Man")
finally:
    myFP.close()
```

## Available APIs
