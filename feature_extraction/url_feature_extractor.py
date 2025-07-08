import re
import socket
import requests
import tldextract

class URLFeatureExtractor:
    def __init__(self):
        pass

    def extract(self, url: str) -> dict:
        features = {}

        # 1. UsingIP
        features['UsingIP'] = 1 if self.__is_ip_address(url) else -1

        # 2. LongURL
        features['LongURL'] = 1 if len(url) >= 75 else -1

        # 3. ShortURL
        features['ShortURL'] = 1 if self.__is_shortening_service(url) else -1

        # 4. Symbol@
        features['Symbol@'] = 1 if "@" in url else -1

        # 5. Redirecting//
        features['Redirecting//'] = 1 if url.count("//") > 1 else -1

        # 6. PrefixSuffix-
        features['PrefixSuffix-'] = 1 if "-" in tldextract.extract(url).domain else -1

        # 7. SubDomains
        features['SubDomains'] = self.__subdomain_score(url)

        # 8. HTTPS
        features['HTTPS'] = 1 if url.startswith("https") else -1

        # 9. DomainRegLen
        features['DomainRegLen'] = -1  # Placeholder (requires WHOIS)

        # 10. Favicon
        features['Favicon'] = -1  # Placeholder (requires HTML parsing)

        # ... (משאיר את השאר להשלמה מדורגת)

        return features

    def __is_ip_address(self, url: str) -> bool:
        ip_pattern = r"(http[s]?://)?(\d{1,3}\.){3}\d{1,3}"
        return bool(re.match(ip_pattern, url))

    def __is_shortening_service(self, url: str) -> bool:
        shorteners = ["bit.ly", "goo.gl", "tinyurl.com", "ow.ly", "t.co"]
        return any(s in url for s in shorteners)

    def __subdomain_score(self, url: str) -> int:
        ext = tldextract.extract(url)
        subdomains = ext.subdomain.split('.')
        count = len([s for s in subdomains if s])
        if count == 0:
            return -1
        elif count == 1:
            return 0
        else:
            return 1