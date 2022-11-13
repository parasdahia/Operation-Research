import json
import copy
import os
from collections import defaultdict
method = ""
LINE = "\n __________________________________________________________________________________________________________\n"

def give_space(*msg):
    try:
        print(f"\n{msg[0]}\n")
    except:
        print(f"\n", end="")


class AssignmentSum:

    def __init__(self):
        self.rows = 0
        self.columns = 0
        self.data = []
        self.whole_problem = {}
        self.existing_values = {}
        self.problem_no = 0
        self.check_existing_data()

    def check_existing_data(self):
        try:
            with open("assignment_problems_data.json", mode="r") as file:
                try:
                    self.existing_values = json.load(file)
                    print(f"\n  There exist {len(self.existing_values)} problem(s) you've tried before. "
                          f"[Assignment Problem(s)]")
                    retrieve = input("  Do you want to Retrieve? (Y/N): ").lower()
                    if retrieve == "y":
                        self.retrieve()
                    else:
                        self.take_values()
                except:
                    self.take_values()

        except FileNotFoundError:
            self.take_values()

        except Exception as e:
            print(e)

    def retrieve(self):
        give_space()

        for prob in self.existing_values:
            print(f"  {prob}, "
                  f"Row(s): {self.existing_values[prob]['Row(s)']}, "
                  f"Column(s): {self.existing_values[prob]['Column(s)']}, "
                  f"First row in the Matrix: {self.existing_values[prob]['Matrix'][0]}", end="\n")
        give_space()

        while True:
            self.problem_no = input("  Enter the 'Problem Number' you want : ")
            try:
                self.rows = self.existing_values[f'Problem-{self.problem_no}']['Row(s)']
                self.columns = self.existing_values[f'Problem-{self.problem_no}']['Column(s)']
                self.data = self.existing_values[f'Problem-{self.problem_no}']['Matrix']
                print("\n ____________________________________________________________________\n")
                break
            except:
                print(f"  Problem-{self.problem_no} does not exist")

    def take_values(self):

        give_space()
        print("  New Problem in 'Assignment Problem'\n")

        # Taking Rows & Columns
        while True:
            try:
                self.rows = int(input("  Enter the Number of Row(s): "))
                if self.rows > 0:
                    self.columns = int(input("  Enter the Number of Column(s): "))
                    if self.columns > 0:
                        break
                    else:
                        print("  Number of COLUMNS(S) couldn't be Zero (0) or Negative(-)")
                else:
                    print("  Number of ROWS(S) couldn't be Zero (0) or Negative(-)")
            except:
                print("  Kindly enter the value in INTEGER!")
        give_space()

        # Feedback for Balanced or Not
        if self.rows == self.columns:
            print(f"  No. of Row(s) = No. of Column(s) = {self.rows}"
                  f"\n  The Given Assignment problem is BALANCED!\n")
        else:
            print(f"  No. of Row(s) '{self.rows}' is NOT EQUAL No. of Column(s) '{self.columns}'"
                  f"\n  The Given Assignment problem is UN-BALANCED!\n")

        # Taking Values [Matrix-Data]
        i, j = 1, 1
        values = []
        while True:
            try:
                value = input(f"  Enter the VALUE for cell ({i}, {j}): ").capitalize()
                if value == "-":
                    pass
                else:
                    value = float(value)
                if j == self.columns:
                    j = 1
                    i += 1
                    values.append(value)
                    self.data.append(values)
                    values = []
                else:
                    j += 1
                    values.append(value)
                if i > self.rows:
                    break
            except:
                print("  Kindly enter VALUE in 'NUMBER'!")

        # Saving All the Data
        self.save_data()

    def save_data(self):
        try:
            with open("assignment_problems_data.json", mode="r") as file:
                try:
                    read = json.load(file)
                    self.whole_problem = {
                        f"Problem-{len(read)+1}":
                            {"Row(s)": self.rows,
                             "Column(s)": self.columns,
                             "Matrix": self.data}
                    }
                    read.update(self.whole_problem)
                    with open("assignment_problems_data.json", mode="w") as new_file:
                        json.dump(read, new_file, indent=0)

                except:
                    self.whole_problem = {
                        f"Problem-1":
                            {"Row(s)": self.rows,
                             "Column(s)": self.columns,
                             "Matrix": self.data}
                    }
                    with open("assignment_problems_data.json", mode="w") as new_file:
                        json.dump(self.whole_problem, new_file, indent=0)

        except:
            self.whole_problem = {
                f"Problem-1":
                    {"Row(s)": self.rows,
                     "Column(s)": self.columns,
                     "Matrix": self.data}
            }
            with open("assignment_problems_data.json", mode="w") as new_file:
                json.dump(self.whole_problem, new_file, indent=0)

        print("\n  All the Data has been Saved in 'assignment_problems_data.json' file.", end="\n\n")

        with open("assignment_problems_data.json", mode="r") as f:
            all_data = json.load(f)
        for problem in all_data:
            self.problem_no = str(problem)[-1]
        print(" ____________________________________________________________________\n", end="")

