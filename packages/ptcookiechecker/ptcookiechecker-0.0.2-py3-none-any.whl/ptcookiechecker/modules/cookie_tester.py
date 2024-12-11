from ptlibs import ptprinthelper, ptjsonlib
import re

class CookieTester:
    def __init__(self):
        pass

    COMMON_COOKIE_NAMES =   [
    ["PHPSESSID", "PHP session cookie", "SESSION", "ERROR"],
    ["JSESSIONID", "Java session cookie", "SESSION", "ERROR"],
    ["Lang", "Standard cookie for save of set language", "standard","INFO"],
    ["password", "Typical name for cookie with password", "sensitive","ERROR"]
]

    COMMON_COOKIE_VALUES = [
        ["PHP", [32, 26]],
        ["ASP", 24],
    ]

    def run(self, response, args, ptjsonlib: object, test_cookie_issues: bool = True, filter_cookie: str = None):
        self.ptjsonlib = ptjsonlib
        self.args = args
        self.use_json = False
        self.filter_cookie = filter_cookie
        self.test_cookie_issues = test_cookie_issues

        set_cookie_list: list = self._get_set_cookie_headers(response)
        cookie_list = response.cookies

        if not cookie_list and not set_cookie_list:
            ptprinthelper.ptprint(f"Site returned no cookies", bullet_type="", condition=not self.use_json)
            return

        for cookie in cookie_list:
            if self.filter_cookie and (self.filter_cookie.lower() != cookie.name.lower()):
                continue
            import json

            full_cookie: str = self._find_cookie_in_headers(cookie_list=set_cookie_list, cookie_to_find=f"{cookie.name}={cookie.value}") or cookie

            cookie_name = f"{cookie.name}={cookie.value}"
            cookie_path = cookie.path
            cookie_domain = cookie.domain
            cookie_expiration = cookie.expires
            cookie_secure_flag = cookie.secure
            cookie_http_flag = bool("httponly" in (key.lower() for key in cookie._rest.keys()))
            cookie_samesite_flag = next((value for key, value in cookie._rest.items() if key.lower() == "samesite"), None)


            node = self.ptjsonlib.create_node_object("cookie", properties={
                "name": cookie_name,
                "path": cookie_path,
                "domain": cookie_domain,
                "cookieExpiration": cookie_expiration,
                "cookieSecureFlag": cookie_secure_flag,
                "cookieHttpOnlyFlag": cookie_http_flag,
                "cookieSameSiteFlag": cookie_samesite_flag
            }, vulnerabilities=[])

            ptprinthelper.ptprint(ptprinthelper.get_colored_text(cookie.name, "TITLE"), condition=not self.use_json, newline_above=True)

            ptprinthelper.ptprint(f"Header:", bullet_type="TEXT", condition=not self.use_json)
            ptprinthelper.ptprint(ptprinthelper.get_colored_text(full_cookie, "ADDITIONS"), condition=not self.use_json, indent=2)


            ptprinthelper.ptprint(f"Name: {cookie.name}", bullet_type="TEXT", condition=not self.use_json)
            if self.test_cookie_issues:
                self.check_cookie_name(cookie.name)

            ptprinthelper.ptprint(f"Value: {cookie.value}", bullet_type="TEXT", condition=not self.use_json)
            if self.test_cookie_issues:
                self.check_cookie_value(cookie.value)

            ptprinthelper.ptprint(f"Domain: {cookie_domain}", bullet_type="TEXT", condition=not self.use_json)
            if self.test_cookie_issues:
                self.check_cookie_domain(cookie_domain)

            ptprinthelper.ptprint(f"Path: {cookie_path}", bullet_type="TEXT", condition=not self.use_json)
            if self.test_cookie_issues:
                self.check_cookie_path(cookie_path)

            ptprinthelper.ptprint(f"Expires: {cookie_expiration}", bullet_type="TEXT", condition=not self.use_json)
            if self.test_cookie_issues:
                self.check_cookie_expiration(cookie_expiration)

            if self.test_cookie_issues:
                ptprinthelper.ptprint(f"Flags: ", bullet_type="TEXT", condition=not self.use_json)
                self.detect_duplicate_attributes(full_cookie)
                self.check_cookie_secure_flag(cookie_secure_flag)
                self.check_cookie_samesite_flag(cookie_samesite_flag)
                self.check_cookie_httponly_flag(cookie_http_flag)
            else:
                ptprinthelper.ptprint(f"Flags: ", bullet_type="TEXT", condition=not self.use_json)
                ptprinthelper.ptprint(f"    SameSite: {cookie_samesite_flag}", bullet_type="TEXT", condition=not self.use_json)
                ptprinthelper.ptprint(f"    Secure: {cookie_secure_flag}", bullet_type="TEXT", condition=not self.use_json)
                ptprinthelper.ptprint(f"    HttpOnly: {cookie_http_flag}", bullet_type="TEXT", condition=not self.use_json)

    def print_flags(self, full_cookie: str):
        cookie_flags = re.findall(r'(\w+)=([^;]+)', full_cookie)

    def detect_duplicate_attributes(self, cookie_string):
        attributes = [attr.strip() for attr in cookie_string.split(';')]
        attribute_counts = {}
        for attr in attributes:
            key = attr.split('=')[0].strip().lower()  # Get the attribute name, case-insensitive
            attribute_counts[key] = attribute_counts.get(key, 0) + 1
        duplicates = {key: count for key, count in attribute_counts.items() if count > 1}
        if duplicates:
            ptprinthelper.ptprint(f"Duplicate attributes detected: {list(duplicates.keys())}", bullet_type="VULN", condition=not self.use_json, indent=4)
        return duplicates

    def _find_cookie_in_headers(self, cookie_list: list, cookie_to_find: str):
        for cookie in cookie_list:
            if re.findall(re.escape(cookie_to_find), cookie):
                return cookie

    def _get_set_cookie_headers(self, response):
        """Returns Set-Cookie headers from raw response headers"""
        raw_cookies: list = []
        if [h for h in response.raw.headers.keys() if h.lower() == "set-cookie"]:
            ptprinthelper.ptprint(ptprinthelper.get_colored_text("Set-Cookie headers:", "ADDITIONS"), "", colortext="WARNING", condition=not self.use_json, indent=0)
            for header, value in response.raw.headers.items():
                if header.lower() == "set-cookie":
                    ptprinthelper.ptprint(ptprinthelper.get_colored_text(f"{header}: {value}", "ADDITIONS"), colortext="WARNING", condition=not self.use_json, indent=2)
                    raw_cookies.append(f"{header}: {value}")
        return raw_cookies

    def _find_technology_by_cookie_value(self, cookie_value):
        result: list = []
        for technology_name, default_len in self.COMMON_COOKIE_VALUES:
            if isinstance(default_len, list):
                for l in default_len:
                    if l == len(cookie_value):
                        result.append(technology_name)
                        break
            else:
                if default_len == len(cookie_value):
                    result.append(technology_name)
        return result

    def _find_technology_by_cookie_name(self, cookie_name):
        for technology_name, message, json_code, bullet_type in self.COMMON_COOKIE_NAMES:
            if technology_name.lower() == cookie_name.lower():
                return (technology_name, message, json_code, bullet_type)

    def check_cookie_expiration(self, expires):
        pass

    def check_cookie_path(self, cookie_path: str):
        pass

    def check_cookie_name(self, cookie_name: str):
        result = self._find_technology_by_cookie_name(cookie_name)
        if result:
            technology_name, message, json_code, bullet_type = result
            vuln_code = "PTV-WEB-INFO-TEDEFSIDNAME"
            #self.ptjsonlib.add_vulnerability(vuln_code) #if args.cookie_name else node["vulnerabilities"].append({"vulnCode": vuln_code})
            ptprinthelper.ptprint(f"Cookie has default name for {technology_name}", bullet_type=bullet_type, condition=not self.use_json, colortext=False, indent=4)
        if not cookie_name.startswith("__Host-"):
            vuln_code = "PTV-WEB-LSCOO-HSTPREFSENS"
            #self.ptjsonlib.add_vulnerability(vuln_code) #if args.cookie_name else node["vulnerabilities"].append({"vulnCode": vuln_code})
            ptprinthelper.ptprint(f"Cookie is missing '__Host-' prefix", bullet_type="VULN", condition=not self.use_json, colortext=False, indent=4)

    def check_cookie_value(self, cookie_value: str):
        #if ((len(cookie_value) == 24 or len(cookie_value) == 26) and re.match(r"^[a-z0-9]*$", cookie_value)) or len(cookie_value) == 32 and re.match(r"^[A-Z0-9]*$", cookie_value):
            result = self._find_technology_by_cookie_value(cookie_value)
            if result:
                vuln_code = "PTV-WEB-INFO-TEDEFSIDFRM"
                ptprinthelper.ptprint(f"Cookie value length has default format for {result if len(result) > 1 else ', '.join(result)} technologies", bullet_type="VULN", condition=not self.use_json, colortext=False, indent=4)
            #self.ptjsonlib.add_vulnerability(vuln_code) if args.cookie_name else node["vulnerabilities"].append({"vulnCode": vuln_code})

    def check_cookie_domain(self, cookie_domain: str):
        if cookie_domain.startswith("."):
            ptprinthelper.ptprint(f"Overscoped cookie issue", bullet_type="WARNING", condition=not self.use_json, colortext=False, indent=4)


    def check_cookie_httponly_flag(self, cookie_http_flag):
        if not cookie_http_flag:
            vuln_code = "PTV-WEB-LSCOO-FLHTTPSENS"
            #self.ptjsonlib.add_vulnerability(vuln_code) #if args.cookie_name else node["vulnerabilities"].append({"vulnCode": vuln_code})
            ptprinthelper.ptprint(f"HttpOnly flag missing", bullet_type="VULN", condition=not self.use_json, colortext=False, indent=4)
        else:
            ptprinthelper.ptprint(f"HttpOnly flag present", bullet_type="OK", condition=not self.use_json, colortext=False, indent=4)

    def check_cookie_samesite_flag(self, cookie_samesite_flag):
        if not cookie_samesite_flag:
            vuln_code = "PTV-WEB-LSCOO-FLSAMESENS"
            #self.ptjsonlib.add_vulnerability(vuln_code) if args.cookie_name else node["vulnerabilities"].append({"vulnCode": vuln_code})
            ptprinthelper.ptprint(f"SameSite flag missing", bullet_type="VULN", condition=not self.use_json, colortext=False, indent=4)
        else:
            # + hodnota
            ptprinthelper.ptprint(f"SameSite={cookie_samesite_flag}", bullet_type="OK", condition=not self.use_json, colortext=False, indent=4)

    def check_cookie_secure_flag(self, cookie_secure_flag):
        if not cookie_secure_flag:
            vuln_code = "PTV-WEB-LSCOO-FLSAMESENS"
            #self.ptjsonlib.add_vulnerability(vuln_code) #if args.cookie_name else node["vulnerabilities"].append({"vulnCode": vuln_code})
            ptprinthelper.ptprint(f"Secure flag missing", bullet_type="VULN", condition=not self.use_json, colortext=False, indent=4)
        else:
            ptprinthelper.ptprint(f"Secure flag present", bullet_type="OK", condition=not self.use_json, colortext=False, indent=4)
