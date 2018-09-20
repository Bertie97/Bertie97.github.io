# 练习答案

#### 赋值

```c
int a=1;
```

```python
a = 1
```

#### 数组和指针

```c
char* s[10];
```

```python
s = [''] * 10
```

#### 循环

```c
int main()
{
    int i, a[10];
    for(i = 0; i < 10; ++i)
        a[i] = i * i;
    return 0;
}
```

```python
def main():
    a = [0] * 10
    for i in range(10):
        a[i] = i * i

if __name__ == "__main__":  main()
    
########OR########
def main(): a = [i ** 2 for i in range(10)]
if __name__ == "__main__": main()
```

#### 格式化输出

```c
#include <stdio.h>
int main()
{
    int x = 0, y = 2;
    printf("%d, %d\n", x, y);
    return 0;
}
```

```python
def main():
    x = 0; y = 2
    print("%d, %d"%(x, y))

if __name__ == "__main__": main()
    
########OR########
def main(): print("{x}, {y}".format(x=0, y=2))
if __name__ == "__main__": main()
```

#### 输入和判断

```c
#include <stdio.h>
int main()
{
    int a;
    scanf("%d", &a);
    if(a > 10)
        printf("too big");
    else if(a < 0)
        printf("too small");
    else
        printf("fine");
    return 0;
}
```

```python
def main():
    a = int(input())
    if a > 10:
        print("too big", end='')
    elif a < 0:
        print("too small", end='')
    else:
        print("fine", end='')

if __name__ == "__main__": main()
```

#### 选择

```c
#include <stdio.h>
int main()
{
    int a;
    scanf("%d", &a);
    switch(a)
    {
        case 1:
            printf("hi\n");
            break;
        case 2:
            printf("bye\n");
            break;
        default:
            printf("go\n");
    }
    return 0;
}
```

```python
def main():
    a = int(input())
    if a == 1:
        print("hi")
    elif a == 2:
        print("bye")
    else:
        print("go")

if __name__ == "__main__": main()
    
########OR########
def main():
    a = int(input())
    switch = {
        1: "hi",
        2: "bye"
    }
    print(switch.get(a, "go"))

if __name__ == "__main__": main()
```

#### 库和数字格式

```c
#include <math.h>
#include <stdio.h>
double mcos(double x) {return cos(x);}
int main()
{
    int a;
    scanf("%d", &a);
    printf("%08.2lf\n", mcos((double)a));
    return 0;
}
```

```python
from math import *
def mcos(x): return cos(x)
def main():
    a = int(input())
    print("%08.2f"%mcos(a))
if __name__ == "__main__": main()
```

#### 简单函数

```c
int max(int a, int b)
    return a < b ? b : a;
```

```python
def maximum(a, b): return b if a < b else a

########OR########
maximum = lambda a, b: b if a < b else a
```

#### 判断复合和移位

```c
if(a > b && (10 > 1 << i)) {a += 1;}
```

```python
if a > b and (10 > 1 << i): a += 1

########OR########
if a > b and (10 > 2 ** i): a += 1
```

#### 多元素输入

```c
print("Input a, b:")
scanf("%d, %d", &a, &b)
```

```python
a, b = eval(input("Input a, b:"))

########OR########
a, b = tuple(int(x) for x in input("Input a, b:").split(','))
```

#### 数字与字符串转换（字符处理）

```c
#include <stdio.h>
#include <string.h>

int main()
{
    int i, k, l;
    int num = 0;
    char str[20], tmp;
    printf("Please input a number:");
    scanf("%s", str);
    for(i = 0; i < strlen(str); ++i)
    {
        num *= 10;
        num += str[i] - '0';
    }
    printf("%d\n", num);
    k = 0;
    while(num > 0)
    {
        str[k] = num % 10 + '0';
        k++;
        num /= 10;
    }
    str[k] = 0;
    l = strlen(str);
    for(i = 0; i < l / 2; ++i)
    {
        tmp = str[i];
        str[i] = str[l-i-1];
        str[l-i-1] = tmp;
    }
    printf("%s\n", str);
    return 0;
}
```

```python
def main():
    string = input("Please input a number:")
    print(int(string))
    print(str(int(string)))
if __name__ == "__main__": main()
```

`Retranslate back from C to python line by line`

```python
def main():
    string = input("Please input a number:")
    num = 0
    for i in range(len(string)):
        num *= 10
        num += ord(string[i]) - ord('0')
    print(num)
    string = ''
    while num > 0:
        string += chr(ord('0') + num % 10)
        num //= 10
    print(string[::-1]) # <- see below
    
if __name__ == "__main__": main()

########REVERSE########
chrList = list(string)
for i in range(len(string) // 2):
    tmp = chrList[i]; chrList[i] = chrList[-i-1]; chrList[-i-1] = tmp;
string = ''.join(chrList)
```

#### 凯撒密码

```c
for(i = 0; i < strlen(string); ++i)
{
    cap = 0;
    if(string[i] <= 'Z' && string[i] >= 'A')
    {
        cap = 1;
        string[i] += 'a' - 'A';
    }
    string[i] += k;
    if(string[i] > 'z')
        string[i] -= 26;
    if(cap == 1)
        string[i] -= 'a' - 'A';
}
```

```python
from string import ascii_lowercase as lc, ascii_uppercase as uc
shift = dict(list(zip(lc, lc[k:] + lc[:k])) + list(zip(uc, uc[k:] + uc[:k])))
str_ = ''.join([shift[c] for c in str_])
```

`Retranslate back from C to python line by line`

```python
out = ''
filter = [c.islower() for c in str_]
str_ = str_.lower()
for i in range(len(str_)):
    od = ord(str_[i]) + k
    if od > ord('z'): od -= 26
    out += chr(od) if filter[i] else chr(od).upper()
str_=out
```

#### 截断/切片

```c
void copy(char a[], char b[])
{
    int i;
    for(i = 0; i <= strlen(a); ++i)
        b[i] = a[i];
}
copy(str1, str2);
str2[end] = 0;
printf("%s\n", str2 + start);
```

```python
str2 = str1
print(str2[start:end])
```

<center><a class="filedownload" href="../CONTENTS/STUDY/C语言转python练习答案.zip" download>下载<code>markdown</code>文件</a></center>

<center><a class="filedownload" href="../CONTENTS/STUDY/C语言转python练习答案.pdf" download><code>pdf</code>文件</a></center>