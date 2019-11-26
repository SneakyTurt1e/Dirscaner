# Dirscaner
- Dirscaner is a tools to brute-force web directories.

# To do
- Try to solve the error exception when requesting IP address from DNS under high thread. [Currently you can try to add IP and corresponding domain in the ***hosts*** file.]
- Add more error exception handling.

#  Features
    -h, --help                        show this help message and exit
    -u url, --url url                 Target url [required]
    -d location                       Wordlist Path
    -o OUTPUT, --output OUTPUT        Location and name of output file
    -b code [code ...]                Baned response code [Default:Null e.g:404 302]
    -e ext [ext ...]                  File extension
    -t THREAD                         Number of thread [Default: 4]
    -s size [size ...]                Size filter,will skip pages with these/this size
    --time-out TIMEOUT                HTTP Timeout [Default 10]
    --time-retry times                The number of retry attempts when the request fails [Default 6]
    --user-agent UA                   Request's user agnet [Default Random]
    --no-color                        Turn off color outputs
    --cookie COOKIES                  Your cookies to use in requests [e.g:key1:value1,key2=value2...]
    --proxy Proxy                     Use proxy to requests 	[e.g:http(s)://user:pass@IP:PORT,proxy2...]
    --add-slash                       Add '/' after each request
    --ssl-check                       Enable SSL certificate verification
    --allow-re                        Follow redirects
    --scraper                         Scraper Mod. Scraper all url in <a href>

# Usage
-     git clone https://github.com/SneakyTurt1e/Dirscaner.git
-     pip install -r requirements.txt
-     python dirscaner.py -h or python3 dirscaner.py -h
# Example
    python dirscaner.py -u http://www.mysite.com -d dir.txt
    ______  _       _____
    |  _  \(_)     /  ___|
    | | | | _  _ __\ `--.   ___  __ _  _ __    ___  _ __
    | | | || || '__|`--. \ / __|/ _` || '_ \  / _ \| '__|
    | |/ / | || |  /\__/ /| (__| (_| || | | ||  __/| |
    |___/  |_||_|  \____/  \___|\__,_||_| |_| \___||_|
    
    +------------------------------------------------------------------------------------
    | DirScaner
    | By SneakyTurt1e https://github.com/SneakyTurt1e/
    +------------------------------------------------------------------------------------
    | Wordlist Path: C:\Users\User\Desktop\new\dirscaner\dir.txt
    | Target Url:  http://www.mysite.com
    | Threads:  4
    | Timeout: 10s
    | User Agent: Random
    | Baned Code:
    | Total requests:  4
    | Start Time: 2019-11-20 10:54:15
    +-----------------------------------------------------------------------------------+
    | PAGE |                                             | SIZE |                | CODE |
    +-----------------------------------------------------------------------------------+
    [-] http://www.mysite.com/abc                         581                      404
    [-] http://www.mysite.com/123                         581                      404
    [-] http://www.mysite.com/def                         581                      404
    [-] http://www.mysite.com/456                         581                      404
    +------------------------------------------------------------------------------------
    [+] Scan Finish
    [+] Time used: 0s
    [+] Finish Time: 2019-11-20 10:54:15

The result of the scan should be similar to this:
![s](https://s2.ax1x.com/2019/11/20/MWK8YR.png )


You can manually turn off the color optput with  --no-color
![](https://s2.ax1x.com/2019/11/20/MWQ6L8.png)


## Scraper Mod
The result should be similar to this:
![](https://s2.ax1x.com/2019/11/21/M5R3Xd.png)

# Bug or Issue
Let me know if there is a bug or issue

# License
See [LICENSE](https://github.com/SneakyTurt1e/Dirscaner/blob/master/LICENSE "LICENSE")
