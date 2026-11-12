
def quick_sort(arr):
    print(len(arr))
    if len(arr)<=1:
        return arr
    pivot = arr[0]
    left=[x for x in arr[1:] if x <=pivot]
    right=[x for x in arr[1:]if x >pivot]
    return quick_sort(left)+[pivot]+quick_sort(right)
n=int(input())
arr=list(map(int,input().split()))
print(quick_sort(arr))

import random
def quick_sort_random(arr):
    if len(arr)<=1:
        return arr
    pivot=random.choice(arr)
    left=[x for x in arr if x <pivot]
    middle=[x for x in arr if x == pivot]
    right=[x for x in arr if x >pivot]
    return quick_sort_random(left)+middle+quick_sort_random(right)
n=int(input())
arr=list(map(int,input().split()))
print(quick_sort_random(arr))

def quick_sort_3way(arr):
    if len(arr)<=1:
        return arr
    pivot=arr[0]
    left=[x for x in arr if x <pivot]
    middle=[x for x in arr if x == pivot]
    right=[x for x in arr if x >pivot]
    return quick_sort_3way(left)+middle+quick_sort_3way(right)
n=int(input())
arr=list(map(int,input().split()))
print(quick_sort_3way(arr))

