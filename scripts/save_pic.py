def save_image(self, name):
	volt_base, volt_unit = self.__get_waveform()
	x_axis = self.__get_x_axis()
	time_unit = self.__get_time_base()
	
	ax_figure.set_xlabel('Time [' + time_unit + ']')
	ax_figure.set_ylabel('Volt [' + volt_unit + ']')
	ax_figure.set_ylim(-4 * volt_base, 4 * volt_base)
	
	plot_label = str(volt_base) + " " + str(volt_unit) + " / Div"
	plot_figure = plot_figure.plot(x_axis, label=plot_label)

	plt.plot()
	fig.savefig(fname=file_name + '.png')