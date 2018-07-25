import csv
import json
import time
import requests
from bs4 import BeautifulSoup

qq_lst = ["1591780418","1694543405","905479605","1079315068","625276872","419787862","3521802053","2316470449","827297477","3404064553","994508974","954218622","1418707618","646904527","1939573143","874226876","2767634033","769433029","862125707","260903088","964083210","1637015088","1097426689","1826234293","205094490","451694727","3164925507","1176079760","515415166","305320602","2447511717","1565077579","1148791191","307141809","370308707","2279763407","408309493","379687474","1096087178","953764089","747161601","617687380","364992932","970926529","2447649126","2323605726","952020917","987064218","157160327","329000175","675974119","444785083","602015530","675763157","1015064114","3167274201","2495327639","460928248","476159804","3345250480","1067321779","601645067","1473196314","250938747","460887059","3092226392","2294681894","459660919","847094155","1253982146","875229001","1796943480","2676997340","1552654599","2964886712","1280787710","457651011","982390429","1576460301","769552592","940499344","1210883049","1807134674","517788430","546454088","379669632","3247714329","1939274655","2570531137","2351783158","770889635","2513041769","983415847","3294978868","2672045322","601980993","470216705","1101853840","754993104","965385284","380002811","1033906346","1574008633","1757303219","1020756414","2416883908","392813912","798960531","1582034172","965097172","1272899331","2787206315","1512299429","409875223","254997741","1498981628","89690976","812075761","444374951","838602547","261225407","1462215002","2289450759","790762116","2545884133","645468673","1597658825","1936381013","2332097795","526910924","245752012","364075883","83347688","425985877","603936882","1554840878","1462825054","1915364342","1076798873","937423523","1358023220","261220529","906218930","624183712","903336698","373171658","1134693876","565404017","1373752369","1227496940","763612666","434786807","444300409","1006084017","773862951","2070655507","1911782251","517747334","1459272362","1354921112","2737539302","3207526350","2452432873","864964006","1814245661","974772488","739886322","1126980556","757798170","2759288199","834194965","1360437513","862843459","632656404","3518970598","1799903589","3367094060","2261238240","2586268628","1396705738","1689223178","1054059790","2654850818","626847133","540105162","1569640579","2509600962","406096277","630720190","364350059","424704113","3030396013","819157967","1272644166","1650123510","761173184","1526451486","769770722","1092426116","1211268292","3207099369","610383267","757911435","959897601","2531226307","2416722685","2975653817","654661573","2192331917","3442784368","995561635","2803536362","617307127","1316641244","375453365","1771882754","3099857298","3547882802","3353652060","592614943","912669332","470419404","918569583","568878913","3549835936","949114596","1220837153","1641474220","1627791542","1129702419","981059614","641796389","35278597","42801402","75861694","382403817","1025624309","2487988211","719428529","3439405704","64090435","2658014610","452066805","810480876","1692262587","2686344379","83465271","1184996095","1261010129","2901180179","453506592","307767151","344822797","1126009127","778078163","643320250","769297107","863648928","370556565","1104890726","690054028","1032030494","840611668","2422840805","2869098867","1243257657","980551997","981176270","3248579132","1067791685","1145500855","12442835","1530952318","479174937","454170989","419990153","951172630","2760969645","912458252","273193113","2836465773","2356869460","749015248","20013430","765670864","3435999687","787371539","1653087275","445255062","993514543","1404273198","1277421717","291190168","1519497143","244259931","1830623316","1287078854","137083233","1509203062","1124499365","3164589354","360095707","2361339374","3039834365","648092066","1018535942","540504729","3361462513","414107873","2337362575","491565693","1974189854","594143986","572645517","1398499715","403425608","2275316862","3146807913","243710577","2826229627","744468381","289516570","550443308","71766848","1415912291","373464877","1428686887","3089484884","1164413540","1391646599","2996152003","1073656775","921251891","1570110883","122929048","2433806725","403707951","763770128","619445730","1533003260","1760287894","1960217292","2623366777","2020780997","2874681973","2507064695","344090436","2967789422","592375016","2260950667","22151289","1602659741","486584659","392666651","523906181","807082910","602396110","243216996","79534096","2394606209","690063828","1002876716","525265579","978127470","2864201752","1900942676","1332935494","1472686939","1519173866","1259740282","1171677967","813540483","1292035678","168549890","3264492346","915859262","654402535","974106459","1192577933","2432822371","1121952284","279408285","454002833","710952230","1585620881","3289187396","244522","603598632","168229383","497692530","923636928","874214313","1002384631","1536213066","754855317","2748925234","2185422325","1059974700","962037459","1529551565","2323414714","673994196","804450828","861040668","474532368","694831248","634307469","209374244","1553387200","180605056","305748112","736353320","641275865","872377689","792499313","654263254","3202587142","647482793","2571884360","911319694","511650967","1768495693"]



def getPage(keyword):
    url = "http://tieba.baidu.com/f/search/res?qw="
    url = url +  keyword
    res = requests.get(url)
    return res.text


def parse(page, qq, keyword, output):
    soup = BeautifulSoup(page, "lxml")
    divs = soup.find_all(class_="s_post")
    for div in divs:
        try:
            title = div.a.text
            content = div.div.text
            url = div.a.attrs["href"]
            keyword = div.em.text
            datetime = div.find(class_="p_date").text
            data = {
                "QQ":qq,
                "关键字":keyword,
                "链接":url,
                "标题": title,
                "内容": content,
                "时间": datetime
            }
            output.writerow(data)
        except:
            print(div)


def main():
    fp = open("result.csv", "w", newline="", encoding="utf-8-sig")
    fieldnames = ["QQ", "关键字", "链接", "标题", "内容", "时间"]
    output = csv.DictWriter(fp,fieldnames=fieldnames)
    output.writeheader()
    for qq in qq_lst:
        keyword = qq
        page = getPage(keyword)
        parse(page, qq, keyword, output)
        keyword = "qq" + qq
        page = getPage(keyword)
        parse(page, qq, keyword, output)
    fp.close()

main()