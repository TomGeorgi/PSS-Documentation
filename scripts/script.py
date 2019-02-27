"""
Module contains some helper methods for crdc parsing.

.. codeauthor:: Tom Georgi <Tom.Georgi@konzept-is.de>
"""
import re
from model.exception_handling import ParseError
from model.micbac import interface, ai, ao, dsi, dso, swb100ma, temp, vdt


def split_pin_information(pin: str):
    """
    Method splits the Pin Information to Connector and Pin.
    Available Pins A01 - D20
    Avialble Connectors A - H

    Args:
        pin (str): CRDC Pin

    Returns:
        Connector and Pin

    Raises:
        ParseError

    See Also:
        :class:`.ParseError`

    Examples:
        >>> example_pin = 'AA01'
        >>>
        >>> try:
        >>>     connector, pin = split_pin_information(pin=example_pin)
        >>>     print('Connector: ', connector)
        >>>     print('Pin: ', pin)
        >>> except ParseError as error:
        >>>     print(error)

        Pin would be 'A01' and Connector would be 'A'
    """
    if len(pin) != 4:
        raise ParseError(message='Pin Name is too short!')
    elif not re.match(r'[A-H]+', pin[0]):
        raise ParseError(message='Wrong Connector!')
    elif not re.match(r'[A-D](0[1-9]|1[0-9]|20)', pin[1:]):
        raise ParseError(message='Wrong Pin!')
    else:
        return pin[0], pin[1:]


def get_interface_from_pin(connector_dict,
                           pin: str):
    """
    Pin Returns the Interface from the given Pin.

    Args:
        connector_dict (dict): Connector Dictionary
        pin (Pin): Connector + Pin (i.e 'AA01')

    Returns:
        str: Pin Interface

    Raises:
        KeyError:
        TypeError:
        ParseError:

    See Also:
        :class:`.ParseError`
    """
    try:
        connector, dict_pin = split_pin_information(pin=pin)
        pin_interface = connector_dict[connector][dict_pin]
    except ParseError as parse_error:
        raise parse_error
    except (KeyError, TypeError) as dict_error:
        raise dict_error

    return pin_interface


def get_interface_information(interface_dict,
                              uut_interface,
                              if_id):
    """
    Returns the Interface Information from Configuration Dictionary.
    UUT_interface means the first key in configuration dict.
    If_id means the second key in configuration dict.

    Args:
        interface_dict (dict): interface configuration dictionary
        uut_interface (str): Unit Under Test Interface from Configuration Dictionary
        if_id (str): Interface Id from Configuration Dictionary

    Returns:
        dict: Interface Information

    Raises:
        KeyError:
        TypeError:
    """
    try:
        if_information = interface_dict[uut_interface][if_id]
    except (KeyError, TypeError) as dict_error:
        raise dict_error

    return if_information


def get_interface_and_id(interface_dict,
                         interface_name):
    """
    Returns the Interface and the Interface ID from Configuration Dictionary.

    Args:
        interface_dict (dict): interface configuration dictionary
        interface_name (str): Interface Name (i.e 'AO +4 +28Vdc L8 1')

    Returns:
        tuple: interface, interface id or None, None
    """
    for uut_interface, if_id in interface_dict.items():
        for info in if_id:
            if if_id[info]['name'] == interface_name:
                return uut_interface, info
    return None, None


