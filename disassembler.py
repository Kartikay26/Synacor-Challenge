class SynacorVM:
    def __init__(self,program):
        self.memory = program
        self.rip = 0
        self.running = True
    def read_num(self):
        r = self.memory[self.rip]
        self.rip += 1
        if r<32768:
            return str(r)
        else:
            return 'r'+str(r-32768)
    def write_step(self):
        if self.rip==len(self.memory):
            self.running = False
            return
        try:
            opcode = int(self.read_num())
        except:
            self.running = False
            print "FUCK"
            return
        #assert 0<=opcode<=21
        print "%d."%self.rip,
        if opcode == 0:
            # halt
            print "halt"
        elif opcode == 1:
            # set a b
            a,b = self.read_num(), self.read_num()
            print "set",a,b
        elif opcode == 2:
            # push a
            a = self.read_num()
            print "push",a
        elif opcode == 3:
            # pop a
            a = self.read_num()
            print "pop",a
        elif opcode == 4:
            # eq a b c
            a,b,c = self.read_num(),self.read_num(),self.read_num()
            print "eq",a,b,c
        elif opcode == 5:
            # gt a b c
            a,b,c = self.read_num(),self.read_num(),self.read_num()
            print "gt",a,b,c
        elif opcode == 6:
            # jmp a
            a = self.read_num()
            print "jmp",a
        elif opcode == 7:
            # jt a b
            a,b = self.read_num(), self.read_num()
            print "jt",a,b
        elif opcode == 8:
            # jf a b
            a,b = self.read_num(), self.read_num()
            print "jf",a,b
        elif opcode == 9:
            # add a b c
            a,b,c = self.read_num(),self.read_num(),self.read_num()
            print "add",a,b,c
        elif opcode == 10:
            # mul a b c
            a,b,c = self.read_num(),self.read_num(),self.read_num()
            print "mul",a,b,c
        elif opcode == 11:
            # mod a b c
            a,b,c = self.read_num(),self.read_num(),self.read_num()
            print "mod",a,b,c
        elif opcode == 12:
            # and a b c
            a,b,c = self.read_num(),self.read_num(),self.read_num()
            print "and",a,b,c
        elif opcode == 13:
            # or a b c
            a,b,c = self.read_num(),self.read_num(),self.read_num()
            print "or",a,b
        elif opcode == 14:
            # not a b
            a,b = self.read_num(),self.read_num()
            print "not",a,b
        elif opcode == 15:
            # rmem a b
            a,b = self.read_num(),self.read_num()
            print "rmem",a,b
        elif opcode == 16:
            # wmem a b
            a,b = self.read_num(),self.read_num()
            print "wmem",a,b
        elif opcode == 17:
            # call a
            a = self.read_num()
            print "call",a
        elif opcode == 18:
            # ret
            print "ret"
        elif opcode == 19:
            # out a
            try:
                a = int(self.read_num())
                if a in range(256):
                    print "out",a,"\t#",chr(a)
                else:
                    print "out",a,"\t#??"
            except ValueError:
                a = self.read_num()
                print "out",a,"\t#??"
        elif opcode == 20:
            # in a
            a = self.read_num()
            print "in",a
        elif opcode == 21:
            # nop
            print "nop"
        else:
            print "??%d"%opcode

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
    vm = SynacorVM(prog)
    while vm.running:
        vm.write_step()
if __name__ == "__main__":
    main()
