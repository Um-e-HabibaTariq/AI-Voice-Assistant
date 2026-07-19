import sounddevice as sd

print("Available Audio Devices:\n")

devices = sd.query_devices()

for i, device in enumerate(devices):
    print(f"{i}: {device['name']}")