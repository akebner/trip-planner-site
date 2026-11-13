from drafter import *
from dataclasses import dataclass
from bakery import assert_equal

@dataclass
class Expense:
    category: str
    option: str
    cost: int

@dataclass
class State:
    budget: int
    budget_remaining: int
    current_category: str
    expenses: list[Expense]
    hotel_cost: int
    meals_cost: int
    activities_cost: int
    stay_duration: int


@route
def index(state: State) -> Page:
    '''
    Creates home page
    This function cannot be unit tested
    '''
    return Page(state, [
        "Welcome to your trip budget planner!\n",
        Button("Set Budget", "set_budget"),
    ])


@route
def set_budget(state: State) -> Page:
    '''
    Creates the set budget page which allows the user to input the budget they want
    There is a button that takes them to the summary page while also saving the user input
    This function cannot be unit tested
    '''
    return Page(state, [
        "Set Your Budget!\n",
        "What is your budget?",
        TextBox("budget_input", ""),
        "\nHow many days would you like to stay?",
        TextBox("days", ""),
        #"What is your location?",
        #TextBox("location_input", "")
        Button("Next Page", "save_budget"),
    ])

@route
def save_budget(state: State, budget_input: str, days: str) -> Page:
    '''
    Takes in the state and user input and saves it to the state class as the budget
    '''
    state.budget = int(budget_input)
    state.budget_remaining = state.budget
    state.stay_duration = int(days)
    return summary(state)

@route
def summary(state: State) -> Page:
    '''
    Creates the summary page which shows the budget, remaining budget,
    and the costs of the chosen expenses
    It has a button that allows the user to add more expenses
    '''
    state.hotel_cost = 0
    state.meals_cost = 0
    state.activities_cost = 0
    if state.expenses:
        for expense in state.expenses:
            if expense.category == "Hotel":
                state.hotel_cost = expense.cost
            if expense.category == "Meal Plan":
                state.meals_cost = expense.cost
            if expense.category == "Activity":
                state.activities_cost = expense.cost
    return Page(state, [
        "Summary Page\n",
        "Budget: $" + str(state.budget)+"\n",
        "Remaining Budget: $" + str(state.budget_remaining)+"\n",
        "Duration: " + str(state.stay_duration)+" days\n",
        "Expenses:\n",
        "Hotel: $"+str(state.hotel_cost)+"\n",
        "Meals: $"+str(state.meals_cost)+"\n",
        "Activities: $"+str(state.activities_cost)+"\n",
        Button("Add Expenses", "choose_expense"),
    ])

@route
def choose_expense(state: State) -> Page:
    '''
    Creates the expense page which allows the user to chose a category to focus on
    This function cannot be unit tested
    '''
    return Page(state, [
        "Expenses Page\n",
        "Category:",
        SelectBox("category",["Hotel", "Meal Plan", "Activity"], "Hotel"),
        Button("Next", "choose_option"),
    ])

@route
def choose_option(state: State, category: str) -> Page:
    '''
    Takes in the state and the users chosen category and redirects the
    user to the specific page corresponding to the users choice
    '''
    state.current_category = category
    if category == "Hotel":
        return hotels_page(state)
    elif category == "Meal Plan":
        return meals_page(state)
    elif category == "Activity":
        return activity_page(state)
    return choose_expense(state)

@route
def hotels_page(state: State) -> Page:
    '''
    Creates the page that allows users to pick hotel options
    This function cannot be unit tested
    '''
    return Page(state, [
        "Hotel Options:\n",
        SelectBox("option",["Hostel ($80)", "Midscale ($120)", "Luxury ($300)"], "Hostel ($80)"),
        Button("Add Expense", "save_expense"),
    ])

@route
def meals_page(state: State) -> Page:
    '''
    Creates the page that allows users to pick meal options
    This function cannot be unit tested
    '''
    return Page(state, [
        "Meal Options:\n",
        SelectBox("option",["2 Meals a day ($25)", "3 Meals a day ($45)", "Unlimited meals ($100)"], "2 Meals a day ($25)"),
        Button("Add Expense", "save_expense"),
    ])

@route
def activity_page(state: State) -> Page:
    '''
    Creates the page that allows users to pick activity options
    This function cannot be unit tested
    '''
    return Page(state, [
        "Activity Options:\n",
        SelectBox("option",["Walking Tour ($20)", "Museum Pass ($30)", "Bus Tour ($40)"], "Walking Tour ($20)"),
        Button("Add Expense", "save_expense"),
    ])

