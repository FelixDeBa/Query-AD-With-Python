import subprocess

class UserNotFound(Exception):
    def __init__(self,msg=None):
        self.msg = msg
        print("Error: User Not Found")
        

def execute_command(columns:str="", properties:str="", search_base:str="", ad_filter:str="", out_format:str="csv", user:str=""):
    if out_format != "csv" and out_format != "":
        raise EOFError("Por el momento solo aceptamos formato CSV o sin formato")
    
    columns = f" | Select {columns}" if not(columns is None or columns == "") else ""
    ad_filter = f" -Filter {ad_filter}" if not(ad_filter == "" or ad_filter is None) else ""
    out_format = " | ConvertTo-" + out_format if not(out_format is None or out_format == "") else "| ConvertTo-Csv"
    properties = f" -Properties \\\"{properties}\\\"" if not (properties is None or properties == "") else ""
    search_base = f" -SearchBase \\\"{search_base}\\\"" if not(search_base is None or search_base == "") else ""
    user = f" -Identity {user}" if not(user is None or user == "") else ""
    
    command = f"%SystemRoot%\\system32\\WindowsPowershell\\v1.0\\powershell.exe -command \"Get-AdUser{user}{ad_filter}{properties}{search_base}{columns}{out_format}\""
    
    # print(command)
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()

    if not err:
        return((str(out.decode("CP437"))).split('\r\n')[1:-1])
    else:
        print(err)

def find_user(user:str, columns:str="SamAccountName,Name,UserPrincipalName,Enabled"):
    found_user = execute_command(user=user, columns=columns)
    if found_user == []:
        raise UserNotFound(f"User {user} Not Found")
    else:
        return found_user
    

def ad_users(columns:str=""):
    users = execute_command(ad_filter="*")
    return users    

def enabled_users(columns:str="SamAccountName,Name,UserPrincipalName,Enabled", out_format:str="csv"):
    enabled_filter = "{Enabled -eq $True}"
    
    usuarios = execute_command(ad_filter=enabled_filter, columns=columns)
    return usuarios

def disabled_users(columns:str="SamAccountName,Name,UserPrincipalName,Enabled", out_format:str="csv"):
    enabled_filter = "{Enabled -eq $False}"
        
    usuarios = execute_command(ad_filter=enabled_filter, properties="LockedOut", columns=columns, out_format=out_format)
    return usuarios
        

#para usuarios en cuarentena la ou debe ser Cuarentena y el dc es DC=cerrey,dc=com,dc=mx
def filter_by_ou(ou:str, dc:str, columns:str="SamAccountName,Name,UserPrincipalName,Enabled", out_format:str="csv", ad_filter:str="*"):
        
    usuarios = execute_command(properties="LockedOut", search_base=f"OU={ou},{dc}", columns=columns, ad_filter=ad_filter)
    return usuarios
        
        
def dump_csv(user_list:list, filename:str, path:str="./"):
    with open(f"{path}{filename}", 'w', encoding="utf8") as file:
        file.write('\n'.join(user_list))
        return "File saves successfully"
