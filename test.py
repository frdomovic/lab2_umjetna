

# def clause_negation(K):
#     temp_set = set()
#     if "v" not in K:
#         temp_set.add(str("~"+K.strip()).replace("~~",""))
#     else:
#         K = K.split(" v ")
#         K.sort()
#         temp_arr = []
#         for literal in K:
#             temp_arr.append(str("~"+literal.strip()).replace("~~",""))
#         temp_arr.sort()
#         temp_set.add(" ^ ".join(temp_arr))
#     return temp_set


# k = clause_negation("~c v ~b v ~a")
# print(k)

# def redundant_check(clauses_set,sos_set):
#     new_set = set()
#     for c1 in clauses_set:
#         temp_c1_literal_set = set(c1.split(" v "))
#         f = True
#         for c2 in sos_set:
#             temp_c2_literal_set = set(c2.split(" v "))
#             if temp_c1_literal_set.issubset(temp_c2_literal_set):
#                 f = False
#         if f:
#             new_set.add(c1)
#     return new_set

# c1 = {"A v B","~A v C","A v D v X","A v ~D"}
# c2 = {"A v D"}
# #print(c1)
# c3 = redundant_check(c1,c2)
# print(c3)

# def compatable_resolvation(c1,c2):
#     c1_lats = set(c1.split(" v "))
#     c2_lats = set(c2.split(" v "))
#     for lat1 in c1_lats:
#         for lat2 in c2_lats:
#             if lat1.replace("~","") == lat2.replace("~","") and lat1 != lat2:
#                 return True
#     return False

# def selectClauses(clause_set,sos_set,used_dict):
#     for c1 in clause_set:
#         for c2 in sos_set:
#             if compatable_resolvation(c1,c2) and (c1,c2) not in used_dict and (c2,c1) not in used_dict:
#                 return c1,c2
#     return "none","none"
                

# used_dict = {}
# clause_set ={"~A v B","~B v C","A"}
# sos_set = {"~C"}
# c1,c2 = selectClauses(clause_set,sos_set,used_dict)


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
        return new_clause
    else:
        return "NIL"
                



a = plResolve("~b v c","~c v b")
print(a)