def loop_expenses(state: State, category: str) -> None:
    '''
    Takes in the state and category and determines if that
    expense category is already in the expenses list
    If it is it adds that expense cost back to the remaining budget
    and removes the expense from the list
    '''
    for expense in state.expenses:
        if expense.category == category:
            state.budget_remaining += expense.cost
            state.expenses.remove(expense)
#assert_equal(loop_expenses(State(None, None, "", [], 0, 0, 0), "Hotel"), )

@route
def save_expense(state: State, option: str) -> Page:
    '''
    Takes in the state and the option the user chose
    Saves the category, option, and cost into an expense dataclass and updates the remaining budget
    If the budget is less than 0 the user is taken to an over budget page
    If the user is not over budget than they will be redirected to the summary page
    '''
    if state.current_category == "Hotel":
        loop_expenses(state, "Hotel")
        if option == "Hostel ($80)":
            state.expenses.append(Expense("Hotel", option, 80*state.stay_duration))
        elif option == "Midscale ($120)":
            state.expenses.append(Expense("Hotel", option, 120*state.stay_duration))
        elif option == "Luxury ($300)":
            state.expenses.append(Expense("Hotel", option, 300*state.stay_duration))
        state.budget_remaining -= state.expenses[len(state.expenses)-1].cost
        if state.budget_remaining < 0:
            return over_budget(state)
        else:
            return summary(state)
    
    elif state.current_category == "Meal Plan":
        loop_expenses(state, "Meal Plan")
        if option == "2 Meals a day ($25)":
            state.expenses.append(Expense("Meal Plan", option, 25*state.stay_duration))
        elif option == "3 Meals a day ($45)":
            state.expenses.append(Expense("Meal Plan", option, 45*state.stay_duration))
        elif option == "Unlimited meals ($100)":
            state.expenses.append(Expense("Meal Plan", option, 100*state.stay_duration))
        state.budget_remaining -= state.expenses[len(state.expenses)-1].cost
        if state.budget_remaining < 0:
            return over_budget(state)
        else:
            return summary(state)
            
    elif state.current_category == "Activity":
        loop_expenses(state, "Activity")
        if option == "Walking Tour ($20)":
            state.expenses.append(Expense("Activity", option, 20))
        elif option == "Museum Pass ($30)":
            state.expenses.append(Expense("Activity", option, 30))
        elif option == "Bus Tour ($40)":
            state.expenses.append(Expense("Activity", option, 40))
        state.budget_remaining -= state.expenses[len(state.expenses)-1].cost
        if state.budget_remaining < 0:
            return over_budget(state)
        else:
            return summary(state)

@route
def over_budget(state: State) -> Page:
    '''
    Creates the over budget page and gives the user the option to reset their budget
    or to go back to the summary page while removing the expense that caused them to go
    over budget
    This function cannot be unit tested
    '''
    return Page(state, [
        "You're Over Budget!\n",
        Button("Back to Summary Page", "remove_expense"),
        Button("Reset Budget", "reset_budget"),
    ])

@route
def remove_expense(state: State) -> Page:
    '''
    Removes the expense that caused the user to go over budget
    and adds the cost back to the remaining budget then redirects user to summary page
    '''
    state.budget_remaining += state.expenses[len(state.expenses)-1].cost
    state.expenses.pop(len(state.expenses)-1)
    return summary(state)

@route
def reset_budget(state: State) -> Page:
    '''
    Resets the budget and resets all prior costs and
    redirects user back to set budget page
    '''
    state.budget = None
    state.budget_remaining = None
    state.stay_duration = 0
    state.hotel_cost = 0
    state.meals_cost = 0
    state.activities_cost = 0
    state.expenses = []
    return set_budget(state)

'''
assert_ equal test cases
'''
# ---------- save_budget ----------

state = State(None, None, "", [], 0, 0, 0, 0)
save_budget(state, "1000", "5")
assert_equal(state.budget, 1000)
assert_equal(state.budget_remaining, 1000)
assert_equal(state.stay_duration, 5)

state = State(
    1000,
    650,
    "",
    [
        Expense("Hotel", "Hostel ($80)", 240),
        Expense("Meal Plan", "3 Meals a day ($45)", 135),
        Expense("Activity", "Museum Pass ($30)", 30)
    ],
    0, 0, 0, 3
)
summary(state)

