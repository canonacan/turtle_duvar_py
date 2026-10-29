# ROS 2 Duvarlardan Kaçan Kaplumbağa

## Proje Hakkında

Bu proje, **ROS 2 Humble** ve Python kullanılarak geliştirilen bir duvardan kaçan kaplumbağa uygulamasıdır. Turtlesim simülasyonundaki kaplumbağanın konumu sürekli takip edilir. Kaplumbağa belirlenen koordinat sınırlarının dışına çıktığında alanın merkezine doğru döner ve hareketine devam eder.

Uygulama ayrıca kaplumbağanın konumunu saniyede bir terminale yazdırır. Bonus özellik olarak ileri hareket hızı, dönüş hızı ve X/Y koordinat sınırları ROS 2 parametreleriyle çalıştırma sırasında ayarlanabilir.

## Kullanılan Teknolojiler

- Ubuntu 22.04
- ROS 2 Humble
- Python 3
- `rclpy`
- `geometry_msgs`
- `turtlesim`
- `colcon`
- Git ve GitHub

## Paket Yapısı

```text
turtle_duvar_py/
├── screenshots/
│   ├── terminal.png
│   └── turtlesim.png
├── turtle_duvar_py/
│   ├── __init__.py
│   └── turtle_duvar.py
├── resource/
│   └── turtle_duvar_py
├── test/
│   ├── test_copyright.py
│   ├── test_flake8.py
│   └── test_pep257.py
├── package.xml
├── setup.cfg
├── setup.py
├── .gitignore
├── LICENSE
└── README.md
```

> Not: Ekran görüntülerinin dosya adlarını kendi klasörünüzde farklı tuttuysanız, aşağıdaki görsel bağlantılarındaki adları da aynı şekilde güncelleyin. Bu depoda önerilen adlar `terminal.png` ve `turtlesim.png` şeklindedir.

## Çalışma Mantığı

1. `turtle_duvar` düğümü, `/turtle1/pose` konusu üzerinden kaplumbağanın X/Y koordinatlarını ve yön açısını alır.
2. Düğüm, `/turtle1/cmd_vel` konusu üzerinden hareket komutları gönderir.
3. Kaplumbağa belirlenen koordinat aralığındaysa ileri doğru hareket eder.
4. X veya Y koordinatı tanımlanan sınırların dışına çıktığında algoritma alanın merkezini hesaplar.
5. `atan2` fonksiyonuyla merkeze doğru hedef yön açısı belirlenir.
6. Mevcut yön ile hedef yön arasındaki açı farkına göre kaplumbağa yerinde döner. Açı farkı yeterince küçüldüğünde yeniden ileri gider.
7. Konum bilgisi her saniye terminale yazdırılır.
8. Hız ve sınır değerleri varsayılan olarak tanımlıdır; ROS 2 parametreleriyle çalıştırma sırasında değiştirilebilir.

**Varsayılan değerler**

| Parametre | Varsayılan değer | Açıklama |
|---|---:|---|
| `speed` | `2.0` | İleri hareket hızı |
| `turn_speed` | `1.5` | Açısal dönüş hızı |
| `min_x` | `1.0` | X koordinatının alt sınırı |
| `max_x` | `10.0` | X koordinatının üst sınırı |
| `min_y` | `1.0` | Y koordinatının alt sınırı |
| `max_y` | `10.0` | Y koordinatının üst sınırı |

> Algoritma sınırın dışına çıkıldığını algıladığında dönüş yapar; sınırın hemen içindeyken önleyici manevra hesaplamaz.

## Ekran Görüntüleri

### Terminal çıktısı

Düğümün başlatılması, kullanılan parametreler ve kaplumbağanın konum logları:

![Terminal çıktısı](screenshots/terminal.png)

### Turtlesim simülasyonu

Kaplumbağanın simülasyondaki hareket izi:

![Turtlesim simülasyonu](screenshots/turtlesim.png)

## Kurulum ve Çalıştırma

### 1. Gereksinimler

Bu adımlar Ubuntu 22.04 ve ROS 2 Humble kurulu bir ortam içindir. Aşağıdaki komutları terminalde çalıştırın.

ROS 2 ortamını etkinleştirin:

```bash
source /opt/ros/humble/setup.bash
```

Gerekli araçların kurulu olduğundan emin olun:

```bash
sudo apt update
sudo apt install -y git python3-colcon-common-extensions python3-rosdep
```

Eğer sistemde `rosdep` daha önce başlatılmadıysa, ilk kullanımda aşağıdaki komut gerekebilir:

```bash
sudo rosdep init
rosdep update
```

> `sudo rosdep init` daha önce yapılmışsa “already initialized” benzeri bir mesaj verebilir; bu durumda tekrar çalıştırmak gerekmez.

### 2. Depoyu GitHub'dan İndirme

Önce ROS 2 workspace klasörünü ve `src` dizinini oluşturun:

```bash
mkdir -p ~/robotik/ros2_ws/src
cd ~/robotik/ros2_ws/src
```

Depoyu klonlayın:

```bash
git clone https://github.com/canonacan/turtle_duvar_py.git
```

Depoyu klonladıktan sonra klasör yapısı şu şekilde olacaktır:

```text
~/robotik/ros2_ws/src/turtle_duvar_py/
```

