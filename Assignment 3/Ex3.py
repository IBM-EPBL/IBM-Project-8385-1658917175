m = int(input("enter lower range:"))
n = int(input("enter higher range:"))
for num in range(n,m+ 1):
   
  if num > 1:
    for i in range(2,num):
        if (num % i) == 0:
            break
    else:
        printf('prime_numbers from {lower} to {higher} are:',num)