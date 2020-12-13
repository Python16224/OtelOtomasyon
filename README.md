## Python Eğitici Eğitimi Python 16224 Proje Grubu Otel Otomasyon Projesi ##

## Otel Otomasyon Projesi ###

[Proje Linki](https://github.com/Python16224/OtelOtomasyon)

![Logo]( https://github.com/Python16224/OtelOtomasyon/blob/master/icon.png)

### Projenin Amacı ###
Otel girişlerinde müşteri kayıt sürelerinin uzun zaman alması göz önünde bulundurularak ve malum pandemi süresince müşteri ve çalışan arasında kimlik v.b. alışverişini en aza indirmek amacıyla müşterinin kimliğini otel otomasyon programının kurulu olduğu bilgisayara bağlı web kameraya uzaklıktan göstererek müşteri kaydının tamamlanması ve aynı şekilde otel çıkışında da tekrar kimliğini kameraya göstererek otel çıkış işlemlerinin tamamlanması amaçlanmaktadır.  

Projemizin stabil çalışması durumunda otellerde müşteri kaydı ve müşteri çıkışı işlemleri, temas en aza indirerek yapılabilecektir. Proje geliştirilerek ödeme işlemi de kredi kartı kameraya tutularak yapılması sağlanabilir.

### Projenin Çalışması ###
Kişi Ekle’ye basıldığında kimlik kameraya gösterilerek okutulan bilgiler mesaj penceresi olarak ekrana gelir. Bilgiler doğru ise OK butonu ile onaylanarak tabloya aktarılır. Cancel ile tekrar kimlik okuma işlemi aktif hale gelir. Eğer veri okumada hata meydana gelirse uyarı mesajı çıkar ve kimlik yeniden okutulur. Kimlik okutulduğunda form öğeleri aktif hale gelir ve veriler seçilip Giriş Yap butonuna tıklandığında veriler veritabanına kaydedilir. Kimlik okutulduğunda veritabanından TC Kimlik No kontrolü yapılır. Eğer kimlik no veritabanında var ise form alanı pasif olur. Sadece Çıkış Yap butonu aktif hale gelir. Çıkış Yap butonuna tıklandığında ise veriler silinir ve kimlik okuma tekrar aktif hale gelir.

### Proje Bileşenleri ve Görevleri ###
Ortam olarak Phyton 3.7, Anaconda, SQLAlchemy veritabanı kullanıldı. Sqlite browser, Vscode, Pycharm tasarımlar için kullanıldı. Kütüphanelerden Opencv, Sqlalchemy, Pyqt5, Datetime, PIL, Pytesseract kullanıldı.

##### Otel Otomasyon programımızın kullanıcı arayüzü: #####
- Kimlik Okuma (Resim çekme/Resmi okuma)
- Müşteri İşlemleri (Müşteri ekle)
- Çıkış İşlemleri (Kayıt sil)
- Giriş-çıkış tarihleri
- Oda ve fiyat bilgisi

##### Proje dosya ağacımız aşağıdaki gibidir: #####
- database.db - Veritabanı,
- database.py - SQLAlchemy kullanarak veritabanı modelimizi oluşturduğumuz dosya,
- icon.png - Uygulamanın başlık kısmında bulunan icon resmi,
- id.jpg - OCR işlemi için kameradan yakalanan anlık görüntü dosyası,
- main.py - Projemizi çalıştıran ana dosya,
- main_ui.ui - Qt Designer tasarım dosyası,
- template.py - Projenin görsel tasarım kodlarının saklandığı dosya,
- thread.py - PC ye bağlı kamera yardımıyla program üzerinde anlık video görüntü aktarımını sağlayan kodların saklandığı dosya.

### Hazırlayanlar ###
Python16224 Proje Grubu

### Lisans ###
MIT Licence
