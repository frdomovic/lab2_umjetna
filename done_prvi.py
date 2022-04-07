from queue import Queue
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
        temp_arr.sort()
        temp_set.add(" v ".join(temp_arr))
    return temp_set
def resolution_algorithm(cset,indexing,final_c):
    clauses_set = cset
    clauses_indexing = indexing
    final_clause = final_c
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
        clauses_indexing[c] = len(clauses_indexing)
    while(True):
        result_clauses = set()
        flag = False
        clauses_set = redundant_check(clauses_set,sos)
        c1,c2 = selectClauses(clauses_set,sos,used_pairs_dict)
        if(c1 != "none" and c2 !="none"):
            resolvents = plResolve(c1,c2)
            if(resolvents != "none"):
                parent_tree[resolvents] = {c1,c2}
            if resolvents == "NIL":
                index = 1
                clauses_indexing[resolvents] = len(clauses_indexing)
                for i in clauses_indexing:
                    if(index <= len(cset)):
                        print(str(clauses_indexing[i]+1)+". "+i)
                        index += 1
                    elif(index == len(cset)+1):
                        print(str(clauses_indexing[i]+1)+". "+i)
                        print("===============")
                        index += 1
                novi = {}
                queue = Queue()
                queue.put(resolvents)
                a,b = parent_tree[resolvents]
                novi[resolvents] = {clauses_indexing[a]+1,clauses_indexing[b]+1}
                while not queue.empty():
                    node = queue.get()
                    if(node in parent_tree and parent_tree[node]):
                        a,b = parent_tree[node]
                        novi[node] = {clauses_indexing[a]+1,clauses_indexing[b]+1}
                        if(a):
                            queue.put(a)
                        if(b):
                            queue.put(b)       
                for k in reversed(novi):
                    a,b = novi[k]
                    print(str(clauses_indexing[k]+1)+". "+k+" ("+str(a)+" , "+str(b)+")")
                print("===============")
                print("[CONCLUSION]: "+final_c+" is true")
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
            clauses_indexing[resolvents] = len(clauses_indexing)
            result_clauses.add(resolvents)
        else:
            index = 0
            for i in clauses_indexing:
                if(index <= len(cset)):
                    print(str(clauses_indexing[i]+1)+". "+i)
                    index += 1
                elif(index == len(cset)+1):
                    print(str(clauses_indexing[i]+1)+". "+i)
                    print("===============")
                    index += 1
            print("[CONCLUSION]: "+final_c+" is unknown")
            return   
        if not flag:
            index = 0
            for i in clauses_indexing:
                if(index <= len(cset)):
                    print(str(clauses_indexing[i]+1)+". "+i)
                    index += 1
                elif(index == len(cset)+1):
                    print(str(clauses_indexing[i]+1)+". "+i)
                    print("===============")
                    index += 1
            print("[CONCLUSION]: "+final_c+" is unknown")
            return
        tmp_sos = redundant_check(result_clauses,sos)
        sos = sos.union(tmp_sos)
def main():
    clauses_set = set()
    clauses_indexing = {}
    final_clause = ""
    with open("resolution_small_example.txt", "r") as f:
            temp_list = f.readlines()
            for i in range(0,len(temp_list)-1):
                if "#" not in temp_list[i] and temp_list[i]  != "\n":
                    clause = temp_list[i].strip().lower().split(" v ")
                    clause.sort()
                    clause = " v ".join(clause)
                    clauses_set.add(clause)
                    clauses_indexing[clause] = len(clauses_indexing)       
            final_clause = temp_list[-1].lower()
    resolution_algorithm(clauses_set,clauses_indexing,final_clause)  
main()