// Menunggu sampai seluruh halaman HTML dimuat sebelum menjalankan script
document.addEventListener("DOMContentLoaded", () => {
  const uploadForm = document.getElementById("upload-form");
  const fileInput = document.getElementById("file-input");
  const fileNameDisplay = document.getElementById("file-name");
  const submitBtn = document.getElementById("submit-btn");

  // Pastikan semua elemen ditemukan sebelum menambahkan event listener
  if (fileInput) {
    // Menampilkan nama file yang dipilih oleh pengguna
    fileInput.addEventListener("change", () => {
      if (fileInput.files.length > 0) {
        fileNameDisplay.textContent = fileInput.files[0].name;
      } else {
        fileNameDisplay.textContent = "Belum ada file yang dipilih";
      }
    });
  }

  if (uploadForm) {
    // Menambahkan efek loading saat form disubmit
    uploadForm.addEventListener("submit", () => {
      // Cek apakah file sudah dipilih
      if (fileInput && fileInput.files.length > 0) {
        submitBtn.textContent = "Mengecek...";
        submitBtn.disabled = true;
      }
    });
  }
});
