
# DUT
- DUT is started as a service
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
- To run DUT manually; just run
```
/home/lyte/work/LyteAssignment/utils/run_dut.sh
```
- To ensure DUT is up
```
systemctl status lytedut.service
```
- Sample Command to control DUT
```
# msg='{"device":"led", "value":1}'
msg='{"device":"stepper", "value":360}'
mosquitto_pub -t lyte/devicecontrol -m $msg
```

# ARDUINO
To use a new Arduino UNO; download the sketch "arduino_sketch.ino" to the UNO board
