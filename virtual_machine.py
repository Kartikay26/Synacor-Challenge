class SynacorVM:
    def __init__(self,program):
        self.memory = [0 for x in range(32768)]
        for i,x in enumerate(program):
            self.memory[i] = x
        self.regs = [0,0,0,0,0,0,0,0]
        self.stack = []
        self.rip = 0

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
