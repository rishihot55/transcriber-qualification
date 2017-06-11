var s,
UserCreateWidget = {
	settings: {
		form: $('#create-user-form'),
		userIdField: $('#create-user-form #user_id'),
		nameField: $('#create-user-form #name'),
		emailField: $('#create-user-form #email')
	},

	createUser: function(data) {
		return $.ajax({
			url: "/users",
			method: "POST",
			data: data
		});
	},

	bindUIActions: function() {
		s.form.submit(function(e) {
			e.preventDefault();

			if (!UserCreateWidget.validateUserData(
				s.userIdField.val(), s.nameField.val(), s.emailField.val())) {
				StatusWidget.showError('Please enter valid data');
				return;
			}

			UserCreateWidget.createUser(s.form.serialize())
			.then(function() {
				StatusWidget.showSuccess('The user has been created!');
			});
		});
	},

	validateUserData: function(userId, name, email) {
		return Validator.validate([
				[userId, [Validator.rules.regexp(/[\w\d_]+/)]],
				[name, [Validator.rules.regexp(/[\w\d_]+/)]],
				[email, [Validator.rules.regexp(/[\w\d._]+@[\w\d.]+/)]]
			]);
	},

	init: function() {
		s = this.settings;
		UserCreateWidget.bindUIActions();
	}
};

var t,
UserUpdateWidget = {
	settings: {
		form: $('#update-user-form'),
		userIdField: $('#update-user-form #user_id'),
		nameField: $('#update-user-form #name'),
		emailField: $('#update-user-form #email'),
		fetchUserButton: $('#fetch-user-button'),
		adminField: $('#update-user-form #admin'),
		transcriberField: $('#update-user-form #transcriber'),
		voicerField: $('#update-user-form #voicer'),

		userNumber: null
	},

	fetchUser: function(userId) {
		if (!userId) {
			StatusWidget.showError('Please enter a user id!');
			return;
		}

		return $.ajax({
			url: "/users/" + userId,
			method: 'GET'
		});
	},

	bindUIActions: function() {
		t.fetchUserButton.click(function(e) {
			e.preventDefault();
			UserUpdateWidget.fetchUser(t.userIdField.val())
			.then(function(data) {
				t.userNumber = data.user_number;
				t.userIdField.val(data.user_id);
				t.nameField.val(data.name);
				t.emailField.val(data.email);
				t.adminField.prop('checked', data.rights[0] == "1");
				t.transcriberField.prop('checked',data.rights[1] == "1");
				t.voicerField.prop('checked',data.rights[2] == "1");
			});
		});

		t.form.submit(function(e) {
			e.preventDefault();

			if (!UserUpdateWidget.validateUserData(
				t.nameField.val(), t.emailField.val())) {
				StatusWidget.showError('Please enter valid data');
				return;
			}

			UserUpdateWidget.updateUser(t.userNumber, t.form.serialize())
			.then(function() {
				StatusWidget.showSuccess('The user has been updated!');
			});
		});
	},

	updateUser: function(userNumber, data) {
		return $.ajax({
			url: "/users/" + userNumber,
			method: "PUT",
			data: data
		});
	},

	validateUserData: function(name, email) {
		return Validator.validate([
				[name, [Validator.rules.regexp(/[\w\d_]+/)]],
				[email, [Validator.rules.regexp(/[\w\d._]+@[\w\d.]+/)]]
			]);
	},

	init: function() {
		t = this.settings;
		UserUpdateWidget.bindUIActions();
	}
};

var UserListWidget = {
	settings: {
		usersTableBody: $("#users > tbody")
	},

	retrieveUsers: function() {
		return $.ajax({
			method: "GET",
			url: "/users"
		});
	},

	renderUsersList: function(users) {
		populateTable(UserListWidget.settings.usersTableBody, users, ["user_id", "name", "email", "rights"])
	},

	init: function() {
		UserListWidget.retrieveUsers()
		.then(UserListWidget.renderUsersList);
	},

	bindUIActions: function() {
		
	}
};

(function() {
	UserCreateWidget.init();
	UserUpdateWidget.init();
	UserListWidget.init();
})();