def send_micbac(self, data: dict):
	uut_interface, if_id = get_interface_and_id(self.interfaces, interface_name)
	interface_name = get_interface_from_pin(self.connectors, data['PIN'])
	if_info = get_interface_information(self.interfaces, uut_interface, if_id)
	interface_obj = load_interface(uut_interface, if_id, if_info)
	interface_obj.register_send(self.connection.send)
	
	dict_if_commands = interface_obj.get_dict_commands()
	for if_command in dict_if_commands:
		if if_command == data['MICBAC']:
			dict_if_commands[if_command]()

	self.connection.received_msg.wait()
	self.connection.received_msg.clear()
	self.received_msg(self.connection.get_data())