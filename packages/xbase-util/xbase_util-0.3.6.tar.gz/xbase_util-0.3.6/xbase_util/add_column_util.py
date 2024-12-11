import os

import pandas as pd
import re

from nltk.corpus import words
from nltk.stem import WordNetLemmatizer
from tldextract import tldextract

# 初始化 lemmatizer
lemmatizer = WordNetLemmatizer()
os.environ["TLDEXTRACT_DISABLE_UPDATE"] = "1"  # 禁用更新

# 下载词库（仅需执行一次）
# nltk.download('wordnet')
# 构建词库集合
common_tlds = {
    # 常见的 gTLD
    ".com", ".org", ".net", ".info", ".biz", ".edu", ".gov", ".mil",
    # 新兴的 gTLD
    ".app", ".blog", ".shop", ".tech", ".xyz", ".online", ".me", ".co", ".tv",
    # 其他 gTLD
    ".name", ".pro", ".mobi", ".aero", ".coop", ".museum",
    # 中国的 ccTLD
    ".cn", ".us", ".uk", ".de", ".jp", ".fr", ".ca", ".in", ".br", ".ru", ".au", ".kr", ".it", ".es",
    # 其他常见的 ccTLD
    ".ar", ".mx", ".ch", ".nl", ".se", ".pl", ".no", ".fi", ".be", ".dk", ".at",
    # 国际化域名 (IDN)
    ".中国", ".한국", ".рф", ".印度"
}
word_set = set(words.words())  # 将词库转换为集合，提高查找速度
word_set.update(
    ["baidu", "qq", "ali", "souhu", "douyin", "jd", "tencent", "taobao", "tianmao", "dewu", "sougou", "anmeng", "weibo",
     "douyu", "huya", "bilibili", "csnd", "zhihu", "huawei", "xiaomi", "vivo", "oppo", "qihu", "yahu", "fanke",
     "xunfei"])


def is_meaningful_word(word):
    """判断单词是否在词库中"""
    return int(lemmatizer.lemmatize(word.lower(), pos='n') in word_set)


def is_meaningful_phrase(phrase):
    """判断是否是有意义的短语（分词后每个词都必须有意义）"""
    words_in_phrase = phrase.split('.')
    return all(is_meaningful_word(word) for word in words_in_phrase)


def is_danger_subdomain(uri):
    """提取并处理子域名"""
    ext = tldextract.extract(uri)

    subdomain = ext.subdomain.replace("www.", "")
    if subdomain:
        subdomain_parts = subdomain.split('.')
        # filtered_parts = [part for part in subdomain_parts if part not in common_prefixes]
        # print(filtered_parts)
        meaningful_parts = [part for part in subdomain_parts if is_meaningful_word(part)]
        # print(meaningful_parts)
        if meaningful_parts:
            return 0
        else:
            return 1
    return 0


def is_danger_domain(uri):
    """提取主域名并判断是否有意义"""
    ext = tldextract.extract(uri)
    domain = ext.domain
    if is_meaningful_word(domain):
        return 0
    return 1


# 判断域名是否过长
def is_long_domain(uri):
    ext = tldextract.extract(uri)
    domain = ext.domain
    subdomain = ext.subdomain
    if subdomain:
        subdomain_parts = subdomain.split(".")
        target = 1 if any(len(part) > 10 for part in subdomain_parts) else 0
    else:
        target = 0
    return int(len(domain) > 10 or target)


def has_uncommon_tld(domain):
    """判断域名是否使用了非常规TLD"""
    ext = tldextract.extract(domain)
    return int(ext.suffix not in common_tlds)


# 判断域名是否包含随机字符（简单示例：检查是否包含非字母数字字符）
def has_random_characters(domain):
    # 正常域名通常只包含字母、数字、和连字符
    return int(bool(re.search(r'[^a-zA-Z0-9-_.]', domain)))


# 判断域名是否包含特殊字符（例如汉字或表情符号）
def has_special_characters(domain):
    # 汉字或特殊字符的 Unicode 范围
    return int(bool(re.search(r'[\u4e00-\u9fff\U0001F600-\U0001F64F]', domain)))


# 判断域名是否包含大量子域名（假设 10 个以上子域名为异常）
def has_large_number_of_subdomains(uri):
    if tldextract.extract(uri).subdomain:
        subdomains_list = uri.split('.')
        # 如果子域名的数量超过 10，则认为它可能是异常的
        return int(len(subdomains_list) > 3)
    else:
        return 0


def parse_list(x):
    if isinstance(x, str):
        if x == "[]":
            x = []
        else:
            x = f"{x}".replace("\"", "").replace("[", "").replace("]", "").split(",")
    elif isinstance(x, list):
        x = [f"{item}" for item in x]
    else:
        print(f"unknown：{x}  {type(x)}")
        x = []
    return x


def handle_dns(origin_list, isDataFrame=False):
    print("handle_dnslist")
    if not isDataFrame:
        origin_list = pd.DataFrame(origin_list)
    origin_list["dnslist"] = origin_list['dns.host'].apply(parse_list)
    origin_list['dns_host_is_long_domain'] = origin_list['dnslist'].apply(
        lambda x: any(is_long_domain(domain) for domain in x))
    origin_list['dns_host_is_random_characters'] = origin_list['dnslist'].apply(
        lambda x: any(has_random_characters(domain) for domain in x))
    origin_list['dns_host_is_special_characters'] = origin_list['dnslist'].apply(
        lambda x: any(has_special_characters(domain) for domain in x))
    origin_list['dns_host_is_large_subdomains'] = origin_list['dnslist'].apply(
        lambda x: any(has_large_number_of_subdomains(domain) for domain in x))
    origin_list['dns_host_is_danger_domain'] = origin_list['dnslist'].apply(
        lambda x: any(is_danger_domain(domain) for domain in x))
    origin_list['dns_host_is_danger_subdomain'] = origin_list['dnslist'].apply(
        lambda x: any(is_danger_subdomain(domain) for domain in x))
    origin_list['dns_host_is_uncommon_tld'] = origin_list['dnslist'].apply(
        lambda x: any(has_uncommon_tld(domain) for domain in x))
    origin_list.drop(columns=['dnslist'], inplace=True)
    return origin_list
