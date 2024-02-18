'''
Copyright (c) 2024 Kota UCHIDA

TSSOP-20 package
'''

from lib import ic

def main():
    obj = ic.new_tssop(20)
    show_object(obj)

if __name__ == '__cq_main__':
    main()
