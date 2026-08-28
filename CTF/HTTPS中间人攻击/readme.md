& "D:\Program Files\Wireshark\tshark.exe" -r target.pcap -o "tls.keylog_file:sslkey.log" -Y http
解密pcap流量并转换成http
 & "D:\Program Files\Wireshark\tshark.exe" -r target.pcap -o "tls.keylog_file:sslkey.log" -Y http -T json > decrypted_http.json
拿到CTF标识，填到网页算通关

