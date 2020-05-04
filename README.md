##OpenCart testing scenarios (BDD, Gherkin)

The following test scenarios use the behavior driven development approach for testing the OpenCart e-commerce platform.


The goal of following test scenarios is to focus on usual weak spots of such systems. 
The main weak spot I have decided to focus on is the user input (user as in user of the system, not the customer).


The main idea about testing the user input is that the system should always end up in a consistent state - either a valid state, 
or a "graceful exit" state.


### Users' use cases


The first part of the test scenarios covers common use cases of the system from the user's point of view. 


User should not end up in a situation where he cannot continue using the site.


User's invalid input should not break unrelated parts of the system (Long note scenario).


### Admins' use cases


The second part of the test scenarios covers some less common actions an admin might perform. 


When an admin performs an action, they should see the action's result clearly, 
e.g. the action was succesful, 
the action could not be finished because XXX, 
or similar (Reward points scenarios).


There should not be a situation when the admin breaks the website accidentally (Interrupted Extension Upload scenario).


The admin section should also reflect well actions performed by users and the system should ensure good continuity of data. (User information change scenario)



