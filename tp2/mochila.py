# -*- encoding: utf-8 -*-
import argparse


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

def exhaustivo(items):
    knapsack = []
    best_volume = 0
    best_value = 0
    iteration = 0
    for item_combination in superset(items):
        iteration += 1
        print 'iteration number: %d' % (iteration)

        current_volume = sum([e[1] for e in item_combination])
        current_value = sum([e[2] for e in item_combination])
        if current_value > best_value and current_volume <= v:
            best_value, best_volume = current_value, current_volume
            knapsack = item_combination

    print 'best value: %d' % (best_value), '\nbest volume: %d' % (best_volume)
    for i in knapsack:
        print 'id: %d   volume: %d      value: %d' % (i[0], i[1], i[2])

def greedy(items):
    pass


def main():
    ''' Problema de la mochila: maximizar valor de mochila con restricción de volumen con determinados elementos dados
    '''
    parser = argparse.ArgumentParser(description='Resuelve el problema de la mochila')
    parser.add_argument('--solution', '-s', dest='solution', action='store', required=True, help='Tipo de solucion a utilizar: exhaustivo o greedy')
    args = parser.parse_args()

    # SET MAX CAPACITY OF THE KNAPSACK
    v = 4200
    # SET NUMBER OF ELEMENTS
    n = 10
    # SET LIST OF VOLUMES AND VALUES
    volumes = [150, 325, 600, 805, 430, 1200, 770, 60, 930, 353]
    values = [20, 40, 50, 36, 25, 64, 54, 18, 46, 28]

    # SET LIST OF ITEMS
    items = build_items(n, volumes, values)
    print superset(items)

    # GET BEST VALUES
    if args.solution == 'exhaustivo':
        exhaustivo(items)
    elif args.solution == 'greedy':
        pass
        #greedy(items)
    else:
        print('unknown kind of solution')

if __name__ == '__main__':
    main()