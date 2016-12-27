import os

def clear_cache(d):
    for item in os.listdir(d):
        absfile = os.path.join(d, item)
        if item.endswith('.pyc'):
            os.remove(absfile)
            print('rm file %s' % absfile)
        elif item == '__pycache__':
            os.system('sudo rm -rf %s' % (absfile,))
            print('rm dir  %s' % absfile)
        elif os.path.isdir(absfile):
            clear_cache(absfile)




clear_cache(os.path.abspath('.'))
