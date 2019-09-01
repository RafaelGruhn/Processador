"""Models."""
import re
import operator


class Memory:
    """Class for control data and instructions for process."""
    instructions = []
    data = {}

    def __init__(self):
        file = open('commands.txt', 'r')
        try:
            for line in file:
                line = line.replace(',', '')
                line = line.replace('\n', '')
                instruction = line.split(' ')
                self.instructions.append({
                    'command': instruction[0],
                    'var1': instruction[1],
                    'var2': instruction[2]
                })
        except Exception as e:
            print(e)
        file.close()

        file_memory = open('memory.txt', 'w')
        for i in range(20):
            self.data['&' + str(i)] = ''
        file_memory.writelines(self.get_data())
        file_memory.close()

    def output(self):
        """Screeam all informations from data in memory.txt"""
        file_memory = open('memory.txt', 'w')
        file_memory.writelines(self.get_data())
        file_memory.close()

    def get_data(self):
        str_data = []
        for key, value in self.data.items():
            str_data.append(key + " = " + str(value) + "\n")
        return str_data


class Register:
    """register."""
    registers = {}
    special_registers = {}
    def __init__(self):
        file_registers = open('registers.txt', 'w')
        for i in range(8):
            self.registers['r' + str(i)] = ''
        self.special_registers['SREG'] = ''
        self.special_registers['SREG1'] = ''
        file_registers.writelines(self.get_registers())
        file_registers.close()
    
    def output(self):
        """Screeam all informations from registers in memory.txt"""
        file_registers = open('registers.txt', 'w')
        file_registers.writelines(self.get_registers())
        file_registers.close()

    def get_registers(self):
        str_register = []
        for key, value in self.registers.items():
            str_register.append(key + " = " + str(value) + "\n")
        for key, value in self.special_registers.items():
            str_register.append(key + " = " + str(value) + "\n")
        return str_register

class ULA:
    """ULA."""
    memory = Memory()
    register = Register()
    li = 0
    ci = li + 1
    exception = Exception("Error: Invalid Command in line %s." % li)

    def execute(self):
        for self.li in range(len(self.memory.instructions)):
            result = None
            if self.memory.instructions[self.li]['command'] == 'ADD':
                result = self.ADD()
            elif self.memory.instructions[self.li]['command'] == 'SUB':
                result = self.SUB()
            elif self.memory.instructions[self.li]['command'] == 'MOV':
                pass
            elif self.memory.instructions[self.li]['command'] == 'GOTO':
                pass
            elif self.memory.instructions[self.li]['command'] == 'JBE':
                pass
            elif self.memory.instructions[self.li]['command'] == 'JLE':
                pass
            else:
                print("Error: Invalid Command in line %s." % self.li)
                break
            if isinstance(result, int):
                if result == 0:
                    self.register.special_registers['SREG'] = '1'
                    self.register.special_registers['SREG1'] = '0'
                elif result < 0:
                    self.register.special_registers['SREG'] = '0'
                    self.register.special_registers['SREG1'] = '1'
                else:
                    self.register.special_registers['SREG'] = '0'
                    self.register.special_registers['SREG1'] = '0'

        self.memory.output()
        self.register.output()

    def set_ci(self, value = 1):
        self.ci = self.li + value

    def ADD(self):
        return self.action(operator.add)

    def SUB(self):
        return self.action(operator.sub)

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
