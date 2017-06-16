var LoginManager = {
	settings: {
		loginForm: $('#login-form')
	},

	init: function() {
		LoginManager.bindUIActions();
	},

	bindUIActions: function() {
		LoginManager.settings.loginForm.submit(function(e) {
			e.preventDefault();
			var userId = $('#user_id').val();

			LoginManager.login(userId)
			.then(redirect('/dashboard'))
			.catch(handleError);
		});
	},

	login: function(userId) {
		return $.ajax({
			url: "/login",
			method: "POST",
			data: {
				"user_id": userId,
			}
		});
	}
};

(function() {
	LoginManager.init();
})();