var layout = {
	// title: {text: 'Hazus Fragility'},
	uirevision:'true',
	xaxis: {
		title: {
		  text: 'Spectral Acceleration (g)',
		  font: {
			//family: 'Courier New, monospace',
			size: 18,
			color: '#7f7f7f'
		  }
		},
		autorange: true
	  },
	  yaxis: {
		title: {
		  text: 'Damage Probability',
		  font: {
			//family: 'Courier New, monospace',
			size: 18,
			color: '#7f7f7f'
		  }
		},
		autorange: true
	  }
};

Plotly.react('hazusPlot', data, layout);

var elem = document.getElementById('hazusPlot');

let curves = JSON.parse(elem.dataset.hazusCurves);

var x = JSON.parse(elem.dataset.hazusX);

// add random data to three line traces
var data = [
	{mode:'lines', line: {color: "#b55400"},  x: x, y: curves.Slight, name: "Slight"},
	{mode: 'lines', line: {color: "#393e46"}, x: x, y: curves.Moderate, name: "Moderate"},
	{mode: 'lines', line: {color: "#222831"}, x: x, y: curves.Extensive, name: "Extensive"},
	{mode: 'lines', line: {color: "#222831"}, x: x, y: curves.Complete, name: "Complete"},
]

Plotly.react('hazusPlot', data, layout);
