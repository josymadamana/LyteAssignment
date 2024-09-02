
# DUT
- DUT is started as a service. Ensure the service "lytedut.service" 
with the below details is running.
```
[Unit]
Description=Lyte DUT sim
After=multi-user.target mosquitto.service

[Service]
Type=simple
ExecStart=/home/lyte/work/LyteAssignment/utils/run_dut.sh
Restart=always

[Install]
WantedBy=multi-user.target
```
- Install MQTT broker

    Refer: https://mosquitto.org/blog/2013/01/mosquitto-debian-repository/


- To run DUT manually; just run
```
/home/lyte/work/LyteAssignment/utils/run_dut.sh
```
- To ensure DUT is up
```
systemctl status lytedut.service
```

# ARDUINO
To use a new Arduino UNO; download the sketch "arduino_sketch.ino" from the 
directory "arduino_sketch" to the UNO board and connect the board to the PI via USB jack.
