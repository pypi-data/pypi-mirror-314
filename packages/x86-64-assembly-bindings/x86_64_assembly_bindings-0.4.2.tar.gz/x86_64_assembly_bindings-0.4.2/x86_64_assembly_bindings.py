from __future__ import annotations
from enum import Enum, EnumMeta
from typing import Literal
import os
import ctypes
import platform

current_os = platform.system()

class Program:
    CURRENT:Program|None = None
    FUNC_STACK:list[Function] = []

    @classmethod
    @property
    def current_function(cls) -> Function:
        return cls.FUNC_STACK[-1]

    def __init__(self, name:str|None = None):
        self.name = name
        self.lines:list[Instruction|Memory|str] = []
        self.functions:dict[str, Function] = {}
        self.__ctypes_lib:ctypes.CDLL = None
        Program.CURRENT = self
        self.compiled = False
        self.linked = False

    def append(self, component:Instruction|Memory):
        self.lines.append(component)

    def write(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return "\n".join(f"global {fun}" for fun in self.functions) + "\n" + "\n".join(i if isinstance(i, str) else f"{'    ' if isinstance(i, Instruction) else ''}{i.write()}" for i in self.lines)

    def save(self, path:str):
        with open(path, "w", encoding="utf-8") as fp:
            fp.write(self.write())

    def comment(self, text:str):
        self.append(f"; {text}")

    def append_line(self, line:str):
        self.append(line)

    def new_line(self):
        self.append("")

    def exit_program(self):
        self.append("    mov rax, 60")
        self.append("    mov rdi, 0")
        self.append("    syscall")

    def compile(self, program:str|None = None, save:bool = True, **arguments_:dict[str, any]):
        program = self.name if program is None else program

        if program is None:
            raise RuntimeError("You must specify a program name either in the \"program\" argument of the \"compile\" function, by setting the \"name\" attribute of your \"Program\" instance or by specifying it as the \"name\" argument when creating your \"Program\" instance.")

        if save:self.save(f"{program}.asm")
        args = {
            "-f":"elf64",
            "-o":f"\"{program}.o\""
        }
        args.update({f"-{k}":str(v) for k,v in arguments_.items()})
        command = ("yasm "+
            ' '.join([f"{k} {v}" for k,v in args.items()])+
            f" \"{program}.asm\"")

        os.system(command)
        self.compiled = True

    def link(self, output:str|None = None, programs:set[Program|str]|None = None, args:dict[str, any|None]|None = None, lib_paths:set[str]|None = None, libs:set[str]|None = None, script:str|None = None, output_extension:str = ""):
        output = self.name if output is None else output
        
        programs = set() if programs is None else programs
        if self.name is not None:
            programs.add(self.name)

        if not programs:
            raise RuntimeError("The \"programs\" argument cannot be empty unless the \"Program\" instance's \"name\" attribute is set.")

        if output is None:
            raise RuntimeError("You must specify a program name either by passing it as the \"output\" argument when calling the link function, by setting the \"name\" attribute of your \"Program\" instance or by specifying it as the \"name\" argument when creating your \"Program\" instance.")

        output = f"{output}{output_extension}"

        out_file = f"-o \"{output}\""
        o_files = "\"" + ' \"'.join([f"{f}.o\"" for f in programs])
        script = "" if script is None else f"-T \"{script}\""
        lib_paths = "" if lib_paths is None else "\"-L"+' \"-L'.join(
            [f"{p}\"" for p in lib_paths]
        )
        libs = "" if libs is None else "\"-l"+' \"-l'.join(
            [f"{l}\"" for l in libs]
        )
        args:str = "" if args is None else ' '.join([f"-{k}" + ("" if v is None else f" \"{v}\"") for k,v in args.items()])


        command = f"ld {args} {out_file} {script} {o_files} {lib_paths} {libs}"

        os.system(command)
        self.linked = True

    def call(self, function_name:str, *arguments:list[any], library:str|None = None) -> any:
        library = library if library else self.name
        if not library:
            raise RuntimeError("Either the \"library\" argument of the call function or \"Program\" instance's \"name\" attribute need to be specified to call an assembled function from python.")
        library = f"./{library}.so" if current_os == "Linux" else f"./{library}.dll"
        if not self.__ctypes_lib or self.__ctypes_lib._name != library:
            self.__ctypes_lib = ctypes.CDLL(library)
        func:Function = self.functions[function_name]
        cfunc = getattr(self.__ctypes_lib, function_name)
        cfunc.argtypes = func.ctypes_arguments
        cfunc.restype = func.ctypes_restype

        return cfunc(*arguments)



    def run(self, *args:list[any], compile_args:dict|None = None, link_args:dict|None = None, skip_compile:bool = False, skip_link:bool = False):
        if self.name is None:
            raise RuntimeError("The \"name\" attribute of the \"Program\" instance must be specified to run the program.")

        compile_args = {} if compile_args is None else compile_args
        link_args = {} if link_args is None else link_args

        if not skip_compile:
            self.compile(**compile_args)
        if not skip_link:
            self.link(**link_args)
        
        args:str = ' '.join([f"'{a}'" for a in args])

        os.system(f"./{self.name} {args}")


Program()# create the current program


class Block:
    block_counter = 0

    def __init__(self, label:str|None = None):
        self.label = label if label else f"block{Block.block_counter}"
        if label is None:
            Block.block_counter += 1

    @property
    def name(self) -> str:
        return self.label

    def __str__(self):
        return f"{self.label}"

    def write(self):
        return f"{self}:"

    def __call__(self, recorder:Program|None = None):
        (recorder if recorder else Program.CURRENT).append(self)
        return self


class MemorySize(Enum):
    BYTE = 8
    WORD = 16
    DWORD = 32
    QWORD = 64
    DQWORD = 128

    def __hash__(self):
        return hash(self.value)

    def to_ctype(self, signed:bool = False, py_type:type = int):
        match py_type.__name__:
            case "int":
                py_type = 0
            case "float":
                if self not in {self.DWORD, self.QWORD, self.DQWORD}:
                    raise RuntimeError(f"{self} sized ctype float does not exist.")
                if not signed:
                    raise RuntimeError("Floating point data must always be signed.")
                py_type = 1
        py_type:int
        return {
            self.BYTE.value:(
                (ctypes.c_ubyte,),
                (ctypes.c_byte,)
            ),
            self.WORD.value:(
                (ctypes.c_ushort,),
                (ctypes.c_short,)
            ),
            self.DWORD.value:(
                (ctypes.c_uint,),
                (ctypes.c_int, ctypes.c_float)
            ),
            self.QWORD.value:(
                (ctypes.c_ulong,),
                (ctypes.c_long, ctypes.c_double)
            ),
            self.DQWORD.value:(
                (ctypes.c_ulong,),
                (ctypes.c_double, ctypes.c_double)
            )
        }[self.value][signed][py_type]
    
    def __eq__(self, other:MemorySize):
        if not isinstance(other, MemorySize):
            return False
        return self.value == other.value

    def __gt__(self, other:Register):
        if not isinstance(other, MemorySize):
            return False
        return self.value > other.value

    def __lt__(self, other:Register):
        if not isinstance(other, MemorySize):
            return False
        return self.value < other.value

    def __repr__(self):
        return f"{self.name}({self.value})"

    def __str__(self):
        return repr(self)

    @property
    def grow(self):
        match self:
            case self.BYTE:
                return self.WORD
            case self.WORD:
                return self.DWORD
            case self.DWORD:
                return self.QWORD
            case self.QWORD:
                return self.DQWORD
            case self.DQWORD:
                return None

    @property
    def shrink(self):
        match self:
            case self.BYTE:
                return None
            case self.WORD:
                return self.BYTE
            case self.DWORD:
                return self.WORD
            case self.QWORD:
                return self.DWORD
            case self.DQWORD:
                return self.QWORD


    @property
    def sec_data_write(self):
        match self:
            case self.BYTE:
                return "db"
            case self.WORD:
                return "dw"
            case self.DWORD:
                return "dd"
            case self.QWORD|self.DQWORD:
                return "dq"

    @property
    def sec_bss_write(self):
        match self:
            case self.BYTE:
                return "resb"
            case self.WORD:
                return "resw"
            case self.DWORD:
                return "resd"
            case self.QWORD|self.DQWORD:
                return "resq"

RDT = RegisterDataType = tuple[str, MemorySize, Literal[0]|Literal[1]]
#                       [name, size, position (0 = upper bytes, 1 = lower bytes)]

MemS = MemorySize

class RegisterData(Enum):
    """
    This enum defines all the sizes and other shared properties of all registers.
    """
    # main registers
    ah:RegisterDataType = ("ah", MemorySize.BYTE, 0)
    al:RegisterDataType = ("al", MemorySize.BYTE, 1)
    dx:RegisterDataType = ("dx", MemorySize.WORD, 0)
    ax:RegisterDataType = ("ax", MemorySize.WORD, 1)
    edx:RegisterDataType = ("edx", MemorySize.DWORD, 0)
    eax:RegisterDataType = ("eax", MemorySize.DWORD, 1)
    rdx:RegisterDataType = ("rdx", MemorySize.QWORD, 0)
    rax:RegisterDataType = ("rax", MemorySize.QWORD, 1)

    rcx:RegisterDataType = ("rcx", MemorySize.QWORD, 0)
    ecx:RegisterDataType = ("ecx", MemorySize.DWORD, 0)
    cx:RegisterDataType = ("cx", MemorySize.WORD, 0)
    ch:RegisterDataType = ("ch", MemorySize.BYTE, 0)
    cl:RegisterDataType = ("cl", MemorySize.BYTE, 1)
    
    dh:RegisterDataType = ("dh", MemorySize.BYTE, 0)
    dl:RegisterDataType = ("dl", MemorySize.BYTE, 1)

    rbx:RegisterDataType = ("rbx", MemorySize.QWORD, 0)
    ebx:RegisterDataType = ("ebx", MemorySize.DWORD, 0)
    bx:RegisterDataType = ("bx", MemorySize.WORD, 0)
    bh:RegisterDataType = ("bh", MemorySize.BYTE, 0)
    bl:RegisterDataType = ("bl", MemorySize.BYTE, 1)

    rsp:RegisterDataType = ("rsp", MemorySize.QWORD, 0)
    esp:RegisterDataType = ("esp", MemorySize.DWORD, 0)
    sp:RegisterDataType = ("sp", MemorySize.WORD, 0)
    spl:RegisterDataType = ("spl", MemorySize.BYTE, 1)

    rbp:RegisterDataType = ("rbp", MemorySize.QWORD, 0)
    ebp:RegisterDataType = ("ebp", MemorySize.DWORD, 0)
    bp:RegisterDataType = ("bp", MemorySize.WORD, 0)
    bpl:RegisterDataType = ("bpl", MemorySize.BYTE, 1)



    # other 64
    rdi:RegisterDataType = ("rdi", MemorySize.QWORD, 0)
    rsi:RegisterDataType = ("rsi", MemorySize.QWORD, 0)
    r8:RegisterDataType = ("r8", MemorySize.QWORD, 0)
    r9:RegisterDataType = ("r9", MemorySize.QWORD, 0)
    r10:RegisterDataType = ("r10", MemorySize.QWORD, 0)
    r11:RegisterDataType = ("r11", MemorySize.QWORD, 0)

    # other 32
    esi:RegisterDataType = ("esi", MemorySize.DWORD, 0)
    edi:RegisterDataType = ("edi", MemorySize.DWORD, 0)
    r8d:RegisterDataType = ("r8d", MemorySize.DWORD, 0)
    r9d:RegisterDataType = ("r9d", MemorySize.DWORD, 0)
    r10d:RegisterDataType = ("r10d", MemorySize.DWORD, 0)
    r11d:RegisterDataType = ("r11d", MemorySize.DWORD, 0)

    # other 16
    si:RegisterDataType = ("si", MemorySize.WORD, 0)
    di:RegisterDataType = ("di", MemorySize.WORD, 0)
    r8w:RegisterDataType = ("r8w", MemorySize.WORD, 0)
    r9w:RegisterDataType = ("r9w", MemorySize.WORD, 0)
    r10w:RegisterDataType = ("r10w", MemorySize.WORD, 0)
    r11w:RegisterDataType = ("r11w", MemorySize.WORD, 0)

    # other 8
    sil:RegisterDataType = ("sil", MemorySize.BYTE, 1)
    dil:RegisterDataType = ("dil", MemorySize.BYTE, 1)
    r8b:RegisterDataType = ("r8b", MemorySize.BYTE, 0)
    r9b:RegisterDataType = ("r9b", MemorySize.BYTE, 0)
    r10b:RegisterDataType = ("r10b", MemorySize.BYTE, 0)
    r11b:RegisterDataType = ("r11b", MemorySize.BYTE, 0)

    r12:RegisterDataType = ("r12", MemS.QWORD, 0)
    r12d:RegisterDataType = ("r12d", MemS.DWORD, 0)
    r12w:RegisterDataType = ("r12w", MemS.WORD, 0)
    r12b:RegisterDataType = ("r12b", MemS.BYTE, 0)

    r13:RegisterDataType = ("r13", MemS.QWORD, 0)
    r13d:RegisterDataType = ("r13d", MemS.DWORD, 0)
    r13w:RegisterDataType = ("r13w", MemS.WORD, 0)
    r13b:RegisterDataType = ("r13b", MemS.BYTE, 0)

    r14:RegisterDataType = ("r14", MemS.QWORD, 0)
    r14d:RegisterDataType = ("r14d", MemS.DWORD, 0)
    r14w:RegisterDataType = ("r14w", MemS.WORD, 0)
    r14b:RegisterDataType = ("r14b", MemS.BYTE, 0)

    r15:RegisterDataType = ("r15", MemS.QWORD, 0)
    r15d:RegisterDataType = ("r15d", MemS.DWORD, 0)
    r15w:RegisterDataType = ("r15w", MemS.WORD, 0)
    r15b:RegisterDataType = ("r15b", MemS.BYTE, 0)

    xmm0:RDT = ("xmm0", MemS.DQWORD, 0)
    xmm1:RDT = ("xmm1", MemS.DQWORD, 0)
    xmm2:RDT = ("xmm2", MemS.DQWORD, 0)
    xmm3:RDT = ("xmm3", MemS.DQWORD, 0)
    xmm4:RDT = ("xmm4", MemS.DQWORD, 0)
    xmm5:RDT = ("xmm5", MemS.DQWORD, 0)
    xmm6:RDT = ("xmm6", MemS.DQWORD, 0)
    xmm7:RDT = ("xmm7", MemS.DQWORD, 0)
    xmm8:RDT = ("xmm8", MemS.DQWORD, 0)
    xmm9:RDT = ("xmm9", MemS.DQWORD, 0)
    xmm10:RDT = ("xmm10", MemS.DQWORD, 0)
    xmm11:RDT = ("xmm11", MemS.DQWORD, 0)
    xmm12:RDT = ("xmm12", MemS.DQWORD, 0)
    xmm13:RDT = ("xmm13", MemS.DQWORD, 0)
    xmm14:RDT = ("xmm14", MemS.DQWORD, 0)
    xmm15:RDT = ("xmm15", MemS.DQWORD, 0)

    @classmethod
    def from_size(cls, size:MemorySize) -> (RegisterData, RegisterData):
        RD = RegisterData
        match size:
            case MemorySize.BYTE:
                return RD.ah, RD.al
            case MemorySize.WORD:
                return RD.dx, RD.ax
            case MemorySize.DWORD:
                return RD.edx, RD.eax
            case MemorySize.QWORD:
                return RD.rdx, RD.rax

    def cast_to(self, size:MemorySize) -> RegisterData:
        RD = RegisterData
        rname = self.name[:3]
        match size:
            case MemorySize.BYTE:
                return RegD[f"{rname}b"]
            case MemorySize.WORD:
                return RegD[f"{rname}w"]
            case MemorySize.DWORD:
                return RegD[f"{rname}d"]
            case MemorySize.QWORD:
                return RegD[f"{rname}"]
    
    @property
    def is_callee_saved(self) -> bool:
        return bool(self.get_callee_saved())

    def get_callee_saved(self) -> RegisterData:
        match self:
            case self.r12|self.r12d|self.r12w|self.r12b:
                return self.r12
            case self.r13|self.r13d|self.r13w|self.r13b:
                return self.r13
            case self.r14|self.r14d|self.r14w|self.r14b:
                return self.r14
            case self.r15|self.r15d|self.r15w|self.r15b:
                return self.r15
            case _:
                return None

    @property
    def register_name(self) -> str:
        return self.value[0]

    @property
    def size(self) -> MemorySize:
        return self.value[1]

    @property
    def position(self) -> Literal[0]|Literal[1]:
        """
        return 0 if upper bytes, return 1 if lower bytes
        """
        return self.value[2]

RegD = RegisterData

class Register:
    data:RegisterData

    available_64:list[RegD] = [RegD.r15, RegD.r14, RegD.r13, RegD.r12, RegD.r11, RegD.r10]
    available_32:list[RegD] = [RegD.r15d, RegD.r14d, RegD.r13d, RegD.r12d, RegD.r11d, RegD.r10d]
    available_16:list[RegD] = [RegD.r15w, RegD.r14w, RegD.r13w, RegD.r12w, RegD.r11w, RegD.r10w]
    available_8:list[RegD] = [RegD.r15b, RegD.r14b, RegD.r13b, RegD.r12b, RegD.r11b, RegD.r10b]

    available_float:list[RegD] = [RegD.xmm15, RegD.xmm14, RegD.xmm13, RegD.xmm12, RegD.xmm11, RegD.xmm10, RegD.xmm9, RegD.xmm8]

    
    def __init__(self, register:str | RegisterData):
        self.data = RegisterData[register] if isinstance(register, str) else register

    def cast_to(self, size:MemorySize) -> Register:
        return Register(self.data.cast_to(size))

    @classmethod
    def free_all(cls):
        "frees all scratch registers"
        cls.available_64 = [RegD.r15, RegD.r14, RegD.r13, RegD.r12, RegD.r11, RegD.r10]
        cls.available_32 = [RegD.r15d, RegD.r14d, RegD.r13d, RegD.r12d, RegD.r11d, RegD.r10d]
        cls.available_16 = [RegD.r15w, RegD.r14w, RegD.r13w, RegD.r12w, RegD.r11w, RegD.r10w]
        cls.available_8 = [RegD.r15b, RegD.r14b, RegD.r13b, RegD.r12b, RegD.r11b, RegD.r10b]
        cls.available_float = [RegD.xmm15, RegD.xmm14, RegD.xmm13, RegD.xmm12, RegD.xmm11, RegD.xmm10, RegD.xmm9, RegD.xmm8]


    def free(self):
        rname = self.data.name[:3]
        if self.data.name.startswith("xmm"):
            self.available_float.append(self.data)
        elif RegD[f"{rname}q"] not in self.available_64:
            self.available_64.append(RegD[f"{rname}"])
            self.available_32.append(RegD[f"{rname}d"])
            self.available_16.append(RegD[f"{rname}w"])
            self.available_8.append(RegD[f"{rname}b"])

    @classmethod
    def __request_wrapper(cls, reg_list:list[RegD], size:int|Literal["float"]) -> Register:
        try:
            reg = reg_list.pop()
            if size != "float":
                if size != 64:
                    cls.available_64.pop()
                if size != 32:
                    cls.available_32.pop()
                if size != 16:
                    cls.available_16.pop()
                if size != 8:
                    cls.available_8.pop()
                if c_reg:=reg.get_callee_saved():
                    Program.current_function.push_callee_saved(cls(c_reg))
            return cls(reg)
        except IndexError as _:
            raise RuntimeError(f"Ran out of {size} bit scratch registers.")

    @classmethod
    def request_float(cls) -> Register:
        return cls.__request_wrapper(cls.available_float, "float")

    @classmethod
    def request_64(cls) -> Register:
        return cls.__request_wrapper(cls.available_64, 64)

    @classmethod
    def request_32(cls) -> Register:
        return cls.__request_wrapper(cls.available_32, 32)

    @classmethod
    def request_16(cls) -> Register:
        return cls.__request_wrapper(cls.available_16, 16)

    @classmethod
    def request_8(cls) -> Register:
        return cls.__request_wrapper(cls.available_8, 8)

    @property
    def name(self) -> str:
        return self.data.register_name

    @property
    def size(self) -> MemorySize:
        return self.data.size

    @property
    def position(self) -> Literal[0,1]:
        """
        return 0 if upper bytes, return 1 if lower bytes
        """
        return self.data.position

    def __eq__(self, other:Register):
        return self.data == other.data

    def __gt__(self, other:Register):
        return self.size.value > other.size.value

    def __lt__(self, other:Register):
        return self.size.value > other.size.value

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"({self.name}[{self.size}] : {'lower' if self.position else 'upper'})"

InstructionDataType = tuple[str, list[list[MemorySize|type|int]], list[MemorySize|type|int|str|tuple[str,str]|None|Block]]
#                          [name, argument permutations (literal integers identify a wildcard size match group), return memory (None means for all permutations, value of str of num means use the same size as that index in the permutation; if str is reg name it loads into that specific reg; val of None means unknown)]

class OffsetRegister(Register):
    def __init__(self, register:Register, offset:str, negative:bool = False):
        self.register = register
        self.offset = offset
        self.negative = negative

    @property
    def name(self):
        return self.register.name

    @property
    def size(self):
        return self.register.size

    @property
    def position(self):
        return self.register.position

    def __str__(self)->str:
        return f"{self.size.name}[{self.name}"+ ("-" if self.negative else "+") +f"{self.offset}]"

class Variable:
    def __init__(self, name:str, size:MemorySize, value:list|int = None):
        self.name = name
        self.size = size
        self.value = value
        self.empty = isinstance(self.value, int)
        
    def write(self) -> str:
        return str(self)
    def __str__(self)->str:
        return f"{self.size.name}[{self.name}]"
    def __getitem__(self, offset:str) -> Variable|OffsetVariable:
        return OffsetVariable(self, offset)

    def declare(self):
        return f"{self.name} {self.size.sec_bss_write if self.empty else self.size.sec_data_write} " + ", ".join(str(a) for a in self.value)


class OffsetVariable(Variable):
    def __init__(self, variable:Variable, offset:str, negative:bool = False):
        self.variable = variable
        self.offset = offset
        self.negative = negative

    @property
    def name(self):
        return self.variable.name

    @property
    def size(self):
        return self.variable.size

    @property
    def value(self):
        return self.variable.value

    def __str__(self)->str:
        return f"{self.size.name}[{self.name}"+ ("-" if self.negative else "+") +f"{self.offset}]"

#redefine enum meta to handle builtin enum names
class InstructionDataEnumMeta(EnumMeta):
    def __getitem__(cls, name):
        return super().__getitem__(
            f"{name}_" if 
            name in {"and", "or", "not", "int"}
            else name
        )

class InstructionData(Enum, metaclass=InstructionDataEnumMeta):
    # this class's enums contains sizes, number of args etc to validate instructions
    mov:InstructionDataType = ("mov", [[0, 1], [0, int], [0, str]], [0,0,0])
    movsx:InstructionDataType = ("movsx", [[0, 1], [0, int], [0, str]], [0,0,0])
    movzx:InstructionDataType = ("movzx", [[0, 1], [0, int], [0, str]], [0,0,0])
    add:InstructionDataType = ("add", [[0, 0], [0, int], [0, str], [0], [int], [str]], [0,0,0,"0",None,None])
    sub:InstructionDataType = ("sub", [[0, 0], [0, int], [0, str], [0], [int], [str]], [0,0,0,"0",None,None])

    mul:InstructionDataType = ("mul", [[0], [int], [str]], ["0", None, None])
    div:InstructionDataType = ("div", [[0]], [("0","0")])

    imul:InstructionDataType = ("imul", [[0, 0, 0], [0, 0, int], [0, 0, str],[0, 0], [0, int], [0, str], [0], [int], [str]], ["0", "0", "0", "0", "0", "0","0", None, None])
    idiv:InstructionDataType = ("idiv", [[0]], [("0","0")])

    inc:InstructionDataType = ("inc", [[0]], [0])
    dec:InstructionDataType = ("dec", [[0]], [0])
    syscall:InstructionDataType = ("syscall", [[]], [])
    ret:InstructionDataType = ("ret", [[]], [])
    cdq:InstructionDataType = ("cdq", [[]], [])

    push:InstructionDataType = ("push", [[MemorySize.QWORD]], [None])
    pop:InstructionDataType = ("pop", [[MemorySize.QWORD]], [0])
    
    cmp:InstructionDataType = ("cmp", [[0, 0], [0, int], [0, str]], [0,0,0])
    test:InstructionDataType = ("test", [[0, 0], [0, int], [0, str]], [0,0,0])

    and_:InstructionDataType = ("and", [[0, 0], [0, int], [0, str]], [0,0,0])
    or_:InstructionDataType = ("or", [[0, 0], [0, int], [0, str]], [0,0,0])
    xor:InstructionDataType = ("xor", [[0, 0], [0, int], [0, str]], [0,0,0])
    not_:InstructionDataType = ("not", [[0]], [0])
    neg:InstructionDataType = ("neg", [[0]], [0])
    shl:InstructionDataType = ("shl", [[0, 0], [0, int], [0, str]], [0,0,0])
    shr:InstructionDataType = ("shr", [[0, 0], [0, int], [0, str]], [0,0,0])
    sar:InstructionDataType = ("sar", [[0, 0], [0, int], [0, str]], [0,0,0])
    rol:InstructionDataType = ("rol", [[0, 0], [0, int], [0, str]], [0,0,0])
    ror:InstructionDataType = ("ror", [[0, 0], [0, int], [0, str]], [0,0,0])

    call:InstructionDataType = ("call", [[Block]], [Block])
    jmp:InstructionDataType = ("jmp", [[Block]], [Block])
    loop:InstructionDataType = ("loop", [[Block]], [Block])
    jne:InstructionDataType = ("jne", [[Block]], [Block])
    jle:InstructionDataType = ("jle", [[Block]], [Block])
    jl:InstructionDataType = ("jl", [[Block]], [Block])
    jge:InstructionDataType = ("jge", [[Block]], [Block])
    jg:InstructionDataType = ("jg", [[Block]], [Block])
    je:InstructionDataType = ("je", [[Block]], [Block])
    jz:InstructionDataType = ("jz", [[Block]], [Block])
    jnz:InstructionDataType = ("jnz", [[Block]], [Block])

    lea:InstructionDataType = ("lea", [[0,1]], [0])

    nop:InstructionDataType = ("nop", [[]], [])
    clc:InstructionDataType = ("clc", [[]], [])
    stc:InstructionDataType = ("stc", [[]], [])
    cld:InstructionDataType = ("cld", [[]], [])
    std:InstructionDataType = ("std", [[]], [])
    rep:InstructionDataType = ("rep", [[]], [])
    int_:InstructionDataType = ("int", [[int], [str]], [None,None])

    sete:InstructionDataType = ("sete", [[0]], [0])
    setz:InstructionDataType = ("setz", [[0]], [0])
    setne:InstructionDataType = ("setne", [[0]], [0])
    setnz:InstructionDataType = ("setnz", [[0]], [0])
    setg:InstructionDataType = ("setg", [[0]], [0])
    setnle:InstructionDataType = ("setnle", [[0]], [0])
    setge:InstructionDataType = ("setge", [[0]], [0])
    setnl:InstructionDataType = ("setnl", [[0]], [0])
    setl:InstructionDataType = ("setl", [[0]], [0])
    setnge:InstructionDataType = ("setnge", [[0]], [0])
    setle:InstructionDataType = ("setle", [[0]], [0])
    setng:InstructionDataType = ("setng", [[0]], [0])
    seta:InstructionDataType = ("seta", [[0]], [0])
    setnbe:InstructionDataType = ("setnbe", [[0]], [0])
    setae:InstructionDataType = ("setae", [[0]], [0])
    setnb:InstructionDataType = ("setnb", [[0]], [0])
    setnc:InstructionDataType = ("setnc", [[0]], [0])
    setb:InstructionDataType = ("setb", [[0]], [0])
    setnae:InstructionDataType = ("setnae", [[0]], [0])
    setc:InstructionDataType = ("setc", [[0]], [0])
    setbe:InstructionDataType = ("setbe", [[0]], [0])
    setna:InstructionDataType = ("setna", [[0]], [0])
    sets:InstructionDataType = ("sets", [[0]], [0])
    setns:InstructionDataType = ("setns", [[0]], [0])
    seto:InstructionDataType = ("seto", [[0]], [0])
    setno:InstructionDataType = ("setno", [[0]], [0])
    setp:InstructionDataType = ("setp", [[0]], [0])
    setpe:InstructionDataType = ("setpe", [[0]], [0])
    setnp:InstructionDataType = ("setnp", [[0]], [0])
    setpo:InstructionDataType = ("setpo", [[0]], [0])

    # floating point operations:
    fld:InstructionDataType = ("fld", [[0]], [None])
    fadd:InstructionDataType = ("fadd", [[]], [])
    fmul:InstructionDataType = ("fmul", [[]], [])
    fstp:InstructionDataType = ("fstp", [[MemorySize.QWORD]], [0])
    fistp:InstructionDataType = ("fistp", [[0]], [0])

    movq:InstructionDataType = ("movq", [[0, 1], [0, int], [0, str]], [0,0,0])
    movd:InstructionDataType = ("movd", [[0, 1], [0, int], [0, str]], [0,0,0])
    movapd:InstructionDataType = ("movapd", [[0, 1], [0, int], [0, str]], [0,0,0])
    movsd:InstructionDataType = ("movsd", [[0, 1], [0, int], [0, str]], [0,0,0])


    # int to float and vice versa

    cvtsi2sd:InstructionDataType = ("cvtsi2sd", [[0, 0]], [0])
    cvtsi2ss:InstructionDataType = ("cvtsi2ss", [[0, 0]], [0])
    cvttsd2si:InstructionDataType = ("cvttsd2si", [[0, 0]], [0]) 
    cvtsd2si:InstructionDataType = ("cvtsd2si", [[0, 0]], [0])

    # float operations

    addps:InstructionDataType = ("addps", [[0, 0], [0, int], [0, str], [0], [int], [str]], [0,0,0,"0",None,None])
    addsd:InstructionDataType = ("addsd", [[0, 0], [0, int], [0, str], [0], [int], [str]], [0,0,0,"0",None,None])
    paddq:InstructionDataType = ("paddq", [[0, 0], [0, int], [0, str], [0], [int], [str]], [0,0,0,"0",None,None])
    subsd:InstructionDataType = ("subsd", [[0, 0], [0, int], [0, str], [0], [int], [str]], [0,0,0,"0",None,None])
    subpd:InstructionDataType = ("subpd", [[0, 0], [0, int], [0, str], [0], [int], [str]], [0,0,0,"0",None,None])
    mulsd:InstructionDataType = ("mulsd", [[0, 0], [0, int], [0, str], [0], [int], [str]], [0,0,0,"0",None,None])
    mulpd:InstructionDataType = ("mulpd", [[0, 0], [0, int], [0, str], [0], [int], [str]], [0,0,0,"0",None,None])
    divsd:InstructionDataType = ("divsd", [[0, 0], [0, int], [0, str], [0], [int], [str]], [0,0,0,"0",None,None])
    divpd:InstructionDataType = ("divpd", [[0, 0], [0, int], [0, str], [0], [int], [str]], [0,0,0,"0",None,None])
    minsd:InstructionDataType = ("minsd", [[0, 0], [0, int], [0, str], [0], [int], [str]], [0,0,0,"0",None,None])
    minpd:InstructionDataType = ("minpd", [[0, 0], [0, int], [0, str], [0], [int], [str]], [0,0,0,"0",None,None])
    maxsd:InstructionDataType = ("maxsd", [[0, 0], [0, int], [0, str], [0], [int], [str]], [0,0,0,"0",None,None])
    maxpd:InstructionDataType = ("maxpd", [[0, 0], [0, int], [0, str], [0], [int], [str]], [0,0,0,"0",None,None])
    sqrtsd:InstructionDataType = ("sqrtsd", [[0, 0], [0, int], [0, str], [0], [int], [str]], [0,0,0,"0",None,None])
    sqrtpd:InstructionDataType = ("sqrtpd", [[0, 0], [0, int], [0, str], [0], [int], [str]], [0,0,0,"0",None,None])
    andpd:InstructionDataType = ("andpd", [[0, 0], [0, int], [0, str], [0], [int], [str]], [0,0,0,"0",None,None])
    orpd:InstructionDataType = ("orpd", [[0, 0], [0, int], [0, str], [0], [int], [str]], [0,0,0,"0",None,None])
    xorpd:InstructionDataType = ("xorpd", [[0, 0], [0, int], [0, str], [0], [int], [str]], [0,0,0,"0",None,None])
    hsubpd:InstructionDataType = ("hsubpd", [[0, 0], [0, int], [0, str], [0], [int], [str]], [0,0,0,"0",None,None])
    haddpd:InstructionDataType = ("haddpd", [[0, 0], [0, int], [0, str], [0], [int], [str]], [0,0,0,"0",None,None])
    cmpsd:InstructionDataType = ("cmpsd", [[0, 0], [0, int], [0, str]], [0,0,0])
    cmppd:InstructionDataType = ("cmppd", [[0, 0], [0, int], [0, str]], [0,0,0])
    comisd:InstructionDataType = ("comisd", [[0, 0], [0, int], [0, str]], [0,0,0])
    ucomisd:InstructionDataType = ("ucomisd", [[0, 0], [0, int], [0, str]], [0,0,0])

    @classmethod
    def from_py_type(cls, name:str, py_type:type) -> InstructionData:
        aliases = {}
        match py_type.__name__:
            case "int":
                pass
            case "float":
                aliases = {
                    "cmp":"comisd",
                    "add":"addsd",
                    "sub":"subsd",
                    "mul":"mulsd",
                    "div":"divsd",
                    "imul":"mulsd",
                    "idiv":"divsd",
                    "sqrt":"sqrtsd",
                    "max":"maxsd",
                    "min":"minsd"
                }

        if name in aliases:
            return cls[aliases[name]]
        return cls[name]
    
    @property
    def instruction_name(self) -> str:
        return self.value[0]

    @property
    def arguments(self) -> list[MemorySize|type|int|str|tuple[str,str]|None|Variable]:
        return self.value[1]

    @property
    def ret_key(self) -> list[MemorySize|type|int|str|tuple[str,str]|None|Variable]:
        return self.value[2]



class Instruction:
    def __init__(self, instruction:str|InstructionData, *arguments:list[Register|str|int|Variable|Block]):
        self.data = InstructionData[instruction] if isinstance(instruction, str) else instruction
        self.arguments = arguments
        self.err_msg = None
        self.__ret = None
        if not self:
            raise SyntaxError(f"Invalid instruction: \"{self}\".\nReason: {self.err_msg}")

    @property
    def name(self) -> str:
        return self.data.instruction_name

    def __str__(self):
        return f"{self.name} " + ", ".join(str(a) for a in self.arguments)

    def write(self):
        if not self:
            raise SyntaxError(f"Invalid instruction: \"{self}\".\nReason: {self.err_msg}")
        return str(self)

    def __bool__(self) -> bool:
        """
        This is where the instruction arguments are validated.
        """
        for arg_perm in self.data.arguments:
            if len(arg_perm) != len(self.arguments):
                continue

            arg_groups = {}
            for a_n, arg in enumerate(self.arguments):
                self.__ret = self.__get_ret(a_n)
                if arg_perm[a_n] is int:
                    if not isinstance(arg, int):
                        if not self.err_msg:
                            self.err_msg = f"Argument #{a_n+1} was expected to be a literal int. Got: {arg!r}"
                        break

                elif arg_perm[a_n] is str:
                    if not isinstance(arg, str):
                        if not self.err_msg:
                            self.err_msg = f"Argument #{a_n+1} was expected to be a literal str. Got: {arg!r}"
                        break

                elif isinstance(arg_perm[a_n], int):
                    if arg_perm[a_n] not in arg_groups:
                        if hasattr(arg, "size"):
                            arg_groups[arg_perm[a_n]] = arg.size
                        else:
                            if not self.err_msg:
                                self.err_msg = f"Argument #{a_n+1} was expected to be a sized type. Got: {arg!r}"
                            break
                        # break means fail and go to the next argument permutation
                    elif hasattr(arg, "size") and arg_groups[arg_perm[a_n]] == arg.size:
                        continue
                    else:
                        if not self.err_msg:
                            self.err_msg = f"Argument #{a_n+1} was expected to be a {arg_groups[arg_perm[a_n]]!r}. Got: {arg!r}"
                        break

                elif isinstance(arg_perm[a_n], MemorySize):
                    if hasattr(arg, "size"):
                        if arg_perm[a_n] != arg.size:
                            if not self.err_msg:
                                self.err_msg = f"Argument #{a_n+1} was expected to be of size {arg_perm[a_n]!r}. Got: {arg.size!r}"
                            break
                    else:
                        if not self.err_msg:
                            self.err_msg = f"Argument must be sized and #{a_n+1} was expected to be of size {arg_perm[a_n]!r}. Got: {arg!r}"
                            break
            else:return True

        return False

    def __get_ret(self, r_ind:int):
        index = self.data.ret_key[r_ind]

        if isinstance(index, int):
            if hasattr(self.arguments[index], "size"):
                return self.arguments[index]
        elif isinstance(index, str):
            int_ind = int(index)
            if hasattr(self.arguments[int_ind], "size"):
                return Register(RegisterData.from_size(self.arguments[int_ind].size))
        elif isinstance(index, tuple):
            ind_1, _ = tuple(int(i) for i in index)
            if hasattr(self.arguments[ind_1], "size"):
                if self.data.instruction_name in {"div", "idiv"}:
                    return tuple(Register(r) for r in
                        RegisterData.from_size(self.arguments[ind_1].size.shrink))
                return tuple(Register(r) for r in RegisterData.from_size(self.arguments[ind_1].size))
        return None


    def __call__(self, recorder:Program|None = None):
        if not self:
            raise SyntaxError(f"Invalid instruction: \"{self}\".\nReason: {self.err_msg}")
        (recorder if recorder else Program.CURRENT).append(self)
        return self.__ret

class Function(Block):
    # None argument gets casted to 64 bit and pushed/popped to the stack
    def __init__(self, arguments:list[Register|None], signed_args:set[int]|None = None, return_register:Register|None = None, return_signed:bool = False, label:str|None = None, ret_py_type:type = int):
        Program.FUNC_STACK.append(self)
        super().__init__(label)
        self.arguments = []
        self.stack_offset = -8
        self.signed_args = {} if signed_args is None else signed_args
        self.return_register = return_register
        self.ret_py_type = ret_py_type
        self.ctypes_restype = self.return_register.size.to_ctype(return_signed, self.ret_py_type) if self.return_register else None
        self.ctypes_arguments = []
        for a_n, arg in enumerate(arguments):
            if arg is None:
                self.stack_offset += 8
                self.arguments.append(OffsetRegister(Register("rsp"), self.stack_offset))
                self.ctypes_arguments.append(MemorySize.QWORD.to_ctype(a_n in self.signed_args))
            else:
                self.arguments.append(arg)
                self.ctypes_arguments.append(arg.size.to_ctype(a_n in self.signed_args))
        self.callee_saved_regs:list[Register] = []
        
    def push_callee_saved(self, reg:Register):
        if reg not in self.callee_saved_regs:
            self.callee_saved_regs.append(reg)

    def end_definition(self):
        Program.FUNC_STACK.pop()

    def __str__(self):
        return f"{self.label}"

    def write(self):
        return f"{self}:"+ ("".join([f"\n    push {reg}" for reg in self.callee_saved_regs]) if self.callee_saved_regs else "") + "\n    push rbp"

    def __call__(self, recorder:Program|None = None):
        (recorder if recorder else Program.CURRENT).append(self)
        (recorder if recorder else Program.CURRENT).functions[self.label] = self
        return self

    def ret(self):
        Instruction("pop", Register("rbp"))()
        for reg in self.callee_saved_regs:
            Instruction("pop", reg)()
        Instruction("ret")()

    def call(self, *arguments:list) -> Register|None:
        if len(list(filter(lambda a:not isinstance(a, OffsetRegister), self.arguments))) != len(self.arguments):
            Instruction("sub", Register("rsp"), 32)()
        for a_n, arg in reversed(list(enumerate(self.arguments))):
            d_ = "d" if hasattr(arguments[a_n], "size") and \
                arg.size == MemorySize.QWORD and \
                arguments[a_n].size == MemorySize.DWORD \
                else ""
            
            if isinstance(arg, Register):
                if arg > arguments[a_n]:
                    Instruction(("movsx" if a_n in self.signed_args else "movzx") + d_, arg, arguments[a_n])()
                else:
                    Instruction("mov", arg, arguments[a_n])()

            elif isinstance(arg, OffsetRegister):
                if arg > arguments[a_n]:
                    Instruction(("movsx" if a_n in self.signed_args else "movzx") + d_, arg, arguments[a_n])()
                else:
                    Instruction("mov", arg, arguments[a_n])()

        Instruction("call", self)()
        return self.return_register

class Memory:
    def __init__(self, text_inclusions:list[str]|None=None, **memory:dict[str, tuple[MemorySize|str, list[any]|int]]):
        self.data = {}
        self.bss = {}
        self.variables = {}
        self.text_inclusions = [] if text_inclusions is None else text_inclusions
        for label, val in memory.items():
            val_new = val if isinstance(val[0], MemorySize) else (MemorySize[val[0]], val[1])
            if isinstance(val_new[1], int):
                self.bss[label] = val_new
            elif isinstance(val_new[1], list):
                self.data[label] = val_new

            self.variables[label] = Variable(label, *val_new)

    def __getitem__(self, value:str) -> Variable:
        return self.variables[value]

    def __str__(self):
        return (
            ("section .data\n    " if self.data else "")+
            "\n    ".join(
                f"{label} {size.sec_data_write} " + ", ".join(str(a) for a in arguments)
                for label, (size, arguments) in self.data.items()
            ) + "\n"+
            ("section .bss\n    " if self.bss else "")+
            "\n    ".join(
                f"{label} {size.sec_bss_write} {arguments}"
                for label, (size, arguments) in self.bss.items()
            ) + "\nsection .text\n    " +
            "\n    ".join(self.text_inclusions)
        )

    def write(self) -> str:
        return str(self)

    def __call__(self, recorder:Program|None = None):
        (recorder if recorder else Program.CURRENT).append(self)
        return self


                
if __name__ == "__main__":
    Reg = Register
    RegD = RegisterData
    Ins = Instruction
    InsD = InstructionData
    
    ah = Reg("ah")
    al = Reg("al")
    dx = Reg("dx")
    ax = Reg("ax")
    edx = Reg("edx")
    eax = Reg("eax")
    rdx = Reg("rdx")
    rax = Reg("rax")
    rdi = Reg("rdi")
    rsi = Reg("rsi")

    Program.CURRENT.name = "test"

    Program.CURRENT.comment("Function start:")
    
    func_add_a_b = Function([rdi, rsi], return_register=rax, label="add_a_b")()

    Program.CURRENT.new_line()

    f_ret = Ins("mov", rax, func_add_a_b.arguments[0])()

    Ins("add", f_ret, func_add_a_b.arguments[1])()
    
    Program.CURRENT.new_line()

    func_add_a_b.ret()

    Program.CURRENT.compile()
    Program.CURRENT.link(args={"shared":None}, output_extension=".so")
    
    total = 0
    for _ in range(1, 101):
        total = Program.CURRENT.call("add_a_b", total, 2)
        print(total)
        print("+")
    print(f" = {total}")
    # prints 7
