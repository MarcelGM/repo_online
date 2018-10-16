import sys
import os
import subprocess
import json
import itertools
import re

json_list = json.load(open('parameters_json_file.json', 'r'))

data = json_list["data"]
parameters = json_list["parameters"]
fixed_parameters = parameters["fixed"]
iterable_parameters = parameters["iterable"]
#print(iterable_parameters)
#print(log_values)

listofvalues=iterable_parameters.values()
args_list = []
for it_key in iterable_parameters:
    #print(it_key, "\t", iterable_parameters[it_key])
    args_list.append(it_key)
parameter_combinations = list(itertools.product(*listofvalues))
#print("\nNumber of combinations to try:", len(parameter_combinations))

class Command_string:
    def __init__(self, initial_string = "python"):
        self.string = initial_string
    
    def change(self, new_string):
        self.string = new_string
    
    def add_arg_str(self, string):
        self.string += " " + string
        
    def add_arg_dic(self, key, dic):
        self.string += " --" + key + " " + str(dic[key])
    
    def add_arg_val(self, key, val):
        self.string += " --" + key + " " + str(val)

fixed_command = Command_string()
fixed_command.add_arg_str(json_list["train.py"])
for path_key in data:
    fixed_command.add_arg_dic(path_key, data)
for fixed_par_key in fixed_parameters:
    fixed_command.add_arg_dic(fixed_par_key, fixed_parameters)
#print(fixed_command.string)

common_list = []
tmp_command = Command_string()
name = []
checkpoint_dirs = []

for comb in parameter_combinations:
    tmp_command.change(fixed_command.string)
    comb_num = parameter_combinations.index(comb)
    name.append("training_" + str(comb_num) + "_")
    for it_par_key in iterable_parameters:
        key_index = list(iterable_parameters.keys()).index(it_par_key)
        tmp_command.add_arg_val(it_par_key, comb[key_index])             # adds --parameterName parameterValue
        name[comb_num] += "__" + it_par_key + "_" + str(comb[key_index]) # adds __parameterName_parameterValue
    common_list.append(tmp_command.string)

test_command = Command_string()
test_list = []

rang = json_list["test_range"]
for training in range(rang[0],rang[1]+1):
    file_name = json_list["sorted_logs"] + "/" + "sorted_log_" + str(training) + ".table" #Change str(3) to str(training)
    #print(file_name)
    log_file = open(file_name, 'r')
    lines = log_file.readlines()#.replace('\n', '')
    log_values = []
    models = []
    for x in lines:
        log_values.append(re.split(r'\t+', x.rstrip('\t').rstrip('\n')))
        models.append(log_values[lines.index(x)][0])
    log_file.close()
    
    for top_num in range(0,json_list["N_best"]):
        test_command.change(common_list[training])
        test_command.add_arg_val("load_check_point", json_list["checkpoints"] + "/" + name[training] \
                                 + "/" + log_values[top_num][0])
        prediction_str = json_list["predictions"] + "/" + "training_" + str(training) + "__top_" + str(top_num + 1) + \
                         "__epoch_" + str(log_values[top_num][1]) + ".prediction"
        test_command.add_arg_val("test_to_file", prediction_str)
        test_list.append(test_command.string)

test_file = open(json_list["output_test"], 'w')
for line in test_list:
    test_file.write(line + "\n")
test_file.close()
