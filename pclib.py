import os
import pygame
import time
import keyboard as kb
os.system("cls")

pygame.mixer.init()
sd = pygame.mixer.Sound("диск.mp3")

class ramsec8:
    class RamError(Exception):
        """Общая ошибка озу-накопителей"""
    class LimitSectorsError(RamError):
        """Ошибка лимита секторов"""
    def __init__(self, sectors: int = 32):
        if sectors <= 32:
            if sectors % 8 == 0 and sectors > 0:
                self.secs = {k: "" for k in range(sectors)}
            else:
                raise ValueError("Количество секторов должно быть кратным к 8 и больше ноля!")
            self.max = 8
            self.limit = 32
        else:
            raise self.LimitSectorsError("Более 32 секторов сейчас, надо мене 32 секторов или же 32 сектора!")
    
    def __getitem__(self, index: int):
        return self.secs[index]
    
    def __setitem__(self, index: int, value: str):
        if len(value) > self.max:
            raise ValueError("Слишком большое значение для хранения")
        if index < self.limit:
            self.secs[index] = value
        else:
            raise IndexError("В плашке ОЗУ не меняется количество секторов!")
    
    def __delitem__(self, index: int):
        if index < self.limit:
            self.secs[index] = ""
        else:
            raise IndexError("В плашке ОЗУ не меняется количество секторов!")

class ramsec16:
    class RamError(Exception):
        """Общая ошибка озу-накопителей"""
    class LimitSectorsError(RamError):
        """Ошибка лимита секторов"""

    def __init__(self, sectors: int = 64):
        if sectors <= 64:
            if sectors % 16 == 0 and sectors > 0:
                self.secs = {k: "" for k in range(sectors)}
            else:
                raise ValueError("Количество секторов должно быть кратным к 16 и больше ноля!")
            self.max = 16
            self.limit = 64
        else:
            raise self.LimitSectorsError("Более 64 секторов сейчас, надо мене 64 секторов или же 64 сектора!")
    
    def __getitem__(self, index: int):
        return self.secs[index]
    
    def __setitem__(self, index: int, value: str):
        if len(value) > self.max:
            raise ValueError("Слишком большое значение для хранения")
        if index < self.limit:
            self.secs[index] = value
        else:
            raise IndexError("В плашке ОЗУ не меняется количество секторов!")
    
    def __delitem__(self, index: int):
        if index < self.limit:
            self.secs[index] = ""
        else:
            raise IndexError("В плашке ОЗУ не меняется количество секторов!")
    
    def __contains__(self, item: str):
        return item in self.secs.values()
    
    def index(self, item: str) -> int | list:
        values = []
        for k, v in self.secs.items():
            if item == v:
                values.append(k)
        if len(values) == 1:
            return values[0]
        elif len(values) == 0:
            return 0
        else:
            return values
    
    def useds(self) -> dict[int, str]:
        values = {}
        for k, v in self.secs.items():
            if v:
                values[k] = v
        return values
    
    def frees(self) -> dict[int, str]:
        values = {}
        for k, v in self.secs.items():
            if v == "":
                values[k] = v
        return values
    
    def stata(self) -> tuple[int, int]:
        return len(self.useds().values()), len(self.frees().values())
    
    def __eq__(self, other: "ramsec16"):
        return self.secs == other.secs
    
    def __ne__(self, other: "ramsec16"):
        return not self == other

