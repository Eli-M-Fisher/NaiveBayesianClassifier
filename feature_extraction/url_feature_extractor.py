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

        # 11. NonStdPort
        features['NonStdPort'] = 1 if self.__has_non_standard_port(url) else -1

        # 12. HTTPSDomainURL
        features['HTTPSDomainURL'] = 1 if "https" in url and "https" in tldextract.extract(url).domain else -1

        # 13. RequestURL
        features['RequestURL'] = -1  # Placeholder – requires HTML parsing

        # 14. AnchorURL
        features['AnchorURL'] = 0  # Placeholder – requires HTML parsing

        # 15. LinksInScriptTags
        features['LinksInScriptTags'] = 0  # Placeholder – requires HTML parsing

        # 16. ServerFormHandler
        features['ServerFormHandler'] = -1  # Placeholder – requires HTML parsing

        # 17. InfoEmail
        features['InfoEmail'] = 1 if "mailto:" in url or "info@" in url else -1

        # 18. AbnormalURL
        ext = tldextract.extract(url)
        domain_in_url = ext.domain
        features['AbnormalURL'] = 1 if domain_in_url not in url else -1

        # 19. WebsiteForwarding
        features['WebsiteForwarding'] = -1  # Placeholder – would need redirect check

        # 20. StatusBarCust
        features['StatusBarCust'] = -1  # Placeholder – JS-based detection

        # 21. DisableRightClick
        features['DisableRightClick'] = -1  # Placeholder – requires JS inspection

        # 22. UsingPopupWindow
        features['UsingPopupWindow'] = -1  # Placeholder – requires JS inspection

        # 23. IframeRedirection
        features['IframeRedirection'] = -1  # Placeholder – requires HTML parsing

        # 24. AgeofDomain
        features['AgeofDomain'] = -1  # Placeholder – requires WHOIS info

        # 25. DNSRecording
        features['DNSRecording'] = 1 if self.__has_dns_record(url) else -1

        # 26. WebsiteTraffic
        features['WebsiteTraffic'] = -1  # Placeholder – requires external traffic API

        # 27. PageRank
        features['PageRank'] = -1  # Placeholder – would need rank API

        # 28. GoogleIndex
        features['GoogleIndex'] = 1 if self.__is_indexed_by_google(url) else -1

        # 29. LinksPointingToPage
        features['LinksPointingToPage'] = 0  # Placeholder – backlink API

        # 30. StatsReport
        features['StatsReport'] = 1 if self.__check_suspicious_keywords(url) else -1

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

    def __has_non_standard_port(self, url: str) -> bool:
        match = re.search(r":(\d+)", url)
        if match:
            port = int(match.group(1))
            return port not in [80, 443]
        return False

    def __has_dns_record(self, url: str) -> bool:
        try:
            domain = tldextract.extract(url).fqdn
            socket.gethostbyname(domain)
            return True
        except Exception:
            return False

    def __is_indexed_by_google(self, url: str) -> bool:
        # NOTE: This is a mock – real check requires Google API
        return "google" in url or "index" in url

    def __check_suspicious_keywords(self, url: str) -> bool:
        keywords = ["login", "verify", "update", "secure", "account", "banking", "confirm", "ebay", "paypal"]
        return any(k in url.lower() for k in keywords)