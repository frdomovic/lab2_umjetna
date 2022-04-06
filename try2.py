

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
    #bolji nacin sutra dns si spaljeeeen
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

def complex_check_redundant(resolvents, result_clauses, clauses_set, sos):
    if resolvents.issubset(result_clauses) or resolvents.issubset(clauses_set) or resolvents.issubset(sos):
        return True
    elif not redundant_check(resolvents,sos) or not redundant_check(resolvents,result_clauses) or not redundant_check(resolvents,clauses_set):
        return True
    else:
        return False


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
    #treba mi mapa koju trebam ispisat
    #za roditelje  znaic [klauzula] = roditelj
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
            #print(str((c1+":"+c2))+" resolved -> "+resolvents)
            if resolvents == "NIL":
                print(parent_tree)
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
            print(final_c+" is unknown")
            return   
        if not flag:
            print(final_c+" is unknown")
            return
        tmp_sos = redundant_check(result_clauses,sos)
        sos = sos.union(tmp_sos)
    #
#1.UPIS PODATAKA DONE
def __main__():
    clauses_set = set()
    clauses_indexing = {}
    final_clause = ""
    with open("resolution_small_example.txt", "r") as f:
            temp_list = f.readlines()
            #tu treba jos sort
            for i in range(0,len(temp_list)-1):
                if "#" not in temp_list[i] and temp_list[i]  != "\n":
                    clause = temp_list[i].strip().lower().split(" v ")
                    clause.sort()
                    clause = " v ".join(clause)
                    clauses_set.add(clause)
                    clauses_indexing[clause] = len(clauses_indexing)       
            final_clause = temp_list[-1].lower()
            #potencijalni problem komentara na zadnjoj liniji i tkave gluposti
    resolution_algorithm(clauses_set,clauses_indexing,final_clause)
    
__main__()



# def clause_negation(final_clause):
#         if "v" not in final_clause:
#             if "~" in final_clause:
#                 return str(final_clause.replace("~",""))
#             else:
#                 return str("~"+final_clause)
#         else:
#             temp_clause_list = final_clause.split("v")
#             temp_final = []
#             for clause in temp_clause_list:
#                     temp_clause = "~"+clause.strip()
#                     temp_final.append(temp_clause.replace("~~",""))
#             return " v ".join(temp_final)



# #clause moze bit obican A
# #ili dupli A v B
# frozen_clauses = clauses_list
# final_clause_arr = []
# final_clause_arr.append(clause_negation(final_clause))

# def plresolve(clause,final_clause):
#     K = clause
#     G = final_clause
#     #G = ~a v ~b
#     #print(K,G)
#     if "v" in K:
#         K = K.split(" v ")
#         #literali
#         temp = []
#         for Klat in K:
#             # A ~B ~C
#             if " v " in G:
#                 # B ~ A
#                 G = G.split(" v ")
                
#                 for Glat in G:
#                     if 

#             else:
#                 #samo je jedan A - A

#                 if G[1:] == Klat:
#                     for Ki in K:
#                         if(Ki != G[1:]):
#                             temp.append(Ki)
#                 # B - A 
                
                    



#     if "v" in K:
#         K = K.split(" v ")
#         for Ki in K:
#             if G[1:] == Ki:
               
#                 temp = []
#                 for Kj in K:
#                     if (Kj != G[1:]):
#                         temp.append(Kj)
#                 return " v ".join(temp)
#         return "NOT-RES"
#     else:
#         if G[1:] == K:
#             return "NIL"
#         else:
#             return "NOT-RES"
        

# index_holder = []
# index_holder += clauses_list
# index_holder += final_clause_arr

# Flag = True
# def resolution(clauses_list,final_clause_arr,index_holder):
#     finalx = "".join(final_clause_arr)
#     for i in range(0,len(clauses_list)):
#         print(str(i+1)+". "+clauses_list[i])
#     print(str(len(clauses_list)+1)+". "+"".join(final_clause_arr))
#     print("===============")
#     index = len(clauses_list)+1
#     temp_resolvents = set(())
#     while(True):
#         for K in clauses_list:
#             for G in final_clause_arr: 
#                 resolvents = plresolve(K,G)
               
#                 if(resolvents == "NIL"):
#                         index_holder.append(lat)
#                         a = []
#                         a.append(index_holder.index(K)+1)
#                         a.append(index_holder.index(G)+1)
#                         a.sort()
#                         #print(str(len(index_holder))+". "+resolvents+" ("+str(a[0])+", "+str(a[1])+")")
#                         #print("===============")
#                         #print("[CONCLUSION]: "+"".join(finalx)+" is true")
#                         return
#                 elif resolvents.strip() != "NOT-RES" :
#                     print(resolvents)
#                     if resolvents not in temp_resolvents:
#                         temp_resolvents.add(resolvents)
#                         for lat in temp_resolvents:
#                             for K in clauses_list:
#                                 if lat in K:
#                                     clauses_list.remove(K)
#                             for G in final_clause_arr:
#                                 if lat in G:
#                                     final_clause_arr.remove(G)
#                             final_clause_arr.append(lat)
#                             index_holder.append(lat)
#                         a = []
#                         a.append(index_holder.index(K)+1)
#                         a.append(index_holder.index(G)+1)
#                         a.sort()
#                         #print(str(len(index_holder))+". "+resolvents+" ("+str(a[0])+" "+str(a[1])+")")
#                     else:
#                         print("ERROR")
#                         return    
#         if(len(temp_resolvents) == 0):
#             #print("===============")
#             #print("[CONCLUSION]: "+"".join(finalx)+" is unknown")
#             return
#         else:
#             temp_resolvents.clear()
# clauses_list.sort()
# index_holder.sort()
# resolution(clauses_list,final_clause_arr,index_holder)