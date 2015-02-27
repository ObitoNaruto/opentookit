#!/usr/bin/env python

import sys

MARGIN = ' '


class TLV:
    def __init__(self, tag, tag_len, tag_len_tag):
        self.tag = tag
        self.tag_len = tag_len
        self.tag_len_tag = tag_len_tag
        self.primitive = True

    @staticmethod
    def hex_single(num):
        s = hex(num).upper()[2:]
        if len(s) % 2 != 0:
            return '0' + s
        return s


    @staticmethod
    def hex_str(num):
        if not num:
            return 'None'
        if type(num) == list:
            return ''.join(map(lambda x: TLV.hex_single(x), num))
        else:
            return TLV.hex_single(num)

    def __str__(self):
        return '[tag: ' + TLV.hex_str(self.tag) \
               + ', len: ' + TLV.hex_str(self.tag_len_tag) \
               + ', primitive: ' + str(self.primitive) \
               + ']'

    def __repr__(self):
        return self.__str__()


def __print_tlv_value(tlv, output, margin, indent):
    output.write(TLV.hex_str(tlv.tag))
    output.write(' ')
    output.write(TLV.hex_str(tlv.tag_len_tag))
    output.write('\n')

    if tlv.primitive:
        output.write(margin)
        output.write(TLV.hex_str(tlv.value))
        output.write('\n')
    else:
        for item in tlv.value:
            output.write(margin)
            __print_tlv_value(item, output, margin + indent, margin)


def print_gracefully(tlv, output):
    __print_tlv_value(tlv, output, MARGIN, MARGIN)


def get_tlv_length(number, start):
    l = number[start]
    if l == 0x80:
        raise Exception("find infinite tag length")
    if l & 0x80 == 0x80:
        # long form length
        len_byte_num = l & 0x7F
        l = 0
        for x in range(len_byte_num):
            l <<= 8
            l += number[start + 1 + x]
        return l, len_byte_num + 1, number[start:start + len_byte_num + 1]
    else:
        return l, 1, number[start:start+1]


def parse_tlv_value(number_list):
    tlv_list = list()
    last = 0
    while last < len(number_list):
        t = number_list[last]
        head_len = 1
        if t & 0x1F == 0x1F:
            # two-byte length tag
            head_len = 2
        len_tuple = get_tlv_length(number_list, last + head_len)
        l = len_tuple[0]
        head_len += len_tuple[1]
        tlv_list.append(parse_tlv(number_list[last:last + l + head_len]))
        last += l + head_len
    return tlv_list


def parse_tlv(number_list):
    flag = t = number_list[0]
    head_len = 1
    if t & 0x1F == 0x1F:
        t <<= 8
        t += number_list[1]
        head_len = 2

    len_tuple = get_tlv_length(number_list, head_len)
    l = len_tuple[0]
    head_len += len_tuple[1]

    tlv = TLV(t, l, len_tuple[2])
    if flag & 0x20 != 0:
        # constructed tag
        tlv.primitive = False
        tlv.value = parse_tlv_value(number_list[head_len:])
    else:
        tlv.primitive = True
        tlv.value = number_list[head_len:]

    return tlv


def hex_to_dec(hex_num):
    if 'a' <= hex_num <= 'f':
        return ord(hex_num) - ord('a') + 10
    if 'A' <= hex_num <= 'F':
        return ord(hex_num) - ord('A') + 10
    if '0' <= hex_num <= '9':
        return ord(hex_num) - ord('0')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "usage: %s <string to format>" % sys.argv[0]
        sys.exit(2)
    else:
        s = sys.argv[1]
        number_str_list = list()
        for x in s:
            if 'a' <= x <= 'f' or 'A' <= x <= 'F' or '0' <= x <= '9':
                number_str_list.append(x)

        print 'number: %s' % ''.join(number_str_list)

        number_list = list()
        for i in xrange(0, len(number_str_list), 2):
            x = hex_to_dec(number_str_list[i]) << 4
            x += hex_to_dec(number_str_list[i + 1])
            number_list.append(x)
        tlv = parse_tlv(number_list)
        print 'tlv: %s' % str(tlv)
        print '======= TLV BEGIN ======='
        print_gracefully(tlv, sys.stdout)
        print '======= TLV  END ========'
