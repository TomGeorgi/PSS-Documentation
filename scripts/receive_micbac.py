def received_msg(self, data_package):
	for data_msg in data_package:
		start_decode_by_msg(interface_obj, data_msg)

	information_str = '\n\t'
	for dict_key in interface_obj.get_dict_information():
		information_str += dict_key + ': ' + dict_information[dict_key] + '\n\t'
	self.logger.info(information_str)