class ramsec32:
    class RamError(Exception):
        """Общая ошибка озу-накопителей"""
    class LimitSectorsError(RamError):
        """Ошибка лимита секторов"""

    def __init__(self, sectors: int = 256):
        if sectors <= 256:
            if sectors % 32 == 0 and sectors > 0:
                self.secs = {k: "" for k in range(sectors)}
            else:
                raise ValueError("Количество секторов должно быть кратным к 32 и больше ноля!")
            self.max = 32
            self.limit = 256
        else:
            raise self.LimitSectorsError("Более 256 секторов сейчас, надо мене 256 секторов или же 256 сектора!")
    
    def __getitem__(self, index: int):
        return self.secs[index]
    
    def __setitem__(self, index: int, value: str):
        if len(value) > self.max:
            raise ValueError("Слишком большое значение для хранения")
        if index < self.limit:
            self.secs[index] = value
        else:
            raise IndexError("В плашке ОЗУ не меняется количество секторов!")
    
    def __delitem__(self, index: int):
        if index < self.limit:
            self.secs[index] = ""
        else:
            raise IndexError("В плашке ОЗУ не меняется количество секторов!")
    
    def __contains__(self, item: str):
        return item in self.secs.values()
    
    def index(self, item: str) -> int | list:
        values = []
        for k, v in self.secs.items():
            if item == v:
                values.append(k)
        if len(values) == 1:
            return values[0]
        elif len(values) == 0:
            return 0
        else:
            return values
    
    def useds(self) -> dict[int, str]:
        values = {}
        for k, v in self.secs.items():
            if v:
                values[k] = v
        return values
    
    def frees(self) -> dict[int, str]:
        values = {}
        for k, v in self.secs.items():
            if v == "":
                values[k] = v
        return values
    
    def stata(self) -> tuple[int, int]:
        return len(self.useds().values()), len(self.frees().values())
    
    def __eq__(self, other: "ramsec32"):
        return self.secs == other.secs
    
    def __ne__(self, other: "ramsec32"):
        return not self == other
    
    def my(self):
        return ramsec32

class LR2:
    class ListError(Exception):
        """Стандартная ошибка списков плашек озу"""
    class ConflictError(Exception):
        """Ошибка при конфликте между компонентами"""
    class LenPlashsError(ListError):
        "Когда некорректная длина плашек"
    def __init__(self, ram1, ram2):
        self.maintype = str
        self.classes = []
        self.plashs = []
        self.TAB = {
            ramsec8: (32, 8),
            ramsec16: (64, 16),
            ramsec32: (256, 32)
        }
        for ram in [ram1, ram2]:
            if not isinstance(ram, (ramsec8, ramsec16, ramsec32)):
                raise TypeError("Не поддержимые плашки озу")
            self.maintype = ram.__class__
            self.classes.append(ram.__class__)
            self.plashs.append(ram)
        if not self.classes == [self.maintype] * 2:
            raise self.ConflictError("Версии озу неодинаковы")
        
    def __getitem__(self, index: int) -> ramsec8 | ramsec16 | ramsec32:
        if index < 2:
            return self.plashs[index]
        raise self.LenPlashsError("Плашек всего 2!")
    
    def __setitem__(self, index: int, ram):
        if index < 2:
            if ram.__class__ == self.maintype:
                self.plashs[index] = ram
                return
            raise self.ConflictError("Версии озу неодинаковы")
        raise self.LenPlashsError("Плашек всего 2!")

    def __len__(self):
        s, l = self.TAB[self.maintype]
        return s * l * 4

class ramsec64:
    class RamError(Exception):
        """Общая ошибка озу-накопителей"""
    class LimitSectorsError(RamError):
        """Ошибка лимита секторов"""

    def __init__(self, sectors: int = 1024):
        if sectors <= 1024:
            if sectors % 64 == 0 and sectors > 0:
                self.secs = {k: "" for k in range(sectors)}
            else:
                raise ValueError("Количество секторов должно быть кратным к 64 и больше ноля!")
            self.max = 64
            self.limit = 1024
        else:
            raise self.LimitSectorsError("Более 1024 секторов сейчас, надо мене 1024 секторов или же 1024 сектора!")
    
    def __getitem__(self, index: int):
        return self.secs[index]
    
    def __setitem__(self, index: int, value: str):
        if len(value) > self.max:
            raise ValueError("Слишком большое значение для хранения")
        if index < self.limit:
            self.secs[index] = value
        else:
            raise IndexError("В плашке ОЗУ не меняется количество секторов!")
    
    def __delitem__(self, index: int):
        if index < self.limit:
            self.secs[index] = ""
        else:
            raise IndexError("В плашке ОЗУ не меняется количество секторов!")
    
    def __contains__(self, item: str):
        return item in self.secs.values()
    
    def index(self, item: str) -> int | list:
        values = []
        for k, v in self.secs.items():
            if item == v:
                values.append(k)
        if len(values) == 1:
            return values[0]
        elif len(values) == 0:
            return 0
        else:
            return values
    
    def useds(self) -> dict[int, str]:
        values = {}
        for k, v in self.secs.items():
            if v:
                values[k] = v
        return values
    
    def frees(self) -> dict[int, str]:
        values = {}
        for k, v in self.secs.items():
            if v == "":
                values[k] = v
        return values
    
    def stata(self) -> tuple[int, int]:
        return len(self.useds().values()), len(self.frees().values())
    
    def __eq__(self, other: "ramsec64"):
        return self.secs == other.secs
    
    def __ne__(self, other: "ramsec64"):
        return not self == other
    
    def my(self):
        return ramsec64

