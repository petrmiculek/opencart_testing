Feature: Admin performs various use cases

	Scenario: User information change is reflected in orders' view

	Given Registered User Bob had made an order X
	And Bob changed their email address after the order X had been made
	When Admin Alice checks order author's email
	Then Email shown will be the new Bob's address


	Scenario: User's reward points are altered (even values)

	Given Admin Alice has opened Registered User's (Bob's) Reward points balance
	When Alice gives Bob K points
	And Alice gives Bob -(K/2) points
	And Alice gives Bob -(K/2) points
	Then Bob's points will be at their previous value


	# breaks for K > INT_MAX
	# input field is clipped to Int32 range
	# User's reward point balance is of wider range

	# Below: alternative scenario for revealing this "bug"


	Scenario: User's reward points are altered (high values)

	Given Admin Alice has opened Registered User's (Bob's) Reward points balance
	When Alice gives Bob K (K > INT_MAX) points
	Then Bob's points will be equal to (K plus his previous points balance)
	# or Error about input validation will be shown (which there isn't any)


	# unused - failed to implement

	# Scenario: Customers Online Report shows customers

	# Given User Bob is Browsing the store
	# When Admin Area Customers Online Report section is opened
	# Then Admin Area Customers Online Report will show Online customer/s

		# Scenario: Extension Installer Upload Interrupted

	# Given Admin Alice is uploading an extension installer
	# When Admin Alice logs out before the upload finishes And
	# And Admin Alice logs back in again
	# Then Administration section Dashboard will be shown