def load_interface(uut_interface_name,
                   interface_id,
                   interface_information):
    # pylint: disable=too-many-branches
    """
    loads an interface.

    Args:
        uut_interface_name (str): Unit Under Test Interface (i.e 'AI 4-20 mA)
        interface_id (str): interface id
        interface_information (dict): interface information

    Returns:
        instance of interface
    """
    if uut_interface_name == 'AI 4-20 mA':
        interface_obj = ai.Ai4_20mA(interface_id, interface_information)
    elif uut_interface_name == 'AI 0-10 Vdc':
        interface_obj = ai.Ai0_10Vdc(interface_id, interface_information)
    elif uut_interface_name == 'AI 0-200 Vac':
        interface_obj = ai.Ai0_200Vac(interface_id, interface_information)
    elif uut_interface_name == 'AO 4-28 Vdc':
        interface_obj = ao.Ao4_28Vdc(interface_id, interface_information)
    elif uut_interface_name == 'AO 0-10 Vdc':
        interface_obj = ao.Ao0_10Vdc(interface_id, interface_information)
    elif uut_interface_name == 'AO -10-10mA':
        interface_obj = ao.AoM10_P10mA(interface_id, interface_information)
    elif uut_interface_name == 'AO 0-175mA':
        interface_obj = ao.Ao0_175mA(interface_id, interface_information)
    elif uut_interface_name == 'DSO Group Isolation 28V':
        interface_obj = dso.Dso10maIso(interface_id, interface_information)#
    elif uut_interface_name == 'DSO Group Isolation GND':
        interface_obj = dso.DsoGrpIsoGnd(interface_id, interface_information)
    elif uut_interface_name == 'SIO NTC 30k':
        interface_obj = temp.Ntc(interface_id, interface_information)
    elif uut_interface_name == 'SIO PT100':
        interface_obj = temp.Pt100(interface_id, interface_information)
    elif uut_interface_name == 'SIO PT1000':
        interface_obj = temp.Pt1000(interface_id, interface_information)
    elif uut_interface_name == 'SIO VDT':
        interface_obj = vdt.Vdt(interface_id, interface_information)
    elif uut_interface_name == 'SW B 100mA':
        interface_obj = swb100ma.Sw_B_100mA(interface_id, interface_information)
    elif uut_interface_name in ('DSO 28V/OPN 250mA',
                                'DSO CIF 250mA',
                                'DSO GND/OPN 250mA'):
        interface_obj = dso.Dso250ma(interface_id, interface_information)
    elif uut_interface_name in ('DSO CIF 1.5A',
                                'DSO GND/OPN 1.5A G5',
                                'DSO GND/OPN 1.5A',
                                'DSO GND/OPN 1.5A Latched'):
        interface_obj = dso.Dso1p5A(interface_id, interface_information)
    elif uut_interface_name in ('DSO 28V/OPN 1.5A G1',
                                'DSO 28V/OPN 1.5A G2',
                                'DSO 28V/OPN 1.5A G2'):
        interface_obj = dso.Dso1p5A(interface_id, interface_information)
    elif uut_interface_name in ('DSI CIF', 'DSI 28V/OPN',
                                'DSI HPP', 'DSI GND/OPN 3mA',
                                'DSI GND/OPN 1-19', 'DSI GND/OPN 20-48',
                                'DSI GND/OPN 20-29'):
        interface_obj = dsi.Dsi(interface_id, interface_information)
    elif uut_interface_name == 'BIT - DSITEST':
        interface_obj = dsi.DsiTest(interface_id, interface_information)
    else:
        interface_obj = interface.Interface(interface_id, interface_information)

    return interface_obj


def start_decode_by_msg(interface_obj,
                        msg):
    """
    decodes the given msg with the decode settings from the given interface instance.

    Args:
        interface_obj: interface instance.
        msg (str): message
    """
    msg = msg.split(" ", 2)
    print(msg)
    status_code = msg[0]
    if status_code == "*1" and len(msg) > 2:
        address = msg[1].capitalize()
        value = msg[2]
        decodes = interface_obj.get_dict_decodes()
        if address in decodes:
            decodes[address](value)

			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
#############################################################
"""
(C) DIEHL Aerospace GmbH

- Project:  CRDC A350
- Author:   $Author: $
- Latest:   $Revision: $
- Date:     $Date: $
- Language: Python 3.5.0
- Cause:    Classes to handle interfaces within micbac.
"""
import logging



