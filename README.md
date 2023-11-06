# TUGAS TEKNOLOGI SISTEM TERINTEGRASI
## ARDHAN NUR URFAN
## 18221118

> To see API docs [_here_](http://shoes-shop.cxfgced6hzfgg7cj.eastus.azurecontainer.io/docs)

### Virtual Shoes Shop API
Core pada layanan ini, seorang pelanggan dapat melihat sepatu yang akan dibeli melalui 3D virtual. Sistem ini diimplementasikan secara microservice. Pada core sistem ini terdapat tiga tabel yakni brands, shoes, dan varians yang memiliki keterkaitan satu sama lain. Terdapat tabel brands yang berisikan merek sepatu yang tersedia pada toko ini. Kemudian, setiap merek memiliki banyak jenis sepatu yang berbeda-beda. Dalam setiap sepatu juga terdapat beberapa warna model berbeda-beda yang dapat dipilih dan dilihat oleh pelanggan. 
Sistem ini merupakan sebuah API yang diimplementasikan menggunakan bahasa pemrograman python3 dan database Azure for MySQL. Adapun library python yang digunakan dalam sistem ini sebagai berikut.

•	fastapi==0.104.1

•	mysql-connector-python==8.2.0

•	pydantic==2.4.2

•	python-dotenv==1.0.0

•	uvicorn==0.24.0.post1

Dalam implementasinya layanan ini dilakukan kontainerisasi menggunakan Docker dan dilakukan deployment di Microsoft Azure.
