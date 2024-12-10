import nslookup
from dns import resolver
import dns.reversename
from .. import Random
import dns

#print("load " + '/'.join(__file__.split('/')[-2:]))

class Nslookup():
    def __init__(self, server:list[str]=["8.8.8.8", "1.1.1.1", "8.8.4.4"], tcp:bool=False) -> None:
        if type(server) == str:
            server = [server]

        self.server = server
        self.tcp = tcp
    
    def A(self, domain:str) -> list[str]:
        nl = nslookup.Nslookup(dns_servers=Random.Choice(self.server, 5), tcp=self.tcp)
        return nl.dns_lookup(domain).answer
    
    def AAAA(self, domain:str) -> list[str]:
        nslookup = nslookup.Nslookup(dns_servers=Random.Choice(self.server, 5), tcp=self.tcp)
        return nslookup.dns_lookup6(domain).answer
    
    def Reverse(self, ip:str) -> str:
        rl = resolver.Resolver()
        rl.nameservers = Random.Choice(self.server, 5)
        return str(resolver.resolve(dns.reversename.from_address(ip), "PTR")[0])
    
    def MX(self, domain:str) -> list[str]:
        rl = resolver.Resolver()
        rl.nameservers = Random.Choice(self.server, 5)

        try:
            answer = rl.resolve(domain, "MX")
        except dns.resolver.NoAnswer:
            return []

        res = {}
        for x in answer:
            x = [i.strip() for i in x.to_text().split()]
            res[int(x[0])] = x[1]
        
        p = list(res)
        p.sort()

        ress = []
        for pp in p:
            ress.append(res[pp])
        
        return ress