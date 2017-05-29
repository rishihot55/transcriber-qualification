function login(userId) {
	return $.ajax({
		url: "/login",
		method: "POST",
		data: {
			"user_id": userId,
		}
	});
}

(function() {
	$('#login-form').submit(function(e) {
		e.preventDefault();
		var userId = $('#user_id').val();

		login(userId)
		.then(redirect('/dashboard'))
		.catch(handleError);
	});
})();