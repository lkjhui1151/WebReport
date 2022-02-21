
context = {}
context2 = {}

list = ["a", "a", "a", "b", "b"]
list2 = {"id": 1, "name": 'ssss', 'Risk': 'sss', 'detail': 5}
list3 = []

for i in list:
    if i in context:
        for j in list2:
            context[i] = list2
    else:
        for j in list2:
            context[i] = list2

context2["Cloud"] = context

print(context2)
