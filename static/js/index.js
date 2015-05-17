(function() {
	$(document).ready(function() {
		function analyzeHandler() {
			var username = $('#username-input').val();
			$('#welcome-text').hide();
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
					//...
				},
			});
		}

		$('#analyze-btn').click(analyzeHandler);
		$('#username-input').keypress(function(event) {
			if(event.which == 13)
				analyzeHandler(event);
		});
	});
})();