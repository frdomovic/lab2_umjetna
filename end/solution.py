import sys
from queue import Queue
import operator
def tautology_check(resolvents):
    literal_list = resolvents.split(" v ")
    new_literals = set()
    for lit in literal_list:
        nlit = str("~"+lit).replace("~~","")
        if nlit not in literal_list:
            new_literals.add(lit)
    if new_literals:
        new_literals = list(new_literals)
        return " v ".join(new_literals)
    else:
        return None
def tautology_check_set(t_set):
    removed_tautology_set = set()
    for t in t_set:
        for t1 in t_set:
            if(t == t1):
                continue
            st = set(t.split(" v "))
            st1 = set(t1.split(" v "))
            if(st.issubset(st1)):
                removed_tautology_set.add(t)
    new_set = set()
    for t in t_set:
        st = set(t.split(" v "))
        for c in removed_tautology_set:
            sc = set(c.split(" v "))
            if(not sc.issubset(st)):
                new_set.add(t)
            elif(sc == st):
                new_set.add(t)
    return new_set
def plResolve(c1,c2):
    c1_lats = c1.split(" v ")
    c2_lats = c2.split(" v ")
    new_clause = set()
    resolved_clauses = set()
    for lat1 in c1_lats:
        for lat2 in c2_lats:
            if lat1.replace("~","") == lat2.replace("~","") and lat1 != lat2:
                resolved_clauses.add(lat1)
                resolved_clauses.add(lat2)
    for c0 in c1_lats:
        if c0 not in resolved_clauses:
            new_clause.add(c0)
    for c0 in c2_lats:
        if c0 not in resolved_clauses:
            new_clause.add(c0)
    if (len(new_clause) > 1):
        temp_l = list(new_clause)
        temp_l.sort()
        return " v ".join(temp_l)
    elif(len(new_clause) == 1):
        return new_clause.pop()
    else:
        return "NIL"
def compatable_resolvation(c1,c2):
    c1_lats = set(c1.split(" v "))
    c2_lats = set(c2.split(" v "))
    for lat1 in c1_lats:
        for lat2 in c2_lats:    
            if lat1.replace("~","") == lat2.replace("~","") and lat1 != lat2:
                return True
    return False
def selectClauses(clause_set,sos_set,used_dict):
    for c1 in clause_set:
        for c2 in sos_set:
            if (compatable_resolvation(c1,c2)) and ((c1,c2) not in used_dict) and ((c2,c1) not in used_dict):
                return c1,c2
    for c1 in sos_set:
        for c2 in sos_set:
            if (c1 == c2):
                continue
            elif (compatable_resolvation(c1,c2)) and ((c1,c2) not in used_dict) and ((c2,c1) not in used_dict):
                return c1,c2
    return "none","none"
def redundant_check(set1,set2):
    new_clauses = set()
    for c1 in set1:
        flag = True
        for c2 in set2:
            temp_c1 = set(c1.split(" v "))
            temp_c2 = set(c2.split(" v "))
            if c1 != c2 and temp_c2.issubset(temp_c1):
                flag = False
        if(flag):
            new_clauses.add(c1)
    return new_clauses
def clause_negation(K):
    temp_set = set()
    if "v" not in K:
        temp_set.add(str("~"+K.strip()).replace("~~",""))
    else:
        K = K.split(" v ")
        K.sort()
        temp_arr = []
        for literal in K:
            temp_arr.append(str("~"+literal.strip()).replace("~~",""))
        for c in temp_arr:
            temp_set.add(c)
    return temp_set
def resolve_plng(cset):
    new_set = set()
    for c in cset:
        sc = c.split(" v ")
        tmp_set = set()
        for c2 in sc:
            
            if ("~" in c2 and c2.replace("~","") in sc) or ("~" not in c2 and str("~"+c2) in sc):
                break
            else:
                tmp_set.add(c2)
        if(tmp_set):
            new_set.add(" v ".join(list(tmp_set)))
    return new_set
