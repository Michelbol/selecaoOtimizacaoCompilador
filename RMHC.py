import random
import os

path_tf = "/home/michel/PycharmProjects/TrabalhoCompiladores1/tf"

executions = {}
options = ['add', 'remove', 'update']


def read_file():
    os.system("opt -debug-pass=Arguments -O3 -disable-output < /dev/null 2> arguments.txt")
    file = os.open("arguments.txt", os.O_RDWR | os.O_CREAT)
    command = os.read(file, 3369)
    command = str(command)
    command = command.replace('Pass Arguments:', '')
    command = command.replace('\\n', '')
    command = command.replace("'", "")
    command = command.replace('"', '')
    command = command.replace("  ", " ")
    command = command[1:]
    return command.split(' ')


def read_run_log_file():
    file = open(path_tf+"/run.log", 'r')
    file.readline()
    line = file.readline()
    return line.split("\t")[3].replace("     ", "")


def run_tf(arguments, is_comp=False):
    opt = 'OPT="'
    for option in range(0, len(arguments)):
        opt += arguments[option] + " "
    opt += '"'
    cmd = "cd " + path_tf + " && "
    if is_comp:
        cmd += "COMPILE=1 EXEC=0 "
    else:
        cmd += "COMPILE=0 EXEC=1 "
    cmd += opt + " ./run.sh"
    os.system(cmd)


def change_bench(i):
    file_bench = open(path_tf + "/benchs.sh", "r")
    bench = ''
    for line in file_bench:
        if 'benchs=(' not in line:
            bench += line
        else:
            bench += 'benchs=( "Alg' + str(i) + '")\n'

    file_bench = open(path_tf + "/benchs.sh", "w")
    file_bench.close()
    file2 = open(path_tf + "/benchs.sh", 'a+')
    file2.write(bench)
    file2.close()


def run_alg(arguments):
    execute = {'time': float("inf"), 'arguments': []}
    for x in range(0, 3):
        run_tf(arguments, True)
        run_tf(arguments)
        time = float(read_run_log_file())
        if time < execute['time']:
            execute = {'time': time, 'arguments': arguments.copy()}
    return execute


def main():
    file = open("times.txt", "w")
    file.close()
    arguments = read_file()
    fitness = {'time': float('inf'), 'arguments': arguments}
    for x in range(1, 100):
        action = options[random.randint(0, 2)]
        if action == 'add':
            fitness['arguments'] = add_argument(fitness['arguments'], arguments)
        elif action == 'remove':
            fitness['arguments'] = remove_argument(fitness['arguments'])
        else:
            fitness['arguments'] = update_argument(fitness['arguments'], arguments)
        execute = run_alg(fitness['arguments'])
        save_partial(execute)
        if execute['time'] < fitness['time']:
            os.system('cd '+path_tf+" && cp run.log fitness.log")
            fitness['time'] = execute['time']
            fitness['arguments'] = execute['arguments']
    save_results(fitness)


def add_argument(fitness_arguments, arguments):
    length_arg = len(arguments)-1
    fitness_arguments.append(arguments[random.randint(0, length_arg)])
    return fitness_arguments


def update_argument(fitness_arguments, arguments):
    length_arg = len(arguments) - 1
    length_fit = len(fitness_arguments) - 1
    random_arg = random.randint(0, length_arg)
    random_fit = random.randint(0, length_fit)
    fitness_arguments[random_fit] = arguments[random_arg]
    return fitness_arguments


def remove_argument(fitness_arguments):
    length = len(fitness_arguments)
    index_to_remove = random.randint(0, length-1)
    del (fitness_arguments[index_to_remove])
    return fitness_arguments


def save_results(fitness):
    file = open("result.txt", "w")
    file.close()
    file = open("result.txt", "a+")
    file.write(" Time:     " + str(fitness['time']) + " Arguments: " + str(fitness['arguments']))
    file.write("\n")
    file.close()


def save_partial(partial):
    file = open("times.txt", "a+")
    file.write(" Time:     " + str(partial['time']) + " Arguments: " + str(partial['arguments']))
    file.write("\n")
    file.close()


main()
