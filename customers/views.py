
import json
from datetime import date, datetime
from dateutil.relativedelta import *
from django.http import HttpResponse
from django.db.models import Q
from customers.models import Plan


# Calculate next billing date AS OF when assignment was given which was 10/13/2020
CONSTANT_TASK_ASSIGNMENT_DATE = date(2020,10,13)


def get_next_billing(request):
 
    output_dict = {}

    user_id = request.GET.get('user_id')
    if (user_id is None):
        output_dict['error'] = "user_id not provided"
        output = json.dumps(output_dict, indent=4, sort_keys=True)           
        return HttpResponse(output, content_type="application/json")


    output_dict['user_id'] = user_id

    # I'm assuming an active plan has either no subscription end date
    # or a subscription end date after the AS OF constant date of when this task was assigned
    # There may be more than one active plan as seen in the sample input for user_pu and user_lp in the
    # sample data.
    # We need the next upcoming billing date across all active plans
    # We also need the latest plan size (based on start_date). These data points: next billing date and
    # latest plan size may not be from the same plan.
    # If no active plans are found I make the assumption I should return 
    # the details of the latest inactive plan
    # If no inactive plans are found then user_id has no plans in our db whatsoever and I return an error

    user_active_plans = Plan.objects.filter(Q(user_id=user_id) & 
                        Q(end_date__isnull=True)|Q(end_date__gte=CONSTANT_TASK_ASSIGNMENT_DATE)).order_by('-start_date')
    print("USER ACTIVE PLANS: " + str(user_active_plans))

    # No active plans found. Look for inactive plans
    if (len(user_active_plans) == 0):
        user_inactive_plans = Plan.objects.filter(user_id=user_id,end_date__lt=CONSTANT_TASK_ASSIGNMENT_DATE).order_by('-start_date')
        print("USER INACTIVE PLANS: " + str(user_active_plans))

        # User_id has never had a plan with us. Return an error
        if (len(user_inactive_plans) == 0):
            output_dict['error'] = "user_id has no storage plan records"
            output = json.dumps(output_dict, indent=4, sort_keys=True)           
            return HttpResponse(output, content_type="application/json")

        # Take the latest inactive plan (queryset is ordered by start_date desc)
        latest_inactive_plan = user_inactive_plans[0]

        output_dict['subscription_start_date'] = datetime.strftime(latest_inactive_plan.start_date, '%b %d, %Y')
        output_dict['is_active'] = 'No'
        output_dict['next_billing_date'] = ''
        output_dict['current_plan'] = ''

    # Active plans were found
    else:
        # Go through each active plan determining its next billing date
        # We want to return the earliest of these billing dates and its associated start_date
        earliest_billing_date = None
        start_date = ''
        for plan in user_active_plans:
        
            next_billing_date = get_next_billing_date(plan.start_date)
            if (earliest_billing_date is None or next_billing_date < earliest_billing_date):
                earliest_billing_date = next_billing_date
                start_date = datetime.strftime(plan.start_date, '%b %d, %Y') if plan.start_date else None
            else:
                continue

        # Now get the latest of their storage plans - the one with the latest start date
        # (Please see the README for some notes on my confusion between the instructions and output data here)
        # Queryset is ordered by start_date desc so the first record is the latest plan
        current_plan = user_active_plans[0].storage_plan

        output_dict['subscription_start_date'] = start_date
        output_dict['is_active'] = 'Yes'
        output_dict['next_billing_date'] = datetime.strftime(earliest_billing_date, '%b %d, %Y') if earliest_billing_date else None
        output_dict['current_plan'] = current_plan

    output = json.dumps(output_dict, indent=4, sort_keys=True)           
    return HttpResponse(output, content_type="application/json")


def get_next_billing_date(start_date):

    if (start_date is None):
        return None

    # Keep adding one month to the start date until you reach a date after 
    # the constant AS OF date CONSTANT_TASK_ASSIGNMENT_DATE
    next_month = start_date
    i = 1
    while(next_month <= CONSTANT_TASK_ASSIGNMENT_DATE):
        next_month=start_date + relativedelta(months=+i)
        i+=1
        #print("next_month: " + str(next_month))
        
    return next_month
    #return datetime.strftime(next_month, '%b %d, %Y')