class AssignmentMethods(AssignmentSum):

    def __init__(self):
        super().__init__()
        global method

        print(f"  Assignment Problem\n\n"
              f"  1. Minimization Method: \n"
              f"  2. Maximization Method: ")

        # Need Particular Solution? ↓
        while True:
            method = input("\n  Choose the method you want to perform (1|2) : ").lower()
            if method == "exit":
                break
            try:
                if method == "1":
                    self.minimization_method()
                elif method == "2":
                    self.maximization_method()
            except Exception as e:
                print(f"  No Such Method Exist, {e}")

    def minimization_method(self):

        data = copy.deepcopy(self.data)
        rows = copy.deepcopy(self.rows)
        columns = copy.deepcopy(self.columns)
        print(" ____________________________________________________________________")
        print("\n\tMinimization Case\n")

        # Feedback forBalanced (or) Unbalanced --- Also making it balance if not
        if rows == columns:
            print(f"  Row(s) = {rows}, Column(s) = {columns}\n"
                  f"  The Given Assignment Problem is BALANCED")
        else:
            print(f"  Row(s) = {rows}, Column(s) = {columns}\n"
                  f"  The Given Assignment Problem is UN-BALANCED. ", end="")
            if rows > columns:
                print("So we add dummy Column(s)")
                while not rows == columns:
                    for row in data:
                        row.append(0.0)
                    columns += 1
            else:
                print("So we add dummy Row(s)")
                while not rows == columns:
                    temp_list = [0.0 for _ in range(columns)]
                    data.append(temp_list)
                    rows += 1

        # Step - 1 Row Reduction
        for R in range(rows):
            minimum = None
            # Finding Minimum Value in a Row
            for C in range(columns):
                if data[R][C] == "-":
                    pass
                elif minimum is None:
                    minimum = data[R][C]
                elif data[R][C] < minimum:
                    minimum = data[R][C]
            # Reducing minimum value in Row
            for C in range(columns):
                if data[R][C] == "-":
                    pass
                else:
                    data[R][C] -= minimum

        print("\n    Step 1 : Row Reduction")
        for i in data:
            print(F"\t{i}")

        # Step - 2 Column Reduction
        for C in range(columns):
            minimum = None
            # Finding Minimum Value in a Row
            for R in range(rows):
                if data[R][C] == "-":
                    pass
                elif minimum is None:
                    minimum = data[R][C]
                elif data[R][C] < minimum:
                    minimum = data[R][C]
            # Reducing minimum value in Row
            for R in range(rows):
                if data[R][C] == "-":
                    pass
                else:
                    data[R][C] -= minimum

        print("\n    Step 2 : Col Reduction")
        for i in data:
            print(f"\t{i}")

        # Step - 3 Assigning Zeros
        assigned_zeros = []
        temp_data = copy.deepcopy(data)

        while not len(assigned_zeros) == rows:

            assigned_col_index = assigned_row_index = []
            for R in range(rows):
                if temp_data[R].count(0) == 1:
                    index = temp_data[R].index(0)
                    if index not in assigned_col_index:
                        if R not in assigned_row_index:
                            assigned_col_index.append(index)
                            assigned_row_index.append(R)
                            assigned_zeros.append(f'cell({R+1},{index+1}')
            break

    def maximization_method(self):

        for data in self.data:
            print(data)

        if self.rows == self.columns:
            print(f"Number of Row(s) = Number of Column(s) = {self.rows}\n"
                  f"The Given Assignment Problem is BALANCED")
        else:
            print(f"Number of Row(s) = {self.rows}, Number of Column(s) = {self.columns}\n"
                  f"The Given Assignment Problem is UN-BALANCED")

