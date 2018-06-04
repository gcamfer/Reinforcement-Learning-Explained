
#---- TESTING CODE for simple 4x4 Gridworld with goal states in upper/left and lower/right corner ----
next_state = {}
next_state[(0, "l")] = 0
next_state[(0, "u")] = 0
next_state[(0, "r")] = 0
next_state[(0, "d")] = 0

next_state[(1, "l")] = 0
next_state[(1, "u")] = 1
next_state[(1, "r")] = 2
next_state[(1, "d")] = 5

next_state[(2, "l")] = 1
next_state[(2, "u")] = 2
next_state[(2, "r")] = 3
next_state[(2, "d")] = 6

next_state[(3, "l")] = 2
next_state[(3, "u")] = 3
next_state[(3, "r")] = 3
next_state[(3, "d")] = 7

next_state[(4, "l")] = 4
next_state[(4, "u")] = 0
next_state[(4, "r")] = 5
next_state[(4, "d")] = 8

next_state[(5, "l")] = 4
next_state[(5, "u")] = 1
next_state[(5, "r")] = 6
next_state[(5, "d")] = 9

next_state[(6, "l")] = 5
next_state[(6, "u")] = 2
next_state[(6, "r")] = 7
next_state[(6, "d")] = 10

next_state[(7, "l")] = 6
next_state[(7, "u")] = 3
next_state[(7, "r")] = 7
next_state[(7, "d")] = 11

next_state[(8, "l")] = 8
next_state[(8, "u")] = 4
next_state[(8, "r")] = 9
next_state[(8, "d")] = 12

next_state[(9, "l")] = 8
next_state[(9, "u")] = 5
next_state[(9, "r")] = 10
next_state[(9, "d")] = 13

next_state[(10, "l")] = 9
next_state[(10, "u")] = 6
next_state[(10, "r")] = 11
next_state[(10, "d")] = 14

next_state[(11, "l")] = 10
next_state[(11, "u")] = 7
next_state[(11, "r")] = 11
next_state[(11, "d")] = 0

next_state[(12, "l")] = 12
next_state[(12, "u")] = 8
next_state[(12, "r")] = 13
next_state[(12, "d")] = 12

next_state[(13, "l")] = 12
next_state[(13, "u")] = 9
next_state[(13, "r")] = 14
next_state[(13, "d")] = 13

next_state[(14, "l")] = 13
next_state[(14, "u")] = 10
next_state[(14, "r")] = 0
next_state[(14, "d")] = 14

def get_available_actions(state):
    actions = ['l', 'u', 'r', 'd']
    return actions

def get_equiprobable_policy_actions(state):
    tuples = [('l', .25), ('u', .25), ('r', .25), ('d', .25)]
    return tuples

def get_transitions(state, action):
    next_state_num = next_state[(state, action)]
    reward = 0 if state == 0 else -1
    prob = 1
    tuple = (next_state_num, reward, prob)
    return [tuple]

def error(msg):
    print("ERROR: " + msg)

def passed(msg):
    print("passed test: " + msg)

def find_rounded_diffs(v, vexpect):
    diffs = 0
    first_diff_index = -1
    for i in range(len(vexpect)):
        diff = abs(round(vexpect[i]) - round(v[i]))

        if diff > 0:       
            #print("DIFF=", diff, ", i=", i, ", vexpect[i]=", vexpect[i], ", v[i]=", v[i])
            if (first_diff_index == -1):
                first_diff_index = i
            diffs += 1

    return (diffs, first_diff_index)

def find_exact_diffs(v, vexpect):
    diff_count = 0
    first_diff_index = -1
    for i in range(len(vexpect)):
        ve = vexpect[i]
        val = v[i]

        if isinstance(ve, tuple):
            diff = (not (val in ve))
        else:
            diff = (val != ve)

        if diff:      
            #print("DIFF=", diff, ", i=", i, ", vexpect[i]=", ve, ", v[i]=", val)
            if (first_diff_index == -1):
                first_diff_index = i
            diff_count += 1

    return (diff_count, first_diff_index)