class ramsec128:
    class RamError(Exception):
        """Общая ошибка озу-накопителей"""
    class LimitSectorsError(RamError):
        """Ошибка лимита секторов"""

    def __init__(self, sectors: int = 4096):
        if sectors <= 4096:
            if sectors % 128 == 0 and sectors > 0:
                self.secs = {k: "" for k in range(sectors)}
            else:
                raise ValueError("Количество секторов должно быть кратным к 128 и больше ноля!")
            self.max = 128
            self.limit = 4096
        else:
            raise self.LimitSectorsError("Более 4096 секторов сейчас, надо мене 4096 секторов или же 4096 сектора!")
    
    def __getitem__(self, index: int):
        return self.secs[index]
    
    def __setitem__(self, index: int, value: str):
        if len(value) > self.max:
            raise ValueError("Слишком большое значение для хранения")
        if index < self.limit:
            self.secs[index] = value
        else:
            raise IndexError("В плашке ОЗУ не меняется количество секторов!")
    
    def __delitem__(self, index: int):
        if index < self.limit:
            self.secs[index] = ""
        else:
            raise IndexError("В плашке ОЗУ не меняется количество секторов!")
    
    def __contains__(self, item: str):
        return item in self.secs.values()
    
    def index(self, item: str) -> int | list:
        values = []
        for k, v in self.secs.items():
            if item == v:
                values.append(k)
        if len(values) == 1:
            return values[0]
        elif len(values) == 0:
            return 0
        else:
            return values
    
    def useds(self) -> dict[int, str]:
        values = {}
        for k, v in self.secs.items():
            if v:
                values[k] = v
        return values
    
    def frees(self) -> dict[int, str]:
        values = {}
        for k, v in self.secs.items():
            if v == "":
                values[k] = v
        return values
    
    def stata(self) -> tuple[int, int]:
        return len(self.useds().values()), len(self.frees().values())
    
    def __eq__(self, other: "ramsec128"):
        return self.secs == other.secs
    
    def __ne__(self, other: "ramsec128"):
        return not self == other
    
    def my(self):
        return ramsec128

class ramsec256:
    class RamError(Exception):
        """Общая ошибка озу-накопителей"""
    class LimitSectorsError(RamError):
        """Ошибка лимита секторов"""

    def __init__(self, sectors: int = 8192):
        if sectors <= 8192:
            if sectors % 128 == 0 and sectors > 0:
                self.secs = {k: "" for k in range(sectors)}
            else:
                raise ValueError("Количество секторов должно быть кратным к 128 и больше ноля!")
            self.max = 256
            self.limit = 8192
        else:
            raise self.LimitSectorsError("Более 8192 секторов сейчас, надо мене 8192 секторов или же 8192 сектора!")
    
    def __getitem__(self, index: int):
        return self.secs[index]
    
    def __setitem__(self, index: int, value: str):
        if len(value) > self.max:
            raise ValueError("Слишком большое значение для хранения")
        if index < self.limit:
            self.secs[index] = value
        else:
            raise IndexError("В плашке ОЗУ не меняется количество секторов!")
    
    def __delitem__(self, index: int):
        if index < self.limit:
            self.secs[index] = ""
        else:
            raise IndexError("В плашке ОЗУ не меняется количество секторов!")
    
    def __contains__(self, item: str):
        return item in self.secs.values()
    
    def index(self, item: str) -> int | list:
        values = []
        for k, v in self.secs.items():
            if item == v:
                values.append(k)
        if len(values) == 1:
            return values[0]
        elif len(values) == 0:
            return 0
        else:
            return values
    
    def useds(self) -> dict[int, str]:
        values = {}
        for k, v in self.secs.items():
            if v:
                values[k] = v
        return values
    
    def frees(self) -> dict[int, str]:
        values = {}
        for k, v in self.secs.items():
            if v == "":
                values[k] = v
        return values
    
    def stata(self) -> tuple[int, int]:
        return len(self.useds().values()), len(self.frees().values())
    
    def __eq__(self, other: "ramsec256"):
        return self.secs == other.secs
    
    def __ne__(self, other: "ramsec256"):
        return not self == other
    
    def my(self):
        return ramsec256
    
    def reset(self):
        self.secs = {k: "" for k in range(self.secs)}
    
    def as_dict(self):
        return self.secs
    
    def __len__(self):
        return len(self.secs)
    
    def writes(self, data: dict[int, str]):
        for k, v in data.items():
            self[k] = v
    
    def grafic(self) -> str:
        graf = ""
        for _, v in self.secs.items():
            graf += "=" if v else " "
        used = len(self.useds().values())
        return f"[{graf}] ({used}/{len(self)})"
    
    def clone(self):
        return self

