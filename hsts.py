import getopt
import json
import sys
import requests
import colorama
from colorama import Fore, Style

VERSION = "1.1"


class File():
    def __init__(self, fileName, mode):
        self.fileName = fileName
        self.mode = mode

    def __enter__(self):
        self.f = open(self.fileName, self.mode)
        return self.f

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f.close()


def usage():
    print("HTTP Strict Transport Security Detect Tool {} ( github.com/ferhatcil )".format(VERSION))
    print("Usage: " + sys.argv[0] + " [OPTIONS]")
    print("   --domain\texample.com")
    print("   --file\tdomains.txt")
    print("   --version\tList version release")
    print("   --help\tThis help menu\n")
    print("Examples:")
    print("   python3 " + sys.argv[0] + " --domain example.com")
    print("   python3 " + sys.argv[0] + " --file file.txt")
    sys.exit(1)


def hstspreload(domain):
    r = requests.get('https://hstspreload.org/api/v2/preloadable?domain=' + domain)
    jsonData = json.loads(r.text)
    for i in jsonData['errors']:
        if 'response.no_header' in i['code']:
            print(f"{Fore.RED}"+domain + f" - Yanıtta HSTS başlığı yok.{Style.RESET_ALL}")
        elif 'domain.tls.invalid_cert_chain' in i['code']:
            print(f"{Fore.YELLOW}"+
                domain + ", eksik veya geçersiz bir sertifika zinciri kullanıyor. Sitenizi https://www.ssllabs.com/ssltest/analyze.html?viaform=on&d=" + domain + f" adresinden inceleyin.{Style.RESET_ALL}")


def hstspreloadFile(filePath):
    try:
        with File(filePath, 'r') as f:
            lines = f.readlines()
        for line in lines:
            hstspreload(line.strip())
    except (KeyboardInterrupt):
        print('Error !')
    finally:
        f.close()


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:f:hv", ["domain=", "file=", "help", "version"])
    except(getopt.GetoptError)  as err:
        print(err)
        sys.exit(-1)

    for o, a in opts:
        if o in ("-d", "--domain"):
            hstspreload(a)
        elif o in ("-f", "--file"):
            hstspreloadFile(a)
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-v", "--version"):
            print(VERSION)
            sys.exit(0)
        else:
            assert False, "unhandled option"
            sys.exit(-1)

    argc = len(sys.argv)
    if argc != 3:
        usage()
