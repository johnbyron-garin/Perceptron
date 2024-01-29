def read_puzzle(input_filename):
    input_filename = f"{input_filename}.txt"
    perceptron_values = []
    try:
        with open(input_filename, "r") as file:
            lines = file.readlines()  # Read all lines into a list
            learning_rate = float(lines[0].strip())  # First line as learning_rate
            threshold = float(lines[1].strip())    # Second line as threshold
            bias = float(lines[2].strip())          # Third line as bias
            for line in lines[3:]:
                row = [int(x) for x in line.strip().split()]
                perceptron_values.append(row)
    except FileNotFoundError:
        print("File 'sample.txt' not found!")
        
    return perceptron_values, learning_rate, threshold, bias

def initialize_perceptron_dictionary(bias, perceptron_values):
    length_perceptron_values = len(perceptron_values)
    i = 0
    perceptron_dictionary = {
        "b": [],
        "a": [],
        "y": []
    }
    bias_array = []
    while(i<length_perceptron_values):
        bias_array.append(bias)
        i += 1
    perceptron_dictionary["b"] = bias_array
    return perceptron_dictionary

def initialize_x0_x1_z(perceptron_dictionary, perceptron_values):
    length_i = len(perceptron_values)
    length_j = len(perceptron_values[0])

    for j in range(length_j - 1):
        column_values = [row[j] for row in perceptron_values]
        dict_key_string = f'x{j}'
        perceptron_dictionary[dict_key_string] = column_values

    z_values = [row[length_j - 1] for row in perceptron_values]
    perceptron_dictionary['z'] = z_values

def initialize_initial_weights_zero(perceptron_dictionary):
    length_j = len(perceptron_values[0])
    wb = [0]
    
    for j in range(length_j - 1):
        dict_key_string = f'w{j}'
        perceptron_dictionary[dict_key_string] = []
        perceptron_dictionary[dict_key_string].append(0)
    
    perceptron_dictionary['wb'] = wb

def initialize_initial_weights_w_values(perceptron_dictionary, final_w_values):
    for j in range(len(final_w_values) - 1):
        dict_key_string = f'w{j}'
        perceptron_dictionary[dict_key_string] = []
        perceptron_dictionary[dict_key_string].append(final_w_values[j])
    perceptron_dictionary['wb'] = []
    perceptron_dictionary['wb'].append(final_w_values[len(final_w_values)-1])

def formatting_labels(length_j):
    string_label_array = []
    x_variable_array = []
    w_variable_array = []
    a = "a"
    y = "y"
    z = "z"
    for i in range(length_j):
        if (i != length_j-1):
            x_label = f"x{i}"
            w_label = f"w{i}"
            x_variable_array.append(x_label)
            w_variable_array.append(w_label)
        else:
            w_label = "wb"
            w_variable_array.append(w_label)
    
    x_variable_array.append("b")
    w_variable_array.append("a")
    w_variable_array.append("y")
    w_variable_array.append("z")
    string_label_array = x_variable_array + w_variable_array
    return string_label_array

def formatting_output(perceptron_dictionary, string_label_array, table_number_counter, input_filename):
    output_filename = f"{input_filename}-output.txt"
    with open(output_filename, 'a') as output_file:  # Open the file in append mode
        output_file.write("Iteration " + str(table_number_counter) + ":\n")
        
        # Calculate the fixed width for each column (e.g., 10 characters)
        column_width = 10
        
        # Write labels with fixed width separation
        for label in string_label_array:
            output_file.write(label.ljust(column_width))
        output_file.write("\n")  # Start a new line for values

        i = 0
        while i < len(perceptron_dictionary["b"]):
            for label in string_label_array:
                value = perceptron_dictionary[label][i]
                value = round(value, 1)
                formatted_value = f"{value:.1f}".ljust(column_width)
                output_file.write(formatted_value)

            i += 1
            output_file.write("\n")  # Start a new line for the next row
        output_file.write("\n")  # Add an indent by writing an extra newline

