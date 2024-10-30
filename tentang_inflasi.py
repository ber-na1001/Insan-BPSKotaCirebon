import streamlit as st

def show():
    st.title("Tentang Inflasi")
    st.write(
        """
        **Inflasi** adalah kenaikan harga barang dan jasa secara umum dalam suatu ekonomi selama periode tertentu. 
        Ini mengindikasikan bahwa daya beli uang menurun, sehingga setiap unit mata uang dapat membeli lebih sedikit barang dan jasa.

        ### Inflasi menurut Year-over-Year (YoY)
        **Inflasi YoY** mengukur perubahan harga dari satu tahun ke tahun berikutnya. Misalnya, jika harga barang dan jasa pada September tahun ini adalah 105 dan pada September tahun lalu adalah 100, maka inflasi YoY adalah 5%. Pengukuran ini memberikan gambaran yang lebih luas tentang tren inflasi dalam jangka panjang.

        ### Inflasi menurut Month-to-Month (MtM)
        **Inflasi MtM** mengukur perubahan harga dari bulan ke bulan. Misalnya, jika harga barang dan jasa pada bulan Agustus adalah 102 dan pada bulan September adalah 105, maka inflasi MtM adalah 2,94% [(105-102)/102 x 100]. Pengukuran ini memberikan pandangan yang lebih langsung dan responsif terhadap perubahan harga dalam waktu singkat.

        ### Inflasi Year-to-Date (YtD)
        **Inflasi YtD** mengukur persentase perubahan harga dari awal tahun hingga periode tertentu dalam tahun yang sama. Misalnya, jika harga barang dan jasa pada Januari adalah 100 dan pada September mencapai 105, maka inflasi YtD adalah 5%. Metode pengukuran ini bermanfaat untuk memantau perubahan harga kumulatif sepanjang tahun berjalan, memberikan perspektif tentang dinamika inflasi yang terjadi dalam kurun waktu lebih pendek dibandingkan inflasi tahunan (YoY).
        """
    )
