Feature: User Performs common use cases

	Scenario Outline: Search for existing product

	Given Main page is loaded
	When <existing product> is searched for
	Then Results will contain <existing product>

	Examples:
	 | existing product |
	 | iMac |
	 # the rest are unused, due to problems with spaces, quoting, escaping ...
	 #| HP LP3065 |
	 #| Samsung Galaxy Tab 10.1 |


	Scenario: New order gets added to Order History (Registered user)

	Given User has N orders in their Order History
	When User creates and submits Order
	Then User's Order History will be N plus 1 Orders long


	Scenario: Make an order with long note (Registered user)

	Given There is a valid order form filled up to the Delivery Method step
	When Malicious user inputs the shipping method and a very long comment about their order before proceeding
	Then Order will proceed or warn user about the comment-too-long problem


	Scenario: Purchase a Gift Certificate

	Given Registered user has opened the Purchase a Gift Certificate page
	When Gift certificate purchase Form is filled and submitted
	Then User is redirected back to the store