def policy_eval_core_test(eval_func, variant):
    print()
    print("Testing: Policy Evaluation (" + variant + ")")

    vexpect = [0, -14, -20, -22, -14, -18, -20, -20, -20, -20, -18, -14, -22, -20, -14]
    
    state_count = len(vexpect)
    actions=['l', 'r', 'u', 'd']
    gamma = 1
    theta=.0001

    v = eval_func(state_count, gamma, theta, get_equiprobable_policy_actions, get_transitions)

    # 1. check type of result
    if (not isinstance(v, list)):
        error("return value is not a list")
        return
    passed("return value is list")
    
    # 2. check length of list
    if (len(v) != len(vexpect)):
        error("length of  list is neq " + str(len(vexpect)))
        return
    passed("length of list = " + str(len(vexpect)))
    
    # 3. check value of elements (compared to 2 decimal places)
    diffs, first_diff_index = find_rounded_diffs(v, vexpect)

    if diffs > 0:
        error("list elements don't match expected values: # of mismatches=" + str(diffs))
        return
    passed("values of list elements")

    # 4. generate a pass code from fractional part of values
    pass_code = str(abs(int(10000000*(v[5] - int(v[5])))))
    pass_code = pass_code[:4] + "-" + pass_code[4:]
    print("PASSED: Policy Evaluation (" + variant + ") passcode = " + pass_code)

def policy_eval_two_arrays_test(eval_func):
    return policy_eval_core_test(eval_func, "two-arrays")

def policy_eval_in_place_test(eval_func):
    return policy_eval_core_test(eval_func, "in-place")

def policy_iteration_core_test(eval_func, name, passcode_index):
    print()
    print("Testing: " + name)

    vexpect =  [0, -1, -2, -3, -1, -2, -3, -2, -2, -3, -2, -1, -3, -2, -1]

    # piexpect is the optimal policy for our Gridworld (tuples represnt ties / equal actions)
    piexpect = [
        ('l', 'u', 'r','d'), 'l', 'l', ('l', 'd'),     # first row (states 0-3)
        'u', ('l', 'u'), ('l', 'u', 'r', 'd'), 'd',    # second row (states 4-7)
        'u', ('l', 'u', 'r', 'd'), ('d', 'r'), 'd',    # third row (states 8-11)
        ('u', 'r'), 'r', 'r']                          # forth row (states 12-14)

    state_count = len(vexpect)
    actions=['l', 'r', 'u', 'd']
    gamma = .999
    theta=.0001

    result = eval_func(state_count, gamma, theta, get_available_actions, get_transitions)

    # 1. check type of result
    if (not isinstance(result, tuple)):
        error("return value is not a tuple")
        return
    passed("return value is tuple")
    
    # 2. check len of result
    if (len(result) != 2):
        error("length of tuple is neq 2")
        return
    passed("length of tuple = 2")

    # split results into variables
    v, pi = result

    # 3. check type/length of v
    if (not isinstance(v, list)) or (len(v) != state_count):
        error("v is not a list of length=" + str(state_count))
        return
    passed("v is list of length=" + str(state_count))

    #riv = [round(iv) for iv in v]
    #print("riv=", riv)

    # 4. check value of elements of v
    diffs, first_diff_index = find_rounded_diffs(v, vexpect)

    if diffs > 0:
        error("v elements don't match expected values: # of mismatches=" + str(diffs))
        return
    passed("values of v elements")

    # 5. check type/length of pi
    if (not isinstance(pi, list)) or (len(pi) != state_count):
        error("pi is not a list of length=" + str(state_count))
        return
    passed("pi is list of length=" + str(state_count))
    
    #print("pi=", pi)

    # 6. check value of elements of pi
    diffs, first_diff_index = find_exact_diffs(pi, piexpect)

    if diffs > 0:
        error("pi elements don't match expected values: # of mismatches=" + str(diffs))
        return
    passed("values of pi elements")

    # 7. generate a pass code from fractional part of values
    pass_value = v[passcode_index]
    pass_code = str(abs(int(10000000*(pass_value - int(pass_value)))))
    pass_code = pass_code[:4] + "-" + pass_code[4:]
    print("PASSED: " + name + " passcode = " + pass_code)
    
def policy_iteration_test(eval_func):
    return policy_iteration_core_test(eval_func, "Policy Iteration", 3)

def value_iteration_test(eval_func):
    return policy_iteration_core_test(eval_func, "Value Iteration", 5)

