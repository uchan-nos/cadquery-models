'''
Copyright (c) 2024 Kota UCHIDA

GW1N-QN48: GW1N series FPGA, QFN48 package (Gowin)
'''

from lib import ic

def new():
    return ic.new_qfn(48, 6, 0.4, mark1='white')

def main():
    show_object(new())

if __name__ == '__cq_main__':
    main()
