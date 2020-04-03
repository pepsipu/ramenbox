def set_carry(cpu, res):
    if res > 0xff:
        cpu.sr |= 0x1
    else:
        cpu.sr &= 0xfe


def set_overflow(cpu, res, operands):
    if (~(operands[0] ^ operands[1])) & (operands[0] ^ res) & 0x80:
        cpu.sr |= 0x40
    else:
        cpu.sr &= 0xbf


def set_zero(cpu, res):
    if res == 0:
        cpu.sr |= 0x2
    else:
        cpu.sr &= 0xfd


def set_negative(cpu, res):
    if res < 0:
        cpu.sr |= 0x80
    else:
        cpu.sr &= 0x7f


def _adc(cpu, data):
    res = data + cpu.ac + (cpu.sr & 0x1)
    set_carry(cpu, res)
    set_zero(cpu, res)
    set_negative(cpu, res)
    set_overflow(cpu, res, (data, cpu.ac))
    cpu.ac = res & 0xff


def _and(cpu, data):
    res = cpu.ac & data
    set_zero(cpu, res)
    set_negative(cpu, res)
    cpu.ac = res


def _asl(cpu, data):
    if data == "ac":
        res = cpu.ac << 1
        cpu.ac = res & 0xff
    else:
        res = cpu.mem.read(data) << 1
        cpu.mem.write(data, res & 0xff)
    set_zero(cpu, res)
    set_negative(cpu, res)
    set_carry(cpu, res)


def _bcc(cpu, data):
    if not (cpu.sr & 0x1):
        cpu.pc = data


def _bcs(cpu, data):
    if cpu.sr & 0x1:
        cpu.pc = data


def _beq(cpu, data):
    if cpu.sr & 0x2:
        cpu.pc = data


def _bit(cpu, data):
    pass


def _bmi(cpu, data):
    if cpu.sr & 0x80:
        cpu.pc = data


def _bne(cpu, data):
    if not (cpu.sr & 0x2):
        cpu.pc = data


def _bpl(cpu, data):
    if not (cpu.sr & 0x80):
        cpu.pc = data


def _brk(cpu, data):
    pass


def _bvc(cpu, data):
    if not (cpu.sr & 0x40):
        cpu.pc = data


def _bvs(cpu, data):
    if cpu.sr & 0x40:
        cpu.pc = data


def _clc(cpu, data):
    cpu.sr &= 0xfe


def _cld(cpu, data):
    pass


def _cli(cpu, data):
    cpu.sr &= 0xfb


def _clv(cpu, data):
    cpu.sr &= 0xbf


def _cmp(cpu, data):
    res = cpu.ac - data
    set_negative(cpu, res)
    set_zero(cpu, res)
    set_carry(cpu, res)


def _cpx(cpu, data):
    res = cpu.x - data
    set_negative(cpu, res)
    set_zero(cpu, res)
    set_carry(cpu, res)


def _cpy(cpu, data):
    res = cpu.y - data
    set_negative(cpu, res)
    set_zero(cpu, res)
    set_carry(cpu, res)


def _dec(cpu, data):
    res = cpu.mem.read(data) - 1
    cpu.mem.write(data, res)
    set_carry(cpu, res)
    set_zero(cpu, res)


def _dex(cpu, data):
    res = cpu.x - 1
    cpu.x = res
    set_carry(cpu, res)
    set_zero(cpu, res)


def _dey(cpu, data):
    res = cpu.y - 1
    cpu.y = res
    set_carry(cpu, res)
    set_zero(cpu, res)


def _eor(cpu, data):
    res = cpu.ac ^ cpu.mem.read(data)
    cpu.ac = res
    set_zero(cpu, res)
    set_negative(cpu, res)


def _inc(cpu, data):
    res = cpu.mem.read(data) + 1
    cpu.mem.write(data, res)
    set_carry(cpu, res)
    set_zero(cpu, res)


def _inx(cpu, data):
    res = cpu.x + 1
    cpu.x = res
    set_carry(cpu, res)
    set_zero(cpu, res)


def _iny(cpu, data):
    res = cpu.y + 1
    cpu.y = res
    set_carry(cpu, res)
    set_zero(cpu, res)


def _jmp(cpu, data):
    cpu.pc = data


def _jsr(cpu, data):
    cpu.sp -= 1
    cpu.mem.write(cpu.sp, cpu.pc + 2)
    cpu.pc = data


def _lda(cpu, data):
    cpu.ac = data
    set_zero(cpu, data)
    set_negative(cpu, data)


def _ldx(cpu, data):
    cpu.x = data
    set_zero(cpu, data)
    set_negative(cpu, data)


def _ldy(cpu, data):
    cpu.y = data
    set_zero(cpu, data)
    set_negative(cpu, data)