class Interface:
    """
    Class to represent an interface from micbac point of view.
    This class represents all common attributes and methods of the used interfaces and is enhanced
    by serveral classes for the specific interface types which are childs of it.
    """

    STP_ADDR = "B200"

    def __init__(self, if_id, information):
        """
        Constructor of the class.

        Args:
            if_id: Unique interface id.
            information: Interface information.
        """
        self.if_id = if_id
        self.name = information["name"]
        self.suffix = information["suffix"]
        self.address_status = information["address_status"]
        self.address_command = information["address_command"]
        self.dict_commands = {}
        self.dict_decodes = {}
        self.dict_information = {}
        self.send_method = None
        self.dict_information.update({"Timestamp": "?"})
        self.logger = logging.getLogger('logger')

    def get_dict_decodes(self):
        """
        Return the decoding dictionary.

        Returns:
            Dictionary fof addresses to decode and their decoding methods.
        """
        return self.dict_decodes

    def get_dict_commands(self):
        """
        Returns the available command of the object.

        Returns:
            A dictionary with the available commands of the object.
        """
        return self.dict_commands

    def get_dict_information(self):
        """
        Returns the readback information available about the object.

        Returns:
            A dictionary with available readback information names and values.
        """
        return self.dict_information

    def get_if_id(self):
        """
        Returns the unique ID of the interface.

        Returns:
            Returns the unique ID of the interface.
        """
        return self.if_id

    def request_status(self):
        """"""
        self.logger.info(self.name + ": REQUEST status.")
        cmd_addr = hex(self.address_status).lstrip("0x")
        self._send("E1 " + self.STP_ADDR + cmd_addr)

    def get_name(self):
        """
        Return the name of the interface.

        Returns:
            The name of the interface.
        """
        return "%s %s" % (self.suffix, self.name)

    def register_send(self, send_method):
        """
        Registers a send method on the object.

        Args:
            send_method: Method which can be called to send messages.
        """
        self.send_method = send_method

    def cmd_reactivation_cmd_fs(self, new_fs, offset=4):
        """
        Commands the functional status of reactivation command.
        Sets the typed in functional status.

        Args:
            new_fs: Functional status to be set.
            offset: Offset of command address in byte. Default = 4.
        """
        cmd_addr = hex(self.address_command + offset).lstrip("0x")
        cur_state = self.dict_commands["Reactivation Cmd"]["last_known_value"]
        if cur_state is None:
            cmd_code = str(new_fs) + "0000000"
        else:
            cmd_code = str(new_fs) + "000000" + str(cur_state)
        self._send("Q1 " + self.STP_ADDR + cmd_addr + " " + cmd_code)
        self.request_command_status()

    def cmd_reactivation_cmd(self, offset=4):
        """
        Toggles the "reactivation cmd".
        Depending on the current state of the "reactivation cmd" is toggled.

        Args:
            offset: Offset of comand address in byte. Default = 4.
        """
        # get command address
        cmd_addr = hex(self.address_command + offset).lstrip("0x")
        # get current status of the switch
        cur_state = self.dict_commands["Reactivation Cmd"]["last_known_value"]
        if cur_state is None:
            self.request_command_status()
            cur_state = self.dict_commands["Reactivation Cmd"]["last_known_value"]
        # decide dependend on the current status if the switch gets closed or opened
        if cur_state == "0":  # -> Off
            cmd_switch = 1
            self.logger.info(self.name + ": CLOSE reactivation.")
        elif cur_state == "1":  # -> On
            cmd_switch = 0
            self.logger.info(self.name + ": OPEN reactivation.")
        else:
            print("ERROR: No valid status information available for " +
                  self.name + " Reactivation cmd status.")
            print("\t setting reactivation to OFF")
            cmd_switch = 0
            self.logger.info(self.name + ": OPEN reactivation.")
        # build command
        cur_state_fs = self.dict_commands["FS Reactivation Cmd"]["last_known_value"]
        if cur_state_fs is None:
            cmd_code = "0000000" + str(cmd_switch)
        else:
            cmd_code = cur_state_fs + "000000" + str(cmd_switch)
        # send command
        self._send("Q1 " + self.STP_ADDR + cmd_addr + " " + cmd_code)
        self.dict_commands["Reactivation Cmd"]["last_known_value"] = str(cmd_switch)
        self.request_command_status()

    def request_command_status(self):
        raise NotImplementedError

    def _send(self, data):
        """
        Generic send method.
        Sends the given data via the registered send method of the object.

        Args:
            data: Data to send.
        """
        self.send_method(data)

    @staticmethod
    def _to_binary(int_data, bits=32):
        """
        Converts a given integer value into its binary representation as a string.

        Args:
            int_data: Integer value to be converted.
            bits: Divisor to be used.

        Returns:
             A string which displays the given value in binary representation.
        """
        # if int_data < 0:
        #    int_data *= -1
        # bin_string = ""
        # while int(divisor) != 0:
        #    bin_string = str(int(int_data / divisor))+bin_string
        #    if (int_data-divisor) > -1:
        #        int_data = int_data-divisor
        #    divisor = divisor / 2
        bin_string = ""
        for i in range(bits):
            if int_data & (1 << (bits - 1 - i)):
                bin_string = "1" + bin_string
            else:
                bin_string = "0" + bin_string
        # print "converted 0x%.8X to %s"%(int_data, bin_string)
        return bin_string

    @staticmethod
    def _get_bits(start_index, stop_index, bit_list):
        """
        Copies out a range of a bit stream represented by a string.
        The result is returned a string.

        Args:
            start_index:
            stop_index:
            bit_list: Binary stream.

        Returns:
            A string which displays the seleced subset of the given "binary" string.
        """
        result = ""
        for i in range(stop_index, start_index - 1, -1):
            result += bit_list[i]
        return result

    def _float_to_q(self, value, q):
        """
        Method gets an integer/float value and returns a hex-value.

        Args:
            value: Value to convert.
            q: Q factor for conversion as Integer.

        Returns:
            Converted value as hex-value
        """
        value = float(value) * (2 ** q)
        value = int(value)
        if value < 0:
            value = self._to_binary(value, 16)
            complement = ""
            for i in range(len(value), 0, -1):
                if str(value[i - 1]) == "0":
                    bit = "1"
                elif str(value[i - 1]) == "1":
                    bit = "0"
                complement += bit
            value = int(complement, 2) + 1
        return hex(value)

    def _q_to_float(self, value, q, signed=False):
        """
        Methods converts a q-formatted hex-value into a float value.

        Args:
            value (int): Value to convert.
            q: Q factor for conversion as Integer.
            signed: Fals if it is a signed ! conversion. Default is False.

        Returns:
            Converted value as float/integer.
        """
        if (signed is True) and (value > 32767):
            value -= 1
            value = self._to_binary(value, 16)
            complement = ""
            for i in range(len(value), 0, -1):
                if str(value[i - 1]) == "0":
                    bit = "1"
                elif str(value[i - 1]) == "1":
                    bit = "0"
                else:
                    print("ERROR: " + str(value[i - 1]) + " not 1 or 0")
                complement += bit
            value = int(complement, 2) * -1
        value = value * (2 ** -q)
        return value
		
		
		
		
		
		
