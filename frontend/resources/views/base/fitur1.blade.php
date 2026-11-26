@extends('base.app')

@section('header_title', 'Peta Kompetensi Dunia Kerja')

@section('content')
    <!-- deskripsi -->
    <div class="flex mb-12 gap-2">
        <svg class="w-5 h-5 shrink-0" fill="none" stroke="#6A7282" stroke-width="1.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
        </svg>

        <span class="text-sm text-gray-500">Agregasi Kompetensi yang Benar-Benar Dibutuhkan Alumni di Bidang Pekerjaannya.
            Filter Untuk Melihat Data Spesifik
        </span>   
    </div>

    <!-- Menu menu -->
    <nav class="grid grid-cols-4 gap-4 border-b border-gray-200">

        <div class="pb-2 border-b-2 {{ request()->is('/') ? 'border-[#1E3A8A]' : 'border-transparent' }}">
            <a href="/"
                class="block px-4 py-2 text-center rounded-lg font-medium transition {{ request()->is('/') ? ' text-[#1E3A8A]' : 'text-gray-700 hover:bg-[#2B72D6]/10 hover:text-[#2B72D6]' }}">
                Hard Skills per Bidang
            </a>
        </div>

        <div class="pb-2 border-b-2 {{ request()->is('soft-skills*') ? 'border-[#1E3A8A]' : 'border-transparent' }}">
            <a href="/soft-skills"
                class="block px-4 py-2 text-center rounded-lg font-medium transition {{ request()->is('soft-skills') ? 'text-[#1E3A8A]' : 'text-gray-700 hover:bg-[#2B72D6]/10 hover:text-[#2B72D6]' }}">
                Soft Skills per Bidang
            </a>
        </div>

        <div class="pb-2 border-b-2 {{ request()->is('sertifikasi*') ? 'border-[#1E3A8A]' : 'border-transparent' }}">
            <a href="/sertifikasi"
                class="block px-4 py-2 text-center rounded-lg font-medium transition {{ request()->is('sertifikasi') ? 'text-[#1E3A8A]' : 'text-gray-700 hover:bg-[#2B72D6]/10 hover:text-[#2B72D6]' }}">
                Sertifikasi yang Bermanfaat
            </a>
        </div>

        <div class="pb-2 border-b-2 {{ request()->is('matriks*') ? 'border-[#1E3A8A]' : 'border-transparent' }}">
            <a href="/matriks"
                class="block px-4 py-2 text-center rounded-lg font-medium transition {{ request()->is('matriks-prodi-bidang') ? 'text-[#1E3A8A]' : 'text-gray-700 hover:bg-[#2B72D6]/10 hover:text-[#2B72D6]' }}">
                Matriks Prodi x Bidang
            </a>
        </div>
    </nav>

    <!-- Dropdown Form -->
    @isset($semua)
        <div class="mt-6">
            <form method="GET">
                <div class="mb-4">
                    <label for="dropdown" class="block text-sm font-medium text-gray-600 mb-2">
                        Pilih Bidang Pekerjaan
                    </label>

                    <div class="relative">
                        <select name="bidang" id="dropdown" onchange="this.form.submit()"
                            class="appearance-none w-full bg-gray-100 text-[#0F294A] px-4 py-2.5 pr-12 rounded-lg border border-transparent cursor-pointer transition
                                hover:bg-gray-200/70
                                focus:outline-none focus:bg-white focus:border-[#2B72D6] focus:ring-2 focus:ring-[#2B72D6]/20">
                            <option value="" @selected($bidang === null)>Semua Bidang</option>
                            @foreach ($bidangList as $b)
                                <option value="{{ $b }}" @selected($b === $bidang)>{{ $b }}</option>
                            @endforeach
                        </select>

                        <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-4 text-gray-600">
                            <svg class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
                            </svg>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    @endisset

    <!-- isi content -->
    <div class="mt-8 px-2">
        @yield('hardskill-content')
        @yield('softskill-content')
        @yield('sertifikasi-content')
        @yield('matrix-content')
    </div>

@endsection
