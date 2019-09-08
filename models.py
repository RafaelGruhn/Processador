"""Models."""
import re
import operator


class Memory:
    """Class for control data and instructions for process."""
    instructions = []
    data = {}

    def __init__(self):
        for instruction in range(self.cont_instructions()):
            self.instructions.append({})

        file_memory = open('memory.txt', 'w')
        for i in range(20):
            self.data['&' + str(i)] = ''
        file_memory.writelines(self.get_data())
        file_memory.close()

    def cont_instructions(self):
        file = open('commands.txt', 'r')
        lines = file.readlines()
        return len(lines)

    def get_data(self):
        str_data = []
        for key, value in self.data.items():
            str_data.append(key + " = " + str(value) + "\n")
        return str_data

    def decode(self, li=0):
        file = open('commands.txt', 'r')
        try:
            lines = file.readlines()
            line = lines[li].replace(',', '')
            line = line.replace('\n', '')
            instruction = line.split(' ')
            self.instructions[li] = {
                'command': instruction[0],
                'var1': instruction[1] if len(instruction) > 1 else None,
                'var2': instruction[2] if len(instruction) > 2 else None
            }
        except Exception as e:
            print(e)
        file.close()


class Register:
    """register."""
    registers = {}
    special_registers = {}
    def __init__(self):
        file_registers = open('registers.txt', 'w')
        for i in range(8):
            self.registers['r' + str(i)] = ''
        self.special_registers['SREG1'] = ''
        self.special_registers['SREG2'] = ''
        file_registers.writelines(self.get_registers())
        file_registers.close()

    def get_registers(self):
        str_register = []
        for key, value in self.registers.items():
            str_register.append(key + " = " + str(value) + "\n")
        for key, value in self.special_registers.items():
            str_register.append(key + " = " + str(value) + "\n")
        return str_register


class Write:
    """Write in output."""
    def get_class(self, register, memory):
        self.register = register
        self.memory = memory

    def output(self):
        """Screeam all informations from registers in memory.txt, from data in memory.txt."""
        file_registers = open('registers.txt', 'w')
        file_registers.writelines(self.register.get_registers())
        file_registers.close()
        file_memory = open('memory.txt', 'w')
        file_memory.writelines(self.memory.get_data())
        file_memory.close()


