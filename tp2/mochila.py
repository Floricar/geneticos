# -*- encoding: utf-8 -*-
import time
START_TIME = time.time()
import argparse

# AUXILIAR FUNCTIONS BEGIN -------------------------------------------
def build_items(n, volumes, values):
    items = []
    for i in range(0, n):
        # item = [(#id, #volume, #value)]
        items.append((i + 1, volumes[i], values[i]))
    return items

def superset(items):
    result = [[]]
    for item in items:
        newset = [r+[item] for r in result]
        result.extend(newset)
    return result

def ordenar_desc(array1, array2):
    # array1 = fobj; array2 = pob
    length = len(array1) - 1
    sorted = False

    while not sorted:
        sorted = True
        for i in range(length):
            if array1[i] < array1[i + 1]:
                sorted = False
                array1[i], array1[i + 1] = array1[i + 1], array1[i]
                array2[i], array2[i + 1] = array2[i + 1], array2[i]

    return array1, array2
# AUXILIAR FUNCTIONS END ----------------------------------------------


def exhaustivo(items, v):
    knapsack = []
    best_volume = 0
    best_value = 0
    iteration = 0
    for item_combination in superset(items):
        iteration += 1
        #print 'iteration number: %d' % (iteration)

        current_volume = sum([e[1] for e in item_combination])
        current_value = sum([e[2] for e in item_combination])
        if current_value > best_value and current_volume <= v:
            best_value, best_volume = current_value, current_volume
            knapsack = item_combination

    print 'best value: %d' % (best_value), '\nbest volume: %d' % (best_volume)
    for i in knapsack:
        print 'id: %d   volume: %d      value: %d' % (i[0], i[1], i[2])
    print 'Execution time: %s' % (time.time() - START_TIME)

def greedy(items, v):
    gain_ratios = []
    for item in items:
        gain_ratio = float(item[2])/float(item[1])
        gain_ratios.append(gain_ratio)

    gain_ratios, items = ordenar_desc(gain_ratios, items)
    knapsack = []
    best_value = 0
    best_volume = 0
    for item in items:
        if best_volume + item[1] <= v:
            best_value += item[2]
            best_volume += item[1]
            knapsack.append(item)
        else:
            break

    print 'best value: %d' % (best_value), '\nbest volume: %d' % (best_volume)
    for i in knapsack:
        print 'id: %d   volume: %d      value: %d' % (i[0], i[1], i[2])
    print 'Execution time: %s' % (time.time() - START_TIME)

def main():
    ''' Problema de la mochila: maximizar valor de mochila con restricción de volumen con determinados elementos dados
    '''
    parser = argparse.ArgumentParser(description='Resuelve el problema de la mochila')
    parser.add_argument('--solution', '-s', dest='solution', action='store', required=True, help='Tipo de solucion a utilizar: exhaustivo o greedy')
    args = parser.parse_args()

    # SET MAX CAPACITY OF THE KNAPSACK
    v = 4200
    #v = 3000
    # SET NUMBER OF ELEMENTS
    n = 10
    #n = 3
    # SET LIST OF VOLUMES AND VALUES
    volumes = [150, 325, 600, 805, 430, 1200, 770, 60, 930, 353]
    #volumes = [1800, 600, 1200]
    values = [20, 40, 50, 36, 25, 64, 54, 18, 46, 28]
    #values = [72, 36, 60]

    # SET LIST OF ITEMS
    items = build_items(n, volumes, values)

    # GET BEST VALUES
    if args.solution == 'exhaustivo':
        exhaustivo(items, v)
    elif args.solution == 'greedy':
        greedy(items, v)
    else:
        print('unknown kind of solution')

if __name__ == '__main__':
    main()