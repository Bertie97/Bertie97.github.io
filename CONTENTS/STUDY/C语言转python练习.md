# 练习

#### 赋值

```c
int a=1;
```

```python

```

#### 数组和指针

```c
char* s[10];
```

```python

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

```

#### 简单函数

```c
int max(int a, int b)
    return a < b ? b : a;
```

```python

```

#### 判断复合和移位

```c
if(a > b && (10 > 1 << i)) {a += 1;}
```

```python

```

#### 多元素输入

```c
print("Input a, b:")
scanf("%d, %d", &a, &b)
```

```python

```

#### 数字与字符串转换（字符处理）

```c

```

```python
def main():
    string = input("Please input a number:")
    print(int(string))
    print(str(int(string)))
if __name__ == "__main__":
    main()
```

`Retranslate back from C to python line by line`

```python

```

#### 凯撒密码

```c

```

```python
from string import ascii_lowercase as lc, ascii_uppercase as uc
shift = dict(list(zip(lc, lc[k:] + lc[:k])) + list(zip(uc, uc[k:] + uc[:k])))
str_ = ''.join([shift[c] for c in str_])
```

`Retranslate back from C to python line by line`

```python

```

#### 截断/切片

```c

```

```python
str2 = str1
print(str2[start:end])
```


<center><a class="filedownload" href="../CONTENTS/STUDY/C语言转python练习.zip" download>下载<code>markdown</code>文件</a></center>

<center><a class="filedownload" href="../CONTENTS/STUDY/C语言转python练习.pdf" download><code>pdf</code>文件</a></center>

