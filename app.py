from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "your_secret_key"

# --- База пользователей (логин: пароль, роль) ---
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"},
}

# --- Список новостей ---
news_list = [
    {"title": "Открытие нового магазина", "date": "2025-10-01", "text": "Мы открыли новый магазин на юге города!"},
    {"title": "Сезонные скидки", "date": "2025-10-15", "text": "Осенние скидки до 30% на мебель и текстиль."},
    {"title": "Новое поступление мебели", "date": "2025-11-01", "text": "В продаже появилась коллекция скандинавской мебели."},
    {"title": "Бонусы постоянным покупателям", "date": "2025-11-10", "text": "Копите бонусы за покупки и оплачивайте ими до 20% следующего заказа."},
    {"title": "Мастер-класс по интерьеру", "date": "2025-11-25", "text": "Приглашаем на бесплатный мастер-класс по созданию уюта в доме."}
]

# --- Статьи по разделам ---
articles_data = {
    "catalog": [
        {"title": "Как выбрать диван для гостиной", "text": "При выборе дивана учитывайте форму комнаты, стиль, материал обивки и частоту использования..."},
        {"title": "Преимущества модульной мебели", "text": "Модульная мебель позволяет легко изменять пространство и подстраивать интерьер под свои нужды..."},
        {"title": "Популярные материалы для мебели", "text": "Качественная мебель чаще всего изготавливается из массива дерева, МДФ или композитов премиум-класса..."},
        {"title": "Как ухаживать за текстилем", "text": "Текстиль необходимо пылесосить, стирать при деликатных настройках и хранить вдали от прямых солнечных лучей..."},
        {"title": "Тренды интерьерного дизайна 2025", "text": "В новом сезоне преобладают спокойные оттенки, натуральные материалы и плавные мягкие формы..."},
    ],
    "promo": [
        {"title": "Сезонные скидки на мебель", "text": "Каждую весну и осень проводится распродажа коллекций прошлого года..."},
        {"title": "Купи два товара — получи скидку", "text": "При покупке комплектов мебели действует специальная программа скидок..."},
        {"title": "Именинникам — 10% скидка", "text": "В день рождения действует персональная скидка при предъявлении паспорта..."},
        {"title": "Программа лояльности", "text": "Постоянные покупатели могут накапливать бонусы и обменивать их на товары..."},
        {"title": "Скидки на доставку", "text": "Доставка по городу со скидкой при заказе от определённой суммы..."},
    ],
    "about": [
        {"title": "История компании", "text": "Наша сеть развивается с 2010 года и сегодня включает более 45 магазинов..."},
        {"title": "Наши ценности", "text": "Мы ориентируемся на качество, доступность и долговечность товаров..."},
        {"title": "Команда специалистов", "text": "Консультанты проходят профессиональную подготовку и знают всё о товарах..."},
        {"title": "Надёжные партнёры", "text": "Мы сотрудничаем только с проверенными производителями..."},
        {"title": "Мы рядом с вами", "text": "Наши магазины представлены в большинстве крупных городов России..."},
    ],
    "contacts": [
        {"title": "Как добраться до магазина", "text": "Наши магазины удобно расположены рядом с метро и крупными транспортными узлами..."},
        {"title": "График работы", "text": "Мы работаем ежедневно с 9:00 до 21:00, без выходных..."},
        {"title": "Служба поддержки", "text": "Вы можете связаться с нами по телефону или электронной почте..."},
        {"title": "Оформление доставки", "text": "Доставка осуществляется курьерской службой с предварительным звонком..."},
        {"title": "Возврат и обмен", "text": "Мы соблюдаем закон о защите прав потребителей и принимаем товар надлежащего качества..."},
    ],
}

# --- Гостевая книга (сообщения пользователей) ---
messages = []

# --- Главная страница ---
@app.route("/")
def index():
    style = session.get("style", "default")
    username = session.get("username")
    userrole = session.get("role")
    # Баннеры — список (можно расширить)
    banners = [
        {
            "img": "img/banner1.jpg",
            "title": "Осенние скидки на всё!",
            "desc": "Скидки до 30% на популярные коллекции мебели. Только в октябре!",
            "link": url_for("promo"),
            "btn": "Подробнее"
        },
        {
            "img": "img/banner2.jpg",
            "title": "Новая коллекция 2025",
            "desc": "Модульные кухни и гостиные — стиль и качество для вашего дома.",
            "link": url_for("catalog"),
            "btn": "В каталог"
        }
    ]
    return render_template("index.html", style=style, username=username, userrole=userrole, banners=banners)

