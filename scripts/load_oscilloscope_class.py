 def load_oscilloscope_interface(self):
        replaced_path = str(self.__oscilloscope).replace(os.path.sep, '.')
        scope = replaced_path.split('.')[-1]
        module_string = replaced_path.rsplit('.', 1)[0]
        module = importlib.import_module(module_string)
        scope_class = getattr(module, scope)
        return scope_class()