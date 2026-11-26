import streamlit as st
import pandas as pd

st.title("🧾 Kasir Sederhana dengan Diskon")

# Daftar barang dan harganya (dict)
katalog = {
    "Nasi Goreng": 15000,
    "Mie Ayam": 12000,
    "Es Teh": 4000,
    "Kopi": 8000,
}


# Fungsi buatan sendiri: menentukan persen diskon (logika if/elif/else)
def hitung_diskon(total, member):
    if total >= 100000:
        persen = 15
    elif total >= 50000:
        persen = 10
    else:
        persen = 0

    if member:
        persen = persen + 5  # bonus diskon untuk member
    return persen


def rupiah(angka):
    return "Rp " + f"{angka:,.0f}".replace(",", ".")


# ---------- INPUT ----------
# Widget 1: pilih barang
dipilih = st.multiselect("Pilih barang", list(katalog.keys()))

# Widget 2: jumlah tiap barang (dibuat dengan loop)
jumlah_barang = {}
for barang in dipilih:
    jumlah_barang[barang] = st.number_input(
        f"Jumlah {barang} ({rupiah(katalog[barang])})",
        min_value=1, value=1, step=1, key=barang,
    )

# Widget 3: status member
member = st.checkbox("Pelanggan member (+5% diskon)")

# Widget 4: uang bayar
uang_bayar = st.number_input("Uang bayar (Rp)", min_value=0, step=1000)

# ---------- PROSES & OUTPUT ----------
if len(dipilih) == 0:
    st.info("Pilih minimal satu barang dulu.")
else:
    total = 0
    daftar_barang = []
    daftar_subtotal = []

    for barang in dipilih:
        subtotal = katalog[barang] * jumlah_barang[barang]
        total = total + subtotal
        daftar_barang.append(barang)
        daftar_subtotal.append(subtotal)

    persen = hitung_diskon(total, member)
    potongan = total * persen / 100
    total_bayar = total - potongan

    # Output 1: st.metric
    kol1, kol2, kol3 = st.columns(3)
    kol1.metric("Total belanja", rupiah(total))
    kol2.metric("Diskon", f"{persen}%", f"- {rupiah(potongan)}", delta_color="off")
    kol3.metric("Total bayar", rupiah(total_bayar))

    # Status pembayaran
    if uang_bayar >= total_bayar:
        st.success(f"Kembalian: {rupiah(uang_bayar - total_bayar)}")
    else:
        st.error(f"Uang kurang: {rupiah(total_bayar - uang_bayar)}")

    # Output 2: grafik subtotal tiap barang
    st.subheader("Grafik subtotal per barang")
    data = pd.DataFrame({"Subtotal": daftar_subtotal}, index=daftar_barang)
    st.bar_chart(data)