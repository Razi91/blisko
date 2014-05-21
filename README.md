#Blisko Academy

System prowadzenia szkoleń w stylu e-learningowym



##Instalacja

System ten zbudowany jest w oparciu o framework Django.
Do uruchomienia wymaga serwera obsługującego tą technologię (CGI)

Po utworzeniu bazy danych (manage.py syncdb) należy włączyć shella
i uruchomić:

```Python
from Blisko.install import *
install_basic()
install_tests()
```
Jeśli baza już była stworzona, należy ją usunąć przed synchronizacją.
Zaleca się stosować login i hasło admina: `admin`.


Zalecana baza danych to SQLite w celach testowych.
