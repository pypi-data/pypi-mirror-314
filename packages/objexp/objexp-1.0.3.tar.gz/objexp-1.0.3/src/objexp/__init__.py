import os
import json
import shutil

def get_terminal_size_shutil():
    return shutil.get_terminal_size((80, 20))  # Default width and height

terminal_size = get_terminal_size_shutil()


attrtype = {

    'func' : [
        "function",
        "module",
    ],
    
    'data' : [
        "int",
        "float",
        "bool",
        "str",
        "list",
        "dict",
        "set",
        "tuple",
    ],
    
    'builtin' : [
        "builtin_function_or_method",
    ],
    
    'other' : [
        "type",
        "method-wrapper",
    ]
}

attrtype_all = [vv for vv in attrtype.values()]
    

resjson = {
    "objname":"",
    "objitms":[]
}

def oxdir(oo):
    print(len(dir(oo)))
    for ooo in dir(oo):
        print(ooo)

def oxvars(oo):
    # TypeError: vars() argument must have __dict__ attribute
    print(len(vars(oo)))
    for ooo in vars(oo):
        print(ooo)


def ox(someobj="test", savefile = None, ifprint = True):
    """
    function ox list members of someobj

    param someobj: what to explor
    param savefile: "md", "json", None, if save the results to a file (md or json, or both of 2).
    param ifprint: True, False, if print the results on console.

    return: str results.

    """
    winww = terminal_size.columns-2
    print(f'Width: {terminal_size.columns}, Height: {terminal_size.lines}')
    result_content_text = "\n"
    result_content_text += "_"*winww+"\n"
    result_content_text += "\n\033[1;44m OBJ'S TYPE: \033[0m\n\n"
    result_content_text += " "*4+str(type(someobj))+"\n"
    result_content_text += "_"*winww+"\n"
    result_content_text += "\n\033[1;44m OBJ'S MEMBERS: \033[0m\n"

    resjson["objname"]=str(someobj)

    print(result_content_text) if ifprint else None


    dirlist = dir(someobj)

    dirResult_sorted = sorted(
        dirlist, 
        key=lambda x: str(type(getattr(someobj,x)))
        )


    previous_type_str = ""
    dirjson = []
    atypeitm = []
    
    
    for objitem in dirResult_sorted:
        current_type_str = str(type(getattr(someobj,objitem)))

        if (previous_type_str != current_type_str):

            dirjson.append([current_type_str,[]])
            
            previous_type_str = current_type_str

        dirjson[-1][1].append(objitem)

    resjson["objitms"]=dirjson

    for iii in dirjson:
        
        content_title_typename = iii[0]
        result_content_text += "\n"+content_title_typename+"\n"
        print("\n"+" "*4+"\033[1;40;34m "+content_title_typename[8:-2].upper()+" \033[0m\033[40;34mmembers: \033[0m") if ifprint else None
        
        content_objs_list = ""
        for jjj in iii[1]:
            content_objs_list += jjj + ", "
            
        print(" "*4+content_objs_list + "\n") if ifprint else None
        result_content_text += content_objs_list + "\n"

    if savefile == "md" or savefile == "both":
        with open("objexp"+".md",'w', encoding="UTF-8") as ff:
            ff.write(result_content_text)

    if savefile == "json" or savefile == "both":
        with open("objexp"+".json",'w', encoding="UTF-8") as ff:
            ff.write(json.dumps(resjson))
    
    return result_content_text


# vars() is alternative to dirs()
if False:
    vvv = vars().copy()
    for kk,vv in vvv.items():
        print(kk,type())
        
if __name__=="__main__":
    ox()