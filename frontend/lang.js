const translations = {
    'id': {
        // App
        'source_context': 'Pilih Sumber Konteks',
        'tab_manual': 'Teks Manual',
        'tab_web': 'URL Web',
        'tab_youtube': 'YouTube',
        'tab_document': 'Dokumen',
        'tab_video': 'Video Lokal',
        'placeholder_manual': "Ketik Topik Berita (misal: 'Berita MotoGP Hari Ini') atau paste teks referensi di sini...",
        'label_file': 'Pilih File',
        'label_video': 'Pilih Video (Semua Format)',
        'article_settings': 'Pengaturan Artikel',
        'generate_btn': 'Generate Artikel',
        'result_header': 'Hasil Artikel',
        'btn_edit': 'Edit',
        'btn_download': 'Unduh',
        'btn_publish': 'Publish',
        'empty_state': 'Artikel yang dihasilkan akan muncul di sini.',
        'settings_title': 'Pengaturan Sistem',
        'tab_model_ai': 'Model AI',
        'tab_wp': 'WordPress',
        'tab_ui': 'Tampilan',
        'label_ai_provider': 'Penyedia AI (AI Provider)',
        'label_groq_model': 'Pilih Model Groq',
        'hint_groq_key': 'Dapatkan key gratis di console.groq.com/keys.',
        'label_wp_url': 'URL Website WordPress',
        'label_wp_user': 'Username WordPress',
        'label_wp_pwd': 'Application Password',
        'label_ui_lang': 'Bahasa Antarmuka Aplikasi',
        'label_theme': 'Tema Aplikasi',
        'save_settings_btn': 'Simpan Pengaturan',
        'opt_style_blog': 'Gaya Blog (Santai & Engaging)',
        'opt_style_news': 'Gaya Berita (Formal & Objektif)',
        'opt_style_academic': 'Gaya Akademik (Analitis)',
        'opt_style_seo': 'Gaya SEO (Optimasi Kata Kunci)',
        'opt_lang_id': 'Bahasa Indonesia',
        'opt_lang_en': 'Bahasa Inggris (English)',
        'opt_prov_gemini': 'Google Gemini (Recommended)',
        'opt_prov_groq': 'Groq (Super Cepat & Gratis)',
        'opt_prov_hf': 'Hugging Face (Teks Saja)',
        'label_gemini_key': 'Gemini API Key',
        'hint_gemini_key': 'Dapatkan key di Google AI Studio.',
        'label_gemini_model': 'Pilih Model Gemini',
        'opt_model_auto': '✨ Otomatis (Rekomendasi Terbaik)',
        'label_hf_key': 'Hugging Face Access Token',
        'hint_hf_key': 'Dapatkan token di huggingface.co/settings/tokens.',
        'label_hf_model': 'Pilih Model Hugging Face',
        'hint_hf_model': 'Hanya model yang mendukung Inference API yang didukung.',
        'label_groq_key': 'Groq API Key',
        'opt_groq_llama': 'Llama 3.1 (8B) - Sangat Cepat',
        'hint_wp_pwd': 'Buat di menu Users > Profile > Application Passwords di dasbor WordPress.',
        'opt_theme_sys': 'Default',
        'opt_theme_dark': 'Dark Mode',
        'opt_theme_light': 'Light Mode',
        'btn_test': 'Test',

        // Global Nav & Footer
        'nav_home': 'HOME',
        'nav_features': 'FITUR',
        'nav_help': 'BANTUAN',
        'btn_login': 'Masuk',
        'btn_dashboard': 'Dashboard',
        'footer_desc': 'Menulis lebih cerdas, berkreasi lebih cepat, dan meraih lebih banyak dengan ARSA - Teman menulis terbaik Anda.',
        'footer_product': 'Produk',
        'footer_about': 'Tentang Kami',
        'footer_contact': 'Kontak',
        'footer_faq': 'Pusat Bantuan',
        'footer_legal': 'Legal',
        'footer_terms': 'Syarat & Ketentuan',
        'footer_privacy': 'Kebijakan Privasi',
        'footer_rights': '&copy; 2026 ARSA. All Rights Reserved',
        'app_menu_settings': 'Pengaturan Akun',
        'app_menu_logout': 'Keluar',
        'app_publish_draft': 'Simpan sebagai Draft',
        'app_publish_live': 'Publish Langsung',

        // Index - Hero
        'hero_badge': 'Versi 1.0 Dirilis',
        'hero_title': 'Buat Artikel SEO dalam <span class="highlight">Hitungan Detik</span>',
        'hero_desc': 'Tingkatkan produktivitas penulisan Anda. Ubah ide, video YouTube, atau dokumen mentah menjadi artikel blog siap publikasi hanya dengan satu klik.',
        'btn_try_free': 'Mulai Sekarang',
        'btn_view_demo': 'Lihat Fitur',

        // Index - Features
        'feat_title': 'Kenapa Memilih ARSA?',
        'feat_1_title': 'AI Super Cerdas',
        'feat_1_desc': 'Memanfaatkan model LLM terbaru (Gemini, Groq) untuk menghasilkan artikel yang natural, bukan gaya robot.',
        'feat_2_title': 'Ekstraksi YouTube',
        'feat_2_desc': 'Hanya dengan menempelkan link YouTube, AI kami akan menonton dan merangkum isinya menjadi artikel.',
        'feat_3_title': 'Sekali Klik Publish',
        'feat_3_desc': 'Terhubung langsung ke WordPress Anda. Tidak perlu lagi copy-paste, cukup satu tombol publish.',

        // Index - Showcase
        'showcase_title': 'Mulai menulis dengan cepat dan mudah.',
        'showcase_desc': 'Dashboard yang intuitif memungkinkan Anda mengatur topik, memilih gaya tulisan, dan mendapatkan hasil dalam hitungan detik. Cukup fokus pada ide Anda, biarkan AI yang merangkainya.',

        // Contact Page
        'contact_title': 'Hubungi Kami',
        'contact_desc': 'Ada pertanyaan, kritik, atau butuh bantuan? Tim dukungan kami siap mendengarkan dan membantu Anda.',
        'contact_label_name': 'Nama Lengkap',
        'contact_label_email': 'Alamat Email',
        'contact_label_subject': 'Subjek',
        'contact_label_msg': 'Pesan',
        'contact_ph_name': 'Masukkan nama Anda',
        'contact_ph_email': 'nama@email.com',
        'contact_ph_msg': 'Tuliskan detail pertanyaan atau masukan Anda di sini...',
        'contact_opt_1': 'Pertanyaan Umum',
        'contact_opt_2': 'Bantuan Teknis',
        'contact_opt_3': 'Kerja Sama / Bisnis',
        'contact_btn_send': 'Kirim Pesan',
        'contact_info': 'Atau email kami langsung di: supportARSA@gmail.com',

        // Help Page
        'help_title': 'Pusat Bantuan',
        'help_desc': 'Temukan jawaban untuk pertanyaan yang paling sering diajukan mengenai ARSA.',
        'faq_1_q': 'Apa itu ARSA?',
        'faq_1_a': 'ARSA adalah platform asisten penulisan berbasis AI yang dirancang untuk membantu pembuat konten, blogger, dan pemasar membuat artikel SEO yang dioptimalkan dalam hitungan detik dari berbagai sumber seperti teks manual, URL web, video YouTube, atau dokumen.',
        'faq_2_q': 'Model AI apa saja yang didukung?',
        'faq_2_a': 'Saat ini kami mendukung berbagai model unggulan, termasuk Google Gemini (Flash, Pro), Groq (Llama 3), dan Hugging Face. Anda dapat mengganti model ini kapan saja di menu Pengaturan Sistem.',
        'faq_3_q': 'Apakah ARSA gratis digunakan?',
        'faq_3_a': 'ARSA versi dasar sepenuhnya gratis untuk dicoba. Anda dapat menggunakan API Key Anda sendiri (bring-your-own-key) seperti Groq atau Gemini untuk menikmati generasi tanpa batas dengan biaya sendiri (atau gratis jika menggunakan kuota gratis mereka).',
        'faq_4_q': 'Bagaimana cara mempublikasikan artikel ke WordPress?',
        'faq_4_a': 'Anda dapat menghubungkan situs WordPress Anda melalui tab Pengaturan Sistem dengan memasukkan URL, username, dan Application Password (bukan password login biasa). Setelah terhubung, akan muncul opsi publish di dashboard hasil artikel.',
        'faq_5_q': 'Format file dokumen apa saja yang didukung?',
        'faq_5_a': 'Anda dapat mengunggah file teks biasa (.txt), Markdown (.md), dokumen Word (.docx), dan PDF (.pdf). Sistem kami akan secara otomatis mengekstrak teks dari dalamnya sebagai referensi.',
        'faq_6_q': 'Apakah artikel yang dihasilkan bebas plagiarisme?',
        'faq_6_a': 'AI kami dilatih untuk memparafrase dan mensintesis informasi menjadi kalimat orisinal. Namun, sebagai langkah kehati-hatian, kami sangat menyarankan Anda untuk meninjau dan mengedit hasil akhir serta melakukan pemeriksaan orisinalitas sebelum publikasi akhir.',

        // Login & Register
        'auth_title_login': 'Selamat Datang Kembali',
        'auth_subtitle_login': 'Silakan masuk ke akun ARSA Anda.',
        'auth_title_register': 'Daftar Akun Baru',
        'auth_subtitle_register': 'Bergabung bersama ribuan penulis cerdas lainnya.',
        'auth_label_name': 'Nama Lengkap',
        'auth_label_email': 'Alamat Email',
        'auth_label_pwd': 'Kata Sandi',
        'auth_btn_login': 'Masuk ke Dashboard',
        'auth_btn_register': 'Daftar Sekarang',
        'auth_link_login': 'Sudah punya akun? Masuk di sini',
        'auth_link_register': 'Belum punya akun? Daftar gratis',

        // Privacy Policy
        'privacy_title': 'Kebijakan Privasi',
        'privacy_desc': 'Terakhir diperbarui: 19 Juni 2026',
        'privacy_intro': 'Privasi Anda adalah prioritas kami.',
        'privacy_intro_desc': 'Di ARSA, kami memahami bahwa informasi pribadi Anda sangat penting. Kebijakan Privasi ini menjelaskan bagaimana kami mengumpulkan, menggunakan, dan melindungi informasi Anda saat menggunakan situs web kami.',
        'privacy_h1': '1. Informasi yang Kami Kumpulkan',
        'privacy_p1': 'Saat Anda mendaftar atau menggunakan layanan kami, kami mungkin mengumpulkan informasi berikut:',
        'privacy_l1_1': 'Informasi pribadi yang Anda berikan secara sukarela (seperti nama, alamat email).',
        'privacy_l1_2': 'Data penggunaan dan log analitik.',
        'privacy_l1_3': 'Konten teks yang Anda unggah untuk keperluan pemrosesan AI.',
        'privacy_h2': '2. Bagaimana Kami Menggunakan Informasi',
        'privacy_p2': 'Informasi Anda digunakan untuk tujuan berikut:',
        'privacy_l2_1': 'Menyediakan dan memelihara layanan aplikasi.',
        'privacy_l2_2': 'Memproses transaksi (jika ada).',
        'privacy_l2_3': 'Mengirimkan pembaruan penting mengenai akun Anda.',
        'privacy_l2_4': 'Menganalisis penggunaan situs web untuk peningkatan pengalaman pengguna.',
        'privacy_h3': '3. Berbagi Data dengan Pihak Ketiga',
        'privacy_p3': 'Kami tidak akan menjual informasi pribadi Anda kepada pihak ketiga. Kami hanya membagikan informasi dengan:',
        'privacy_l3_1': 'Penyedia layanan AI (seperti Google Gemini atau Groq) semata-mata untuk memproses permintaan penulisan Anda.',
        'privacy_l3_2': 'Pihak berwajib jika diwajibkan secara hukum.',
        'privacy_h4': '4. Keamanan Data',
        'privacy_p4': 'Kami menerapkan langkah-langkah keamanan standar industri untuk melindungi data Anda. Namun, tidak ada metode transmisi di internet yang 100% aman.',
        'privacy_h5': '5. Hak Anda',
        'privacy_p5': 'Anda memiliki hak untuk mengakses, mengubah, atau meminta penghapusan data pribadi Anda dengan menghubungi kami melalui Pusat Bantuan.',

        // Terms of Service
        'terms_title': 'Syarat dan Ketentuan',
        'terms_desc': 'Terakhir diperbarui: 19 Juni 2026',
        'terms_intro': '1. Pendahuluan',
        'terms_intro_desc': 'Selamat datang di ARSA. Syarat dan Ketentuan ini ("Perjanjian") mengatur akses dan penggunaan Anda terhadap layanan, situs web, produk, dan aplikasi yang disediakan oleh ARSA. Dengan mengakses atau menggunakan layanan kami, Anda setuju untuk terikat dengan ketentuan ini.',
        'terms_h2': '2. Lisensi Penggunaan',
        'terms_p2': 'ARSA memberikan Anda lisensi terbatas, non-eksklusif, dan tidak dapat dialihkan untuk menggunakan perangkat lunak kami untuk tujuan pribadi dan komersial (yaitu menghasilkan artikel).',
        'terms_h3': '3. Konten Pengguna',
        'terms_p3': 'Anda mempertahankan semua hak atas input (topik, teks mentah) dan output (artikel yang dihasilkan). Anda setuju untuk tidak menggunakan alat kami untuk tujuan menghasilkan spam, ujaran kebencian, atau konten ilegal.',
        'terms_h4': '4. API Pihak Ketiga',
        'terms_p4': 'Platform kami bergantung pada penyedia layanan bahasa pihak ketiga. Anda setuju untuk mematuhi ketentuan layanan dari penyedia AI pilihan Anda (misalnya Google, Groq, dll).',
        'terms_h5': '5. Pembatasan Tanggung Jawab',
        'terms_p5': 'Kami tidak menjamin bahwa layanan kami akan terbebas dari kesalahan, tanpa gangguan, atau bahwa konten yang dihasilkan 100% akurat. Pengguna bertanggung jawab untuk memverifikasi akurasi informasi yang dihasilkan oleh AI sebelum dipublikasikan.'
    },
    'en': {
        // App
        'source_context': 'Select Context Source',
        'tab_manual': 'Manual Text',
        'tab_web': 'Web URL',
        'tab_youtube': 'YouTube',
        'tab_document': 'Document',
        'tab_video': 'Local Video',
        'placeholder_manual': "Type a News Topic (e.g., 'MotoGP News Today') or paste reference text here...",
        'label_file': 'Choose File',
        'label_video': 'Choose Video (Any Format)',
        'article_settings': 'Article Settings',
        'generate_btn': 'Generate Article',
        'result_header': 'Generated Article',
        'btn_edit': 'Edit',
        'btn_download': 'Download',
        'btn_publish': 'Publish',
        'empty_state': 'The generated article will appear here.',
        'settings_title': 'System Settings',
        'tab_model_ai': 'AI Model',
        'tab_wp': 'WordPress',
        'tab_ui': 'Appearance',
        'label_ai_provider': 'AI Provider',
        'label_groq_model': 'Select Groq Model',
        'hint_groq_key': 'Get a free key at console.groq.com/keys.',
        'label_wp_url': 'WordPress Website URL',
        'label_wp_user': 'WordPress Username',
        'label_wp_pwd': 'Application Password',
        'label_ui_lang': 'Application Interface Language',
        'label_theme': 'Application Theme',
        'save_settings_btn': 'Save Settings',
        'opt_style_blog': 'Blog Style (Casual & Engaging)',
        'opt_style_news': 'News Style (Formal & Objective)',
        'opt_style_academic': 'Academic Style (Analytical)',
        'opt_style_seo': 'SEO Style (Keyword Optimized)',
        'opt_lang_id': 'Indonesian (Bahasa Indonesia)',
        'opt_lang_en': 'English',
        'opt_prov_gemini': 'Google Gemini (Recommended)',
        'opt_prov_groq': 'Groq (Super Fast & Free)',
        'opt_prov_hf': 'Hugging Face (Text Only)',
        'label_gemini_key': 'Gemini API Key',
        'hint_gemini_key': 'Get your key at Google AI Studio.',
        'label_gemini_model': 'Select Gemini Model',
        'opt_model_auto': '✨ Auto (Best Recommended)',
        'label_hf_key': 'Hugging Face Access Token',
        'hint_hf_key': 'Get token at huggingface.co/settings/tokens.',
        'label_hf_model': 'Select Hugging Face Model',
        'hint_hf_model': 'Only models that support Inference API are supported.',
        'label_groq_key': 'Groq API Key',
        'opt_groq_llama': 'Llama 3.1 (8B) - Super Fast',
        'hint_wp_pwd': 'Create in Users > Profile > Application Passwords on WordPress dashboard.',
        'opt_theme_sys': 'System Default',
        'opt_theme_dark': 'Dark Mode',
        'opt_theme_light': 'Light Mode',
        'btn_test': 'Test',

        // Global Nav & Footer
        'nav_home': 'HOME',
        'nav_features': 'FEATURES',
        'nav_help': 'HELP',
        'btn_login': 'Login',
        'btn_dashboard': 'Dashboard',
        'footer_desc': 'Write smarter, create faster, and achieve more with ARSA - Your ultimate writing companion.',
        'footer_product': 'Product',
        'footer_about': 'About Us',
        'footer_contact': 'Contact',
        'footer_faq': 'Help Center',
        'footer_legal': 'Legal',
        'footer_terms': 'Terms of Service',
        'footer_privacy': 'Privacy Policy',
        'footer_rights': '&copy; 2026 ARSA. All Rights Reserved',
        'app_menu_settings': 'Account Settings',
        'app_menu_logout': 'Logout',
        'app_publish_draft': 'Save as Draft',
        'app_publish_live': 'Publish Immediately',

        // Index - Hero
        'hero_badge': 'Version 1.0 Released',
        'hero_title': 'Create SEO Articles in <span class="highlight">Seconds</span>',
        'hero_desc': 'Boost your writing productivity. Turn ideas, YouTube videos, or raw documents into publish-ready blog articles with just one click.',
        'btn_try_free': 'Try Now',
        'btn_view_demo': 'See Features',

        // Index - Features
        'feat_title': 'Why Choose ARSA?',
        'feat_1_title': 'Super Smart AI',
        'feat_1_desc': 'Leveraging the latest LLM models (Gemini, Groq) to generate natural-sounding articles, not robotic text.',
        'feat_2_title': 'YouTube Extraction',
        'feat_2_desc': 'Just by pasting a YouTube link, our AI will watch and summarize its content into an article.',
        'feat_3_title': 'One-Click Publish',
        'feat_3_desc': 'Connects directly to your WordPress. No more copy-pasting, just a single publish button.',

        // Index - Showcase
        'showcase_title': 'Start writing quickly and easily.',
        'showcase_desc': 'The intuitive dashboard lets you set topics, choose writing styles, and get results in seconds. Just focus on your ideas, let the AI string them together.',

        // Contact Page
        'contact_title': 'Contact Us',
        'contact_desc': 'Have a question, feedback, or need help? Our support team is ready to listen and assist you.',
        'contact_label_name': 'Full Name',
        'contact_label_email': 'Email Address',
        'contact_label_subject': 'Subject',
        'contact_label_msg': 'Message',
        'contact_ph_name': 'Enter your name',
        'contact_ph_email': 'name@email.com',
        'contact_ph_msg': 'Write the details of your question or feedback here...',
        'contact_opt_1': 'General Inquiry',
        'contact_opt_2': 'Technical Support',
        'contact_opt_3': 'Partnership / Business',
        'contact_btn_send': 'Send Message',
        'contact_info': 'Or email us directly at: supportARSA@gmail.com',

        // Help Page
        'help_title': 'Help Center',
        'help_desc': 'Find answers to the most frequently asked questions about ARSA.',
        'faq_1_q': 'What is ARSA?',
        'faq_1_a': 'ARSA is an AI-powered writing assistant platform designed to help content creators, bloggers, and marketers create SEO-optimized articles in seconds from various sources like manual text, web URLs, YouTube videos, or documents.',
        'faq_2_q': 'What AI models are supported?',
        'faq_2_a': 'We currently support several top-tier models, including Google Gemini (Flash, Pro), Groq (Llama 3), and Hugging Face. You can switch models anytime in the System Settings menu.',
        'faq_3_q': 'Is ARSA free to use?',
        'faq_3_a': 'The basic version of ARSA is completely free to try. You can use your own API Keys (bring-your-own-key) like Groq or Gemini to enjoy unlimited generations at your own cost (or for free if using their free tier).',
        'faq_4_q': 'How do I publish articles to WordPress?',
        'faq_4_a': 'You can connect your WordPress site through the System Settings tab by entering your URL, username, and Application Password (not your regular login password). Once connected, a publish option will appear in the generated article dashboard.',
        'faq_5_q': 'What document file formats are supported?',
        'faq_5_a': 'You can upload plain text files (.txt), Markdown (.md), Word documents (.docx), and PDFs (.pdf). Our system will automatically extract the text within them as a reference.',
        'faq_6_q': 'Are the generated articles plagiarism-free?',
        'faq_6_a': 'Our AI is trained to paraphrase and synthesize information into original sentences. However, as a precaution, we strongly recommend that you review and edit the final output and perform originality checks before final publication.',

        // Login & Register
        'auth_title_login': 'Welcome Back',
        'auth_subtitle_login': 'Please log in to your ARSA account.',
        'auth_title_register': 'Create a New Account',
        'auth_subtitle_register': 'Join thousands of other smart writers.',
        'auth_label_name': 'Full Name',
        'auth_label_email': 'Email Address',
        'auth_label_pwd': 'Password',
        'auth_btn_login': 'Login to Dashboard',
        'auth_btn_register': 'Register Now',
        'auth_link_login': 'Already have an account? Login here',
        'auth_link_register': 'Don\'t have an account? Register for free',

        // Privacy Policy
        'privacy_title': 'Privacy Policy',
        'privacy_desc': 'Last updated: June 19, 2026',
        'privacy_intro': 'Your privacy is our priority.',
        'privacy_intro_desc': 'At ARSA, we understand that your personal information is very important. This Privacy Policy explains how we collect, use, and protect your information when using our website.',
        'privacy_h1': '1. Information We Collect',
        'privacy_p1': 'When you register or use our services, we may collect the following information:',
        'privacy_l1_1': 'Personal information you voluntarily provide (such as name, email address).',
        'privacy_l1_2': 'Usage data and analytics logs.',
        'privacy_l1_3': 'Text content you upload for AI processing purposes.',
        'privacy_h2': '2. How We Use Information',
        'privacy_p2': 'Your information is used for the following purposes:',
        'privacy_l2_1': 'Providing and maintaining application services.',
        'privacy_l2_2': 'Processing transactions (if applicable).',
        'privacy_l2_3': 'Sending important updates regarding your account.',
        'privacy_l2_4': 'Analyzing website usage to improve user experience.',
        'privacy_h3': '3. Sharing Data with Third Parties',
        'privacy_p3': 'We will not sell your personal information to third parties. We only share information with:',
        'privacy_l3_1': 'AI service providers (such as Google Gemini or Groq) solely to process your writing requests.',
        'privacy_l3_2': 'Authorities if legally required.',
        'privacy_h4': '4. Data Security',
        'privacy_p4': 'We implement industry-standard security measures to protect your data. However, no method of transmission over the internet is 100% secure.',
        'privacy_h5': '5. Your Rights',
        'privacy_p5': 'You have the right to access, modify, or request the deletion of your personal data by contacting us through the Help Center.',

        // Terms of Service
        'terms_title': 'Terms of Service',
        'terms_desc': 'Last updated: June 19, 2026',
        'terms_intro': '1. Introduction',
        'terms_intro_desc': 'Welcome to ARSA. These Terms of Service ("Agreement") govern your access to and use of the services, websites, products, and applications provided by ARSA. By accessing or using our services, you agree to be bound by these terms.',
        'terms_h2': '2. Usage License',
        'terms_p2': 'ARSA grants you a limited, non-exclusive, and non-transferable license to use our software for personal and commercial purposes (i.e., generating articles).',
        'terms_h3': '3. User Content',
        'terms_p3': 'You retain all rights to inputs (topics, raw text) and outputs (generated articles). You agree not to use our tools for the purpose of generating spam, hate speech, or illegal content.',
        'terms_h4': '4. Third-Party APIs',
        'terms_p4': 'Our platform relies on third-party language service providers. You agree to comply with the terms of service of your chosen AI provider (e.g., Google, Groq, etc.).',
        'terms_h5': '5. Limitation of Liability',
        'terms_p5': 'We do not guarantee that our services will be error-free, uninterrupted, or that the generated content is 100% accurate. Users are responsible for verifying the accuracy of the information generated by the AI before publication.'
    }
};

const savedUiLang = localStorage.getItem('app_ui_lang') || 'id';

function applyUILanguage(lang) {
    if (!translations[lang]) return;
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[lang][key]) {
            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                el.placeholder = translations[lang][key];
            } else if (el.tagName === 'OPTION') {
                el.textContent = translations[lang][key];
            } else {
                el.innerHTML = translations[lang][key];
            }
        }
    });

    const globalLangSelectors = document.querySelectorAll('.global-lang-selector');
    globalLangSelectors.forEach(select => {
        if (select.value !== lang) {
            select.value = lang;
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    applyUILanguage(savedUiLang);

    const globalLangSelectors = document.querySelectorAll('.global-lang-selector');
    globalLangSelectors.forEach(select => {
        select.value = savedUiLang;
        select.addEventListener('change', (e) => {
            const newLang = e.target.value;
            localStorage.setItem('app_ui_lang', newLang);
            applyUILanguage(newLang);
            // Optionally reload to ensure placeholders/attributes apply if needed
            // location.reload();
        });
    });
});
