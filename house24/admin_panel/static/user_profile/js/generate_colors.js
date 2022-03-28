function dynamicColors(labels){
	let colors = [];
	for(label in labels){
		let r = Math.floor(Math.random() * 255);
	    let g = Math.floor(Math.random() * 255);
	    let b = Math.floor(Math.random() * 255);
	    colors.push("rgb(" + r + "," + g + "," + b + ")");
	}
	return colors;
}
