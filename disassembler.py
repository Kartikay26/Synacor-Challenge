class SynacorVM:
    def __init__(self,program):
        self.memory = program
        self.rip = 0
        self.cur_inst = 0
        self.running = True
    def read_num(self):
        r = self.memory[self.rip]
        self.rip += 1
        if r<32768:
            return str(r)
        else:
            return 'r'+str(r-32768)
    def write_step(self):
        self.rip = self.cur_inst
        try:
            opcode = self.memory[self.cur_inst]
        except IndexError:
            self.running = False
            return
        self.rip += 1
        #assert 0<=opcode<=21
        out = ""
        out += fxn(("%d.  "%(self.cur_inst)))
        if opcode == 0:
            # halt
            out += fxn(("halt"))
        elif opcode == 1:
            # set a b
            a,b = self.read_num(), self.read_num()
            out += fxn(("set",a,b))
        elif opcode == 2:
            # push a
            a = self.read_num()
            out += fxn(("push",a))
        elif opcode == 3:
            # pop a
            a = self.read_num()
            out += fxn(("pop",a))
        elif opcode == 4:
            # eq a b c
            a,b,c = self.read_num(),self.read_num(),self.read_num()
            out += fxn(("eq",a,b,c))
        elif opcode == 5:
            # gt a b c
            a,b,c = self.read_num(),self.read_num(),self.read_num()
            out += fxn(("gt",a,b,c))
        elif opcode == 6:
            # jmp a
            a = self.read_num()
            out += fxn(("jmp",a))
        elif opcode == 7:
            # jt a b
            a,b = self.read_num(), self.read_num()
            out += fxn(("jt",a,b))
        elif opcode == 8:
            # jf a b
            a,b = self.read_num(), self.read_num()
            out += fxn(("jf",a,b))
        elif opcode == 9:
            # add a b c
            a,b,c = self.read_num(),self.read_num(),self.read_num()
            out += fxn(("add",a,b,c))
        elif opcode == 10:
            # mul a b c
            a,b,c = self.read_num(),self.read_num(),self.read_num()
            out += fxn(("mul",a,b,c))
        elif opcode == 11:
            # mod a b c
            a,b,c = self.read_num(),self.read_num(),self.read_num()
            out += fxn(("mod",a,b,c))
        elif opcode == 12:
            # and a b c
            a,b,c = self.read_num(),self.read_num(),self.read_num()
            out += fxn(("and",a,b,))
        elif opcode == 13:
            # or a b c
            a,b,c = self.read_num(),self.read_num(),self.read_num()
            out += fxn(("or",a,b))
        elif opcode == 14:
            # not a b
            a,b = self.read_num(),self.read_num()
            out += fxn(("not",a,b))
        elif opcode == 15:
            # rmem a b
            a,b = self.read_num(),self.read_num()
            out += fxn(("rmem",a,b))
        elif opcode == 16:
            # wmem a b
            a,b = self.read_num(),self.read_num()
            out += fxn(("wmem",a,b))
        elif opcode == 17:
            # call a
            a = self.read_num()
            out += fxn(("call",a))
        elif opcode == 18:
            # ret
            out += fxn(("ret"))
        elif opcode == 19:
            # out a
            try:
                a = int(self.read_num())
                if a in range(256):
                    out += fxn(("out",a,"\t#",chr(a)))
                else:
                    out += fxn(("out",a,"\t#??"))
            except ValueError:
                a = self.read_num()
                out += fxn(("out",a,"\t#??"))
        elif opcode == 20:
            # in a
            a = self.read_num()
            out += fxn(("in",a))
        elif opcode == 21:
            # nop
            out += fxn(("nop"))
        else:
            out += fxn(("?? %d"%opcode))
        print out+' '*(30-len(out))+"(%d)"%self.rip,
        self.cur_inst += 1
        print ""

def fxn(x):
    if type(x)==str:
        return x
    else:
        return " ".join(str(z) for z in x)

def bit15complement(a):
    x = bin(a)[2:]
    x = "0"*(15-len(x))+x
    x = ['1' if y=='0' else '0' for y in x]
    x = "".join(x)
    return int(x,2)

def main():
    prog = []
    for num in open("program.txt"):
        prog += [int(num)]
    import time
    vm = SynacorVM(prog)
    while vm.running:
        vm.write_step()

if __name__ == "__main__":
    main()
