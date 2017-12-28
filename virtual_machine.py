class SynacorVM:
    def __init__(self,program):
        self.memory = [0 for x in range(32768)]
        for i,x in enumerate(program):
            self.memory[i] = x
        self.regs = [0,0,0,0,0,0,0,0]
        self.stack = []
        self.running = True
        self.rip = 0
    def read_num(self):
        r = self.memory[self.rip]
        self.rip += 1
        return r
    def jump_to(self, addr):
        self.rip = addr
    def set_mem(self, addr, value):
        if 0<=addr<=32767:
            self.memory[addr] = value
        elif 32768<=addr<=32775:
            addr -= 32768
            self.regs[addr] = value
        else:
            print addr
            raise "Invalid Memory Address Write"
    def get_mem(self, addr, value):
        if 0<=addr<=32767:
            return self.memory[addr]
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
            #self.set_mem(self.read_num(),self.read_num())
        elif opcode == 2:
            # set a b
            #self.stack.append(self.read_num())

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
