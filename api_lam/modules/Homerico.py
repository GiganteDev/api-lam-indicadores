import ctypes, dotenv, os

dotenv.load_dotenv(dotenv.find_dotenv())

#Informa o caminho da dll
MyDllObject = ctypes.cdll.LoadLibrary(os.path.dirname(os.path.abspath(__file__)) + '/homerico.dll')
#Declare a função que deseja usar e seus parâmetros
Validar = MyDllObject.Validar
Validar.restype = ctypes.c_wchar_p
Validar.argtypes = [ctypes.c_wchar_p]
Validar("homerico.avb")

Login = MyDllObject.Login
Login.restype = ctypes.c_wchar_p
Login.argtypes = [ctypes.c_wchar_p,ctypes.c_wchar_p]
Login(os.getenv('user'), os.getenv('pass'))

RelatorioLista = MyDllObject.RelatorioLista
RelatorioLista.restype = ctypes.c_wchar_p
RelatorioLista.argtypes = [ctypes.c_wchar_p,ctypes.c_wchar_p,ctypes.c_wchar_p]
#print(RelatorioLista("01/05/2021","30/06/2021","6"))

RelatorioGerencialReport = MyDllObject.RelatorioGerencialReport
RelatorioGerencialReport.restype = ctypes.c_wchar_p
RelatorioGerencialReport.argtypes = [ctypes.c_wchar_p,ctypes.c_wchar_p]
#print(RelatorioGerencialReport("07/05/2021","16"))

RelatorioBoletim = MyDllObject.RelatorioBoletim
RelatorioBoletim.restype = ctypes.c_wchar_p
RelatorioBoletim.argtypes = [ctypes.c_wchar_p,ctypes.c_wchar_p]
#print(RelatorioBoletim("13/05/2021","13/05/2021","12"))

ProducaoLista = MyDllObject.ProducaoLista
ProducaoLista.restype = ctypes.c_wchar_p
ProducaoLista.argtypes = [ctypes.c_wchar_p,ctypes.c_wchar_p]
#print(ProducaoLista("19/05/2021","2361"))

#Informar a data desejada e o código do registro(vai retornar os dados do registro filtrado)
RelatorioGerencialRegistro = MyDllObject.RelatorioGerencialRegistro
RelatorioGerencialRegistro.restype = ctypes.c_wchar_p
RelatorioGerencialRegistro.argtypes = [ctypes.c_wchar_p,ctypes.c_wchar_p]
# data, código registro
# print(RelatorioGerencialRegistro("01/05/2020","2"))

