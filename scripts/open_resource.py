def open_resource(self, path):
	resource_manager = visa.ResourceManager(visa_library=path)

	try:
		instruments = resource_manager.list_resources()
		gpib = [x for x in instruments if str(x).startswith('GPIB')]

		if len(gpib) != 1:
			raise Exception('Bad instrument list', instruments)

		self.scope = resource_manager.open_resource(gpib[0])
		self.scope.timeout = 5000
	except Exception:
		raise OscilloscopeError(message='Failed to open resource')