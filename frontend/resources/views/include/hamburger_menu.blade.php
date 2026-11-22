<!-- Hamburger menu biar keluar dari kiri -->
<aside id="sidebar_drawer" class="fixed top-0 left-0 z-50 w-76 h-full bg-white shadow-[#c1c1c1] shadow-lg transform -translate-x-full transition-transform duration-300 ease-in-out">
    
    <!-- Header Hamburger -->
    <div class="bg-white text-[#0F294A] h-22 px-6 flex items-center gap-4 border-b-2 border-[#febb3d]">
        <span class="text-4xl font-bold tracking-wide">🎓</span>
        <span class="text-xl font-bold tracking-wide">Tracer Study App</span>
    </div>
    <!-- <div class="bg-white border-b-2 border-[#febb3d] flex items-center justify-between"></div> -->

    <!-- Daftar Menu Hamburger (Otomatis Menyala Saat Aktif) -->
    <nav class="p-4 space-y-4">
        <!-- Menu 1: Peta Kompetensi Dunia Kerja -->
        <a href="/" 
           class="flex items-center gap-4 px-4 py-3 rounded-lg font-medium transition {{ request()->is('/', 'soft-skills*', 'sertifikasi*', 'matriks*') ? 'bg-[#1E3A8A] text-white shadow-sm' : 'text-gray-700 hover:bg-[#2B72D6]/10 hover:text-[#2B72D6]' }}">

            <!-- Ikon Map  -->
            <svg class="w-6 h-6 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 6.75V15m6-6v8.25m.503 3.498 4.875-2.437c.381-.19.622-.58.622-1.006V4.82c0-.836-.88-1.38-1.628-1.006l-3.869 1.934c-.317.159-.69.159-1.006 0L9.503 3.252a1.125 1.125 0 0 0-1.006 0L3.622 5.689C3.24 5.88 3 6.27 3 6.695V19.18c0 .836.88 1.38 1.628 1.006l3.869-1.934c.317-.159.69-.159 1.006 0l4.994 2.497c.317.158.69.158 1.006 0Z" />
            </svg>
            <span>Peta Kompetensi Dunia Kerja</span>
        </a>

        <!-- Menu 2: Analisis Skill Gap -->
        <a href="/skill-gap" 
           class="flex items-center gap-4 px-4 py-3 rounded-lg font-medium transition {{ request()->is('skill-gap*') ? 'bg-[#1E3A8A] text-white shadow-sm' : 'text-gray-700 hover:bg-[#2B72D6]/10 hover:text-[#2B72D6]' }}">
            <!-- Ikon Chart -->
            <svg class="w-6 h-6 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 0 1 3 19.875v-6.75ZM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V8.625ZM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V4.125Z" />
            </svg>
            <span>Analisis Skill Gap</span>
        </a>

        <!-- Menu 3: Dashboard Tracer Study -->
        <a href="/dashboard-tracer-study" 
           class="flex items-center gap-4 px-4 py-3 rounded-lg font-medium transition {{ request()->is('dashboard-tracer-study*') ? 'bg-[#1E3A8A] text-white shadow-sm' : 'text-gray-700 hover:bg-[#2B72D6]/10 hover:text-[#2B72D6]' }}">
            <!-- Ikon Dashboard -->
            <svg class="w-6 h-6 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6A2.25 2.25 0 0 1 6 3.75h2.25A2.25 2.25 0 0 1 10.5 6v2.25a2.25 2.25 0 0 1-2.25 2.25H6a2.25 2.25 0 0 1-2.25-2.25V6ZM3.75 15.75A2.25 2.25 0 0 1 6 13.5h2.25a2.25 2.25 0 0 1 2.25 2.25V18a2.25 2.25 0 0 1-2.25 2.25H6A2.25 2.25 0 0 1 3.75 18v-2.25ZM13.5 6a2.25 2.25 0 0 1 2.25-2.25H18A2.25 2.25 0 0 1 20.25 6v2.25A2.25 2.25 0 0 1 18 10.5h-2.25a2.25 2.25 0 0 1-2.25-2.25V6ZM13.5 15.75a2.25 2.25 0 0 1 2.25-2.25H18a2.25 2.25 0 0 1 2.25 2.25V18A2.25 2.25 0 0 1 18 20.25h-2.25A2.25 2.25 0 0 1 13.5 18v-2.25Z" />
            </svg>
            <span>Dashboard Tracer Study</span>
        </a>

        <!-- Menu 4: Career Navigation System -->
        <a href="/career-navigation" 
           class="flex items-center gap-4 px-4 py-3 rounded-lg font-medium transition {{ request()->is('career-navigation*') ? 'bg-[#1E3A8A] text-white shadow-sm' : 'text-gray-700 hover:bg-[#2B72D6]/10 hover:text-[#2B72D6]' }}">
            <!-- Ikon Compas -->
            <svg class="w-6 h-6 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="9" stroke-linecap="round" stroke-linejoin="round" />
                <polygon points="15.5 8.5 13.5 13.5 8.5 15.5 10.5 10.5 15.5 8.5" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
            <span>Career Navigation System</span>
        </a>
    </nav>
</aside>

<!-- 3. Script JavaScript Buka-Tutup Menu -->
<script>
    document.addEventListener('DOMContentLoaded', function () {
        const toggleBtn = document.getElementById('button_hamburger');
        // const closeBtn = document.getElementById('close_hamburger');
        const drawer = document.getElementById('sidebar_drawer');
        const mainContent = document.getElementById('main_content');

        function toggleSidebar() {
            drawer.classList.toggle('-translate-x-full');
            if (mainContent) {
                mainContent.classList.toggle('ml-76');
            }
        }

        if (toggleBtn) toggleBtn.addEventListener('click', toggleSidebar);
        if (closeBtn) closeBtn.addEventListener('click', toggleSidebar);
    });
</script>