def resolution_algorithm(cset,indexing,final_c):
    clauses_set = cset.copy()
    clauses_indexing = dict(indexing)
    final_clause = ''+final_c
    used_pairs_dict = {}
    starting_data = {} 
    parent_tree = {}
    sos = clause_negation(final_clause)
    for c in clauses_set:
        starting_data[c] = 0
        parent_tree[c] = None
    for c in sos:
        starting_data[c] = 0
        parent_tree[c] = None
        clauses_indexing[c] = len(clauses_indexing)+1
    while(True):
        result_clauses = set()
        flag = False
        #clauses_set = tautology_check_set(clauses_set)
        clauses_set = resolve_plng(clauses_set)
        clauses_set = redundant_check(clauses_set,sos)
        clauses_set = redundant_check(clauses_set,clauses_set)
        c1,c2 = selectClauses(clauses_set,sos,used_pairs_dict)
        if(c1 != "none" and c2 !="none"):
            resolvents = plResolve(c1,c2)
            if(resolvents != "none"):
                parent_tree[resolvents] = {" v ".join(sorted(c1.split(" v ")))," v ".join(sorted(c2.split(" v ")))}
            if resolvents == "NIL":
                index = 1
                new_indexing = {}
                clauses_indexing[resolvents] = len(clauses_indexing)+1
                for i in clauses_indexing:
                    if(index <= len(cset)):
                        new_indexing[i] = len(new_indexing)+1
                        index += 1
                    elif(index == len(cset)+1):
                        new_indexing[i] = len(new_indexing)+1
                        index += 1
                queue = Queue()
                queue.put(resolvents)
                a,b = parent_tree[resolvents]
                new_indexing[resolvents] = len(new_indexing)      
                tmp_arr = []
                while not queue.empty():
                    node = queue.get()
                    if(node in parent_tree and parent_tree[node]):
                        a,b = parent_tree[node]
                        tmp_arr.append(node)
                        if(a):
                            queue.put(a)
                        if(b):
                            queue.put(b)
                tmp_arr = tmp_arr[::-1]
                for el in tmp_arr:   
                    new_indexing[el] = len(new_indexing)        
                sorted_x = sorted(new_indexing.items(), key=operator.itemgetter(1))
                b = int(len(cset))
                i=0
                for k in sorted_x: 
                    if(i < b):
                        print(str(k[1])+". "+str(k[0]))
                        i += 1
                    elif(i == b):
                        print(str(k[1])+". "+str(k[0]))
                        print("============")
                        i += 1
                    elif(i > b and i < len(sorted_x)):
                        a = list(parent_tree[k[0]])
                        if(a[0] in new_indexing and a[1] in new_indexing):
                            index_lista = []
                            index_lista.append(new_indexing[a[0]])
                            index_lista.append(new_indexing[a[1]])
                            index_lista.sort()
                            print(str(k[1])+". "+str(k[0])+" ("+str(index_lista[0])+" , "+str(index_lista[1])+")")
                        else:
                            continue
                print("===============")
                print("[CONCLUSION]: "+str(final_c.strip())+" is true")
                return
            used_pairs_dict[(c1,c2)] = True
            flag = True
            resolvents = tautology_check(resolvents)
            tmp = {resolvents}
            if resolvents != "none":
                if tmp.issubset(sos) or tmp.issubset(result_clauses) or tmp.issubset(clauses_set):
                    continue
            else:
                continue
            result_clauses = redundant_check(result_clauses,tmp)
            sos = redundant_check(sos,tmp)
            clauses_set = redundant_check(clauses_set,tmp)
            resol_tmp = " v ".join(sorted(resolvents.split(" v ")))
            clauses_indexing[resol_tmp] = len(clauses_indexing)
            result_clauses.add(resolvents)
        else:
            print("[CONCLUSION]: "+final_c.strip()+" is unknown")
            return   
        if not flag:
            print("[CONCLUSION]: "+final_c.strip()+" is unknown")
            return
        tmp_sos = redundant_check(result_clauses,sos)
        sos = sos.union(tmp_sos)


def main_prog():
    argv_list = " ".join(sys.argv).split(" ")
    logic_function = argv_list[1]
    clauses_list_path = argv_list[2]
    operation_list_path = ""
    try:
        if(logic_function == "cooking"):
            operation_list_path = argv_list[3]
            clauses_set = set()
            clauses_index = {}
            final_clause = ""
            with open(clauses_list_path, "r") as f:
                temp_list = f.readlines()
                for i in range(0,len(temp_list)):
                    if "#" not in temp_list[i] and temp_list[i]  != "\n":
                        clause = temp_list[i].strip().lower().split(" v ")
                        clause.sort()
                        clause = " v ".join(clause)
                        clauses_set.add(clause)
                        clauses_index[clause] = len(clauses_index)+1   
            commands = []
            with open(operation_list_path,"r") as f:
                temp_list = f.readlines()
                for el in temp_list:
                    commands.append(el.strip().lower())
            print("Constructed with knowledge:")
            for cls in clauses_set:
                print(cls)
            print()
            for command in commands:
                print("User's command: "+command)
                tmp_1 = command[0:len(command)-2]
                cmd_list = [tmp_1,command[-1]]
                if(cmd_list[1] == "?"):
                    a = resolution_algorithm(clauses_set,clauses_index,cmd_list[0])
                    print()
                elif(cmd_list[1] == "+"):
                    clauses_set.add(cmd_list[0])
                    clauses_index[cmd_list[0]] = len(clauses_index)+1
                    print("Added "+cmd_list[0]+"\n")
                elif(cmd_list[1] == "-"):
                    cls_cpy = dict(clauses_index)
                    clauses_index.clear()
                    for el in clauses_set:
                        sc1 = set(el.split(" v "))
                        sc2 = set(cmd_list[0].split(" v "))
                        if(sc1 == sc2):
                            clauses_set.remove(el)
                        for cls in cls_cpy:
                            if(cls != cmd_list[0]):
                                clauses_index[cls] = len(clauses_index)+1
                    print("removed "+cmd_list[0]+"\n")

        elif(logic_function == "resolution"):
            clauses_set = set()
            clauses_index = {}
            final_clause = ""
            with open(clauses_list_path, "r") as f:
                    temp_list = f.readlines()
                    for i in range(0,len(temp_list)-1):
                        if "#" not in temp_list[i] and temp_list[i]  != "\n":
                            clause = temp_list[i].strip().lower().split(" v ")
                            clause.sort()
                            clause = " v ".join(clause)
                            clauses_set.add(clause)
                            clauses_index[clause] = len(clauses_index)+1       
                    final_clause = temp_list[-1].lower()
            resolution_algorithm(clauses_set,clauses_index,final_clause)  
        else:
            print("WRONG INPUT!")
    except:
        print("WRONG ARGUMENTS")

main_prog()

