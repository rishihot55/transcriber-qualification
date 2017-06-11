function logout(e) {
	e.preventDefault();
	$.ajax({
		url: '/logout',
		method: 'GET'
	})
	.then(function() {
		redirect('/login');
	});
}

function redirect(url) {
	console.log('Setting location to : ' + url);
	window.location = url;
}

function handleError(err) {
	if (err.status == 401) {
		redirect('/login');
	}
}

var StatusWidget = {

	settings: {
		successPanel: $('#success-panel'),
		errorPanel: $('#error-panel'),
	},

	init: function() {
		this.settings.successPanel.hide();
		this.settings.errorPanel.hide();
	},

	showSuccess: function (message) {
		StatusWidget.setMessage(this.settings.successPanel, message);
		StatusWidget.animate(this.settings.successPanel);
	},

	showError: function (message) {
		StatusWidget.setMessage(this.settings.errorPanel, message);
		StatusWidget.animate(this.settings.errorPanel);
	},

	setMessage: function(panel, message) {
		panel.text(message);
	},

	animate: function(panel) {
		panel.show().delay(5000).fadeOut();
	}
};

var Validator = {
	rules: {
		required: function(data) {
			if (data) return true;
			return false; 
		},
		
		regexp: function(pattern) {
			if (!(pattern instanceof RegExp)) {
				throw Error('Invalid regular expression');
			}

			return function (data) {
				return pattern.test(data);
			}
		},
		
		file: function(data) {
			return data instanceof File;
		},

		audioFile: function(data) {
			return Validator.rules.file(data) && (data.type === 'audio/mp3' || data.type === 'audio/wav');
		}
	},

	validate: function(validationEntity) {
		if (!Array.isArray(validationEntity)) {
			throw Error('Invalid validation entity');
		}

		var i = 0;
		for (i = 0 ; i < validationEntity.length ; i++) {
			var data = validationEntity[i][0];
			var rules = validationEntity[i][1];

			var j = 0;

			for (j = 0 ; j < rules.length; j++) {
				if (!rules[j](data)) return false;
			}
		}

		return true;
	}
};

function populateTable(tableBody, data, fields) {
	var idx = 1;
	var tableFragment = document.createDocumentFragment();
	for (var idx = 0 ; idx < data.length ; idx++) {
		var rowElement = document.createElement("TR");
		var rowText = "<td>" + (idx + 1) + "</td>";
		for (var j = 0 ; j < fields.length ; j++) {
			rowText += "<td>" + data[idx][fields[j]] + "</td>";
		}
		rowElement.innerHTML = rowText;
		tableFragment.appendChild(rowElement);
	}

	tableBody.append(tableFragment);
}

(function() {
	StatusWidget.init();
	$('#logout-link').click(logout);
})();