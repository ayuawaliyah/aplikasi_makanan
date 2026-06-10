from flask import Flask, render_template, request

app = Flask(__name__)

# ============================================
# CLASS MENU
# ============================================

class Menu:

    def __init__(self, id_menu, nama_menu, harga):
        self.id_menu = id_menu
        self.nama_menu = nama_menu
        self.harga = harga


# ============================================
# CLASS PESANAN
# ============================================

class Pesanan:

    def __init__(self):
        self.daftar_pesanan = []

    def tambah_pesanan(self, menu, qty):
        self.daftar_pesanan.append((menu, qty))

    def hitung_total(self):

        total = 0

        for menu, qty in self.daftar_pesanan:
            total += menu.harga * qty

        return total


# ============================================
# DATA MENU
# ============================================

daftar_menu = [

    Menu(1, "Nasi Goreng", 20000),
    Menu(2, "Mie Ayam", 15000),
    Menu(3, "Ayam Geprek", 18000),
    Menu(4, "Es Teh", 5000)

]


# ============================================
# HALAMAN LOGIN
# ============================================

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # ====================================
        # LOGIN ADMIN
        # ====================================

        if username == "admin" and password == "admin123":

            return render_template(
                "admin.html",
                menu=daftar_menu
            )

        # ====================================
        # LOGIN PELANGGAN
        # ====================================

        elif username == "ayu" and password == "123":

            return render_template(
                "menu.html",
                menu=daftar_menu
            )

        else:
            return """
            <h2>Login gagal!</h2>
            <a href='/'>Kembali Login</a>
            """

    return render_template("login.html")


# ============================================
# TAMBAH MENU (ADMIN)
# ============================================

@app.route("/tambah_menu", methods=["POST"])
def tambah_menu():

    nama = request.form["nama"]
    harga = int(request.form["harga"])

    id_baru = len(daftar_menu) + 1

    menu_baru = Menu(
        id_baru,
        nama,
        harga
    )

    daftar_menu.append(menu_baru)

    return render_template(
        "admin.html",
        menu=daftar_menu
    )


# ============================================
# PESAN MAKANAN (PELANGGAN)
# ============================================

@app.route("/pesan", methods=["POST"])
def pesan():

    pesanan = Pesanan()

    for menu in daftar_menu:

        qty = request.form.get(
            f"qty_{menu.id_menu}"
        )

        if qty and int(qty) > 0:

            pesanan.tambah_pesanan(
                menu,
                int(qty)
            )

    total = pesanan.hitung_total()

    return render_template(
        "struk.html",
        pesanan=pesanan.daftar_pesanan,
        total=total
    )


# ============================================
# RUN PROGRAM
# ============================================

if __name__ == "__main__":
    app.run(debug=True)