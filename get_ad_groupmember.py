import subprocess


def execute_command(group:str, columns:str="", out_format:str="csv"):
    if out_format != "csv" and out_format != "":
        raise EOFError("Por el momento solo aceptamos formato CSV o sin formato")
    if group=="" or group is None:
        raise EOFError("No se especificó ningún grupo")
    group=f'\\\"{group}\\\"'
    columns = f" | Select {columns}" if not(columns is None or columns == "") else ""
    out_format = " | ConvertTo-" + out_format if not(out_format is None or out_format == "") else "| ConvertTo-Csv"
        
    command = f"%SystemRoot%\\system32\\WindowsPowershell\\v1.0\\powershell.exe -command \"Get-AdGroupMember {group} -Recursive | Foreach {{Get-AdUser $_.SamAccountName -Properties EmailAddress,LockedOut}} {columns}{out_format}\""
    
    # print(command)
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()

    if not err:
        return((str(out.decode("CP437"))).split('\r\n')[1:-1])
    else:
        print(err)

#citrix for ctrix, PPTP Users for VPN
def users_of_group(group:str, out_format:str="csv", columns:str="SamAccountName,Name,EmailAddress,Enabled,LockedOut"):
    
    usuarios = execute_command(group=group, columns=columns, out_format=out_format)
    return usuarios
        
def dump_csv(user_list:list, filename:str, path:str="./"):
    with open(f"{path}{filename}", 'w', encoding="utf8") as file:
        file.write('\n'.join(user_list))
        return "File saves successfully"