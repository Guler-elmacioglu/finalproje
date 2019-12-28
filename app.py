import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = "çok gizli key"

# Veri tabanı bağlantısı
uri = os.getenv("MONGO_ATLAS_URI")
client = MongoClient(uri)
db = client.galeri.uyeler
db2 = client.galeri.yorumlar

@app.route('/')
def anasayfa():
    return render_template('anasayfa.html')
@app.route('/hakkımızda')
def hakkımızda():
    return render_template('hakkımızda.html')
@app.route('/modeller')
def modeller():
    return render_template('modeller.html')
@app.route('/audi')
def audi():
    return render_template('audi.html')
@app.route('/bmw')
def bmw():
    return render_template('bmw.html')
@app.route('/mercedes')
def mercedes():
    return render_template('mercedes.html')
@app.route('/opel')
def opel():
    return render_template('opel.html')
@app.route('/peugeot')
def peugeot():
    return render_template('peugeot.html')
@app.route('/porsche')
def porsche():
    return render_template('porsche.html')
@app.route('/girisekran')
def girisekran():
    return render_template('giris.html')
@app.route('/uyeol')
def uyelik():
    return render_template('uyelik.html')

@app.route('/yorumsayfa')
def yorumsayfa():
    try:
        if session['ad'] is not None:
            return render_template('yorumsayfa.html')
    except:
        durum="Giriş yapınız"
        return render_template('giris.html',hata=durum)

@app.route('/dusuncelerimiz')
def dusuncelerimiz():
    yapilacaklar = []
    for yap in db2.find():
          yapilacaklar.append({"_id": str(yap['_id']), "ad": yap['ad'], "konu": yap['konu'],"yorum": yap['yorum']}) 
    return render_template('dusuncelerimiz.html',veri=yapilacaklar)

@app.route('/yorumyap',methods=['POST'])
def yorumyap():
    try:
        if session['ad'] is not None:
            if request.method == 'POST':
             # index.html formundan isim gelecek
                 ad =session['ad']
                 baslik = request.form["konu"]
                 yorum = request.form["yorum"]
                 mydict = { "ad": ad,"konu":baslik,"yorum":yorum}
                 db2.insert_one(mydict)
                 return redirect('/dusuncelerimiz')
            return redirect('/dusuncelerimiz')
    except:
        durum="Giriş yapınız"
        return render_template('giris.html',hata=durum)
 


@app.route('/uyekaydet',methods=['POST'])
def uyekaydet():
      if request.method == 'POST':
        # index.html formundan isim gelecek
        ad = request.form["ad"]
        soyad = request.form["soyad"]
        mail = request.form["email"]
        telefon = request.form["tel"]
        cinsiyet = request.form["cinsiyet"]
        parola = request.form["parola"]
       
        mydict = { "ad": ad, "soyad":soyad, "mail": mail , "telefon": telefon,"cinsiyet": cinsiyet,"parola":parola}
        u = db.find_one({'mail':mail})
        if u is None :
                x = db.insert_one(mydict)
        else:
            durum="eposta adresi daha önceden sistemde kayıtlı"
            return render_template('uyelik.html',hata=durum)

        return redirect('/')

@app.route('/giris',methods=['GET', 'POST'])
def giris():
    if request.method == 'POST':
        # index.html formundan isim gelecek
        mail = request.form["email"]
        parola = request.form["parola"]
        veritabani=db.find_one({"mail": mail})
        # epostaya ait olan kullanıcı var
        if   veritabani is not  None :
          if parola == veritabani.get('parola'):
            # şifre de eşleşiyorsa giriş başarılıdır
            # kullanıcının epostasını session içine al
            session['ad'] =  veritabani.get('ad')
            # todo ekleyebileceği sayfaya yönlendiriyoruz.
            return redirect('/yorumsayfa')
          else:
            durum="Hatalı şifre girdiniz"
            return render_template('giris.html',hata=durum)
        else:
            durum="Hatalı email girdiniz"
            return render_template('giris.html',hata=durum)
    else:
        return render_template('giris.html')

@app.route('/kapat')
def kapat():
    session.pop('eposta', None)
    return redirect('/')

@app.route('/kaydol',methods=["POST"])
def kayit():
  if request.method == 'POST':
        # index.html formundan isim gelecek
        ad = request.form["first_name"]
        soyad = request.form["last_name"]
        mail = request.form["email"]
        telefon = request.form["icon_telephone"]
        cinsiyet = request.form["cins"]
        parola = request.form["password"]
       
        mydict = { "ad": ad, "soyad":soyad, "mail": mail , "telefon": telefon,"cinsiyet": cinsiyet,"parola":parola}
        u = db.find_one({'mail':mail})
        if u is None :
                x = db.insert_one(mydict)
        else:
            flash(f"{mail} eposta adresi daha önceden sistemde kayıtlı")
            return redirect('/')
  return redirect('/')
@app.route('/cikisyap',methods=['GET', 'POST'])
def cikisyap():
    session.pop('ad', None)
    return redirect('/')

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 
