🛡️ SLAM — Splunk Log & Attack Monitoring

SLAM (Splunk Log & Attack Monitoring) — локальна SIEM-лабораторія та симулятор веб-атак, створений для демонстрації практичних навичок SOC Analyst / Security Engineer.

Проєкт дозволяє розгорнути ізольоване середовище моніторингу безпеки, збирати логи веб-сервера NGINX у Splunk Enterprise, виявляти підозрілу активність за допомогою власних SPL-запитів та відпрацьовувати процес реагування на інциденти.

⸻

📌 Основні можливості

* 🏗️ Контейнеризована SIEM-інфраструктура на базі Docker.
* 📊 Централізований збір та аналіз логів через Splunk Enterprise.
* 🌐 NGINX як тестова Web-мiшень для генерації реалістичних логів.
* 🤖 Кастомний Python Attack Simulator для генерації різних типів трафіку.
* 🔍 Виявлення:
    * SQL Injection;
    * Path Traversal;
    * Brute-force;
    * підозрілих HTTP-запитів.
* 📈 Аналіз активності атак у часовій шкалі за допомогою timechart.
* 🎯 Визначення IP-адрес, з яких надходить найбільша кількість підозрілих запитів.
* 🚨 Створення Alert-логіки для виявлення Brute-force.
* 🧠 Використання rex для динамічного вилучення полів із нестандартних логів.
* 🛡️ Практичний SOC Playbook для реагування на інциденти.
* 🍎 Підтримка запуску на Apple Silicon через Docker x86_64 emulation.

⸻

🏗️ Архітектура

SLAM складається з трьох основних компонентів:

1. Splunk Enterprise

Центральний компонент лабораторії, який використовується для:

* збору логів;
* індексації подій;
* пошуку підозрілої активності;
* написання SPL-запитів;
* створення Alert;
* аналізу та візуалізації подій.

У проєкті використовується Splunk Enterprise 9.3.0.

2. NGINX

NGINX виступає тестовим Web-сервером та генерує стандартні:

access.log
error.log

Саме ці логи надалі передаються до Splunk для аналізу.

3. SLAM Attack Simulator

attack_sim.py — кастомний Python-скрипт на базі бібліотеки requests.

Він генерує суміш:

* легітимного HTTP-трафіку;
* Brute-force спроб;
* SQL Injection payloads;
* Path Traversal запитів;
* звернень до адміністративних endpoint’ів.

Це дозволяє отримати контрольований потік подій для тестування SIEM та правил детектування.

⸻

🚀 Запуск лабораторії

1. Необхідне програмне забезпечення

Перед запуском переконайтеся, що встановлені:

* Docker
* Docker Compose
* Python 3.10+
* Git

Для запуску Splunk рекомендується використовувати Docker Desktop.

⸻

2. Запуск Docker-інфраструктури

Перейдіть до директорії проєкту:

cd SLAM

Запустіть контейнери:

docker-compose up -d

Перевірте стан контейнерів:

docker-compose ps

Після успішного запуску Web-інтерфейс Splunk буде доступний за адресою:

http://localhost:8000

🔑 Облікові дані

Username: admin
Password: Secur1tyP@ssw0rd!

⚠️ Ці облікові дані призначені виключно для локальної лабораторії. Не використовуйте їх у production-середовищі.

⸻

📊 Налаштування збору логів у Splunk

Після запуску Splunk необхідно налаштувати Input для логів NGINX.

Крок 1 — Data Inputs

У Splunk відкрийте:

Settings
→ Data Inputs
→ Files & Directories

Натисніть:

New Local Data

⸻

Крок 2 — Вкажіть директорію логів

Використайте:

/var/log/nginx_logs

⸻

Крок 3 — Sourcetype

На етапі Set Sourcetype створіть новий тип:

access_combined

⸻

Крок 4 — Index

У Input Settings створіть або виберіть індекс:

web_logs

Після завершення Splunk почне індексувати логи NGINX.

⸻

🤖 Запуск Attack Simulator

Встановіть Python-залежності:

pip install -r requirements.txt

Запустіть симулятор:

python attack_sim.py

Після запуску скрипт почне генерувати HTTP-запити до NGINX.

У потоці трафіку будуть присутні як звичайні запити, так і симульовані атаки.

⸻

🔍 SPL Detection Rules

SLAM використовує власні SPL-запити для виявлення підозрілої активності.