# --- Каталог товаров ---
@app.route("/catalog")
def catalog():
    style = session.get("style", "default")
    return render_template("catalog.html", style=style)

# --- Карточка товара ---
@app.route("/product/<int:product_id>")
def product(product_id):
    style = session.get("style", "default")
    return render_template("product.html", style=style, product_id=product_id)

# --- Акции ---
@app.route("/promo")
def promo():
    style = session.get("style", "default")
    return render_template("promo.html", style=style)

# --- О компании ---
@app.route("/about")
def about():
    style = session.get("style", "default")
    return render_template("about.html", style=style)

# --- Контакты ---
@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    style = session.get("style", "default")
    # Форма обратной связи (не сохраняет в базу, просто имитация)
    sent = False
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        sent = True
    return render_template("contacts.html", style=style, sent=sent)

# --- Гостевая книга (обмен сообщениями) ---
@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    style = session.get("style", "default")
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        message = request.form.get("message", "").strip()
        if name and message:
            messages.append({"name": name, "message": message})
    return render_template("feedback.html", style=style, messages=messages)

# --- Лента новостей ---
@app.route("/news")
def news():
    style = session.get("style", "default")
    return render_template("news.html", style=style, news_list=news_list)

# --- Карта сайта ---
@app.route("/sitemap")
def sitemap():
    style = session.get("style", "default")
    return render_template("sitemap.html", style=style)

# --- Переключение стиля ---
@app.route("/set_style/<theme>")
def set_style(theme):
    if theme in ["default", "accessible"]:
        session["style"] = theme
    return redirect(request.referrer or url_for("index"))

# --- Авторизация ---
@app.route("/login", methods=["GET", "POST"])
def login():
    style = session.get("style", "default")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = users.get(username)
        if user and user["password"] == password:
            session["username"] = username
            session["role"] = user["role"]
            flash("Вы успешно вошли!", "success")
            return redirect(url_for("index"))
        else:
            flash("Неверный логин или пароль", "danger")
    return render_template("login.html", style=style)

# --- Регистрация ---
@app.route("/register", methods=["GET", "POST"])
def register():
    style = session.get("style", "default")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users:
            flash("Пользователь уже существует", "danger")
        else:
            users[username] = {"password": password, "role": "user"}
            flash("Регистрация успешна. Теперь вы можете войти.", "success")
            return redirect(url_for("login"))
    return render_template("register.html", style=style)

# --- Выход ---
@app.route("/logout")
def logout():
    session.clear()
    flash("Вы вышли из системы.", "info")
    return redirect(url_for("index"))

# --- Админ-панель (только для admin) ---
@app.route("/admin")
def admin_panel():
    style = session.get("style", "default")
    if session.get("role") != "admin":
        flash("Доступ запрещён: только для администратора!", "danger")
        return redirect(url_for("index"))
    return render_template("admin_panel.html", style=style, users=users)

# --- Поиск по статьям и новостям ---
@app.route("/search", methods=["GET", "POST"])
def search():
    style = session.get("style", "default")
    results = []
    query = ""
    if request.method == "POST":
        query = request.form.get("query", "").lower().strip()
        # Поиск по статьям всех разделов
        for section, articles in articles_data.items():
            for article in articles:
                if query in article["title"].lower() or query in article["text"].lower():
                    results.append({"type": "Статья", "section": section, "title": article["title"], "text": article["text"]})
        # Поиск по новостям
        for news in news_list:
            if query in news["title"].lower() or query in news.get("text", "").lower():
                results.append({"type": "Новость", "section": "news", "title": news["title"], "text": news.get("text", "")})
    return render_template("search.html", style=style, results=results, query=query)

# --- Статьи по разделам ---
@app.route("/articles/<section>")
def articles(section):
    style = session.get("style", "default")
    if section not in articles_data:
        flash("Раздел не найден.", "warning")
        return redirect(url_for('sitemap'))
    return render_template("articles.html", style=style, articles_list=articles_data[section], section=section)

# --- 404 страница ---
@app.errorhandler(404)
def page_not_found(e):
    style = session.get("style", "default")
    return render_template("404.html", style=style), 404

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
