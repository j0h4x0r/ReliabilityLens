(function() {
	function analyzeHandler() {
		var username = $('#username-input').val();
		$('#welcome-text').hide();
		$('#no-result').hide();
		$('#result').hide();
		$('#loading-text').show();
		$.ajax({
			url: '/analyze',
			data: {username: username},
			dataType: 'json',
			success: function(data) {
				$('#loading-text').hide();
				if(!data['success']) {
					$('#no-result').show();
					return;
				}
				$('#result').show();
				visualizeData(data);
			},
		});
	}

	function visualizeData(data) {
		// statistics
		$('#rating').text(data.analysis.total.toFixed(1) * 10);
		$('#statistics').children().remove();
		for(k in data.analysis) {
			if(k == 'total')
				continue;
			$('#statistics').append('<li class="list-group-item active">' + k + ' analysis</li>');
			for(item in data.analysis[k]) {
				$('#statistics').append('<li class="list-group-item">' + item + ': ' + data.analysis[k][item] * 10 + '</li>');
			}
		}
		// word cloud
		var min = max = data.data.words[0][1]
		data.data.words.forEach(function(d) {
			min = d[1] < min ? d[1] : min;
			max = d[1] > max ? d[1] : max;
		});
		var scale = d3.scale.linear().domain([min, max]).range([30, 300]);
		var wordData = data.data.words.map(function(d) {
			return {text: d[0], size: scale(d[1])};
		});
		drawWordCloud(wordData);
		// friend graph
		nodes = data.data.friends;
		self = {
			screen_name: data.user.screen_name,
			friends_count: data.user.friends_count,
			profile_image_url: data.user.profile_image_url,
		};
		links = nodes.map(function(d) {
			return {source: self, target: d};
		});
		nodes.append(self);
	}

	function drawWordCloud(data) {
		var fill = d3.scale.category20();
		d3.layout.cloud().size([300, 300])
			.words(data)
			.padding(5)
			.rotate(function() { return ~~(Math.random() * 2) * 90; })
			.font("Impact")
			.fontSize(function(d) { return d.size; })
			.on("end", draw)
			.start();

		function draw(words) {
			$('#word-cloud').children().remove();
			d3.select("#word-cloud").append("svg")
				.attr("width", 300)
				.attr("height", 300)
				.append("g")
				.attr("transform", "translate(150,150)")
				.selectAll("text")
				.data(words)
				.enter().append("text")
				.style("font-size", function(d) { return d.size + "px"; })
				.style("font-family", "Impact")
				.style("fill", function(d, i) { return fill(i); })
				.attr("text-anchor", "middle")
				.attr("transform", function(d) {
					return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
				})
				.text(function(d) { return d.text; });
		}
	};

	$(document).ready(function() {
		$('#analyze-btn').click(analyzeHandler);
		$('#username-input').keypress(function(event) {
			if(event.which == 13)
				analyzeHandler(event);
		});
	});

})();