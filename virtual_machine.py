from disassembler import dism
import time

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
        self.outbuffer = ""
        self.instcount = 0
    def read_num(self):
        r = self.memory[self.rip]
        self.rip += 1
        return r
    def jump_to(self, addr):
        self.rip = addr
    def set_mem(self,addr,value):
        self.set_regs(addr,value)
    def set_regs(self, addr, value):
        if 0<=addr<=32767:
            self.memory[addr] = value
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
    def get_mem(self, addr):
        if 0<=addr<=32767:
            return self.memory[addr]
        elif 32768<=addr<=32775:
            addr -= 32768
            return self.regs[addr]
        else:
            print addr
            raise "Invalid Memory Address Read"
    def execute_step(self):
        debug = False
        init_addr = self.rip
        self.instcount += 1
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
            a = self.get_val(a)
            if a!=0:
                self.jump_to(b)
        elif opcode == 8:
            # jf a b
            a,b = self.read_num(), self.read_num()
            a = self.get_val(a)
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
            self.set_regs(a,self.get_mem(b))
        elif opcode == 16:
            # wmem a b
            a,b = self.read_num(),self.read_num()
            a = self.get_val(a)
            b = self.get_val(b)
            # write value b at address a
            self.set_mem(a,b)
        elif opcode == 17:
            # call a
            a = self.get_val(self.read_num())
            if a==6027:
                self.regs[7] = 25734
                self.regs[0] = 6
                return #"debug"
            self.stack.append(self.rip)
            self.jump_to(a)
        elif opcode == 18:
            # ret
            self.jump_to(self.stack.pop())
        elif opcode == 19:
            # out a
            outchr = chr(self.get_val(self.read_num()))
            if outchr == '\n':
                print self.outbuffer
                self.outbuffer = ""
            else:
                self.outbuffer += outchr
        elif opcode == 20:
            # in a
            a = self.read_num()
            if len(self.inputBuffer)==0:
                z = raw_input()
                inp = list(z+"\n")
                inp.reverse()
                self.inputBuffer = inp
                print ">>>>>",z
                #time.sleep(1)
                if "use teleporter" in z:
                    debug = True
            self.set_regs(a, ord(self.inputBuffer.pop()))
        elif opcode == 21:
            # nop
            pass
        if debug:
            return "debug"

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
    d = dism(prog)
    print "Initialised SynacorVM..."
    print "="*80
    debugmode = False
    try:
        while vm.running:
            s = vm.execute_step()
            dm = d.inst(vm.rip)
            if s == "debug":
                print "="*80
                print "ACTIVATING DEBUG MODE"
                print "="*80
                #debugmode = True
                vm.regs[7] = 1
            if vm.instcount==877178:
                #debugmode = True
                pass
            if debugmode:
                time.sleep(0.1)
                print "###",dm,' '*(50-len(dm)),"(%d)"%vm.instcount,
                stc = str(vm.regs)
                print stc,' '*(50-len(stc)),
                print '*'*len(vm.stack)
    except Exception as e:
        raise e
    finally:
        print "="*80
        print "Synacor VM ended with state, "
        print vm.regs, vm.rip, vm.stack
        print "Instructions executed = %d"%vm.instcount
if __name__ == "__main__":
    main()
