import os
import time

import pytest
import logging
from libs.dut_monitor import DUTMonitor
from libs.mqtt import MqttClient

logger = logging.getLogger('LyteProject')

def pytest_addoption(parser):
    """Pytest commandline options.
    :param parser:
    :return:
    """
    parser.addoption("--dut_ip", action="store", default="127.0.0.1",
                     help="IP address of the device under test"),
    parser.addoption("--arduino_port", action='store',
                     default="/dev/ttyUSB0", help="Arduino UNO port")
    parser.addoption('--repeat', action='store',
                     help='Number of times to repeat each test')

def arduino_port(request):
    """Read arduino port from pytest parameters.
    :param request:
    :return: Arduino port string
    """
    arduino_port = request.config.getoption("--arduino_port")
    return arduino_port

def dut_ip(request):
    """Read DUT IP from pytest parameters.
    :param request:
    :return: DUT IP string
    """
    dut_ip = request.config.getoption("--dut_ip")
    return dut_ip

@pytest.fixture(scope="function")
def dut_monitor(request):
    """DUT monitor fixture.
    :param request:
    :return:DUT monitor object
    """
    logger.info(f"arduino_port: {arduino_port(request)}")
    return DUTMonitor(arduino_port=arduino_port(request))

@pytest.fixture(scope="module")
def dut_mqtt(request):
    """MQTT connection fixture.
    :param request:
    :return: mqtt client object
    """
    logger.info(f"dut_ip: {dut_ip(request)}")
    return MqttClient(host=dut_ip(request), port=1883)

def pytest_generate_tests(metafunc):
    """capability to repeat test execution.
    :param metafunc:
    :return:
    """
    if metafunc.config.option.repeat is not None:
        count = int(metafunc.config.option.repeat)

        # Add a new fixture 'repeat_test'
        metafunc.fixturenames.append('repeat_test')

        # Parametrize the tests with 'repeat_test' fixture
        # @pytest.mark.parametrize('repeat_test', range(count))
        metafunc.parametrize('repeat_test', range(count))

def pytest_sessionstart(session):
    """Called after the Session object has been created and
    before performing collection and entering the run test loop.
    Can be used to upgrade the DUT and ensure it is in good
    state before test execution.
    """
    os.system("sudo /usr/bin/systemctl restart lytedut.service")
    time.sleep(5)


def pytest_sessionfinish(session, exitstatus):
    """Called after whole test run finished, right before
    returning the exit status to the system.
    This can be used to get DUT back to a known good state.
    """
    os.system("sudo /usr/bin/systemctl restart lytedut.service")
    time.sleep(5)