class ramsec512:
    class RamError(Exception):
        """Общая ошибка озу-накопителей"""
    class LimitSectorsError(RamError):
        """Ошибка лимита секторов"""

    def __init__(self, sectors: int = 32768):
        if sectors <= 32768:
            if sectors % 128 == 0 and sectors > 0:
                self.secs = {k: "" for k in range(sectors)}
            else:
                raise ValueError("Количество секторов должно быть кратным к 128 и больше ноля!")
            self.max = 512
            self.limit = 32768
        else:
            raise self.LimitSectorsError("Более 32768 секторов сейчас, надо мене 32768 секторов или же 32768 сектора!")
    
    def __getitem__(self, index: int):
        return self.secs[index]
    
    def __setitem__(self, index: int, value: str):
        if len(value) > self.max:
            raise ValueError("Слишком большое значение для хранения")
        if index < self.limit:
            self.secs[index] = value
        else:
            raise IndexError("В плашке ОЗУ не меняется количество секторов!")
    
    def __delitem__(self, index: int):
        if index < self.limit:
            self.secs[index] = ""
        else:
            raise IndexError("В плашке ОЗУ не меняется количество секторов!")
    
    def __contains__(self, item: str):
        return item in self.secs.values()
    
    def index(self, item: str) -> int | list:
        values = []
        for k, v in self.secs.items():
            if item == v:
                values.append(k)
        if len(values) == 1:
            return values[0]
        elif len(values) == 0:
            return 0
        else:
            return values
    
    def useds(self) -> dict[int, str]:
        values = {}
        for k, v in self.secs.items():
            if v:
                values[k] = v
        return values
    
    def frees(self) -> dict[int, str]:
        values = {}
        for k, v in self.secs.items():
            if v == "":
                values[k] = v
        return values
    
    def stata(self) -> tuple[int, int]:
        return len(self.useds().values()), len(self.frees().values())
    
    def __eq__(self, other: "ramsec512"):
        return self.secs == other.secs
    
    def __ne__(self, other: "ramsec512"):
        return not self == other
    
    def my(self):
        return ramsec512
    
    def reset(self):
        self.secs = {k: "" for k in range(len(self))}
    
    def as_dict(self):
        return self.secs
    
    def __len__(self):
        return len(self.secs)
    
    def writes(self, data: dict[int, str]):
        for k, v in data.items():
            self[k] = v
    
    def grafic(self) -> str:
        graf = ""
        for _, v in self.secs.items():
            graf += "=" if v else " "
        used = len(self.useds().values())
        return f"[{graf}] ({used}/{len(self)})"
    
    def clone(self):
        return self
    
    def defrag(self) -> dict[int, int]:
        usery = self.useds().items()
        self.reset()
        newindexs = {}
        i = 0
        for k, v in usery:
            self[i] = v
            newindexs[k] = i
            i += 1
        return newindexs
    
    def reverse(self):
        self.secs = {k: v for k, v in zip(self.secs.keys(), self.secs.values()[::-1])}


