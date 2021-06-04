# Crystal ball

```
components:
-----------
    $15 raspi zero w
    $5  8-16gb+ micro SD card
    $6  mini usb mic (Kinobo USB 2.0)
    $3  mini-usb to usb-B cable adapter
    $3  mini-hdmi to hdmi cable adapter

    $15 raspi audio hat (Adafruit Speaker Bonnet)
    $15 speakers (Adafruit Stereo Enclosed Speaker Set - 3W 4 Ohm)
    $11 LED lights (NeoPixel Ring - 16 x WS2812 5050 RGB LED with Integrated Drivers )
    $3  motion sensor (HC-SR501 Infrared PIR Motion Sensor Module)
    $15 snow globe (Darice Make, Plastic, 130mm Waterglobe Kit, Clear )
    ==========
    $91 total

also need:
----------
    1500 grit sand paper 
    hot glue gun
    tea box
    raspi breadboard jumper wires
    soldering iron & solder
    monitor and computer


bonnet install:
    https://learn.adafruit.com/adafruit-speaker-bonnet-for-raspberry-pi/raspberry-pi-usage

leds:
    https://learn.adafruit.com/adafruit-neopixel-uberguide/python-circuitpython

raspi assistant:
    looked into rhaspy but scrapped it after having trouble

    https://www.instructables.com/Pi-Home-a-Raspberry-Powered-Virtual-Assistant/

    https://pimylifeup.com/raspberry-pi-google-assistant/
    https://github.com/googlesamples/assistant-sdk-python/issues/235#issuecomment-409523986

    must compile from scratch as premade binaries don't work on pi zero
    -------------------------------------------------------------------
    pip uninstall grpc grpcio
    rm -rf ~/.cache/pip/*
    apt install libffi-dev libssl-dev
    python -m pip install --upgrade --no-binary :all: grpcio

    first start example:
    --------------
    google-oauthlib-tool --client-secrets ~/credentials.json \
    --scope https://www.googleapis.com/auth/assistant-sdk-prototype \
    --scope https://www.googleapis.com/auth/gcm \
    --save --headless

    later start?:
    ------------
    googlesamples-assistant-pushtotalk --project-id raspi-assistant-id --device-model-id raspi-assistant-model-id

    modified:
    ---------
    /home/pi/venv/lib/python3.7/site-packages/googlesamples/assistant/grpc/pushtotalk.py

    /home/pi/venv/lib/python3.7/site-packages/googlesamples/assistant/grpc/crystalball.py


hardware pins used:
-------------------
    sound: 18, 19, 21  https://learn.adafruit.com/adafruit-speaker-bonnet-for-raspberry-pi/pinouts
    lights: 12, 5v, G  https://learn.adafruit.com/adafruit-neopixel-uberguide/python-circuitpython
    motion: 13, 5v, G  https://learn.adafruit.com/pir-passive-infrared-proximity-motion-sensor/circuitpython-code


extra installs:
---------------
                motion   stocks
    pip install gpiozero yfinance
    
    apt-get install espeak


sound conf:  /etc/asound.conf
-----------------------------
pcm.speakerbonnet {
    type hw card 0
}

pcm.dmixer {
    type dmix
    ipc_key 1024
    ipc_perm 0666
    slave {
        pcm "speakerbonnet"
        period_time 0
        period_size 1024
        buffer_size 8192
        rate 44100
        channels 2
    }
}

ctl.dmixer {
    type hw card 0
}

pcm.softvol {
    type softvol
    slave.pcm "dmixer"
    control.name "PCM"
    control.card 0
}

ctl.softvol {
    type hw
    card 0
}

pcm.mic {
  type plug
  slave {
    pcm "hw:1,0"
    rate 44100
  }
}

pcm.!default {
    type            plug
    slave.pcm       "softvol"
    slave.pcm       "mic"
}
```
