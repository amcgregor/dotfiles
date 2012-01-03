# encoding: utf-8

TLDs = "AC AD AE AERO AF AG AI AL AM AN AO AQ AR ARPA AS ASIA AT AU AW AX AZ BA BB BD BE BF BG BH BI BIZ BJ BM BN BO BR BS BT BV BW BY BZ CA CAT CC CD CF CG CH CI CK CL CM CN CO COM COOP CR CU CV CX CY CZ DE DJ DK DM DO DZ EC EDU EE EG ER ES ET EU FI FJ FK FM FO FR GA GB GD GE GF GG GH GI GL GM GN GOV GP GQ GR GS GT GU GW GY HK HM HN HR HT HU IE IL IM IN INFO INT IO IQ IR IS IT JE JM JO JOBS JP KE KG KH KI KM KN KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MG MH MIL MK ML MM MN MO MOBI MP MQ MR MS MT MU MUSEUM MV MW MX MY MZ NA NAME NC NE NET NF NG NI NL NO NP NR NU NZ OM ORG PA PE PF PG PH PK PL PM PN PR PRO PS PT PW PY QA RE RO RS RU RW SA SB SC SD SE SG SH SI SJ SK SL SM SN SO SR ST SU SV SY SZ TC TD TEL TF TG TH TJ TK TL TM TN TO TP TR TRAVEL TT TV TW TZ UA UG UK US UY UZ VA VC VE VG VI VN VU WF WS YE YT ZA ZM ZW".lower().split()
NAMEs = "identity identify identifyme user self dentity dentify openid myid".split()

for name in NAMEs:
    for tld in TLDs:
        if tld not in name: continue
        if name.index(tld) == 0: continue
        
        print 'http://' + name[:name.index(tld)] + '.' + tld + '/' + name[name.index(tld)+len(tld):]