class LR4:
    class ListError(Exception):
        """Стандартная ошибка списков плашек озу"""
    class ConflictError(Exception):
        """Ошибка при конфликте между компонентами"""
    class LenPlashsError(ListError):
        "Когда некорректная длина плашек"
    def __init__(self, ram1, ram2, ram3, ram4):
        self.maintype = str
        self.classes = []
        self.plashs = []
        self.TAB = {
            ramsec64: (1024, 64),
            ramsec128: (4096, 128),
            ramsec256: (8192, 256),
            ramsec512: (32768, 512)
        }
        for ram in [ram1, ram2, ram3, ram4]:
            if not isinstance(ram, (ramsec64, ramsec128, ramsec256, ramsec512)):
                raise TypeError("Не поддержимые плашки озу")
            self.maintype = ram.__class__
            self.classes.append(ram.__class__)
            self.plashs.append(ram)
        if not self.classes == [self.maintype] * 4:
            raise self.ConflictError("Версии озу неодинаковы")
        
    def __getitem__(self, index: int) -> ramsec64 | ramsec128 | ramsec256 | ramsec512:
        if index < 4:
            return self.plashs[index]
        raise self.LenPlashsError("Плашек всего 4!")
    
    def __setitem__(self, index: int, ram):
        if index < 4:
            if ram.__class__ == self.maintype:
                self.plashs[index] = ram
                return
            raise self.ConflictError("Версии озу неодинаковы")
        raise self.LenPlashsError("Плашек всего 4!")

    def __len__(self):
        s, l = self.TAB[self.maintype]
        return s * l * 4

class Disks:
    "Утилита для списка дисков"
    class Disk:
        class DiskError(Exception):
            "Стандартная ошибка чтения и записи дисков"
        
        class SectorError(DiskError):
            "Ошибка секторов"
        
        class ReadError(SectorError):
            "Ошибка чтения сектора"
        
        class WriteError(SectorError):
            "Ошибка чтения сектора"

        class Sector:
            "Сектор на 512"
            def __init__(self, value: str):
                if len(value) < 513:
                    self.data = value
                else:
                    raise ValueError("Длина сектора более 512 символов!")
            
            def __str__(self):
                return self.data
            
            def load(self, data):
                if isinstance(data, (self.__class__, str)):
                    if isinstance(data, str):
                        self.data = data
                    else:
                        self.data = data.data
                    if len(self.data) > 512:
                        raise ValueError("Длина сектора более 512 символов!")
                raise TypeError("Значение не сектор и не строка")

        def __init__(self, name: str):
            self.name = name
            self.path = "disks/" + name
        
        def __sc(self, x: int): # Шустрая проверка
            return x > -1
        
        def __getitem__(self, x: int):
            if self.__sc(x):
                time.sleep(0.01)
                sd.play()
                try:
                    with open(f"{self.path}/{str(x)}.sector", encoding="utf-8") as file:
                        return self.Sector(file.read())
                except:
                    raise self.ReadError(f"Ошибка чтения сектора {str(x)}")
            else:
                raise ValueError("Сектор не может быть не положительным числом")
        
        def __setitem__(self, x: int, data: Sector):
            if self.__sc(x):
                time.sleep(0.02)
                sd.play()
                try:
                    with open(f"{self.path}/{str(x)}.sector", "w", encoding="utf-8") as file:
                        file.write(str(data))
                except:
                    raise self.WriteError(f"Ошибка записи сектора {str(x)}")
            else:
                raise ValueError("Сектор не может быть не положительным числом")

    class Real:
        "Класс для реальных операций созданных на абстрактной основе"
        class RealError(Exception):
            "Стандартная ошибка реальных операций"

        def __init__(self):
            self.disks = os.listdir("disks")
        
        def append(self, new: str, sectors: int):
            if not new in self.disks:
                self.disks.append(new)
                os.mkdir(f"disks/{new}")
                for i in range(sectors):
                    with open(f"disks/{new}/{i}.sector", "w") as file:
                        file.write("")
            else:
                raise self.RealError("Такой диск уже существует!")
        
        def remove(self, fordel: str):
            if fordel in self.disks:
                self.disks.remove(fordel)
                os.system(f'rmdir /s /q "disks/{fordel}"')
            else:
                raise self.RealError("Такой диск не существует!")
        
        def exist(self, disk: str):
            return os.path.exists(f"disks/{disk}")
    
    class Virt:
        def __init__(self, parent: "Disks"):
            self.parent = parent
        
        def get(self, name: str):
            disks = self.parent.real.disks
            if name in disks:
                return self.parent.Disk(name)
            else:
                raise KeyError("Диск не найден")

    def __init__(self):
        self.real = self.Real()
        self.virt = self.Virt(self)