assert_equal(state.hotel_cost, 240)
assert_equal(state.meals_cost, 135)
assert_equal(state.activities_cost, 30)

# ---------- choose_option ----------

state = State(1000, 1000, "", [], 0, 0, 0, 3)
choose_option(state, "Hotel")
assert_equal(state.current_category, "Hotel")

state = State(1000, 1000, "", [], 0, 0, 0, 3)
choose_option(state, "Meal Plan")
assert_equal(state.current_category, "Meal Plan")

state = State(1000, 1000, "", [], 0, 0, 0, 3)
choose_option(state, "Activity")
assert_equal(state.current_category, "Activity")

# ---------- loop_expenses ----------

state = State(
    1000,
    760,
    "",
    [Expense("Hotel", "Hostel ($80)", 240)],
    0, 0, 0, 3
)
loop_expenses(state, "Hotel")
assert_equal(state.budget_remaining, 1000)
assert_equal(state.expenses, [])

# ---------- save_expense (Hotel) ----------

state = State(1000, 1000, "Hotel", [], 0, 0, 0, 2)
save_expense(state, "Hostel ($80)")
assert_equal(state.budget_remaining, 840)
assert_equal(
    state.expenses,
    [Expense("Hotel", "Hostel ($80)", 160)]
)

# ---------- save_expense (Meal Plan) ----------

state = State(1000, 1000, "Meal Plan", [], 0, 0, 0, 2)
save_expense(state, "3 Meals a day ($45)")
assert_equal(state.budget_remaining, 910)
assert_equal(
    state.expenses,
    [Expense("Meal Plan", "3 Meals a day ($45)", 90)]
)

# ---------- save_expense (Activity) ----------

state = State(1000, 1000, "Activity", [], 0, 0, 0, 5)
save_expense(state, "Museum Pass ($30)")
assert_equal(state.budget_remaining, 970)
assert_equal(
    state.expenses,
    [Expense("Activity", "Museum Pass ($30)", 30)]
)

# ---------- remove_expense ----------

state = State(
    500,
    -20,
    "",
    [Expense("Activity", "Bus Tour ($40)", 40)],
    0, 0, 0, 2
)

remove_expense(state)

assert_equal(state.budget_remaining, 20)
assert_equal(state.expenses, [])

# ---------- reset_budget ----------

state = State(
    1000,
    650,
    "",
    [
        Expense("Hotel", "Luxury ($300)", 300)
    ],
    300,
    100,
    40,
    5
)

reset_budget(state)

assert_equal(state.budget, None)
assert_equal(state.budget_remaining, None)
assert_equal(state.stay_duration, 0)
assert_equal(state.hotel_cost, 0)
assert_equal(state.meals_cost, 0)
assert_equal(state.activities_cost, 0)
assert_equal(state.expenses, [])

# ---------- loop_expenses tests ----------

# Removes an existing hotel expense
state1 = State(
    1000, 800, "",
    [Expense("Hotel", "Hostel ($80)", 200)],
    0, 0, 0, 0
)
loop_expenses(state1, "Hotel")
assert_equal(state1.budget_remaining, 1000)
assert_equal(state1.expenses, [])

# Removes only the meal plan expense
state2 = State(
    1000, 600, "",
    [
        Expense("Hotel", "Hostel ($80)", 200),
        Expense("Meal Plan", "3 Meals a day ($45)", 200)
    ],
    0, 0, 0, 0
)
loop_expenses(state2, "Meal Plan")
assert_equal(state2.budget_remaining, 800)
assert_equal(state2.expenses,
             [Expense("Hotel", "Hostel ($80)", 200)])

# Category does not exist
state3 = State(
    1000, 700, "",
    [Expense("Hotel", "Luxury ($300)", 300)],
    0, 0, 0, 0
)
loop_expenses(state3, "Activity")
assert_equal(state3.budget_remaining, 700)
assert_equal(state3.expenses,
             [Expense("Hotel", "Luxury ($300)", 300)])

# Empty expense list
state4 = State(
    1000, 1000, "",
    [],
    0, 0, 0, 0
)
loop_expenses(state4, "Hotel")
assert_equal(state4.budget_remaining, 1000)
assert_equal(state4.expenses, [])
    
    
        


start_server(State(None, None, "", [], 0, 0, 0, 0))