Через невеликий початковий обсяг логів Splunk може автоматично призначити їм технічний sourcetype:

access-too_small

Для стабільного аналізу використовуються регулярні вирази через команду:

rex

Це дозволяє динамічно вилучати необхідні поля без залежності від автоматичного парсингу Splunk.

⸻

1. Загальний лічильник Web-атак

Запит підраховує кількість подій, які містять характерні ознаки SQL Injection або Path Traversal.

index="web_logs" source="*access.log" ("*OR*" OR "*UNION*" OR "*SELECT*" OR "*etc/passwd*" OR "*win.ini*")
| stats count as Total_Web_Attacks

Результат:

Total_Web_Attacks
-----------------
       42

⸻

2. Топ IP-адрес нападників

Запит визначає IP-адреси з найбільшою кількістю підозрілих HTTP-запитів.

index="web_logs" source="*access.log" ("*OR*" OR "*UNION*" OR "*etc/passwd*" OR "GET /login" OR "POST /login" OR "POST /admin" OR "GET /administrator")
| rex field=_raw "^(?<clientip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
| stats count by clientip
| sort - count
| head 5

Це дозволяє швидко визначити найбільш активні джерела підозрілої активності.

⸻

3. Динаміка атак у часі

За допомогою timechart можна побудувати часовий графік атак.

index="web_logs" source="*access.log" ("*OR*" OR "*UNION*" OR "*etc/passwd*" OR "GET /login" OR "POST /login" OR "POST /admin" OR "GET /administrator")
| rex field=_raw "\"(?:GET|POST) (?<uri_path>[^\s\?]+)"
| eval Attack_Type=case(
searchmatch("*etc/passwd*") OR searchmatch("*win.ini*"), "Path Traversal",
searchmatch("*UNION*") OR searchmatch("*OR*"), "SQL Injection",
searchmatch("login") OR searchmatch("admin"), "Brute-force",
1=1, "Other"
)
| timechart span=1m count by Attack_Type

Отриманий графік дозволяє побачити:

* коли почалася атака;
* її тривалість;
* інтенсивність;
* співвідношення різних типів атак.

⸻

4. Brute-force Detection

Це правило виявляє понад 15 спроб доступу за одну хвилину з однієї IP-адреси.

index="web_logs" source="*access.log" ("login" OR "admin")
| rex field=_raw "^(?<clientip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[[^\]]+\] \"(?<method>\w+) (?<uri_path>[^\s\?]+)[^\"]*\" (?<status>\d+)"
| search uri_path="*login*" OR uri_path="*admin*"
| bin _time span=1m
| stats count by clientip, uri_path, _time
| where count > 15

У production-середовищі такий запит може бути основою для Splunk Alert.

⸻

🚨 SOC Alert

При спрацюванні правила можна використовувати назву:

SLAM Alert: High Volume of Login Failures

Alert сигналізує про можливу Brute-force атаку та передає подію на подальший аналіз SOC-аналітику.

⸻

🛡️ SOC Playbook

SLAM Alert: High Volume of Login Failures

1. 🔎 Triage

Перший етап — перевірити контекст інциденту.

Аналітик повинен:

* визначити clientip;
* перевірити джерело трафіку;
* визначити кількість спроб;
* перевірити User-Agent;
* перевірити цільові endpoint’и;
* встановити часовий проміжок атаки.

Особливу увагу слід звернути на автоматизовані User-Agent або характерні ознаки інструментів автоматизації.

⸻

2. 🔬 Post-Exploitation Check

Після серії невдалих спроб необхідно перевірити, чи не було успішної авторизації.

Приклад SPL:

index="web_logs" clientip="<IP_нападника>" status=200

Інтерпретація:

Немає успішних відповідей → ймовірно, атака неуспішна
Є успішна відповідь → необхідне подальше розслідування

⚠️ Статус 200 сам по собі не доводить компрометацію облікового запису. Необхідно перевірити контекст запиту та поведінку застосунку.

⸻

3. 🚧 Containment

У разі підтвердження атаки:

1. Заблокувати джерело на Firewall або WAF.
2. Перевірити інші запити з тієї ж IP-адреси.
3. Якщо є ознаки успішної компрометації — заблокувати відповідний обліковий запис.
4. Ініціювати скидання пароля.
5. Перевірити активні сесії.
6. Зібрати додаткові логи для Incident Response.

⸻

🍎 Сумісність з Apple Silicon