class TransportationSum:

    def __init__(self):
        self.units = 0
        self.destinations = 0
        self.demand = []
        self.supply = []
        self.data = []
        self.whole_problem = {}
        self.existing_values = {}
        self.problem_no = 0
        self.check_existing_data()

    def check_existing_data(self):
        try:
            with open("transportation_problems_data.json", mode="r") as file:
                try:
                    self.existing_values = json.load(file)
                    print(f"\n  There exist {len(self.existing_values)} problem(s) you've tried before. "
                          f"[Transportation Problem(s)]")
                    retrieve = input("  Do you want to Retrieve? (Y/N): ").lower()
                    if retrieve == "y":
                        self.retrieve()
                    else:
                        self.take_values()
                except:
                    self.take_values()

        except FileNotFoundError:
            self.take_values()

        except Exception as e:
            print(e)

    def retrieve(self):
        give_space()

        for prob in self.existing_values:
            print(f"  {prob}, "
                  f"Units: {self.existing_values[prob]['units']}, "
                  f"Destinations: {self.existing_values[prob]['destinations']}, "
                  f"Demand: {self.existing_values[prob]['demand']}, "
                  f"Supply: {self.existing_values[prob]['supply']} ", end="\n")
        give_space()
        while True:
            self.problem_no = input("  Enter the 'Problem Number' you want : ")
            try:
                self.units = self.existing_values[f'Problem-{self.problem_no}']['units']
                self.destinations = self.existing_values[f'Problem-{self.problem_no}']['destinations']
                self.demand = self.existing_values[f'Problem-{self.problem_no}']['demand']
                self.supply = self.existing_values[f'Problem-{self.problem_no}']['supply']
                self.data = self.existing_values[f'Problem-{self.problem_no}']['costs']
                os.system('cls')
                print(LINE)
                print("\t OPERATION RESEARCH METHOD • TRANSPORTATION PROBLEM")
                break
            except:
                print(f"  Problem-{self.problem_no} does not exist")

    def take_values(self):
        give_space()
        os.system('cls')
        print(LINE)
        print("\t OPERATION RESEARCH METHOD • TRANSPORTATION PROBLEM")
        print("\n   New Problem in 'Transportation Problem'\n")

        # Taking Units & Destinations
        while True:
            try:
                self.units = int(input("  Enter the No. of Unit(s): "))
                if self.units > 0:
                    self.destinations = int(input("  Enter the No. of Destination(s): "))
                    if self.destinations > 0:
                        break
                    else:
                        print("  Value of DESTINATION(S) couldn't be Zero (0) or Negative(-)")
                else:
                    print("  Value of UNIT(S) couldn't be Zero (0) or Negative(-)")
            except:
                print("  Kindly enter the value in INTEGER!")
        give_space()

        # Taking Demand
        num = 0
        while True:
            num += 1
            if num > self.destinations:
                break
            try:
                demand_value = int(input(f"  Enter the demand at 'Destination {num}': "))
                if demand_value <= 0:
                    give_space(f"  Demand at 'Destination {num}' cannot be <= 0")
                    num -= 1
                else:
                    self.demand.append(demand_value)
            except:
                give_space("  Kindly Enter 'INTEGER' value for Demand")
                num -= 1
        give_space()

        # Taking Supply
        num = 0
        while True:
            num += 1
            if num > self.units:
                break
            try:
                supply_value = int(input(f"  Enter the Supply from 'Unit {num}': "))
                if supply_value <= 0:
                    give_space(f"  Supply from 'Unit {num}' cannot be <= 0")
                    num -= 1
                else:
                    self.supply.append(supply_value)
            except:
                give_space("  Kindly Enter 'INTEGER' value for Supply")
                num -= 1

        if sum(self.demand) == sum(self.supply):
            print(f"\n  ΣA(i) = ΣB(j) = {sum(self.demand)}"
                  f"\n  The Given Transportation problem is BALANCED!\n")
        else:
            print(f"\n  ΣA(i) != ΣB(j) [Supply is NOT EQUAL to Demand]"
                  f"\n  The Given Transportation problem is UN-BALANCED!\n")

        # Taking Costs [Matrix-Data]
        i, j = 1, 1
        values = []
        while True:
            try:
                cost = float(input(f"  Enter the VALUE for cell ({i}, {j}): "))
                if j == self.destinations:
                    j = 1
                    i += 1
                    values.append(cost)
                    self.data.append(values)
                    values = []
                else:
                    j += 1
                    values.append(cost)
                if i > self.units:
                    break
            except:
                print("  Kindly enter VALUE in 'NUMBER'!")

        self.save_data()

    def save_data(self):
        try:
            with open("transportation_problems_data.json", mode="r") as file:
                try:
                    read = json.load(file)
                    self.whole_problem = {
                        f"Problem-{len(read)+1}":
                            {"units": self.units,
                             "destinations": self.destinations,
                             "demand": self.demand,
                             "supply": self.supply,
                             "costs": self.data}
                    }
                    read.update(self.whole_problem)
                    with open("transportation_problems_data.json", mode="w") as new_file:
                        json.dump(read, new_file, indent=0)
                except:
                    self.whole_problem = {
                        f"Problem-1":
                            {"units": self.units,
                             "destinations": self.destinations,
                             "demand": self.demand,
                             "supply": self.supply,
                             "costs": self.data}
                    }
                    with open("transportation_problems_data.json", mode="w") as new_file:
                        json.dump(self.whole_problem, new_file, indent=0)
        except:
            self.whole_problem = {
                f"Problem-1":
                    {"units": self.units,
                     "destinations": self.destinations,
                     "demand": self.demand,
                     "supply": self.supply,
                     "costs": self.data}
            }
            with open("transportation_problems_data.json", mode="w") as new_file:
                json.dump(self.whole_problem, new_file, indent=0)

        os.system('cls')
        print(LINE)
        print("\t OPERATION RESEARCH METHOD • TRANSPORTATION PROBLEM")
        print("\n  | All the Data has been Saved in 'transportation_problems_data.json' file. |", end="\n")

        with open("transportation_problems_data.json", mode="r") as f:
            all_data = json.load(f)
        for problem in all_data:
            self.problem_no = str(problem)[-1]
        print(LINE, end="")

