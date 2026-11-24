@extends('base.app')

@section('header_title', 'Analisis Skill Gap')

@section('content')
    <!-- deskripsi -->
    <div class="flex mb-12 gap-2">
        <svg class="w-5 h-5 shrink-0" fill="none" stroke="#6A7282" stroke-width="1.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
        </svg>

        <span class="text-sm text-gray-500">Membandingkan Kompetensi yang Dibutuhkan Industri VS yang Dirasa Kurang oleh Alumni
        </span>   
    </div>

    <!-- menu menu -->
    <div class="grid grid-cols-4 gap-4 border-b border-gray-200">
        <div class="pb-2 border-b-2 {{ request()->is('skill-gap*') ? 'border-[#1E3A8A]' : 'border-transparent' }}">
            <a href="/skill-gap"
                class="block px-4 py-2 text-center rounded-lg font-medium transition {{ request()->is('skill-gap*') ? ' text-[#1E3A8A]' : 'text-gray-700 hover:bg-[#2B72D6]/10 hover:text-[#2B72D6]' }}">
                Ranking Skill Gap Terbesar
            </a>
        </div>

        <div class="pb-2 border-b-2 {{ request()->is('dibutuhkan-dirasakurang*') ? 'border-[#1E3A8A]' : 'border-transparent' }}">
            <a href="/dibutuhkan-dirasakurang"
                class="block px-4 py-2 text-center rounded-lg font-medium transition {{ request()->is('dibutuhkan-dirasakurang*') ? 'text-[#1E3A8A]' : 'text-gray-700 hover:bg-[#2B72D6]/10 hover:text-[#2B72D6]' }}">
                Dibutuhkan Industri VS Dirasa Kurang
            </a>
        </div>

        <div class="pb-2 border-b-2 {{ request()->is('tren-angkatan*') ? 'border-[#1E3A8A]' : 'border-transparent' }}">
            <a href="/tren-angkatan"
                class="block px-4 py-2 text-center rounded-lg font-medium transition {{ request()->is('tren-angkatan*') ? 'text-[#1E3A8A]' : 'text-gray-700 hover:bg-[#2B72D6]/10 hover:text-[#2B72D6]' }}">
                Tren Antar Angkatan
            </a>
        </div>

        <div class="pb-2 border-b-2 {{ request()->is('waktu-tunggu*') ? 'border-[#1E3A8A]' : 'border-transparent' }}">
            <a href="/waktu-tunggu"
                class="block px-4 py-2 text-center rounded-lg font-medium transition {{ request()->is('waktu-tunggu*') ? 'text-[#1E3A8A]' : 'text-gray-700 hover:bg-[#2B72D6]/10 hover:text-[#2B72D6]' }}">
                Waktu Tunggu VS Gap
            </a>
        </div>
    </div>

    <!-- isi content -->
    <div class="mt-10">
        @yield('skillgap-content')
        @yield('dibutuhkan-content')
        @yield('tren-angkatan-content')
        @yield('waktu-tunggu-content')
    </div>

@endsection