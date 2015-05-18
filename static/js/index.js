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
		// information
		$('#information').children().remove();
		$('#information').append('<li class="list-group-item active">' + data.user['screen_name'] + '</li>');
		for(k in data.user) {
			if(k == 'screen_name' || k == 'id' || k == 'profile_image_url') {
				continue;
			} else {
				$('#information').append('<li class="list-group-item">' + k + ': ' + data.user[k]+ '</li>');
			}
		}
		// statistics
		$('#rating').text('Rating: ' + data.analysis.total.toFixed(2) * 10);
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
		// only show 100 friends
		if(nodes.length > 50)
			nodes = _.sample(nodes, 50);
		self = {
			screen_name: data.user.screen_name,
			followers_count: data.user.followers_count,
			profile_image_url: data.user.profile_image_url,
		};
		var max = nodes[0].followers_count || 0;
		links = nodes.map(function(d) {
			max = d.followers_count > max ? d.followers_count : max;
			return {source: self, target: d};
		});
		nodes.push(self);
		drawFriendNetwork(nodes, links, self, max);
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

	function drawFriendNetwork(nodes, links, self, max_count) {
		var width = 600,
			height = 600;

		$('#friend-network').children().remove();

		var svg = d3.select("#friend-network").append("svg")
			.attr("width", width)
			.attr("height", height);

		var force = d3.layout.force()
			.gravity(0)
			.distance(200)
			.charge(-30)
			.size([width, height])
			.nodes(nodes)
			.links(links)
			.start();

		var link = svg.selectAll(".link")
			.data(links)
			.enter().append("line")
			.attr("class", "link");

		var node = svg.selectAll(".node")
			.data(nodes)
			.enter().append("g")
			.attr("class", "node")
			.call(force.drag);

		node.append("image")
			.attr("xlink:href", function(d) { return d.profile_image_url; })
			.attr("x", function(d) { return -24; })
			.attr("y", function(d) { return -24; })
			.attr("width", function(d) {
				var w = 48 * d.followers_count / max_count;
				if(d.screen_name == self.screen_name)
					w = 48;
				return w > 24 ? w : 24;
			})
			.attr("height", function(d) {
				var h = 48 * d.followers_count / max_count;
				if(d.screen_name == self.screen_name)
					h = 48;
				return h > 24 ? h : 24;
			});

		node.append("text")
			.attr("dx", 12)
			.attr("dy", ".5em")
			.text(function(d) { return d.screen_name; });

		force.on("tick", function() {
			link.attr("x1", function(d) { return d.source.x; })
				.attr("y1", function(d) { return d.source.y; })
				.attr("x2", function(d) { return d.target.x; })
				.attr("y2", function(d) { return d.target.y; });
			node.attr("transform", function(d) {
				return "translate(" + d.x + "," + d.y + ")";
			});
		});
	}

	$(document).ready(function() {
		$('#analyze-btn').click(analyzeHandler);
		$('#username-input').keypress(function(event) {
			if(event.which == 13)
				analyzeHandler(event);
		});
	});

})();