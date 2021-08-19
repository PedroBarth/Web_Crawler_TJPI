from bs4 import BeautifulSoup
from datetime import datetime
from unidecode import unidecode
import re

build_headers= {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7',
    'Connection': 'keep-alive',
    'Host': 'tjpi.pje.jus.br',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}

def crawler(response):
    try:
        soup = BeautifulSoup(response.body, 'html.parser')
    except:
        print("Erro ao buscar dados")


    return {
        
        'uf' : 'PI',
        'partes' : _search_parties(soup)
        
    }

def _search_parties(soup):

    todasPartes = []

    parteAtiva = soup.find('span' ,id="j_id130:processoPartesPoloAtivoResumidoList:0:j_id277")

    if parteAtiva is None:
        return None

    parteAtiva= parteAtiva.find('span')

    parteAtiva = parteAtiva.text

    nomeParte1 = parteAtiva.split('-')[0].strip()

    CPNJParte1 = parteAtiva.split(':')[1].strip().split(' ')[0]
    CPNJParte1 = CPNJParte1.replace('/', '').replace('.', '').replace('-', '')

    tipo1 = parteAtiva.split(' ')
    tipo1 = tipo1[len(tipo1)-1].replace('(', '').replace(')', '')

    todasPartes.append({
        'cnpj' : unidecode(CPNJParte1),
        'nome' : unidecode(nomeParte1),
        'polo' : "ATIVO",
        'tipo': unidecode(tipo1)
    })

    ########################AQUI AS COISAS FICAM ESTRANHAS##################################

    parte = soup.find('tbody', id="j_id130:processoPartesPoloPassivoResumidoList:tb")

    if parte is None:
        return None
    
    parte = parte.find_all('tr')

    for par in parte:
        linha = par.find('td')
        texto1 = linha.text.strip()

        if "REU" in texto1:
            advogados = []
            nomeReu = texto1.split('-')[0]

            for part in parte:
                texto2 = par.find('td').text.strip()
                
                if "ADVOGADO" in texto2:

                    nomeAdv = texto2.split('-')[0]
                    cpfAdv = texto2.split(':')[1].strip()
                    cpfAdv = cpfAdv.split(' ')[0]
                    cpfAdv = cpfAdv.replace('.','').replace('-','')

                    oabTexto = texto2.split('-')[1].strip()

                    oab = re.findall(r'(\w+?)(\d+)', oabTexto)[0] 

                    oab_uf = oab[0]
                    oab_numero = oab[1]

                    advogados.append({
                        'cpf' : cpfAdv,
                        'oab': {
                            'uf' : oab_uf,
                            'numero' : oab_numero
                        },
                        'nome' : nomeAdv,
                        'tipo' : 'ADVOGADO'
                    })     

            if "CPF" in texto1:       
                cpfReu = texto1.split(':')[1].strip()
                cpfReu = cpfReu.split(' ')[0]
                cpfReu = cpfReu.replace('.','').replace('-','')     

            if "CNPJ" in texto1:
                cnpjReu = texto1.split(':')[1].strip()
                cnpjReu = cnpjReu.split(' ')[0]
                cnpjReu = cnpjReu.replace('.','').replace('/','').replace('-','') 

        
            
            
            if 'CNPJ' in texto1:
                todasPartes.append({
                    'cnpj' : cnpjReu,
                    'nome' : nomeReu,
                    'polo' : 'PASSIVO',
                    'tipo' : 'REU',
                    'advogados': advogados
                })

            if 'CPF' in texto1:
                todasPartes.append({
                    'cpf' : cpfReu,
                    'nome' : nomeReu,
                    'polo' : 'PASSIVO',
                    'tipo' : 'REU',
                    'advogados': advogados
                })
                  
        
    return todasPartes