def _lsr(cpu, data):
    if data == "ac":
        res = cpu.ac >> 1
        cpu.ac = res & 0xff
    else:
        res = cpu.mem.read(data) << 1
        cpu.mem.write(data, res & 0xff)
    set_zero(cpu, res)
    set_negative(cpu, res)
    set_carry(cpu, res)


def _nop(cpu, data):
    pass


def _ora(cpu, data):
    cpu.ac |= data


def _pha(cpu, data):
    cpu.sp -= 1
    cpu.mem.write(cpu.sp, cpu.ac)


def _php(cpu, data):
    cpu.sp -= 1
    cpu.mem.write(cpu.sp, cpu.sr)


def _pla(cpu, data):
    res = cpu.mem.read(cpu.sp)
    cpu.sp += 1
    cpu.ac = res
    set_negative(cpu, res)
    set_zero(cpu, res)


def _plp(cpu, data):
    cpu.sr = cpu.mem.read(cpu.sp)
    cpu.sp += 1


def _rol(cpu, data):
    if data == "ac":
        res = cpu.ac << 1 | cpu.ac >> 7
        cpu.ac = res & 0xff
    else:
        res = cpu.mem.read(data) << 1
        cpu.mem.write(data, res & 0xff)
    set_zero(cpu, res)
    set_negative(cpu, res)
    set_carry(cpu, res)


def _ror(cpu, data):
    if data == "ac":
        res = cpu.ac >> 1 | cpu.ac << 7
        cpu.ac = res & 0xff
    else:
        res = cpu.mem.read(data) << 1
        cpu.mem.write(data, res & 0xff)
    set_zero(cpu, res)
    set_negative(cpu, res)
    set_carry(cpu, res)


def _rti(cpu, data):
    _plp(cpu, 0)
    cpu.pc = cpu.mem.read(cpu.sp)
    cpu.sp += 1


def _rts(cpu, data):
    cpu.pc = cpu.mem.read(cpu.sp) + 1
    cpu.sp += 1


def _sbc(cpu, data):
    res = data - cpu.ac - (cpu.sr & 0x1)
    set_carry(cpu, res)
    set_zero(cpu, res)
    set_negative(cpu, res)
    set_overflow(cpu, res, (data, cpu.ac))
    cpu.ac = res & 0xff


def _sec(cpu, data):
    cpu.sr |= 0x1


def _sed(cpu, data):
    pass


def _sei(cpu, data):
    cpu.sr |= 0x4


def _sta(cpu, data):
    cpu.mem.write(data, cpu.ac)


def _stx(cpu, data):
    cpu.mem.write(data, cpu.x)


def _sty(cpu, data):
    cpu.mem.write(data, cpu.y)


def _tax(cpu, data):
    cpu.x = cpu.ac
    set_zero(cpu, cpu.ac)
    set_negative(cpu, cpu.ac)


def _tay(cpu, data):
    cpu.y = cpu.ac
    set_zero(cpu, cpu.ac)
    set_negative(cpu, cpu.ac)


def _tsx(cpu, data):
    cpu.x = cpu.sp
    set_zero(cpu, cpu.sp)
    set_negative(cpu, cpu.sp)


def _txa(cpu, data):
    cpu.ac = cpu.x
    set_zero(cpu, cpu.x)
    set_negative(cpu, cpu.x)


def _txs(cpu, data):
    cpu.sp = cpu.x
    set_zero(cpu, cpu.x)
    set_negative(cpu, cpu.x)


def _tya(cpu, data):
    cpu.y = cpu.ac
    set_zero(cpu, cpu.ac)
    set_negative(cpu, cpu.ac)


# custom ramenbox ops

# transfer display buffer (TDB)
# reads e1 banks from the specified page.
# page is specified using sdp instruction
def _tdb(cpu, data):
    cpu.mem.display(cpu.display)


# set display page index as specified data (immediate or indirect x)
def _sdp(cpu, data):
    cpu.mem.display_page = data


#
# bank swapping
# page selection: specified register
# bank selection: data (can be set as an immediate value or indirect x)
# in pxy, bank swapping addressing is implied as it uses x for the page selection and y for the bank selection

# bank swap using accumulator
def _psa(cpu, data):
    if data > 0x80:
        cpu.sr |= 0x1
    else:
        cpu.mem.pages[cpu.ac]["active_bank"] = data
        cpu.sr &= 0xfe


# bank swap using x
def _psx(cpu, data):
    if data > 0x80:
        cpu.sr |= 0x1
    else:
        cpu.mem.pages[cpu.y]["active_bank"] = data
        cpu.sr &= 0xfe


# bank swap using y
def _psy(cpu, data):
    if data > 0x80:
        cpu.sr |= 0x1
    else:
        cpu.mem.pages[cpu.y]["active_bank"] = data
        cpu.sr &= 0xfe


# bank swap using x and y
def _pxy(cpu, data):
    if data > 0x80:
        cpu.sr |= 0x1
    else:
        cpu.mem.pages[cpu.x]["active_bank"] = cpu.y
        cpu.sr &= 0xfe