def infinite_loop(input_filename):
    output_filename = f"{input_filename}-output.txt"
    with open(output_filename, 'w') as output_file:
        output_file.write("not converging")


######################       THIS IS WHERE THE CODE STARTS       #########################
input_filename = "triple"
output_filename = f"{input_filename}-output.txt"
with open(output_filename, 'w') as output_file:
    pass

perceptron_values, learning_rate, threshold, bias = read_puzzle(input_filename)
length_i = len(perceptron_values) # number of rows
length_j = len(perceptron_values[0]) # number of weight values that must be computed
done_switch = False
table_number_counter = 1
final_w_values = []

while (done_switch == False):
    # catches the infinite loop
    if (table_number_counter != 10000):
        # initializes
        perceptron_dictionary = initialize_perceptron_dictionary(bias, perceptron_values)
        initialize_x0_x1_z(perceptron_dictionary, perceptron_values)

        if (table_number_counter == 1):
            initialize_initial_weights_zero(perceptron_dictionary) # initializes the weights value into zero when it is the first table
        else:
            initialize_initial_weights_w_values(perceptron_dictionary, final_w_values) # otherwise, uses the final_w_values of the previous table iteration

        table_row_iteration_counter = 0
        for i in range(length_i):
            # computes the summation value of a
            a_summation = 0
            y = 0
            for j in range(length_j-1):
                a = (perceptron_dictionary[f'x{j}'][i]) * (perceptron_dictionary[f'w{j}'][i])
                a_summation += a

            a = (perceptron_dictionary['b'][i]) * (perceptron_dictionary[f'wb'][i])
            a_summation += a
            perceptron_dictionary['a'].append(a_summation) # store the a summation to the dictionary
            
            # computes the value of y
            if(a_summation > threshold):
                y = 1
            else:
                y = 0
                
            perceptron_dictionary['y'].append(y) # store the y value to the dictionary

            # computes for the w values which will be stored initially to an array
            w_array = []
            for j in range(length_j-1):
                w = perceptron_dictionary[f'w{j}'][i] + (learning_rate * perceptron_dictionary[f'x{j}'][i] * (perceptron_dictionary['z'][i] - perceptron_dictionary['y'][i]))
                w_array.append(w)
                
            w = perceptron_dictionary['wb'][i] + (learning_rate * (perceptron_dictionary['b'][i]) * (perceptron_dictionary['z'][i] - perceptron_dictionary['y'][i]))
            w_array.append(w)

            # checks if last batch na ng w values yung kukunin, pag last batch na hindi na sya i-aappend sa array sa loob ng dict
            final_w_values = []
            if (table_row_iteration_counter != length_i-1):
                w_counter = 0
                # distributes the computed w values from the w_array to their appropriate arrays that the dict keys hold
                for w in w_array:
                    if (w_counter != length_j-1):
                        perceptron_dictionary[f'w{w_counter}'].append(w)
                    else:
                        perceptron_dictionary['wb'].append(w)
                    w_counter += 1
            # last batch ng w values (w_b) na store sa final_w_values
            else:
                w_counter = 0
                for w in w_array:
                    final_w_values.append(w)
                    w_counter += 1

            table_row_iteration_counter += 1

        # if the rows from index 1 to rowlength-1 is already the same, final_array will be appended one element for each w_i array 
        # final_array is needed because it will compared final_w_values (the array that contains the w values outside the dictionary)
        final_array = [] 
        for i in range(length_j-1):
            arr = perceptron_dictionary[f'w{i}']
            first_element = arr[0]
            for element in arr:
                if element != first_element:
                    done_switch = False
                else:
                    done_switch = True
        if (done_switch == True):
            for i in range(length_j-1):
                arr = perceptron_dictionary[f'w{i}']
                final_array.append(arr[1])
            final_array.append(perceptron_dictionary['wb'][1])
            if (final_w_values == final_array):
                done_switch = True
            else:
                done_switch = False

        string_label_array = formatting_labels(length_j)
        formatting_output(perceptron_dictionary, string_label_array, table_number_counter, input_filename)
        table_number_counter += 1
    else:
        infinite_loop(input_filename)
        break