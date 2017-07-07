"""
 Python. Practical Work #2
 This code allows to send packages from input file to addressant by ip-address
"""

#!/usr/bin/env python
from c_code import c_code
import json
import re
import time
from scapy.all import sr1, send, IP, ICMP, UDP, sniff, RAW

# Constants for working with files
JSONFILE_EXTENSION = '.json'
TXTFILE_EXTENSION = '.txt'

# Regular expression for searching message for addressant
IVASYK_PATTERN = '(.{2})+$'
DMYTRYK_PATTERN = '^[A-Z]'
LESYA_PATTERN = '^.+\Wend$'

# Default values for working with packets
DEFAULT_TIMEOUT = 2
DEFAULT_TTL = 20
DEFAULT_PORT = 8000
SEND_PACKET = 'udp'
CODING = 'utf-8'
# Messages for exceptions
CANNOT_OPEN_FILE_MESSAGE = "Can not open"
EMPTY_MESSAGE = "It is empty"
NOT_FOUND_ADDRESSANT_MESSAGE = "The addressant is not found"
ADDRESSANT_OFFLINE_MESSAGE = "Addressant is offline!!!"

# Functions for searching addressant by message
def check_ivasyk(message):
    """
    Checking message for Ivasyk
    ---------------------------
        :param message : str
    """

    return re.match(IVASYK_PATTERN, message)

def check_dmytryk(message):
    """
    Checking message for Dmytryk
    ----------------------------
        :param message : str
    """

    return not check_ivasyk(message) and re.match(DMYTRYK_PATTERN, message)

def check_ostap(message):
    """
    Checking message for Ostap
    --------------------------
        :param message : str
    """

    return not check_ivasyk(message) and not check_dmytryk(message) and not check_lesya(message)

def check_lesya(message):
    """
    Checking message for Lesya
    --------------------------
        :param message : str
    """

    return re.match(LESYA_PATTERN, message)


# Dictionary for storing functions for addressants
dict = {'Ivasyk': check_ivasyk,
        'Dmytryk': check_dmytryk,
        'Ostap': check_ostap,
        'Lesya': check_lesya}


class Addressant:
    """
    The class allow store data about addressant
    -------------------------------------------
        :param name : str
                addressant's name
        :param ip : str
                addressant's ip-address
        :param messages : list of str
                addressant's messages
    """

    def __init__(self, name, ip):
        """
        Constructor of class
        --------------------
        :param name: str
                addressant's name
        :param ip: str
                addressant's ip-address
        """

        self.name = name
        self.ip = ip
        self.messages = []

    def __str__(self):
        """
        The method is overridden for better showing data of class
        ---------------------------------------------------------
        :return: str
        """

        return '| name - ' + self.name + ' | ip_address - ' + self.ip + ' |'


def generator(file_name='messages'):
    """
    Generators for reading one string from file
    :param file_name: str
            path to file
    :yield one string from file
    :raise exception if can not open input file or file is empty
    """
    if c_code.open_file(file_name + TXTFILE_EXTENSION) == -1:
        error = IOError()
        error.strerror = CANNOT_OPEN_FILE_MESSAGE
        error.filename = file_name + TXTFILE_EXTENSION
        raise error

    msg = c_code.get_message()
    # if file is empty then raise exception
    if not msg:
        error = IOError()
        error.strerror = EMPTY_MESSAGE
        error.filename = file_name + TXTFILE_EXTENSION
        raise error

    while msg:
        yield msg
        # read next string
        msg = c_code.get_message()


def read_json(name_file='addressants'):
    """
    Function for reading data about addressants
    -------------------------------------------
    :param name_file: str
            path to json file with data about addressants
    :return: dictionary of addressants name as key and ip-address as value
    """

    with open(name_file + JSONFILE_EXTENSION, 'r') as file:
        addresants = json.load(file)

    return  addresants


def get_addressants():
    """
    Function for getting list of addressants
    ----------------------------------------
    :return: list of addressants
    """

    addressants = []

    # generating list
    for name, ip in read_json().items():
        addressants.append(Addressant(name, ip))

    return addressants


def fill_messages(addressant, messages):
    """
    Function for filling list of addressant's messages
    --------------------------------------------------
    :param addressant: Addressant
            object of class Addressant
    :param messages: list of str
            all messages from input file
    :return: None if addressant is not found
    """

    check_func = dict.get(addressant.name, None)

    if not check_func:
        print(NOT_FOUND_ADDRESSANT_MESSAGE)
        return

    for message in messages:
        if check_func(message.strip('\n')): # set message without '\n' in end
            addressant.messages.append(message)

def ping(ip):
    """
    Function for pinging ip-address
    -------------------------------
    :param ip: str
            ip-address to pinging
    :return: bool
            True - ip-address is connected
            False - ip-address is not connected
    """

    reply = sr1(IP(dst=ip, ttl=DEFAULT_TTL) / ICMP(), timeout=DEFAULT_TIMEOUT, verbose=False)

    return bool(reply)

def send_messages(addressant):
    """
    Function for sending all messages for one addressant
    ----------------------------------------------------
    :param addressant: Addressant
            object of class Addressant
    :return: None if addressant is offline
    """

    if not ping(addressant.ip):
        print(ADDRESSANT_OFFLINE_MESSAGE)
        return

    # sending each message for addressant that is online by UDP
    for msg in addressant.messages:
        packet = IP(dst=addressant.ip) / UDP(sport=DEFAULT_PORT, dport=DEFAULT_PORT) / msg
        send(packet, verbose=False)
        sniff_packet(packet, addressant.ip, addressant.name)

def sniff_packet(packet, ip, name):
    """
    Function for sniffing packet
    :param packet: str
            full packet
    :param ip: str
            addressant's ip-address
    :param name: str
            addressant's name
    :return: None
    """

    msg = packet.getlayer(Raw).load.decode(CODING)

    catched_packtes = sniff(filter=SEND_PACKET, timeout=DEFAULT_TIMEOUT)

    for pckt in catched_packtes:
        try:
            packet_load = pckt.getlayer(Raw).load

            if pckt.getlayer(IP).dst == ip and packet_load.decode(CODING) == msg:
                print('Message -' + msg + '- was sent to ' + name)
                return

        except UnicodeDecodeError:
            pass
        except AttributeError:
            pass

        print('Message -' + msg + '- was not send to ' + name)

def main():
    """
    Main function of this program.
    This function shows result of working program
    ---------------------------------------------

    """
    try:
        messages = [msg for msg in generator() if msg != '\n']

        for i in get_addressants():
            fill_messages(i, messages)
            send_messages(i)
    except IOError as e:
            print(e.strerror + " - " + str(e.filename))
    except Exception as e:
            print(e)

if __name__ == '__main__':
    main()