#############################################
    def __send_micbac(self,
                      data: dict):
        """
        This Private Method sends a MICBAC to CRDC.

        Args:
            data (dict): data with Pin Information and MICBAC Command

        Raises:
            KeyError, TypeError
            ParseError: Pin could not be parsed

        See Also:
            :class:`.ParseError`
        """
        try:
            interface_name = helper_methods.get_interface_from_pin(connector_dict=self.connectors,
                                                                   pin=data['PIN'])
        except ParseError as parse_error:
            raise parse_error
        except (KeyError, TypeError) as dict_error:
            raise dict_error

        uut_interface, if_id = helper_methods.get_interface_and_id(interface_dict=self.interfaces,
                                                                   interface_name=interface_name)
        if uut_interface is None:
            self.logger.info('No interface found!')
            return

        try:
            if_info = helper_methods.get_interface_information(interface_dict=self.interfaces,
                                                               uut_interface=uut_interface,
                                                               if_id=if_id)
        except (KeyError, TypeError) as dict_error:
            raise dict_error

        interface_obj = helper_methods.load_interface(uut_interface_name=uut_interface,
                                                      interface_id=if_id,
                                                      interface_information=if_info)
        interface_obj.register_send(send_method=self.connection.send)

        commands = data['MICBAC'].split('\n')
        logging_pin = data['PIN']
        for command in commands:
            self.logger.info("Sending '" + command + "' to PIN " + logging_pin)
            cmd_found = False
            dict_if_commands = interface_obj.get_dict_commands()
            for if_command in dict_if_commands:
                if if_command in command.strip() \
                        and dict_if_commands[if_command]['type'] == 'Entry':
                    entry = command.replace(if_command, '').strip()
                    dict_if_commands[if_command]['action'](entry)
                    cmd_found = True
                elif if_command == command.strip():
                    dict_if_commands[if_command]['action']()
                    cmd_found = True

            if not cmd_found:
                raise ParseError(command + ' not found!')

            self.logger.info('waiting for response')
            while True:
                self.connection.received_msg.wait(timeout=2)
                if self.connection.received_msg.is_set():
                    break
                elif self.connection.abort.is_set():
                    self.logger.info('Test Abort')
                    return

            self.connection.received_msg.clear()
            data_package = self.connection.get_data()

            for data_msg in data_package:
                helper_methods.start_decode_by_msg(interface_obj=interface_obj,
                                                   msg=data_msg)

            information_str = '\n\t'
            dict_information = interface_obj.get_dict_information()
            for dict_key in dict_information:
                information_str += dict_key + ': ' + dict_information[dict_key] + '\n\t'

            self.logger.info(information_str)