class ULA:
    """ULA."""
    memory = Memory()
    register = Register()
    li = 0
    ci = li + 1
    exception = Exception("Error: Invalid Command in line %s." % li)

    def execute(self):
        while self.li < self.memory.cont_instructions():
            print('Number of LI: ', self.li)
            print('Number of CI: ', self.ci)
            self.memory.decode(self.li)
            result = None
            if self.memory.instructions[self.li].get('command', '') == 'ADD':
                result = self.ADD()
            elif self.memory.instructions[self.li].get('command', '') == 'SUB':
                result = self.SUB()
            elif self.memory.instructions[self.li].get('command', '') == 'MOV':
                self.MOV()
            elif self.memory.instructions[self.li].get('command', '') == 'GOTO':
                self.GOTO()
                continue
            elif self.memory.instructions[self.li].get('command', '') == 'SBRC':
                if self.SBRC():
                    self.li = self.li + 1
                    self.set_ci()
            elif self.memory.instructions[self.li].get('command', '') == 'SBRS':
                if self.SBRS():
                    self.li = self.li + 1
                    self.set_ci()
            elif self.memory.instructions[self.li].get('command', '') == 'HALF':
                self.li = len(self.memory.instructions) - 1
                self.set_ci()
            else:
                print("Error: Invalid Command in line %s." % self.li)
                break
            if isinstance(result, int):
                if result == 0:
                    self.register.special_registers['SREG1'] = '1'
                    self.register.special_registers['SREG2'] = '0'
                elif result < 0:
                    self.register.special_registers['SREG1'] = '0'
                    self.register.special_registers['SREG2'] = '1'
                else:
                    self.register.special_registers['SREG1'] = '0'
                    self.register.special_registers['SREG2'] = '0'

            teste = Write()
            teste.get_class(self.register, self.memory)
            teste.output()
            self.li = self.ci
            self.set_ci()

    def set_ci(self, value = 1):
        self.ci = self.li + value

    def SBRS(self):
        if re.match(r'r', self.memory.instructions[self.li]['var1']):
            return self.register.registers.get(self.memory.instructions[self.li]['var1'], 0) == 1
        else:
            raise self.exception

    def SBRC(self):
        if re.match(r'r', self.memory.instructions[self.li]['var1']):
            return self.register.registers.get(self.memory.instructions[self.li]['var1'], 0) == 0
        else:
            raise self.exception

    def GOTO(self):
        self.li = int(self.memory.instructions[self.li].get('var1', 0))
        self.set_ci()

    def ADD(self):
        return self.action(operator.add)

    def SUB(self):
        return self.action(operator.sub)

    def MOV(self):
        if re.match(r'&', self.memory.instructions[self.li]['var1']):
            if re.match(r'&', self.memory.instructions[self.li]['var2']):
                self.memory.data[self.memory.instructions[self.li]['var1']] = self.memory.data.get(self.memory.instructions[self.li]['var2'], 0)
            elif re.match(r'r', self.memory.instructions[self.li]['var2']):
                self.memory.data[self.memory.instructions[self.li]['var1']] = self.register.registers.get(self.memory.instructions[self.li]['var2'], 0)
            else:
                raise self.exception
        elif re.match(r'r', self.memory.instructions[self.li]['var1']):
            if re.match(r'&', self.memory.instructions[self.li]['var2']):
                self.register.registers[self.memory.instructions[self.li]['var1']] = self.memory.data.get(self.memory.instructions[self.li]['var2'], 0)
            elif re.match(r'r', self.memory.instructions[self.li]['var2']):
                self.register.registers[self.memory.instructions[self.li]['var1']] = self.register.registers.get(self.memory.instructions[self.li]['var2'], 0)
            else:
                raise self.exception
        else:
            raise self.exception

    def action(self, operator):
        if re.match(r'&', self.memory.instructions[self.li]['var1']):
            if self.memory.instructions[self.li]['var1'] in self.memory.data:
                if re.match(r'&', self.memory.instructions[self.li]['var2']):
                    if self.memory.instructions[self.li]['var2'] in self.memory.data:
                        if isinstance(self.memory.data[self.memory.instructions[self.li]['var1']], str):
                            self.memory.data[self.memory.instructions[self.li]['var1']] = 0
                        self.memory.data[self.memory.instructions[self.li]['var1']] = operator(self.memory.data[self.memory.instructions[self.li]['var1']], self.memory.data[self.memory.instructions[self.li]['var2']])
                        return self.memory.data[self.memory.instructions[self.li]['var1']]
                    else:
                        raise self.exception
                elif re.match(r'r', self.memory.instructions[self.li]['var2']):
                    if self.memory.instructions[self.li]['var2'] in self.register.registers:
                        if isinstance(self.memory.data[self.memory.instructions[self.li]['var1']], str):
                            self.memory.data[self.memory.instructions[self.li]['var1']] = 0
                        self.memory.data[self.memory.instructions[self.li]['var1']] = operator(self.memory.data[self.memory.instructions[self.li]['var1']], self.register.registers[self.memory.instructions[self.li]['var2']])
                        return self.memory.data[self.memory.instructions[self.li]['var1']]
                    else:
                        raise self.exception
                elif int(self.memory.instructions[self.li]['var2']):
                    if isinstance(self.memory.data[self.memory.instructions[self.li]['var1']], str):
                        self.memory.data[self.memory.instructions[self.li]['var1']] = 0
                    self.memory.data[self.memory.instructions[self.li]['var1']] = operator(self.memory.data[self.memory.instructions[self.li]['var1']], int(self.memory.instructions[self.li]['var2']))
                    return self.memory.data[self.memory.instructions[self.li]['var1']]
                else:
                    raise self.exception
            else:
                raise self.exception
        elif re.match(r'r', self.memory.instructions[self.li]['var1']):
            if self.memory.instructions[self.li]['var1'] in self.register.registers:
                if re.match(r'&', self.memory.instructions[self.li]['var2']):
                    if self.memory.instructions[self.li]['var2'] in self.memory.data:
                        if isinstance(self.register.registers[self.memory.instructions[self.li]['var1']], str):
                            self.register.registers[self.memory.instructions[self.li]['var1']] = 0
                        self.register.registers[self.memory.instructions[self.li]['var1']] = operator(self.register.registers[self.memory.instructions[self.li]['var1']], self.memory.data[self.memory.instructions[self.li]['var2']])
                        return self.register.registers[self.memory.instructions[self.li]['var1']]
                    else:
                        raise self.exception
                elif re.match(r'r', self.memory.instructions[self.li]['var2']):
                    if self.memory.instructions[self.li]['var2'] in self.register.registers:
                        if isinstance(self.register.registers[self.memory.instructions[self.li]['var1']], str):
                            self.register.registers[self.memory.instructions[self.li]['var1']] = 0
                        self.register.registers[self.memory.instructions[self.li]['var1']] = operator(self.register.registers[self.memory.instructions[self.li]['var1']], self.register.registers[self.memory.instructions[self.li]['var2']])
                        return self.register.registers[self.memory.instructions[self.li]['var1']]
                    else:
                        raise self.exception
                elif int(self.memory.instructions[self.li]['var2']):
                    if isinstance(self.register.registers[self.memory.instructions[self.li]['var1']], str):
                        self.register.registers[self.memory.instructions[self.li]['var1']] = 0
                    self.register.registers[self.memory.instructions[self.li]['var1']] = operator(self.register.registers[self.memory.instructions[self.li]['var1']], int(self.memory.instructions[self.li]['var2']))
                    return self.register.registers[self.memory.instructions[self.li]['var1']]
                else:
                    raise self.exception
            else:
                raise self.exception
        else:
            raise self.exception
