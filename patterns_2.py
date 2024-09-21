from tree import *

class JouetteArchitecture:
    def __init__(self):
        self.instruction_costs = {
            "ADD": 1,
            "MUL": 1,
            "SUB": 1,
            "DIV": 1,
            "ADDI": 1,
            "SUBI": 1,
            "LOAD" : 1,
            "STORE" : 1,
            "MOVEM": 2, 

            "TEMP": 0,
            "CONST": 1,
            "MEM": 1
        }
        
        self.instruction_patterns = {
            "ADD": "ADD {src1}, {src2}",
            "MUL": "MUL {src1}, {src2}",
            "SUB": "SUB {src1}, {src2}",
            "DIV": "DIV {src1}, {src2}",
            "ADDI": "ADDI {src}, {const}",
            "SUBI": "SUBI {src}, {const}",
            "LOAD": "LOAD {dest}, {src}",
            "STORE": "STORE {src}, {dest}",
            "MOVEM": "MOVEM {src}, {dest}",

            "TEMP": "USE TEMP {index}",
            "CONST": "LOAD CONST {value}",
            "MEM": "MEM LOAD/STORE"
        }

    def select_instruction(self, node: Node) -> Tuple[str, int]:
        """
        Seleciona a instrução e calcula o custo com base na árvore de instruções.
        Identifica a necessidade de usar ADDI ou SUBI com base na presença de constantes.
        """
        instruction = node.instruction.split()[0]
        parts = node.instruction.split()
        
        # Verifica se é uma operação aritmética
        if instruction in ["ADD", "SUB"]:
            left_is_const = "CONST" in parts[1]  # Verifica se o operando esquerdo é constante
            right_is_const = "CONST" in parts[2]  # Verifica se o operando direito é constante

            if left_is_const and not right_is_const:
                # Usar ADDI ou SUBI (constante à esquerda)
                pattern = self.instruction_patterns[instruction + "I"]
                return pattern, self.instruction_costs[instruction + "I"]
            elif not left_is_const and right_is_const:
                # Usar ADDI ou SUBI (constante à direita)
                pattern = self.instruction_patterns[instruction + "I"]
                return pattern, self.instruction_costs[instruction + "I"]
            else:
                # Usar ADD normal (sem constantes)
                pattern = self.instruction_patterns[instruction]
                return pattern, self.instruction_costs[instruction]
        
        # Instruções comuns como CONST, TEMP, etc.
        elif instruction in self.instruction_patterns:
            pattern = self.instruction_patterns[instruction]
            cost = self.instruction_costs[instruction]
            return pattern, cost
        else:
            raise ValueError(f"Instrução desconhecida: {instruction}")
    
    def format_pattern(self, node: Node, pattern: str) -> str:
        """
        Formata o padrão da instrução com os operandos corretos.
        """
        parts = node.instruction.split()
        if pattern.startswith("ADD") or pattern.startswith("SUB") or pattern.startswith("MUL") or pattern.startswith("DIV"):
            return pattern.format(src1=parts[1], src2=parts[2])
        elif pattern.startswith("ADDI") or pattern.startswith("SUBI"):
            if "CONST" in parts[1]:  # Constante à esquerda
                return pattern.format(const=parts[1].split()[1], src=parts[2])
            else:  # Constante à direita
                return pattern.format(src=parts[1], const=parts[2].split()[1])
        elif pattern.startswith("LOAD CONST"):
            return pattern.format(value=parts[1])
        elif pattern.startswith("USE TEMP"):
            return pattern.format(index=parts[1])
        return pattern

        
class InstructionSelector:
    def __init__(self, tree: Tree, architecture: JouetteArchitecture):
        self.tree = tree
        self.architecture = architecture
        self.generated_code = []
        self.total_cost = 0

    def generate(self, node: Node):
        if node is None:
            return
        
        # Pós-ordem: processar subárvores antes do nó atual
        self.generate(node.left)
        self.generate(node.right)
        
        # Selecionar instrução e calcular custo
        pattern, cost = self.architecture.select_instruction(node)
        formatted_instruction = self.architecture.format_pattern(node, pattern)
        
        # Adicionar instrução ao código gerado
        self.generated_code.append(formatted_instruction)
        self.total_cost += cost

    def select_instructions(self):
        self.generate(self.tree.root)
        return self.generated_code, self.total_cost

# Exemplo de uso
tree = Tree()
tree.createTree("MOVEM TEMP 1 CONST 2")  # Exemplo de código linear
architecture = JouetteArchitecture()
selector = InstructionSelector(tree, architecture)
assembly_code, total_cost = selector.select_instructions()

# Exibir código gerado e o custo total
print("Código gerado:")
for instr in assembly_code:
    print(instr)
print(f"Custo total: {total_cost}")