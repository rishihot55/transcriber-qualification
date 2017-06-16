var s,
UserCreateWidget = {
	settings: {
		form: $('#create-user-form'),
		userIdField: $('#create-user-form #user_id'),
		nameField: $('#create-user-form #name'),
		emailField: $('#create-user-form #email')
	},

	bindUIActions: function() {
		s.form.submit(function(e) {
			e.preventDefault();

			if (!UserCreateWidget.validateUserData(
				s.userIdField.val(), s.nameField.val(), s.emailField.val())) {
				StatusWidget.showError('Please enter valid data');
				return;
			}

			UserService.create(s.form.serialize())
			.then(function() {
				StatusWidget.showSuccess('The user has been created!');
				UserListWidget.refresh();
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

	bindUIActions: function() {
		t.fetchUserButton.click(function(e) {
			e.preventDefault();

			if (!t.userIdField.val()) {
				StatusWidget.showError('Please enter a user id!');
				return;
			}

			UserService.find(t.userIdField.val())
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

			UserService.update(t.userNumber, t.form.serialize())
			.then(function() {
				StatusWidget.showSuccess('The user has been updated!');
				UserListWidget.refresh();
			});
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

	renderUsersList: function(users) {
		var usersData = transformArrayObjectProperty(users, "rights", parseRights);
		populateTable(UserListWidget.settings.usersTableBody, usersData, ["user_id", "name", "email", "rights"])
	},

	init: function() {
		UserService.all()
		.then(UserListWidget.renderUsersList);
	},

	clearUsersList: function() {
		this.settings.usersTableBody.html("");
	},

	refresh: function() {
		UserListWidget.clearUsersList();
		UserService.all()
		.then(UserListWidget.renderUsersList);
	}
};

function parseRights(userRights) {
	var rights = [];
	if (userRights[0] == "1")
		rights.push("Admin")
	if (userRights[1] == "1")
		rights.push("Transcriber");
	if (userRights[2] == "1")
		rights.push("Voicer");
	if (rights.length == 0)
		rights.push("Disabled");
	return rights.join();
}

(function() {
	UserCreateWidget.init();
	UserUpdateWidget.init();
	UserListWidget.init();
})();