class TransportationMethods(TransportationSum):

    def __init__(self):
        global method
        super().__init__()

        self.methods = {
            "1": self.north_west_corner_rule,
            "2": self.least_cost_method,
            "3": self.vogel_approximation_method,
            "4": self.maximum_profits
        }

        give_space()
        # Need Particular Solution? ↓
        while True:
            os.system('cls')
            print(LINE)
            print("\t OPERATION RESEARCH METHOD • TRANSPORTATION PROBLEM\n")

            print(f"  • TRANSPORTATION COST • IBFS\n\n"
                  f"   1. North-West-Corner Rule:        Rs. {self.north_west_corner_rule(need_only_cost=True)}/-\n"
                  f"   2. Least Cost Method:             Rs. {self.least_cost_method(need_only_cost=True)}/-\n"
                  f"   3. Vogel's Approximation Method:  Rs. {self.vogel_approximation_method(need_only_cost=True)}/-\n"
                  f"   4. Maximization Method.")

            method = input("\n  Choose the method you want to perform (1|2|3|4) : ").lower()
            if method == "exit":
                break
            try:
                self.methods[method]()
            except Exception as e:
                pass

    def north_west_corner_rule(self, need_only_cost=False):
        # Copying all Values
        units = [self.units].copy()[0]
        destinations = [self.destinations].copy()[0]
        supply = self.supply.copy()
        demand = self.demand.copy()
        data = copy.deepcopy(self.data)
        balanced = True

        # Balancing the Equation
        if sum(demand) > sum(supply):
            data.append([0.0 for _ in range(len(demand))])
            supply.append(sum(demand) - sum(supply))
            units += 1
            balanced = False
        elif sum(demand) < sum(supply):
            for rows in data:
                rows.append(0)
            demand.append(sum(supply) - sum(demand))
            destinations += 1
            balanced = False

        # Creating Dictionaries & Variables
        allocation = {f"({i + 1},{j + 1})": None for i in range(units) for j in range(destinations)}
        cost = {f"({i + 1},{j + 1})": data[i][j] for i in range(units) for j in range(destinations)}
        RS, DS, S, D = 0, 0, 0, 0
        transportation_cost = 0

        # Algorithm for North-West Corner Rule (Balanced)
        while not sum(demand) == sum(supply) == 0:
            if demand[D] < supply[S]:
                key = f"({DS + 1},{RS + 1})"
                allocation[key] = demand[D]
                supply[S] -= demand[D]
                demand[D] = 0
                RS += 1
                D += 1
            elif demand[D] > supply[S]:
                key = f"({DS + 1},{RS + 1})"
                allocation[key] = supply[S]
                demand[D] -= supply[S]
                supply[S] = 0
                DS += 1
                S += 1
            else:
                key = f"({DS + 1},{RS + 1})"
                allocation[key] = supply[S]
                demand[D] = supply[S] = 0
                RS += 1
                DS += 1
                S += 1
                D += 1

        for key in allocation:
            if allocation[key] is not None:
                transportation_cost += allocation[key] * cost[key]

        if need_only_cost:
            return transportation_cost

        os.system('cls')
        print(LINE)
        print("\t OPERATION RESEARCH METHOD • TRANSPORTATION PROBLEM\n")
        print(f"  • TRANSPORTATION COST • IBFS")

        print("\n\t\t\t  NORTH WEST CORNER RULE")
        print(" ____________________________________________________________________")

        # Giving Info about Balanced (or) Not-Balanced
        if balanced:
            print(f"\n  ΣA(i) = ΣB(j)\n"
                  f"  The Given Transportation problem is BALANCED!")
        else:
            print(f"\n  ΣA(i) != ΣB(j)"
                  f"\n  Total Demand: {sum(self.demand)}"
                  f"\n  Total Supply: {sum(self.supply)}"
                  f"\n  The Given Transportation problem is UN-BALANCED!")

        print("\n  BY North-West-Corner Rule ↓\n  Allocations in:")

        no_of_allocation = 0
        for key in allocation:
            if allocation[key] is not None:
                no_of_allocation += 1
                print(f"  cell{key} = {allocation[key]}")

        if no_of_allocation == (len(demand)+len(supply)-1):
            print("\n  It is Non-Degenerative Basic Feasible Solution")
        else:
            print("\n  It is Degenerative Basic Feasible Solution.")  # Epsilon (ε) in Cell(,)
        print(f"  Total Transportation Cost : Rs. {transportation_cost}/-")

        print(" ____________________________________________________________________")
        input("\n Press 'Enter' key to exit")

    def least_cost_method(self, need_only_cost=False):

        units = [self.units].copy()[0]
        destinations = [self.destinations].copy()[0]
        supply = self.supply.copy()
        demand = self.demand.copy()
        data = copy.deepcopy(self.data)
        balanced = True

        # Balancing the Equation
        if sum(demand) > sum(supply):
            data.append([0.0 for _ in range(len(demand))])
            supply.append(sum(demand) - sum(supply))
            units += 1
            balanced = False
        elif sum(demand) < sum(supply):
            for rows in data:
                rows.append(0)
            demand.append(sum(supply) - sum(demand))
            destinations += 1
            balanced = False

        # Creating Dictionaries & Variables
        allocation = {f"({i + 1},{j + 1})": None for i in range(units) for j in range(destinations)}
        cost = {f"({i + 1},{j + 1})": data[i][j] for i in range(units) for j in range(destinations)}
        transportation_cost = 0

        # Algorithm for Least Cost Method (Balanced)
        while not sum(demand) == sum(supply) == 0:

            minimum_values = []
            no_of_min_value = 0
            index = []

            for i in data:
                minimum = -1
                maximum = max(i)
                if -1 in i:
                    for _ in i:
                        if -1 < _ <= maximum:
                            if minimum == -1:
                                minimum = _
                            elif _ < minimum:
                                minimum = _
                    if minimum != -1:
                        minimum_values.append(minimum)
                else:
                    minimum_values.append(min(i))
            for i in data:
                no_of_min_value += i.count(min(minimum_values))

            if no_of_min_value == 1:

                for i in data:
                    if min(minimum_values) in i:
                        index.append(data.index(i))
                        index.append(i.index(min(minimum_values)))
                D = index[1]
                S = index[0]

                if demand[D] > supply[S]:
                    key = f"({S + 1},{D + 1})"
                    allocation[key] = supply[S]
                    demand[D] -= supply[S]
                    supply[S] = 0
                    for _ in range(len(data[S])):
                        data[S][_] = -1

                elif demand[D] < supply[S]:
                    key = f"({S + 1},{D + 1})"
                    allocation[key] = demand[D]
                    supply[S] -= demand[D]
                    demand[D] = 0
                    for _ in data:
                        _[D] = -1

                else:
                    key = f"({S + 1},{D + 1})"
                    allocation[key] = demand[D]
                    demand[D] = 0
                    supply[S] = 0
                    for _ in data:
                        _[D] = -1
                    for _ in range(len(data[S])):
                        data[S][_] = -1
            else:
                least_value = -1
                d_variable = 0
                s_variable = 0

                # Picking up all the indexes
                m = n = 0
                for i in data:
                    for j in i:
                        values = []
                        if j == min(minimum_values):
                            values.append(m)
                            values.append(n)
                            index.append(values)
                        n += 1
                    m += 1
                    n = 0

                # Comparing the lowest
                for i in index:
                    S = i[0]
                    D = i[1]

                    if demand[D] > supply[S]:
                        if least_value == -1:
                            least_value = supply[S]
                            d_variable = D
                            s_variable = S
                        elif supply[S] < least_value:
                            least_value = supply[S]
                            d_variable = D
                            s_variable = S
                    elif demand[D] < supply[S]:
                        if least_value == -1:
                            least_value = demand[D]
                            d_variable = D
                            s_variable = S
                        elif supply[S] < least_value:
                            least_value = demand[D]
                            d_variable = D
                            s_variable = S
                    else:
                        if least_value == -1:
                            least_value = demand[D]
                            d_variable = D
                            s_variable = S
                        elif supply[S] < least_value:
                            least_value = demand[D]
                            d_variable = D
                            s_variable = S

                # Algorithm starts
                D = d_variable  # index[1]
                S = s_variable  # index[0]
                if demand[D] > supply[S]:
                    key = f"({S + 1},{D + 1})"
                    allocation[key] = supply[S]
                    demand[D] -= supply[S]
                    supply[S] = 0
                    for _ in range(len(data[S])):
                        data[S][_] = -1
                elif demand[D] < supply[S]:
                    key = f"({S + 1},{D + 1})"
                    allocation[key] = demand[D]
                    supply[S] -= demand[D]
                    demand[D] = 0
                    for _ in data:
                        _[D] = -1
                else:
                    key = f"({S + 1},{D + 1})"
                    allocation[key] = demand[D]
                    demand[D] = 0
                    supply[S] = 0
                    for _ in data:
                        _[D] = -1
                    for _ in range(len(data[S])):
                        data[S][_] = -1

        for key in allocation:
            if allocation[key] is not None:
                transportation_cost += allocation[key] * cost[key]

        if need_only_cost:
            return transportation_cost

        os.system('cls')
        print(LINE)
        print("\t OPERATION RESEARCH METHOD • TRANSPORTATION PROBLEM\n")
        print(f"  • TRANSPORTATION COST • IBFS")

        print("\n\t\t\t  LEAST COST METHOD")
        print(" ____________________________________________________________________")

        # Balanced or Not
        if balanced:
            print(f"\n  ΣA(i) = ΣB(j)\n"
                  f"  The Given Transportation problem is BALANCED!")
        else:
            print(f"\n  ΣA(i) != ΣB(j)"
                  f"\n  The Given Transportation problem is UN-BALANCED!"
                  f"\n  Total Demand: {sum(self.demand)}"
                  f"\n  Total Supply: {sum(self.supply)}")

        print("\n  BY Least-Cost-Method ↓\n  Allocations in:")
        no_of_allocation = 0
        for key in allocation:
            if allocation[key] is not None:
                no_of_allocation += 1
                print(f"  cell{key} = {allocation[key]}")

        if no_of_allocation == (len(demand) + len(supply) - 1):
            print("\n  It is Non-Degenerative Basic Feasible Solution")
        else:
            print("\n  It is Degenerative Basic Feasible Solution.")  # Epsilon (ε) in Cell(,)
        print(f"  Total Transportation Cost : Rs. {transportation_cost}/-")

        print(" ____________________________________________________________________")
        input("\n Press 'Enter' key to exit")

    def vogel_approximation_method(self, need_only_cost=False):

        # Copying all variables
        units = [self.units].copy()[0]
        destinations = [self.destinations].copy()[0]
        my_supply = self.supply.copy()
        my_demand = self.demand.copy()
        data = copy.deepcopy(self.data)
        balanced = True

        # Balancing the Equation
        if sum(my_demand) > sum(my_supply):
            data.append([0.0 for _ in range(len(my_demand))])
            my_supply.append(sum(my_demand) - sum(my_supply))
            units += 1
            balanced = False
        elif sum(my_demand) < sum(my_supply):
            for rows in data:
                rows.append(0)
            my_demand.append(sum(my_supply) - sum(my_demand))
            destinations += 1
            balanced = False

        check_degeneracy = len(my_demand) + len(my_supply) - 1

        # Creating Operation Variables in particular format
        allocations = []
        demand = {}
        supply = {}
        costs = {}

        # for Costs
        number1 = 1
        number2 = 1
        for row in data:
            sample_dict = {}
            for value in row:
                sample_dict[f"{number2})"] = value
                number2 += 1
            costs[f"({number1},"] = sample_dict
            number2 = 1
            number1 += 1


        # for Demand
        number = 1
        for value in my_demand:
            demand[f"{number})"] = value
            number += 1
        cols = sorted(demand.keys())

        # for Supply
        number = 1
        for value in my_supply:
            supply[f"({number},"] = value
            number += 1
        res = dict((k, defaultdict(float)) for k in costs)

        # Algorithm : Vogel's Approximation Method
        g = {}
        for x in supply:
            g[x] = sorted(costs[x].keys(), key=lambda g: costs[x][g])
        for x in demand:
            g[x] = sorted(costs.keys(), key=lambda g: costs[g][x])

        while g:
            sample = []
            d = {}
            for x in demand:
                d[x] = (costs[g[x][1]][x] - costs[g[x][0]][x]) if len(g[x]) > 1 else costs[g[x][0]][x]
            s = {}
            for x in supply:
                s[x] = (costs[x][g[x][1]] - costs[x][g[x][0]]) if len(g[x]) > 1 else costs[x][g[x][0]]
            f = max(d, key=lambda n: d[n])
            t = max(s, key=lambda n: s[n])
            t, f = (f, g[f][0]) if d[f] > s[t] else (g[t][0], t)
            sample.append(f)
            sample.append(t)

            v = min(supply[f], demand[t])
            allocations.append(f"cell{''.join(sample)} = {v}")
            res[f][t] += v
            demand[t] -= v
            if demand[t] == 0:
                for k, n in supply.items():
                    if n != 0:
                        g[k].remove(t)
                del g[t]
                del demand[t]
            supply[f] -= v
            if supply[f] == 0:
                for k, n in demand.items():
                    if n != 0:
                        g[k].remove(f)
                del g[f]
                del supply[f]


        transportation_cost = 0
        for g in sorted(costs):
            for n in cols:
                y = res[g][n]
                transportation_cost += y * costs[g][n]

        if need_only_cost:
            return transportation_cost

        os.system('cls')
        print(LINE)
        print("\t OPERATION RESEARCH METHOD • TRANSPORTATION PROBLEM\n")
        print(f"  • TRANSPORTATION COST • IBFS")

        print("\n\t\t\t  VOGEL's APPROXIMATION METHOD")
        print(" ____________________________________________________________________")

        # Giving Info about Balanced (or) Not-Balanced
        if balanced:
            print(f"\n  ΣA(i) = ΣB(j)\n"
                  f"  The Given Transportation problem is BALANCED!")
        else:
            print(f"\n  ΣA(i) != ΣB(j)"
                  f"\n  Total Demand: {sum(self.demand)}"
                  f"\n  Total Supply: {sum(self.supply)}"
                  f"\n  The Given Transportation problem is UN-BALANCED!")

        print("\n  BY Vogel's Approximation Method ↓\n  Allocations in:")
        allocations = sorted(allocations)
        no_of_allocations = 0
        for _ in allocations:
            no_of_allocations += 1
            print(f"  {_}")

        if no_of_allocations == check_degeneracy:
            print("\n  It is Non-Degenerative Basic Feasible Solution")
        else:
            print("\n  It is Degenerative Basic Feasible Solution.")  # Epsilon (ε) in Cell(,)
        print(f"  Total Transportation Cost : Rs. {transportation_cost}/-")

        print(" ____________________________________________________________________")
        input("\n Press 'Enter' key to exit")

    def maximum_profits(self):
        give_space()

        os.system('cls')
        print(LINE)
        print("\t OPERATION RESEARCH METHOD • TRANSPORTATION PROBLEM\n")
        print(f"  • TRANSPORTATION COST • IBFS")

        print("\n\tMaximum profit [Assuming minimization table]")
        print(" ____________________________________________________________________\n")

        with open("transportation_problems_data.json", mode="r") as f:
            all_data = json.load(f)
        current_problem = all_data[f"Problem-{self.problem_no}"]
        self.data = current_problem["costs"]

        max_values = [max(i) for i in self.data]
        max_value = max(max_values)

        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                self.data[i][j] = max_value - self.data[i][j]

        print(f"  1. By North-West Corner Rule: Rs {self.north_west_corner_rule(need_only_cost=True)}/-")

        with open("transportation_problems_data.json", mode="r") as f:
            all_data = json.load(f)
        current_problem = all_data[f"Problem-{self.problem_no}"]
        self.data = current_problem["costs"]

        max_values = [max(i) for i in self.data]
        max_value = max(max_values)

        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                self.data[i][j] = max_value - self.data[i][j]

        print(f"  2. By Least Cost Method: Rs {self.least_cost_method(need_only_cost=True)}/-")

        with open("transportation_problems_data.json", mode="r") as f:
            all_data = json.load(f)
        current_problem = all_data[f"Problem-{self.problem_no}"]
        self.data = current_problem["costs"]

        max_values = [max(i) for i in self.data]
        max_value = max(max_values)

        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                self.data[i][j] = max_value - self.data[i][j]

        print(f"  3. By Vogel's Approximation Method: Rs {self.vogel_approximation_method(need_only_cost=True)}/-")
        print(" ____________________________________________________________________")
        input("\n Press 'Enter' key to exit")

while True:
    os.system('cls')
    print(LINE)
    method = input(f"\t\t\t OPERATION RESEARCH METHODS\n"
                   f"\n  1. Assignment Problem."
                   f"\n  2. Transportation Problem\n"
                   f"\n  Choose the Method (1|2): ").lower()
    if method == "exit":
        break

    if method == "1":
        os.system('cls')
        print(LINE)
        print("\t OPERATION RESEARCH METHOD • ASSIGNMENT PROBLEM")

        answer = AssignmentMethods()
    elif method == "2":
        os.system('cls')
        print(LINE)
        print("\t OPERATION RESEARCH METHOD • TRANSPORTATION PROBLEM")

        answer = TransportationMethods()