class Console:
    def __init__(self, ram: ramsec8 | ramsec16 | ramsec32 | ramsec64 | ramsec128 | ramsec256 | ramsec512):
        self.ram = ram
    
    def drobic(self, string: str, k: int):
        new = []
        t = ""
        for l in string:
            if len(t) == k:
                new.append(t)
                t = ""
            t += l
        if len(new) != 0:
            if len(t) != 0:
                new.append(t)
        return new
    
    def update(self):
        os.system("cls")
        i = 0
        l = []
        while True:
            try:
                l.append(self.ram[i].replace("\\n", '\n'))
            except:
                break
            i += 1
        nl = []
        y = False
        for string in l:
            if not y:
                nl.append("")
            if string:
                string = string.replace("\\p", "")
            else:
                continue
            for i in string:
                if i == "\t":
                    y = True
                elif i == "\r":
                    y = False
                else:
                    nl[len(nl) - 1] += i
        print("\n".join(nl))
    
    def __getitem__(self, index: int):
        return self.ram[index]
    
    def __setitem__(self, index: int, value: str):
        self.ram[index] = value
    
    def __delitem__(self, index: int):
        del self.ram[index]
    
    def __len__(self):
        i = 0
        while True:
            try:
                if self.ram[i] == "":
                    break
                i += 1
            except:
                break
        return i
    
    def __call__(self, message: str, output: bool = True):
        if message == "": message = "\\p"
        message = message.replace("\n", "\\n")
        self.ram[len(self)] = message
        if output: self.update()
    
    def clear(self):
        i = 0
        while True:
            try:
                self.ram[i] = ""
            except:
                break
            i += 1
        os.system("cls")
    
class BIOS:
    def __init__(self, lr: LR2 | LR4, diskIterface: Disks):
        self.lr = lr
        self.di = diskIterface
        self.cl = Console(lr[0])
    
    def biosing(self):
        return self.di.virt.get("disk")
    
    def first(self, boot: bool = True):
        return self.biosing()[7] if boot else self.biosing()[0]
    
    def booting(self):
        exec(str(self.first()))
    
    def interface(self):
        exec(str(self.first(False)))
    
    def start(self):
        self.cl("**** **\t", False)
        self.cl("**\r", False)
        self.cl("**** **\t", False)
        self.cl("**\r", False)
        self.cl("**** **\t", False)
        self.cl("**\r", False)
        self.cl("**** **\t", False)
        self.cl("**\r", False)
        self.cl("BIOS ST\t", False)
        self.cl("ARTED\r")
        time.sleep(0.5)
        self.cl.clear()
        self.cl("-------\t", False)
        self.cl("-------", False)
        self.cl("-------\r")
        self.cl("RAM: \t", False)
        self.cl(str(len(self.lr) / 1024) + "KB\n")
        self.cl(f"DISKNAM\t", False)
        self.cl("E: ", False)
        self.cl(f"{self.biosing().name}\r")
        self.cl("-------\t", False)
        self.cl("-------", False)
        self.cl("-------\r")
        time.sleep(1.0)
        self.cl(".")
        start = time.time()
        while time.time() - start < 5:
            if kb.is_pressed("del"):
                self.interface()
                self.cl.clear()
                self.start()
        self.cl[11] = "START O\t"
        self.cl("S...\r")
        time.sleep(1.0)
        self.booting()
        self.cl("[END]")
