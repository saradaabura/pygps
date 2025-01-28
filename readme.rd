READMEの書き方がよくわかりません...
使い方
詳しくはQiitaにあります
https://qiita.com/raspico/items/fef7e46387bd15120f84
注意点
patterns = {
    'GGA': re.compile(r'\$GNGGA,.*?\*..'),
    'GLL': re.compile(r'\$GNGLL,.*?\*..'),
    'GSA': re.compile(r'\$GNGSA,.*?\*..'),
    'GSV': re.compile(r'\$GNGSV,.*?\*..|\$BDGSV,.*?\*..|\$GLGSV,.*?\*..|\$GPGSV,.*?\*..'),
    'RMC': re.compile(r'\$GNRMC,.*?\*..'),
    'VTG': re.compile(r'\$GNVTG,.*?\*..')
}
このGSVにはGPSモジュールに合わせたプログラムに変更してください。
他のデータも変更してください。
使い方(簡易)
nmea0183 = raw[raw.find("$GNGGA"):raw.find("$GNGST")]
if raw.find("$GNGGA") != -1 and raw.find("$GNGST") != -1:
  listdata = nmea0183.split("\\r\\n")　#ここは$を使用してもいいですがプログラムを変えてください
  i = pygps.parse_nmea_sentences(listdata) #これで大まかなデータを解析し、各データを解析していきます。
その後以下のようなことをすることで動作、取得できます。
GPSにはUART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))のように定義してください
def gps(shared_data):
    raw = GPS.read(2048)
    if raw:
        raw = str(raw)
        nmea0183 = raw[raw.find("$GNGGA"):raw.find("$GNGST")]###ここは自分のGPSデバイスに合わせてください。
        if raw.find("$GNGGA") != -1 and raw.find("$GNGST") != -1:
            listdata = nmea0183.split("\\r\\n")
            i = pygps.parse_nmea_sentences(listdata)
            gsa = pygps.parse_gsa(i["GSA"])
            if gsa["fixtype"] >= 2:###これがないと**データがNone~~**と怒られます。
                rmc = pygps.parse_rmc(i["RMC"])
                gsv = pygps.parse_gsv(i["GSV"])
                gll = pygps.parse_gll(i["GLL"])
                gga = pygps.parse_gga(i["GGA"])
                vtg = pygps.parse_vtg(i["VTG"])
                if rmc and gsv and gll and gga and vtg:###先程と同様
                    #好きなように...
確認済みのモジュール
Air530Z
→AT6558RなのでM5STACKのモジュールも動作すると思います(V1.1は不明)
