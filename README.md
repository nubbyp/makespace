# INSTRUCTIONS

These are the steps needed to run this project. It is built using Python and a Django framework with the
built in sqllite database:

1. Make and activate a virtual environment
```
python3 -m venv .venv
source .venv/bin/activate
```

2. Install two needed libraries:

`pip3 install Django python-dateutil`

3. Run the database migration:

`./manage.py migrate`

4. Populate the sqllite db with the provided input.csv data using a Django management command, passing in the provided
input data which I've named plan_input.csv and saved in the customers/data subdirectory. 

`./manage.py populate_plans plan_input.csv`

Optionally populate additional test data from my own csv file in the same subdirectory which tests edge cases such 
as adding a month to January 31st where February doesn't have a 31st day. And also trying out dates that don't exist
and various combinations of active and inactive plans for users. 

`./manage.py populate_plans plan_input_ap_test.csv`


5. Start up the localhost server:

`./manage.py runserver`


6. Call the API endpoint get_next_billing to get the next billing date for a user_id:

Pass in user_id as a parameter

`http://localhost:8000/customers/get_next_billing?user_id=user_pu`


You will get back JSON that matches the data in the provided output.csv file. 
Here is an example:

```
{
    "current_plan": "5x5",
    "is_active": "Yes",
    "next_billing_date": "Nov 01, 2020",
    "subscription_start_date": "Jan 01, 2020",
    "user_id": "user_pu"
}
```

7. To run unit tests type:

`./manage.py test`

# NOTE

I believe the output data for one example, user_lp, has an error in it. 

The confusion for me was in the case of a user_id having multiple active plans. There were two examples
of this: user_lp and user_pu. The user_pu is consistent with my understanding of these instructions but user_lp is not.
 The instructions said:
"For purposes of this exercise - We are only interested in their next billing date and the latest plan size."

I took this to mean I should consider all the active plans a user has and for each see what the next billing date would be.
Then of those billing dates, return the earliest one (return this plan's corresponding start_date too). 
In addition, regardless of which plan has the next billing date, 
in the current_plan column, return the latest plan size based on start_date. 

The instructions specify that an "AS OF" date for the next billing date computations was: 09/21/2020

In the case of user_pu the input data is this:

```
user_pu,"Jan 1, 2020",2x2,
user_pu,"Jan 5, 2020",5x5,
```

The next billing dates for these two plans as of 9/21/2020 are 10/1/2020 and 10/5/2020 respectively. 
By my reading of the instructions above, the earliest next billing date would be 10/1/2020. However the 
latest storage plan is the other record - the 5x5 one. 

Indeed the output data provided matches this interpretation:

`user_pu,5x5,"Jan 1, 2020",10/1/2020,Yes`


HOWEVER, in the case of user_lp the input data is this:

```
user_lp,"Mar 3, 2020",10x10,
user_lp,"Apr 1, 2020",2x4,
```

The next billing dates for these two plans as of 9/21/2020 are 10/3/2020 and 10/1/2020 respectively. 
By my reading of the instructions above, the earliest next billing date would be 10/1/2020. The latest
storage plan happens to be the same record in this case - the 2x4 one started on Apr, 1 2020. 

The output data returned however is this:

`user_lp,2x4,"Mar 3, 2020",10/3/2020,Yes`

I believe the current_plan here is correct but the next_billing_date here of 10/3/2020 is incorrect and should be 10/1/2020.

Apologies if I misinterpreted this. I couldn't find another explanation that reconciled the output with the directions 
for all provided data points. 