Окремою особливістю проєкту є запуск Splunk на комп’ютерах із процесорами Apple Silicon.

Проблема

Нові версії Splunk використовують оновлений KV Store, який базується на MongoDB 7.0.

MongoDB 7.0 має вимогу щодо підтримки AVX-інструкцій.

Apple Silicon не підтримує AVX, тому запуск відповідних x86-образів через емуляцію може призводити до проблем із KV Store та Web UI Splunk.

⸻

Рішення

У проєкті зафіксовано:

Splunk Enterprise 9.3.0

та використовується:

platform: linux/amd64

Це дозволяє запускати контейнер Splunk через Docker Desktop на Apple Silicon із використанням x86_64-емуляції.

Такий підхід призначений саме для лабораторного середовища та може мати більші накладні витрати порівняно з нативним ARM64-запуском.

⸻

📂 Приклад структури проєкту

SLAM/
├── docker-compose.yml
├── attack_sim.py
├── requirements.txt
├── README.md
│
├── nginx/
│   ├── nginx.conf
│   └── logs/
│
└── splunk/
└── ...

Фактична структура може відрізнятися залежно від конфігурації конкретної версії проєкту.

⸻

🧪 Сценарії, які демонструє лабораторія

Сценарій	Джерело	Детектування
SQL Injection	attack_sim.py	SPL + rex
Path Traversal	attack_sim.py	SPL + rex
Brute-force	attack_sim.py	Threshold Alert
Підозрілий HTTP-трафік	NGINX	SPL
Масові запити з IP	NGINX	stats
Активність у часі	NGINX	timechart

⸻

🎯 Навички, які демонструє проєкт

SLAM демонструє практичні навички, актуальні для позицій SOC Analyst та Security Engineer:

SOC / Detection Engineering

* написання SPL;
* створення Detection Rules;
* робота з SIEM;
* аналіз Web-логів;
* Threat Hunting;
* побудова Alert;
* аналіз IP та HTTP-поведінки;
* класифікація типів атак.

Security Engineering

* Docker;
* контейнеризація;
* побудова локальної лабораторної інфраструктури;
* інтеграція NGINX та Splunk;
* логування;
* troubleshooting;
* робота з різними CPU-архітектурами.

Incident Response

* Triage;
* Investigation;
* Post-Exploitation Check;
* Containment;
* аналіз наслідків інциденту;
* створення SOC Playbook.

⸻

📝 Висновки

Розгортання та тестування SLAM дозволило продемонструвати повний базовий цикл роботи з Web Security Monitoring:

Attack Simulation
↓
NGINX
↓
Log Collection
↓
Splunk
↓
Detection Rules
↓
Alert
↓
SOC Investigation
↓
Response

Ключові висновки

1. SIEM можна ефективно використовувати навіть у локальній лабораторії.

Docker дозволяє швидко створити ізольоване середовище для тестування правил детектування без необхідності розгортати повноцінну корпоративну інфраструктуру.

2. Regex є важливим інструментом SOC-аналітика.

Автоматичний парсинг логів не завжди працює ідеально. Використання rex дозволяє самостійно витягувати необхідні поля та проводити аналіз навіть нестандартних логів.

3. Детектування має враховувати контекст.

Сам факт наявності підозрілого рядка не завжди означає успішну атаку. Необхідно аналізувати IP, endpoint, HTTP-метод, статус відповіді, час та інші пов’язані події.

4. Detection Engineering та Incident Response повинні працювати разом.

Виявлення атаки — лише перший етап. SOC-аналітик повинен мати чіткий процес для Triage, Investigation та Containment.

5. Проєкт максимально наближений до реальних SOC-задач.

SLAM демонструє не лише написання SPL-запитів, а повний workflow:

Infrastructure
↓
Log Collection
↓
Detection
↓
Alerting
↓
Investigation
↓
Incident Response

⸻

⚠️ Disclaimer

SLAM призначений виключно для навчання, тестування та дослідження кібербезпеки в контрольованому середовищі.

Attack Simulator повинен використовуватися лише проти локальної тестової інфраструктури або систем, на які ви маєте явний дозвіл.

Не використовуйте компоненти цього проєкту для атак на сторонні системи без відповідної авторизації.

Автор не несе відповідальності за шкоду або наслідки, спричинені неправомірним використанням проєкту.

⸻

👤 Автор

Розроблено dreamyr
