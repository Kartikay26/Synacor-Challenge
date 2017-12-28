class SynacorVM:
    def __init__(self,program):
        self.memory = [0 for x in range(32768)]
        for i,x in enumerate(program):
            self.memory[i] = x
        self.regs = [0,0,0,0,0,0,0,0]
        self.stack = []
        self.running = True
        self.rip = 0
        self.inputBuffer = []
    def read_num(self):
        r = self.memory[self.rip]
        self.rip += 1
        return r
    def jump_to(self, addr):
        self.rip = addr
    def set_regs(self, addr, value):
        if 0<=addr<=32767:
            print addr
            raise "Invalid Memory Address Write"
        elif 32768<=addr<=32775:
            addr -= 32768
            self.regs[addr] = value
        else:
            print addr
            raise "Invalid Memory Address Write"
    def get_val(self, addr):
        if 0<=addr<=32767:
            return addr
        elif 32768<=addr<=32775:
            addr -= 32768
            return self.regs[addr]
        else:
            print addr
            raise "Invalid Memory Address Read"
    def execute_step(self):
        assert self.running
        opcode = self.read_num()
        assert 0<=opcode<=21
        if opcode == 0:
            # halt
            self.running = False
        elif opcode == 1:
            # set a b
            self.set_regs(self.read_num(),
                          self.get_val(self.read_num()))
        elif opcode == 2:
            # push a
            self.stack.append(self.get_val(self.read_num()))
        elif opcode == 3:
            # pop a
            self.set_regs(self.read_num(),self.stack.pop())
        elif opcode == 4:
            # eq a b c
            a,b,c = self.read_num(),self.read_num(),self.read_num()
            b,c = self.get_val(b),self.get_val(c)
            self.set_regs(a,1 if b==c else 0)
        elif opcode == 5:
            # gt a b c
            a,b,c = self.read_num(),self.read_num(),self.read_num()
            b,c = self.get_val(b),self.get_val(c)
            self.set_regs(a,1 if b>c else 0)
        elif opcode == 6:
            # jmp a
            a = self.read_num()
            self.jump_to(a)
        elif opcode == 7:
            # jt a b
            a,b = self.read_num(), self.read_num()
            if a!=0:
                self.jump_to(b)
        elif opcode == 8:
            # jf a b
            a,b = self.read_num(), self.read_num()
            if a==0:
                self.jump_to(b)
        elif opcode == 9:
            # add a b c
            a,b,c = self.read_num(),self.read_num(),self.read_num()
            b,c = self.get_val(b),self.get_val(c)
            self.set_regs(a,(b+c)%32768)
        elif opcode == 10:
            # mul a b c
            a,b,c = self.read_num(),self.read_num(),self.read_num()
            b,c = self.get_val(b),self.get_val(c)
            self.set_regs(a,(b*c)%32768)
        elif opcode == 11:
            # mod a b c
            a,b,c = self.read_num(),self.read_num(),self.read_num()
            b,c = self.get_val(b),self.get_val(c)
            self.set_regs(a,(b%c))
        elif opcode == 12:
            # and a b c
            a,b,c = self.read_num(),self.read_num(),self.read_num()
            b,c = self.get_val(b),self.get_val(c)
            self.set_regs(a,(b&c))
        elif opcode == 13:
            # or a b c
            a,b,c = self.read_num(),self.read_num(),self.read_num()
            b,c = self.get_val(b),self.get_val(c)
            self.set_regs(a,(b|c))
        elif opcode == 14:
            # not a b
            a,b = self.read_num(),self.read_num()
            b = self.get_val(b)
            self.set_regs(a,bit15complement(b))
        elif opcode == 15:
            # rmem a b
            a,b = self.read_num(),self.read_num()
            b = self.get_val(b)
            self.set_regs(a,self.memory[b])
        elif opcode == 16:
            # wmem a b
            a,b = self.read_num(),self.read_num()
            b = self.get_val(b)
            self.memory[a] = b
        elif opcode == 17:
            # call 17 a
            a = self.get_val(self.read_num())
            self.stack.push(self.rip+1)
            self.jump_to(a)
        elif opcode == 18:
            # ret
            self.jump_to(self.stack.pop())
        elif opcode == 19:
            # out a
            print self.get_val(self.read_num())
        elif opcode == 20:
            # in a
            a = self.read_num()
            if len(self.inputBuffer)==0:
                self.inputBuffer = list(raw_input())
            else:
                self.set_regs(a, self.inputBuffer.pop())
        elif opcode == 21:
            # nop
            pass

def bit15complement(a):
    x = bin(a)[2:]
    x = "0"*(15-len(x))+x
    x = ['1' if y=='0' else '0' for y in x]
    x = "".join(x)
    return int(x,2)


def main():
    print "Starting virtual machine ..."
    print "Importing data..."
    prog = []
    for num in open("program.txt"):
        prog += [int(num)]
    print "Read %d-word program..."%len(prog)
    vm = SynacorVM(prog)
    print "Initialised SynacorVM,",vm,"..."

if __name__ == "__main__":
    main()