> Depoyu doğrudan `~/robotik/ros2_ws/src/` içine klonladıysanız ayrıca `mv` komutu çalıştırmanız gerekmez.

### 3. Bağımlılıkları Yükleme

Workspace kök dizinine geçin ve ROS 2 ortamını etkinleştirin:

```bash
cd ~/robotik/ros2_ws
source /opt/ros/humble/setup.bash
```

Depodaki bağımlılıkları `rosdep` ile yüklemeyi deneyin:

```bash
rosdep install --from-paths src --ignore-src -r -y
```

### 4. Paketi Derleme

```bash
cd ~/robotik/ros2_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select turtle_duvar_py
source install/setup.bash
```

Derleme başarılı olduğunda paket, ROS 2 tarafından çalıştırılabilir hâle gelir.

### 5. Turtlesim Simülasyonunu Başlatma

Birinci terminali açın ve şu komutları çalıştırın:

```bash
source /opt/ros/humble/setup.bash
ros2 run turtlesim turtlesim_node
```

Turtlesim penceresi açılacaktır. Bu terminal açık kalmalıdır.

### 6. Duvarlardan Kaçan Kaplumbağa Düğümünü Başlatma

İkinci terminali açın:

```bash
cd ~/robotik/ros2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run turtle_duvar_py turtle_duvar
```

Kaplumbağa ileri gitmeli, belirlenen koordinat sınırlarının dışına çıktığında merkeze doğru dönmeli ve konum bilgileri terminalde görünmelidir.

### 7. Parametrelerle Çalıştırma (Bonus)

Parametreleri değiştirmek için düğümü çalıştırırken `--ros-args -p` sözdizimini kullanabilirsiniz. Örneğin:

```bash
ros2 run turtle_duvar_py turtle_duvar --ros-args \
  -p speed:=3.0 \
  -p turn_speed:=1.5 \
  -p min_x:=2.0 \
  -p max_x:=9.0 \
  -p min_y:=2.0 \
  -p max_y:=9.0
```

Bu örnekte ileri hız `3.0`, dönüş hızı `1.5` olur ve koordinat sınırları X/Y için `2.0–9.0` olarak ayarlanır. Parametre verilmezse uygulamadaki varsayılan değerler kullanılır.

Çalışan düğümün parametrelerini görüntülemek için başka bir terminal açın:

```bash
source /opt/ros/humble/setup.bash
ros2 param list /turtle_duvar
```

Bir parametrenin değerini okumak için:

```bash
ros2 param get /turtle_duvar speed
ros2 param get /turtle_duvar min_x
ros2 param get /turtle_duvar max_x
```

> Bu uygulama parametre değerlerini düğüm başlatılırken okur. Mevcut kodda çalışma esnasında `ros2 param set` ile değiştirilen değerler hareket algoritmasına otomatik olarak yeniden aktarılmaz; farklı değerlerle çalışmak için düğümü yeni parametrelerle yeniden başlatın.

### 8. ROS 2 Konularını Kontrol Etme

Düğüm çalışırken konuları listelemek için:

```bash
source /opt/ros/humble/setup.bash
ros2 topic list
```

Kaplumbağanın konum verisini görmek için:

```bash
ros2 topic echo /turtle1/pose
```

Hareket komutlarının gönderildiğini kontrol etmek için:

```bash
ros2 topic echo /turtle1/cmd_vel
```

İsterseniz ROS 2 düğüm grafiğini görüntülemek için `rqt_graph` kullanabilirsiniz:

```bash
sudo apt install -y ros-humble-rqt-graph
ros2 run rqt_graph rqt_graph
```

### 9. Düğümü Durdurma

Çalışan düğümleri durdurmak için ilgili terminal penceresinde `Ctrl + C` tuşlarına basın.

## Beklenen Çıktı

Düğüm başladığında terminalde benzer mesajlar görünür:

```text
[turtle_duvar]: Duvardan kacan kaplumbaga baslatildi.
[turtle_duvar]: Hiz: 2.0, Donus hizi: 1.5
[turtle_duvar]: X siniri: 1.0-10.0, Y siniri: 1.0-10.0
[turtle_duvar]: Konum: x=7.34, y=5.54
```

Koordinatlar kaplumbağanın hareketine göre değişir; yukarıdaki konum değeri yalnızca örnektir.

## ROS 2 Konuları ve Düğüm

- **Düğüm:** `/turtle_duvar` — konumu takip eder ve hareket kararlarını verir.
- **Abone olunan konu:** `/turtle1/pose` — kaplumbağanın konum ve yön bilgisini sağlar.
- **Yayınlanan konu:** `/turtle1/cmd_vel` — kaplumbağanın doğrusal ve açısal hız komutlarını taşır.
- **Simülasyon düğümü:** `/turtlesim` — kaplumbağa simülasyonunu çalıştırır.

## GitHub Deposu

Kaynak kodu ve ekran görüntüleri:

[https://github.com/canonacan/turtle_duvar_py](https://github.com/canonacan/turtle_duvar_py)

## Lisans

Paketin `setup.py` dosyasında lisans Apache-2.0 olarak belirtilmiştir. Bu lisans kullanılacaksa depoda lisansın tam metnini içeren bir `LICENSE` dosyası bulunmalıdır. Lisansı resmen seçmediyseniz, lisans seçimini yapmadan bu alanı kesinleştirmeyin.
